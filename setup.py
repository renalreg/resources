from setuptools import setup, find_packages
import pkg_resources
import xml.etree.ElementTree as ET


xsd_file_path = pkg_resources.resource_filename('schema.ukrdc', 'UKRDC.xsd')  # File path relative to the repo, like /schema/ukrdc/UKRDC.xsd
xsd_schema = ET.parse(xsd_file_path)
root = xsd_schema.getroot()
version = root.attrib.get('version')  # Get the version attribute from the root element

setup(
    name='resources',
    version=version,  # Set the version to correspond with the XSD schema version
    packages=find_packages(),
    package_data={'schema.ukrdc': ['*.xsd'], 'schema.pv2': ['*.xsd'], 'schema.rrtf': ['*.xsd']},
    include_package_data=True
)