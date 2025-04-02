import xmlschema

schema_file = "/Users/ksloan/Workbenches/OpenStudioWorkBench/util/GBxml.xsd"
    
schema = xmlschema.XMLSchema("schema_file")
campas = schema.elements["Campas"]
    
enumerate_values = {}
for c in campas.type.content:
    for comp in c.type.iter_components():
        if isinstance(comp, xmlschema.validators.XsdEnumerationFacets):
           enumerate_values[c.local_name] = [x.get("value") for x in comp]
    
print(enumerate_values)
