from setuptools import setup
from setuptools import find_packages

setup(
    name="ukrdc_xsdata",
    version="3.3.0-post.1",
    long_description="XSData models for the UKRDC",
    author="UK Renal Registry",
    author_email="rrsystems@renalregistry.nhs.uk",
    url="https://www.renalreg.org/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["xsdata"],
)
