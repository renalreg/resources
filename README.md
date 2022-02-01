# UKRDC Resources

XSD schemas, Python binding libraries, and schema analysis scripts for the UKRDC and related projects.

## `schema`

Contains XSD schemas for UKRDC, PV, and RRTF files.

## `sample_files`

Contains sample UKRDC XML files used for schema testing.

## `tests`

Uses PyTest to ensure that the current schema correctly matches a sample file.

### Usage

* Install Tox (`pip install tox`)
* Run tox from the repository root (`tox`)

## `xsdata_build` (XSData Schemas)

This is the code to build the `ukrdc-xsdata` models library.

See [xsdata_build/README.md](./xsdata_build/README.md) for details

## `schema_build` (PyXB Schemas)

This is the code to build the PyXB packages which then form the ukrdc_schema package.

See [schema_build/README.md](./schema_build/README.md) for details

## `scripts`

This contains a script to produce an Excel document which compares the UKRDC XML schema to the UKRDC database with the idea of identifying where there is a mismatch between the field size and the restriction on the XML element etc.

It is not currently used.

See [scripts/README.md](./scripts/README.md) for details.
