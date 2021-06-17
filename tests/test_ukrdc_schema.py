from unittest import TestCase

import lxml


class TestUKRDCSchema(TestCase):
    def setUp(self):
 
        xmlschema_doc = etree.parse(open('../schema/ukrdc/UKRDC.xsd', 'r'))
        self.ukrdc_xmlschema = etree.XMLSchema(xmlschema_doc)

    def test_sample_file(self):

        xml_doc = etree.parse(open('../sample_files/ukrdc/ukrdc.xml', 'r', encoding='utf-8'))
        self.ukrdc_xmlschema.validate(xml_doc)
        
        tree = etree.ElementTree(xml_doc.getroot())
        
        errors_found = False
        
        for i, error in enumerate(xmlschema.error_log):
        
            errors_found = True
        
            line_number = error.line
            column_number = error.column
            error_message = error.message

            for e in tree.xpath('.//*'):
                if line_number == e.sourceline:
                    print("Error: ", i)
                    print(tree.getpath(e))
                    print(error.message)
                    
                    
        self.assertFalse(errors_found)