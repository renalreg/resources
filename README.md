# UKRDC Schema

This package generates pyxb models as a Python library, and contains copies of schemas used for this.

* schema/pv2
* schema/rrtf - The reference copy of this is in https://bitbucket.renalregistry.nhs.uk/projects/RR/repos/rr_resources/browse/rr/resources/schema
* schema/ukrdc - This is the reference copy.

There is a Bamboo job to copy the UKRDC schema to github ( https://github.com/renalreg/ukrdc ).

## Installing the built schema module

`pip install ukrdc-schema`

It is **strongly** suggested you specify a version wherever possible, e.g.

`pip install ukrdc-schema==2.4.0`

## schema_build

This is the code to build the pyxb packages which then form the ukrdc_schema package.

## schema_build/ukrdc_schema/transforms/RR_XML_to_TXT.xsl

This turns an XML in the format defined by schema/rrtf to the "RR" format most UKRR Quarterly files are submitted in. This is also a copy of a file from the rr_resources repo.

This is included in the ukrdc_schema package so it can be referenced by the UKRDC UKRR Export.

## scripts

This is a script to produce an Excel document which compares the UKRDC XML schema to the UKRDC database with the idea of identifying where there is a mismatch between the field size and the restriction on the XML element etc.. It is published as an Artifact in Bamboo. It is not currently used.
