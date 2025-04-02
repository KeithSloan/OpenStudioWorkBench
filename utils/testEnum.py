def get_value(self, field: str, code: str, file: str):
        
        desc = ""
            
        xsd_xml = ET.parse(file)
        search_elem = f".//{{http://www.w3.org/2001/XMLSchema}}element[@name='{field}']"
        element = xsd_xml.find(search_elem)
            
        search_enum = f".//{{http://www.w3.org/2001/XMLSchema}}enumeration[@value='{code}']"
        enumeration = element.find(search_enum)
            
        if enumeration is not None:
            documentation = enumeration.find(".//{http://www.w3.org/2001/XMLSchema}documentation")
            desc = documentation.text
        else:
            desc = "N/A"
            
        return desc
