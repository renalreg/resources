#!/bin/sh -x
ssh -f -N -M -S /tmp/ukrdc_resources_socket root@10.38.181.121 -L 6000:db.ukrdc.nhs.uk:5432
source env/bin/activate
pip install ukrdc-services
pip install xlwt
pip install lxml
python scripts/schema_report.py
ssh -S /tmp/ukrdc_resources_socket -O exit xxx
exit 0
