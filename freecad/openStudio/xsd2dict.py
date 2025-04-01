import xmlschema
#data_schema = xmlschema.XMLSchema('my_schema.xsd')
data_schema = xmlschema.XMLSchema('./Resources/gbxml.xsd')
#data=data_schema.to_dict('my_data.xml')
data=data_schema.to_dict('../../../Sample_gbxml_files/Urban_HouseMEP.xml')
