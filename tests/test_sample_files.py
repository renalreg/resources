from unittest import TestCase
import glob

from lxml import etree


class ValidationError(Exception):
    pass


class TestSampleFileValidation(TestCase):
    def test_sample_files(self):
        # For each sample file
        for sample_path in glob.glob("sample_files/ukrdc/*.xml"):
            # Run as a subtest
            with self.subTest(msg=sample_path):
                # Open the schema and sample files for reading
                with open(
                    "schema/ukrdc/UKRDC.xsd", "r", encoding="utf-8"
                ) as schema_file, open(
                    sample_path, "r", encoding="utf-8"
                ) as sample_file:

                    # Create a new schema object to track errors for this file
                    xml_schema = etree.XMLSchema(
                        etree.parse(
                            schema_file,
                            parser=None,
                        )
                    )

                    # Try validating the sample file against the schema
                    try:
                        xml_schema.assertValid(etree.parse(sample_file, None))
                    # Initially catch errors to allow reporting multiple issues in one file
                    except etree.DocumentInvalid as e:
                        # Print all errors
                        print("Validation error(s):")
                        for error in xml_schema.error_log:
                            print("  Line {}: {}".format(error.line, error.message))
                        # Raise an exception to fail the test and report the full error list
                        raise ValidationError(
                            f"{len(xml_schema.error_log)} validation error(s) in {sample_path}. See full output above for details."
                        ) from e
