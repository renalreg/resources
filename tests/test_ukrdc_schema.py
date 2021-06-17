from unittest import TestCase

from lxml import etree


class TestUKRDCSchema(TestCase):
    def setUp(self):

        xmlschema_doc = etree.parse(open("schema/ukrdc/UKRDC.xsd", "r"))
        self.ukrdc_xmlschema = etree.XMLSchema(xmlschema_doc)

    def test_sample_file(self):

        import os

        print("XXX")
        print(os.getcwd())
        print("XXX")
        xml_doc = etree.parse(
            open("sample_files/ukrdc/ukrdc.xml", "r", encoding="utf-8")
        )
        self.ukrdc_xmlschema.validate(xml_doc)

        tree = etree.ElementTree(xml_doc.getroot())

        errors_found = False

        for i, error in enumerate(self.ukrdc_xmlschema.error_log):

            errors_found = True

            line_number = error.line
            column_number = error.column
            error_message = error.message

            xml_path = None

            for e in tree.xpath(".//*"):
                if line_number == e.sourceline:
                    xml_path = tree.getpath(e)

            print("Error: ", i)
            print(error_message)
            print(f"Line Number {line_number} Column Number: {column_number}")
            if xml_path:
                print(xml_path)

        self.assertFalse(errors_found)
