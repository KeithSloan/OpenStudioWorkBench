from  lxml import etree as ET
import argparse

# Define the namespace for XSD elements
namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
ns = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

def printInfo(element):
    print(f"values {element.values()}")
    print(f"keys {element.keys()}")
    print(f"attrib {element.attrib}")
    name = element.get('name')
    type_ = element.get('type')
    print(f"name {name} type {type_}")
    #print(f"tag {element.tag}")  
    #print(f"nsmap {element.nsmap}")  

def getElementType(element):
    ###
    # 1 - FC Object
    # 2 - Enumeration
    # 3 - String
    # 4 - Integer
    print(f"get Element Type")
    #print(dir(element))
    printInfo(element)
    #print("iterChildren")
    #for subElem in element.iterchildren(): 
    #    printInfo(subElem)
    #    subName = subElem.xpath('local-name()')
    #    if subName == "ComplexType":
    #        print("Deal with Complex Type")
    #    elif subName == "choice":
    #        print(f"Get type : choice")
    #for subElem in element.findall('*'): 
    #    printInfo(subElem)
    print("Siblings")
    for sibling in element.itersiblings(): 
        printInfo(sibling)
    for sibling in element.xpath('local-name()'):
        print(f"Format {sibling.format()}")
        print(f"isalnum {sibling.isalnum()}")
        print(f"isalpha {sibling.isalpha()}")
        print(f"isascii' {sibling.isascii()}")
        print(f"isdecimal {sibling.isdecimal()}")
        print(f"isdigit {sibling.isdigit()}")
        #print(dir(sibling))
        

    
def getElementInfo(element):
    refName = element.get('ref')
    minOccurs = element.get('minOccurs')
    maxOccurs = element.get('maxOccurs')
    if minOccurs is None: minOccurs = ''
    if maxOccurs is None: maxOccurs = ''
    elemType = getElementType(element)
    print(f"Element {refName} type {elemType}")



def processChoice(element):
    print("Deal with Choice Type")
    #for subElem in element.findall('./xsd:element', namespaces):
    for elem in element.xpath('./xsd:*', namespaces=ns):
        localName = elem.xpath('local-name()')
        if localName == "element":
            print(f"Choice : {localName} : {elem.get('ref')}")
        else:
            print(f"Choice {localName}")


def createFCObject(etree, root, element):
    print(f"create FC Object")
    name = element.get('name')
    print(f"FC Object : {name}")
    for elem in element.iter():
		#print(subElem) 
		#print(subElem.tag)
        # Register the namespace
        ns = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
        #nsE = u'{%s}' % ns
        #nsLen = len(nsE)

        # Use the registered namespace in the XPath expression
        #element = etree.xpath('//my_namespace:element', namespaces=ns)[0]
        #element = etree.xpath('//xsd:*', namespaces=ns)
        #print(element.text)  # Output: Value
        #subName = subElem.xpath('local-name()')
        #subName = subElem.xpath('./xsd:*', namespaces = {root.nsmap})
        # Following works but get url
        #subName = subElem.xpath('./xsd:*', namespaces=ns)
        #print(f"subName {subName}")
        #for elem in subName:
        localName = elem.xpath('local-name()')
            #if elem.tag.startswith(nsE):
            #    print(elem.tag[nsLen:])
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
        elif localName == "ComplexType":
            print("Deal with Complex Type")
        elif localName == "choice":
            processChoice(elem)
        elif localName == "restriction":
            print(f"{localName} : {elem.get('base')}")
        elif localName == "attribute":
            print(f"{localName} : {elem.get('name')} type {elem.get('type')} use {elem.get('use')}")
        elif localName == "enumeration":
             print(f"{localName} : {elem.get('value')}")
        elif localName == "documentation":
            print(f"{localName} : {elem.text}")
        else:
            print(localName)

    

# Define a function to parse the XSD schema and extract the elements and their properties
def parse_xsd(xsd_file):
    etree = ET.parse(xsd_file)
    root = etree.getroot()

	# Define the namespace for XSD elements
    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}

    gbXML = root.find('./xsd:element[@name="gbXML"]', namespaces)
    name = gbXML.get('name')
    print(f"gbXML {gbXML} {name}")
    createFCObject(etree, root, gbXML)
    return

    for element in root.findall('./xsd:element', namespaces):
        name = element.get('name')
        type_ = element.get('type')
        
	# Handle complex types
    if type_ is None:
            # Handle case where the element is a complex type or a sequence of elements
            complex_type = element.find('./xsd:complexType', namespaces)
            if complex_type is not None:
                # Nested elements in complex type
                nested_elements = []
                for sub_element in complex_type.findall('.//xsd:element', namespaces):
                    nested_name = sub_element.get('name')
                    nested_type = sub_element.get('type')
                    nested_elements.append((nested_name, nested_type))
                elements.append((name, 'complex', nested_elements))
            else:
                # Simple elements (i.e., only one type)
                elements.append((name, type_, []))
    else:
		# Simple element with a direct type
        elements.append((name, type_, []))
    
    return elements

# Function to generate FreeCAD FeaturePython code
def generate_freecad_code(elements):
    feature_code = """import FreeCAD, FreeCADGui
from PySide2 import QtCore
from FreeCAD import Base
import Part

class MyFeature(FreeCAD.FeaturePython):
    def __init__(self, obj):
        obj.addProperty("App::PropertyString", "Name", "Data", "Name of the object").Name = "Default"
"""
    
    # Generate properties for each element found
    for name, type_, nested_elements in elements:
        # Generate a property based on the type
        if type_ == 'string':
            feature_code += f'        obj.addProperty("App::PropertyString", "{name}", "Data", "{name} property")\n'
        elif type_ == 'int':
            feature_code += f'        obj.addProperty("App::PropertyInteger", "{name}", "Data", "{name} property")\n'
        elif type_ == 'float':
            feature_code += f'        obj.addProperty("App::PropertyFloat", "{name}", "Data", "{name} property")\n'
        elif type_ == 'complex':
            feature_code += f'        obj.addProperty("App::PropertyString", "{name}", "Data", "Complex {name} property")\n'
            # For nested complex types, we can generate additional properties
            for nested_name, nested_type in nested_elements:
                if nested_type == 'string':
                    feature_code += f'        obj.addProperty("App::PropertyString", "{nested_name}", "{name}", "Nested {nested_name} property")\n'
                elif nested_type == 'int':
                    feature_code += f'        obj.addProperty("App::PropertyInteger", "{nested_name}", "{name}", "Nested {nested_name} property")\n'
                elif nested_type == 'float':
                    feature_code += f'        obj.addProperty("App::PropertyFloat", "{nested_name}", "{name}", "Nested {nested_name} property")\n'

    # Finalizing the FreeCAD FeaturePython class
    feature_code += """
    def execute(self, obj):
        # Implement the feature calculation here
        pass
"""

    return feature_code

# Main function to parse command line arguments and process the XSD file
def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Generate FreeCAD FeaturePython code from an XSD schema.")
    parser.add_argument("xsd_file", help="Path to the XSD file")
    args = parser.parse_args()
    
    # Parse the XSD schema
    elements = parse_xsd(args.xsd_file)
    
    # Generate the FreeCAD FeaturePython code
    #freecad_code = generate_freecad_code(elements)
    
    # Output the generated code
    #with open("generated_feature.py", "w") as f:
    #    f.write(freecad_code)

    #print("FreeCAD FeaturePython code has been generated in 'generated_feature.py'")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()

