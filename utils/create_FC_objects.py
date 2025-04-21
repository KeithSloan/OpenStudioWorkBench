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

def getElementTypeOld(element):
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

def getElementType(root, eName):
    #
    #   1 enum
    #
    print(f"Get Element Type by Name {eName}")
    print('./xsd:element[@name="'+eName+'"]')
    element = root.find('./xsd:element[@name="'+eName+'"]', namespaces)
    #element = root.find("./xsd:element[@name='{}']/Assignment".format(elemName), namespaces)
    print(f"element {element.text}")
    #print(f"Element Found {element.get('name')}")
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "element":
            print(f"{localName}")
        elif localName == "choice":
            return "enum"
        elif localName == "complexType":
            return "complexType"    
        else:
            # annotation - just print
            print(localName)
    
def getElementInfo(element):
    refName = element.get('ref')
    minOccurs = element.get('minOccurs')
    maxOccurs = element.get('maxOccurs')
    if minOccurs is None: minOccurs = ''
    if maxOccurs is None: maxOccurs = ''
    elemType = getElementType(element)
    print(f"Element {refName} type {elemType}")

def processChoice(root, element):
    print("Deal with Choice Type")
    #for subElem in element.findall('./xsd:element', namespaces):
    for elem in element.xpath('./xsd:*', namespaces=ns):
        localName = elem.xpath('local-name()')
        if localName == "element":
            type_ = getElementType(root, elem.get('ref'))
            print(f"Choice : {localName} : {elem.get('ref')} <=== /p{type_}")
        else:
            print(f"Choice {localName}")

def processComplexType(root, element):
    name = element.get('name')
    print(f"Process ComplexType : {name}")   
    for elem in element:
        localName = elem.xpath('local-name()')
            #if elem.tag.startswith(nsE):
            #    print(elem.tag[nsLen:])
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
        #elif localName == "ComplexType":
        #    print("Deal with Complex Type")
        elif localName == "choice":
            processChoice(root, elem)
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

def processElement(etree, root, element):
    name = element.get('name')
    print(f"Process Element : {name}")   
    for elem in element:
        localName = elem.xpath('local-name()')
            #if elem.tag.startswith(nsE):
            #    print(elem.tag[nsLen:])
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
        elif localName == "complexType":
            print("Deal with Complex Type")
            processComplexType(root, elem)
        elif localName == "choice":
            processChoice(root, elem)
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

def createFCObject(etree, root, element):
    print(f"create FC Object")
    name = element.get('name')
    print(f"FC Object : {name}")   
    for elem in element.iter():
    #for elem in element:
        localName = elem.xpath('local-name()')
            #if elem.tag.startswith(nsE):
            #    print(elem.tag[nsLen:])
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
        elif localName == "ComplexType":
            print("Deal with Complex Type")
            processComplexType(elem)
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
    #createFCObject(etree, root, gbXML)
    processElement(etree, root, gbXML)
    return


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

