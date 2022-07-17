# UKRDC-Schema

PyXB models for the UKRDC.

## Installation

`pip install ukrdc-schema`

It is **strongly** suggested you specify a version wherever possible, e.g.

`pip install ukrdc-schema==2.4.0`

## Transformers

### ukrdc_schema/transforms/RR_XML_to_TXT.xsl

This turns an XML in the format defined by schema/rrtf to the "RR" format most UKRR Quarterly files are submitted in. This is also a copy of a file from the rr_resources repo.

This is included in the ukrdc_schema package so it can be referenced by the UKRDC UKRR Export.

## Basic usage

### Creating UKRDC XML

```python
import datetime
import pyxb
from ukrdc_schema import ukrdc_schema

patient_record = ukrdc_schema.PatientRecord()

patient_record.SendingFacility = "RFBAK"
patient_record.SendingExtract = "PV"

patient_record.Patient = ukrdc_schema.Patient()

patient_record.Patient.Names = pyxb.BIND()
patient_record.Patient.Names.append(
    ukrdc_schema.Name(use="L", Family="A TEST PATIENT", Given="TESTING")
)

patient_record.Patient.PatientNumbers = pyxb.BIND()
patient_record.Patient.PatientNumbers.append(
    ukrdc_schema.PatientNumber(
        Number="1111111111",
        Organization="CHI",
        NumberType="NI"
    )
)
patient_record.Patient.PatientNumbers.append(
    ukrdc_schema.PatientNumber(
        Number="U0000000",
        Organization="LOCALHOSP",
        NumberType="MRN"
    )
)

patient_record.Patient.BirthTime = datetime.datetime(year=1950, month=10, day=1)
patient_record.Patient.Gender = "9"

patient_record.Patient.Addresses = pyxb.BIND()
address_1 = ukrdc_schema.Address(Street="1 TEST STREET", Town="TEST TOWN", County="TEST COUNTY", Postcode="DK1 3GG")
address_1.Country = pyxb.BIND()
address_1.Country.CodingStandard = "ISO3166-1"
address_1.Country.Code = "GB"
address_1.Country.Description = "United Kingdom"
patient_record.Patient.Addresses.append(
    address_1
)

print(patient_record.toxml())
```

will render

```xml
<?xml version="1.0"?>
<ns1:PatientRecord xmlns:ns1="http://www.rixg.org.uk/">
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
</ns1:PatientRecord>
```
