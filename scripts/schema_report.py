"""Produces an XLS Report comparing the UKRDC Schema to
the Repository Database"""

import os
from ukrdc.services.database import Connection
from lxml import etree
import xlwt

# NOTE: This may assume a PostgreSQL DB


def get_db_table_list(cursor):
    sqlstring = """
    SELECT DISTINCT
        table_name
    FROM
        information_schema.columns
    WHERE
         information_schema.columns.table_schema = 'extract'
    """

    cursor.execute(sqlstring)
    return [row[0] for row in cursor.fetchall()]


def get_db_column_metadata(cursor, tablename):
    sqlstring = """
    SELECT
        tab_columns.column_name,
        data_type,
        character_maximum_length,
        numeric_precision,
        is_nullable,
        tab_constraints.constraint_type,
        col_constraints.constraint_name,
        col_check_constraints.check_clause
    FROM
        information_schema.columns AS tab_columns
    LEFT OUTER JOIN
        information_schema.constraint_column_usage AS col_constraints ON
            tab_columns.table_name = col_constraints.table_name AND
            tab_columns.column_name = col_constraints.column_name
    LEFT OUTER JOIN
        information_schema.table_constraints AS tab_constraints ON
        tab_constraints.constraint_name = col_constraints.constraint_name
    LEFT OUTER JOIN
        information_schema.check_constraints AS col_check_constraints ON
        col_check_constraints.constraint_name = tab_constraints.constraint_name
    WHERE
        tab_columns.table_name = %s AND
        tab_columns.table_schema = 'extract'
    ORDER BY ordinal_position;
    """

    cursor.execute(sqlstring, (tablename, ))
    return cursor.fetchall()


def get_field_contents_stats(cursor, table_name, column_name):

    # We could add MAX/MIN/AVG here but it wouldn't make much sense
    # As ResultValue/ObservationValue will be across all tests

    sqlstring = """
    SELECT
        COUNT(*) AS ROW_COUNT,
        SUM(CASE WHEN """ + column_name + """ IS NOT NULL THEN 1 ELSE 0 END) AS VALUE_COUNT,
        COUNT(DISTINCT """ + column_name + """) AS DISTINCT_VALUE_COUNT
    FROM
    """ + table_name

    cursor.execute(sqlstring)
    return cursor.fetchone()


class DBMetadata(object):

    def __init__(self, cursor, xsdpath):
        self.cursor = cursor
        self.xsdpath = xsdpath

    def set_db_metadata(self):

        db_metadata = dict()

        cursor = self.cursor
        table_names = get_db_table_list(cursor)

        for table_name in table_names:
            print(table_name)
            db_metadata[table_name] = dict()
            for row in get_db_column_metadata(cursor, table_name):
                column_name = row[0]
                field_stats = get_field_contents_stats(
                    cursor,
                    table_name,
                    column_name
                )
                row = list(row)
                row.extend(field_stats)
                db_metadata[table_name][column_name] = row

        self.db_metadata = db_metadata

    def process_xsd_file(self, fh):
        ns = 'http://www.w3.org/2001/XMLSchema'
        xml_doc = etree.parse(fh)
        appinfo_nodes = xml_doc.xpath(
            '//xs:appinfo',
            namespaces={'xs': ns}
        )
        xml_metadata = self.xml_metadata
        for appinfo_node in appinfo_nodes:
            appinfo_text = appinfo_node.text
            # Assume value in format:
            # table_name.column_name
            split_appinfo_text = appinfo_text.split('.')
            table_name = split_appinfo_text[0]
            column_name = split_appinfo_text[1]

            documentation_node = appinfo_node.xpath(
                'following-sibling::xs:documentation',
                namespaces={'xs': ns})[-1]
            documentation_text = documentation_node.text

            # NOTE: Here we go "up" from the documentation tag looking
            # for the first element which doesn't match exclusions
            # This may not be necessary and we might just be able to look
            # for xs:element nodes.
            element_node = appinfo_node.xpath(
                'ancestor::*[not(self::xs:annotation)]',
                namespaces={'xs': ns})[-1]
            xml_element_name = element_node.attrib['name']

            xml_element_type = element_node.attrib.get('type', None)

            # If not present minOccurs default is 1
            xml_element_minoccurs = element_node.attrib.get('minOccurs', '1')

            xml_element_maxoccurs = element_node.attrib.get('maxOccurs', None)

            if table_name not in xml_metadata:
                xml_metadata[table_name] = dict()

            xml_metadata[table_name][column_name] = (
                xml_element_name,
                xml_element_type,
                xml_element_minoccurs,
                xml_element_maxoccurs,
                documentation_text
            )

    def set_xml_metadata(self):
        self.xml_metadata = dict()
        for root, dirs, files in os.walk(self.xsdpath, topdown=False):
            for name in files:
                if not name.endswith('.xsd'):
                    continue
                fp = os.path.join(root, name)
                with open(fp) as fh:
                    self.process_xsd_file(fh)

    def run(self):
        self.set_db_metadata()
        self.set_xml_metadata()
        xml_metadata = self.xml_metadata
        db_metadata = self.db_metadata
        xml_md_keys = xml_metadata.keys()
        for table_name in db_metadata.keys():
            xml_md_table_keys = xml_metadata[table_name].keys()
            for column_name in db_metadata[table_name].keys():
                extra = all((
                    table_name in xml_md_keys,
                    column_name in xml_md_table_keys
                ))
                if extra:
                    # Add the extra XML columns if there's a match
                    db_column_data = db_metadata[table_name][column_name]
                    xml_column_data = xml_metadata[table_name][column_name]
                    db_column_data.extend(xml_column_data)
                    db_metadata[table_name][column_name] = db_column_data


def make_report(db_metadata, filepath):

    work_book = xlwt.Workbook()
    fields = (
        'Column Name',
        'Data Type',
        'Max Length',
        'Numeric Precision',
        'Is Nullable',
        'Constraint Type',
        'Constraint Name',
        'Check Clause',
        'Row Count',
        'Value Count',
        'Distinct Value Count',
        'XML Element Name',
        'XML Type',
        'XML MinOccurs',
        'XML MaxOccurs',
        'XML Description'
    )
    for table_name in db_metadata.keys():
        work_sheet = work_book.add_sheet(table_name)
        row = work_sheet.row(0)

        for x, header in enumerate(fields):
            row.write(x, header)

        y = 1
        for column_name in db_metadata[table_name]:
            field_row = db_metadata[table_name][column_name]
            row = work_sheet.row(y)
            for x, value in enumerate(field_row):
                row.write(x, value)
            y += 1
    work_book.save(filepath)


def main():
    xsd_path = 'schema/ukrdc/'
    conn = Connection.create_psycopg2_connection(dbkey='ukrdc3')
    dbm = DBMetadata(conn.cursor(), xsd_path)
    dbm.run()
    make_report(
        dbm.db_metadata,
        'dataset_report.xls'
    )


if __name__ == "__main__":
    main()
