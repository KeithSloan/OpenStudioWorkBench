# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2025 Keith Sloan <keith@sloan-home.co.uk>              *
# *                                                                        *
# *                                                                        *
# *   This program is free software; you can redistribute it and/or modify *
# *   it under the terms of the GNU Lesser General Public License (LGPL)   *
# *   as published by the Free Software Foundation; either version 2 of    *
# *   the License, or (at your option) any later version.                  *
# *   for detail see the LICENCE text file.                                *
# *                                                                        *
# *   This program is distributed in the hope that it will be useful,      *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# *   GNU Library General Public License for more details.                 *
# *                                                                        *
# *   You should have received a copy of the GNU Library General Public    *
# *   License along with this program; if not, write to the Free Software  *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# *   USA                                                                  *
# *                                                                        *
# *   Acknowledgements :                                                   *
#                                                                          *
#    Takes as input a Volume Name, GDML file  and outputs                  *
#              a directory structure starting at the specified Volume Name *
#                                                                          *
#                                                                          *
############################################################################

import FreeCAD, FreeCADGui

from freecad.openStudio.BMIclass import BMIclass

#if open.__module__ in ['__builtin__', 'io']:
#    pythonopen = open # to distinguish python built-in open function from the one declared here

def createStructure(self):
	print(f"Create GBxml Structure {self}")
	self.checkGroup()
	self.gbXML = self.xmlRoot.find('./xsd:element[@name="gbXML"]', self.namespaces)
	name = self.gbXML.get('name')
	print(f"gbXML {self.gbXML} {name}")
	self.processElement(self.gbXML)

def printInfo(self, element):
    print(f"values {element.values()}")
    print(f"keys {element.keys()}")
    print(f"attrib {element.attrib}")
    name = element.get('name')
    type_ = element.get('type')
    print(f"name {name} type {type_}")
    #print(f"tag {element.tag}")  
    #print(f"nsmap {element.nsmap}")  
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

def getElementType(self, eName):
    #
    #   1 enum
    #
    print(f"Get Element Type by Name {eName}")
    print('./xsd:element[@name="'+eName+'"]')
    element = self.root.find('./xsd:element[@name="'+eName+'"]', self.namespaces)
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
   elif localName == "documentation":
            print(f"{localName} : {elem.text}")
        else:
            print(localName)

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



