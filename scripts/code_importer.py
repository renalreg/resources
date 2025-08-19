import csv
import argparse
import sys
import os

import psycopg2

from ukrdc.database import Connection


class CodeUpdater(object):
    def upload(self):
        for row in self.rows:
            self.add_row(row)
        self.connection.commit()

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection
        self.cursor = connection.cursor()

    def insert(self, sql, row):
        try:
            self.cursor.execute(sql, (row))
        except psycopg2.IntegrityError as e:
            self.connection.rollback()
            print("Problem with integrity " + str(e))
        except Exception:
            print(sql)
            print(row)
            raise

    def select(self, sql, row):
        try:
            self.cursor.execute(sql, (row))
            return list(self.cursor.fetchall())
        except psycopg2.Error as e:
            print(e)


class CodeList(CodeUpdater):
    def __init__(self):
        self.rows = []

    def truncate(self):
        sqlstring = """
        TRUNCATE TABLE CODE_LIST
        """
        self.cursor.execute(sqlstring)
        self.connection.commit()

    def get_row(self, *args):
        sql = """
        select
            coding_standard, code, description, object_type
        from
            extract.code_list
        where
            coding_standard = %s and
            code = %s and
            description = %s and
            object_type = %s
        """
        return self.insert(sql, args)

    def update(self):
        for row in self.rows:
            results = self.get_row(row)
            if results:
                print("Yes we have that row")
            else:
                self.update_row(row[0], row[1], row)

    def add_row(self, row):
        sqlstring = """
        INSERT INTO CODE_LIST
            (
                CODING_STANDARD,
                CODE,
                DESCRIPTION,
                OBJECT_TYPE,
                UNITS
            )
        VALUES (%s, %s, %s, %s, %s)
        """
        self.insert(sqlstring, row)

    def read_csv(self):
        base_folder = "conf/pv2_codes/code_lists/"

        for filename in os.listdir(base_folder):
            print(f"Reading {filename}")
            fp = os.path.join(base_folder, filename)
            csvreader = csv.reader(open(fp, "r", encoding="utf-8"))

            for row in csvreader:
                # Get Row to expected length
                row = list(row)[:5]
                diff_len = 5 - len(row)
                if diff_len > 0:
                    row = row + [None] * diff_len
                if row[0] == "":
                    print("Empty Row, continue")
                    continue
                self.rows.append(row)


class CodeMap(CodeUpdater):
    def __init__(self):
        self.rows = []

    def truncate(self):

        sqlstring = """
        TRUNCATE TABLE CODE_MAP
        """
        self.cursor.execute(sqlstring)
        self.connection.commit()

    def add_row(self, row):
        sqlstring = """
        INSERT INTO CODE_MAP
            (
            SOURCE_CODING_STANDARD,
            SOURCE_CODE,
            DESTINATION_CODING_STANDARD,
            DESTINATION_CODE
            )
        VALUES(%s, %s, %s, %s)"""
        self.insert(sqlstring, row)

    def read_csv(self):
        # Code Conv List

        base_folder = "conf/pv2_codes/code_conv_lists/"

        for filename in os.listdir(base_folder):
            fp = os.path.join(base_folder, filename)
            print(fp)
            csvreader = csv.reader(open(fp, "r", encoding="utf-8"))
            for row in csvreader:
                self.rows.append(row)


class SatelliteMap(CodeUpdater):
    def __init__(self):
        self.rows = []

    def truncate(self):

        sqlstring = """
        TRUNCATE TABLE SATELLITE_MAP
        """
        self.cursor.execute(sqlstring)
        self.connection.commit()

    def add_row(self, row):
        sqlstring = """
        INSERT INTO SATELLITE_MAP
            (
            SATELLITE_CODE,
            MAIN_UNIT_CODE
            )
        VALUES(%s, %s)"""
        self.insert(sqlstring, row)

    def read_csv(self):
        # Satellite Mapping List

        base_folder = "conf/pv2_codes/satellite_map/"

        for filename in os.listdir(base_folder):

            fp = os.path.join(base_folder, filename)
            print(fp)
            csvreader = csv.reader(open(fp, "r", encoding="utf-8"))
            for row in csvreader:
                self.rows.append(row)


def main():

    servers = ["ukrdc_dev", "ukrdc_staging", "ukrdc_live"]

    parser = argparse.ArgumentParser(description="Update codes")
    parser.add_argument("--server", nargs="+", default=servers)
    parser.add_argument("--upload-codelist", action="store_true")
    parser.add_argument("--upload-codemap", action="store_true")
    parser.add_argument("--upload-satellitemap", action="store_true")

    if not len(sys.argv) > 1:
        parser.print_help()
        return
    args = parser.parse_args()
    if args.upload_codelist:
        codelist = CodeList()
        codelist.read_csv()
    if args.upload_codemap:
        codemap = CodeMap()
        codemap.read_csv()
    if args.upload_satellitemap:
        satellitemap = SatelliteMap()
        satellitemap.read_csv()

    for server in args.server:
        print(f"server: {server}")
        engine = Connection.get_engine_from_file(None, server)
        connection = engine.raw_connection()
        print("Connected")
        if args.upload_codelist:
            codelist.connection = connection
            print("Truncating Code List")
            codelist.truncate()
            print("Populating Code List")
            codelist.upload()
        if args.upload_codemap:
            codemap.connection = connection
            print("Truncating Code Map")
            codemap.truncate()
            print("Populating Code Map")
            codemap.upload()
        if args.upload_satellitemap:
            satellitemap.connection = connection
            print("Truncating Satellite Map")
            satellitemap.truncate()
            print("Uploading Satellite Map")
            satellitemap.upload()
        connection.close()


if __name__ == "__main__":
    main()
