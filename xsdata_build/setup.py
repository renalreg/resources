from setuptools import setup
from setuptools import find_packages
from pathlib import Path

# Read the contents of the README file
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name="ukrdc-xsdata",
    version="3.3.0.post1",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="UK Renal Registry",
    author_email="rrsystems@renalregistry.nhs.uk",
    url="https://www.renalreg.org/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["xsdata"],
)
