xsdata ../schema/ukrdc/UKRDC.xsd --config .xsdata.xml --package ukrdc_xsdata.ukrdc
xsdata ../schema/pv2/PV_2_0.xsd --config .xsdata.xml --package ukrdc_xsdata.pv
xsdata ../schema/rrtf/RRTF_4.xsd --config .xsdata.xml --package ukrdc_xsdata.rrtf

# Add py.typed to top-level package to enable type checking
touch ukrdc_xsdata/py.typed
