# UKRDC Resources

XSD schemas, Python binding libraries, and schema analysis scripts for the UKRDC and related projects.

[Current schema documentation](https://renalreg.github.io/resources/master/)

[Current schema diagram](https://renalreg.github.io/resources/master/diagram.svg)

## Versions and branches

The `master` branch of this repository should contain the currently accepted version of all schemas.

All in-development versions will be within other branches.

Old versions will be tagged.

## `schema`

Contains XSD schemas for UKRDC, PV, and RRTF files.

## `sample_files`

Contains sample UKRDC XML files used for schema testing.

## `tests`

Uses PyTest to ensure that the current schema correctly matches a sample file.

### Usage

* Install Tox (`pip install tox`)
* Run tox from the repository root (`tox`)

## `docs_build`

Builds HTML and SVG schema documentation, and deploys to GitHub Pages.

Each branch and tag gets it's own documentation subdirectory, so old schema versions will still have documentation available, and in-development changes can be viewed.

## `xsdata_build` (XSData Schemas)

This is the code to build the `ukrdc-xsdata` models library.

See [xsdata_build/README.md](./xsdata_build/README.md) for details

## `pyxb_build` (PyXB Schemas)

This is the code to build the PyXB packages which then form the ukrdc_schema package.

See [pyxb_build/README.md](./pyxb_build/README.md) for details

## `scripts`

This contains a script to produce an Excel document which compares the UKRDC XML schema to the UKRDC database with the idea of identifying where there is a mismatch between the field size and the restriction on the XML element etc.

It is not currently used.

See [scripts/README.md](./scripts/README.md) for details.

## Developer Notes

### Setting versions

To set the XSD schema version *and* both library versions (PyXB and XSData), run:

`./setversions.sh ${VERSION_TO_SET}`

replacing `${VERSION_TO_SET}` with the version you want to set.

Alternatively, you can omit the version number and the script will set the version to the latest git tag, if it is a valid semantic version number.
