from setuptools import setup
from setuptools import find_packages
import re

with open('ukrdc_schema/__init__.py', 'r') as f:
    match_pat = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(match_pat, f.read(), re.MULTILINE).group(1)

data = {'ukrdc_schema': ['transforms/*.xsl', 'py.typed'], }
setup(
    name='ukrdc_schema',
    version=version,
    long_description='Built schema for the ukrdc',
    author='UK Renal Registry',
    author_email='rrsystems@renalregistry.nhs.uk',
    url='https://www.renalreg.org/',
    packages=find_packages(),
    include_package_data=True,
    package_data=data,
    zip_safe=False,
)
