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

class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

def createStructure(self):
    import FreeCAD
    print(f"Create GBxml Structure {self}")
    #doc = FreeCAD.ActiveDocument
    #self.checkGroup()
    #self.gbXML = self.xmlRoot.find('./xsd:element[@name="gbXML"]', namespaces=self.ns)
    self.gbXML = self.xmlRoot.find('./xsd:element[@name="Cost"]', namespaces=self.ns)
    name = self.gbXML.get('name')
    print(f"gbXML {self.gbXML} {name}")
    obj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", 'gbXML')
    processElement(self, obj, self.gbXML, decend=False)

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

def getElementTypeByName(self, eName):
    print(f"Get Element Type by Name  <=== {eName} ===>")
    print('./xsd:element[@name="'+eName+'"]')
    element = self.xmlRoot.find('./xsd:element[@name="'+eName+'"]', namespaces=self.ns)
    #element = root.find("./xsd:element[@name='{}']/Assignment
    return getElementType(self, element)

def getElementType(self, element):
    #
    #   1 enum
    #
    print(f"element : text {element.text}")
    #print(f"Element Found {element.get('name')}")
    #for elem in element: 
    for elem in element:
        localName  = elem.xpath('local-name()')
        if localName == "element":
            print(f"{localName}")
            return localName
        elif localName == "complexType":
            state = localName
            break
        elif nextName == "simpleContent":
            state = localName
            break
        elif nextName == "extension":
            if 'base' in elem.keys:
                return elem.get('base')
        elif nextName == "choice":
            state = localName
            break
        else:
            # annotation - just print
            print(localName)
    #for subElem in element.findall('./xsd:element', namespaces):
    #for elem in element.xpath('./xsd:*', namespaces=self.ns):
    #    localName = elem.xpath('local-name()')
    #    if localName == "element":
    #        type_ = getElementType(self.xmlRoot, elem.get('ref'))
    #        print(f"Choice : {localName} : {elem.get('ref')} <=== {type_} ===>")
    #    else:
    #        print(f"Choice {localName}")

def addProperty(self, obj, elemName, type_, decend):
    print(f"Add property {elemName} type {type_} Parent {obj.Label}")
    while switch(type_):
        if case("complexType"):
            obj.addProperty("App::PropertyLink", elemName, "GBxml", "Description for "+elemName)
            #obj.ThePropertyName = None
            if decend:
                print(f"Parent {obj.Label}")
                subObj = findAndProcessSubElement(self, obj, elemName)
                setattr(obj, elemName, subObj)

        if case(None):
            obj.addProperty("App::PropertyString", elemName, "GBxml", "Description for "+elemName)
            #obj.ThePropertyName = None

        print(f"Element {elemName} type {type_} Not yet handled ")
        return

def processChoice(self, parent, element, decend):
    print(f"Process Choice <=== choice ===> ")
    #for subElem in element.findall('./xsd:element', namespaces):
    for elem in element.xpath('./xsd:*', namespaces=self.ns):
        localName = elem.xpath('local-name()')
        if localName == "element":
            elemName = elem.get('ref')
            #type_ = getElementTypeByName(self, elem.get('ref'))
            #print(f"Choice : {localName} : {elemName} <=== {type_} ===>")
            print(f"Choice : {localName} : {elemName}")
            #parent = parent.newObject("App::DocumentObjectGroupPython", name)
            #newParent = addProperty(self, parent, elemName, type_, decend)
            processElementByName(self, parent, elemName, decend)
            #processElementByName(self, parent, elemName, decend)
        else:
            print(f"Choice {localName}")

def processRestriction(self, parent, element):
    print(f"Process <=== Restriction ===> ")
    for elem in element:
    #or elem in element.xpath('./xsd:*', namespaces=self.ns):
        localName = elem.xpath('local-name()')
        if localName == "enumeration":
            print(f"Enumeration {elem.get('value')}")
        else:
            print(f"Restriction {localName}")

def processSimpleTypeByName(self, parent, elemName):
    element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
    processSimpleType(self, parent, element)

def processSimpleContentType(self, parent, element):
    print(f"Process <=== SimpleType ===>")
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "extension":
            print(f"Extentsion {elem.get('base')}")
        else:
            print(f"simpleType {localName}")

#def processSimpleType(self, element, obj):
#    name = element.get('name')
#    #print(f"Process <=== SimpleType ===> - Name : {name}")
#    for elem in element:
#        localName = elem.xpath('local-name()')
#        if localName == "annotation":
#            print("annottaion")
#        elif localName == "documenttion":
#            print("documentation {elem.text}")
#        elif localName == "restriction":
#            processRestriction(self, elem, obj)
#        elif localName == "enumeration":
#             print(f"Enumeration {elem.get('value')}")
    

def processAttribute(self, parent, elem):
    print(f"Process Attribute {elem.get('name')} type {elem.get('type')} use {elem.get('use')}")
    processSimpleContentType(self, parent, elem)

def processComplexType(self, element, parent, decend=False):
    name = element.get('name')
    print(f"Process <=== ComplexType ===> - Name : {name}")
    for elem in element:
        localName = elem.xpath('local-name()')
        print(f"{localName}")
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
            elemName = elem.get('ref')
            parent.addProperty("App::PropertyLink", elemName, "GBxml", "Description - "+elemName)
            if not decend:
                parent.ThePropertyName = None
            else:
                parent.ThePropertyName = findAndProcessSubElement(self, parent, elemName)
        elif localName == "choice":
            processChoice(self, parent, elem, decend)
        elif localName == "attribute":
            processAttribute(self, parent, elem)
        elif localName == "simpleContent":
            processSimpleContentType(self, parent, elem)
        #
        # Following ??
        #
        elif localName == "restriction":
            print(f"{localName} : {elem.get('base')}")
            processRestriction(self, elem, obj)
        elif localName == "simpleContent":
            processSimpleContent(self, elem, obj)
        elif localName == "attribute":
            processAttribute(self, elem)
            print(f"{localName} : {elem.get('name')} type {elem.get('type')} use {elem.get('use')}")
        elif localName == "enumeration":
             print(f"{localName} : {elem.get('value')}")
        elif localName == "documentation":
            print(f"{localName} : {elem.text}")
        else:
            print(localName)

def processElementByName(self, parent, elemName, decend=False):
    element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
    processElement(self, parent, element, decend)

def processElement(self, parent, element, decend=False):
    #from freecad.openStudio.baseObject import ViewProvider 
    
    parentType = type(parent)
    name = element.get('name')
    print(f"Process Element : {name} parent type {parentType}")
    parent = parent.newObject("App::DocumentObjectGroupPython", name) 
    #print(f"Element {name} type {getElementType(self, element)}")
    for elem in element:
        localName  = elem.xpath('local-name()')
        print(f"localName {localName}")
        if localName == "element":
            continue
        elif localName == "complexType":
            state = localName
            processComplexType(self, elem, parent, decend)
            break

        # Following ????
        #
        elif localName == "simpleContent":
            state = localName
            continue
        elif localName == "extension":
            if 'base' in elem.keys:
                return elem.get('base')
        elif localName == "choice":
            processChoice(self, elem)
            break
        else:
            # annotation - just print
            print(localName)

    return 
    parentType = type(parent)
    print(f"Process Element : {name} parent type {parentType}")
    if isinstance(parent, FreeCAD.Document):
        #obj  = parent.addObject("App::DocumentObjectGroup", name)
        obj = parent.addObject("App::DocumentObjectGroupPython", name)
    else:
        #obj  = parent.Group.addObject("App::DocumentObjectGroup", name)
        obj  = parent.newObject("App::DocumentObjectGroup", name)
    #ViewProvider(obj.ViewObject)
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
        elif localName == "complexType":
            print("Deal with Complex Type")
            return processComplexType(self, elem, obj, decend)
        elif localName == "choice":
            processChoice(self, elem)
        elif localName =="simpleType":
            processSimpleType(self, elem, obj)
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
        return None

def findAndProcessSubElement(self, parent, elemName):
    element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
    return processElement(self, parent, element, decend=False)

def createFCObject(self, element):
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
