#!/bin/bash

# Matching based on https://gist.github.com/rverst/1f0b97da3cbeb7d93f4986df6e8e5695

# NOTE: This is currently only compatible with standard semantic versions, with pre-release or build metadata separated with a dash (-)
# E.g. 1.0.0, 1.0.0-alpha.1, 1.0.0-alpha.1+build.1, 1.0.0-post1 etc.

function chsv_check_version() {
    if [[ $1 =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-((0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)(\.(0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*))*))?(\+([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*))?$ ]]; then
        echo "$1"
    else
        echo ""
    fi
}

function chsv_check_version_ex() {
    if [[ $1 =~ ^v.+$ ]]; then
        chsv_check_version "${1:1}"
    else
        chsv_check_version "${1}"
    fi
}

# Get first argument, if given
versiontoset=$1

# If not given, find latest git tag
if [ -z "$versiontoset" ]
then
    echo "\$versiontoset is empty. Finding latest git tag"
    versiontoset=$(git describe --abbrev=0 --tags)
fi

# Normalize to a semantic version number
semver=$(chsv_check_version_ex "$versiontoset")

if [ -z "$semver" ]
then
    echo "Invalid version code. Exiting"
    exit 1
fi

echo "Setting versions to $semver"

# Set paths to files to be changed
xsdatapath="xsdata_build/setup.py"
pyxbpath="pyxb_build/ukrdc_schema/__init__.py"
schemapath="schema/ukrdc/UKRDC.xsd"

samplesdir="sample_files/ukrdc"

# Set version in files
sed -i "s/__version__ = \"[^\"]*\"/__version__ = \"${semver}\"/g" "$pyxbpath"
sed -i "s/version=\"[^\"]*\"/version=\"${semver}\"/g" "$xsdatapath"
sed -i "s/version=\"[^\"]*\"/version=\"${semver}\"/g" "$schemapath"

for sample_file in $samplesdir/*.xml; do sed -i "s/schemaVersion=\"[^\"]*\"/schemaVersion=\"${semver}\"/g" "$sample_file"; done

echo "Done"
