# UKRDC-XSData

XSData models for the UKRDC.

## Installation

`pip install ukrdc-xsdata`

## Basic usage

### Creating UKRDC XML

```python
import datetime
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc import PatientRecord, Patient, types

record = PatientRecord(
    sending_facility = "RFBAK",
    sending_extract = "PV",
    patient = Patient(
        birth_time = XmlDateTime.from_datetime(datetime.datetime(year=1950, month=10, day=1)),
        gender = types.gender.Gender.VALUE_9,
        names = Patient.Names(
            name = [
                types.Name(
                    use="L",
                    family="A TEST PATIENT", 
                    given="TESTING"
                )
            ]
        ),
        addresses = Patient.Addresses(
            address = [
                types.Address(
                    street="1 TEST STREET",
                    town="TEST TOWN",
                    county="TEST COUNTY",
                    postcode="DK1 3GG",
                    country=types.Address.Country(
                        coding_standard="ISO3166-1",
                        code="GB",
                        description="United Kingdom"
                    )
                )
            ]
        ),
        patient_numbers = types.PatientNumbers(
            patient_number = [
                types.PatientNumber(
                    number="1111111111",
                    organization=types.PatientNumberOrganization.CHI,
                    number_type=types.PatientNumberNumberType.NI,
                ),
                types.PatientNumber(
                    number="U0000000",
                    organization=types.PatientNumberOrganization.LOCALHOSP,
                    number_type=types.PatientNumberNumberType.MRN,
                )
            ]
        )
    )
)


from xsdata.formats.dataclass.serializers.xml import XmlSerializer

print(XmlSerializer().render(record))
```

will render

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ns0:PatientRecord xmlns:ns0="http://www.rixg.org.uk/">
    <SendingFacility>RFBAK</SendingFacility>
    <SendingExtract>PV</SendingExtract>
    <Patient>
        <PatientNumbers>
            <PatientNumber>
                <Number>1111111111</Number>
                <Organization>CHI</Organization>
                <NumberType>NI</NumberType>
            </PatientNumber>
            <PatientNumber>
                <Number>U0000000</Number>
                <Organization>LOCALHOSP</Organization>
                <NumberType>MRN</NumberType>
            </PatientNumber>
        </PatientNumbers>
        <Names>
            <Name use="L">
                <Family>A TEST PATIENT</Family>
                <Given>TESTING</Given>
            </Name>
        </Names>
        <BirthTime>1950-10-01T00:00:00</BirthTime>
        <Gender>9</Gender>
        <Addresses>
            <Address>
                <Street>1 TEST STREET</Street>
                <Town>TEST TOWN</Town>
                <County>TEST COUNTY</County>
                <Postcode>DK1 3GG</Postcode>
                <Country>
                    <CodingStandard>ISO3166-1</CodingStandard>
                    <Code>GB</Code>
                    <Description>United Kingdom</Description>
                </Country>
            </Address>
        </Addresses>
    </Patient>
</ns0:PatientRecord>
```

### Reading UKRDC XML

```python
in_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<ns0:PatientRecord xmlns:ns0="http://www.rixg.org.uk/">
    <SendingFacility>RFBAK</SendingFacility>
    <SendingExtract>PV</SendingExtract>
    <Patient>
        <PatientNumbers>
            <PatientNumber>
                <Number>1111111111</Number>
                <Organization>CHI</Organization>
                <NumberType>NI</NumberType>
            </PatientNumber>
            <PatientNumber>
                <Number>U0000000</Number>
                <Organization>LOCALHOSP</Organization>
                <NumberType>MRN</NumberType>
            </PatientNumber>
        </PatientNumbers>
        <Names>
            <Name use="L">
                <Family>A TEST PATIENT</Family>
                <Given>TESTING</Given>
            </Name>
        </Names>
        <BirthTime>1950-10-01T00:00:00</BirthTime>
        <Gender>9</Gender>
        <Addresses>
            <Address>
                <Street>1 TEST STREET</Street>
                <Town>TEST TOWN</Town>
                <County>TEST COUNTY</County>
                <Postcode>DK1 3GG</Postcode>
                <Country>
                    <CodingStandard>ISO3166-1</CodingStandard>
                    <Code>GB</Code>
                    <Description>United Kingdom</Description>
                </Country>
            </Address>
        </Addresses>
    </Patient>
</ns0:PatientRecord>
"""

from ukrdc_xsdata.ukrdc import PatientRecord
from xsdata.formats.dataclass.parsers import XmlParser

obj = XmlParser().from_string(in_xml, PatientRecord)
```

The object `obj` can then be used to access the data as a standard Python dataclass instance.
E.g. `obj.sending_facility` or `obj.patient.names.name`.
