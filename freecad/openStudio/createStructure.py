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
    self.gbXML = self.xmlRoot.find('./xsd:element[@name="gbXML"]', namespaces=self.ns)
    #self.gbXML = self.xmlRoot.find('./xsd:element[@name="Cost"]', namespaces=self.ns)
    #self.gbXML = self.xmlRoot.find('./xsd:element[@name="LightingSystem"]', namespaces=self.ns)
    #self.gbXML = self.xmlRoot.find('./xsd:element[@name="AltEnergySource"]', namespaces=self.ns)
    #self.gbXML = self.xmlRoot.find('./xsd:element[@name="MinFlow"]', namespaces=self.ns)
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
            print(f"Not handled Choice {localName}")

def processRestriction(self, parent, element):
    print(f"Process <=== Restriction ===> ")
    eNumLst = []
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "enumeration":
            eNumValue = elem.get('value')
            print(f"Enumeration {eNumValue}")
            eNumLst.append(eNumValue)
            
        else:
            print(f"Not Handled Restriction {localName}")

    return eNumLst

def processXsdType(self, obj, name, type_):
    print(f"Process XsdType {type_} {type(type_)}")
    XSD_TO_FC_MAP = {
        "xsd:string": "App::PropertyString",
        "xsd:int": "App::PropertyInteger",
        "xsd:integer": "App::PropertyInteger",
        "xsd:float": "App::PropertyFloat",
        "xsd:double": "App::PropertyFloat",
        "xsd:decimal": "App::PropertyFloat",
        "xsd:boolean": "App::PropertyBool",
        "xsd:dateTime": "App::PropertyTime",
        "xsd:duration": "App::PropertyTime",
        "xsd:ID" : "App::PropertyString",
        "xsd:IDREF" : "App::PropertyString",
        }
    FC_Type = XSD_TO_FC_MAP.get(type_)
    if FC_Type is not None:
    #    print(f" Not Mapped must be Enumerate")
    #    FC_Type = "App::PropertyEnumration"
    #    element = self.xmlRoot.find('./xsd:element[@name="'+name+'"]', namespaces=self.ns)
    #    eNumLst = processRestriction(self, obj, element)
    #    obj.addProperty("App::PropertyEnumeration", name, "GBxml", "Description")
    #    setattr(obj, name, eNumLst)
        chkName = checkName(self, name)
        print(f"Add property {chkName} to {obj.Label} type {type_}")
        obj.addProperty(FC_Type, chkName, "GBxml")
        return True
    else:
        print("Not Single processXsdType {type_}")
        return False
        # Could be Enum

def processExtension(self, parent, element):
    varType = element.get('base')
    print(f"Process Extension - Type {varType} Parent {parent.Label}")
    processXsdType(self, parent, parent.Label, varType)
    #processRestriction(self, parent, elem)
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "attribute":
            processAttribute(self, parent, elem)
        else:
            print(f"Not Handled -  Extension {localName}")

def processUnion(self, parent, element):
    # return set for unique values
    memberTypes = element.get('memberTypes')
    print(f"Process Union : parent {parent.Label} memberTypes [{memberTypes}]")
    if memberTypes is not None:
        # Use set for unique values
        XsdEnumLst = []
        for member in memberTypes.split(' '):
            XsdEnumLst.extend(processSimpleTypeByName(self, parent, member))
        print(XsdEnumLst)
        return set(XsdEnumLst)
    else:
        print("Not handled process Union")

def processSimpleType(self, parent, element):
    print(f"Process <=== SimpleType ===> Parent Name {parent.Label}")
    # SimpleType - should only be one elem
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "extension":
            processExtension(self, parent, elem)
        elif localName == "restriction":
            return processRestriction(self, parent, elem)
        elif localName == "union":
            return list(processUnion(self, parent, elem))
        else:
            print(f"Not handled - simpleType {localName}")

def processSimpleTypeByName(self, parent, elemName):
    print(f"Process SingleType By Name {elemName}")
    element = self.xmlRoot.find('./xsd:simpleType[@name="'+elemName+'"]', namespaces=self.ns)
    print(f"Process SingleType By Name - Found {element}")
    return processSimpleType(self, parent, element)

def processAnnotation(self, parent, element):
    print(f"Process <=== Annotation ===> Parent Name {parent.Label}")
    for elem in element:
        localName = elem.xpath('local-name()')
        if localName == "documentation":
            print(f"{localName} : {elem.text}")
        else:
            print(f"Annotation Not Handled {localName}")

def processAttribute(self, parent, element):
    print(f"Process Attribute parent {parent.Label} name {element.get('name')} type {element.get('type')} use {element.get('use')}")
    elemName = element.get('name')
    typeName = element.get('type')
    use = element.get('use')
    if typeName is None:
        print(f"Process Attribute - Type is None")
        for elem in element:
            localName = elem.xpath('local-name()')
            if localName == "simpleType":
                XsdEnumLst = processSimpleType(self, parent, elem)
            elif localName == "documentation":
                print(f"Attribute - documentatton {elem.text}")
            else:
                print(f"Not  Handled - Process Attribute {localName}")
                break
            print(f"Add Enumertion Property to {parent.Label} name {elemName} length {len(XsdEnumLst)}")
            print(f"XsdEnumLst {XsdEnumLst}"
            )
            eNumObj = parent.addProperty("App::PropertyEnumeration", elemName, "GBxml", elemName+"Desctription")
            setattr(eNumObj, elemName, XsdEnumLst) 

    # Check for eNum types are enumerations in restricted in simplType
    #eNumList = processSimpleTypeByName(self, parent, typeName)
    elif not processXsdType(self, parent, elemName, typeName):
        element = self.xmlRoot.find('./xsd:simpleType[@name="'+typeName+'"]', namespaces=self.ns)
        print(f"Process XsdType - Found {element}")
        XsdEnumLst = processSimpleType(parent, parent, element)
        print(f"Add Enumertion Property to {parent.Label} name {elemName} length {len(XsdEnumLst)}")
        eNumObj = parent.addProperty("App::PropertyEnumeration", elemName, "GBxml", elemName+"Desctription")
        setattr(eNumObj, elemName, XsdEnumLst)        
    else:
        print("Not Handled Process Attribute")

def processComplexType(self, element, parent, decend=False):
    name = element.get('name')
    print(f"Process <=== ComplexType ===> - Name : {name} ParentName {parent.Label}")
    for elem in element:
        localName = elem.xpath('local-name()')
        print(f"{localName}")
        if localName == "element":
            print(f"{localName} : {elem.get('ref')}")
            elemName = elem.get('ref')
            parent.addProperty("App::PropertyLink", elemName, "GBxml", "Description - "+elemName)
            print(f"Add property {elemName} to {parent.Label}")
            # Should handling of decend be im processElement
            if not decend:
                parent.ThePropertyName = None
            else:
                parent.ThePropertyName = findAndProcessSubElement(self, parent, elemName)
        elif localName == "choice":
            processChoice(self, parent, elem, decend)
        elif localName == "attribute":
            processAttribute(self, parent, elem)
        elif localName == "simpleContent":
            processSimpleType(self, parent, elem)
        #
        # Following ??
        #
        elif localName == "restriction":
            print(f"{localName} : {elem.get('base')}")
            processRestriction(self, elem, obj)
        elif localName == "enumeration":
             print(f"{localName} : {elem.get('value')}")
        elif localName == "documentation":
            print(f"{localName} : {elem.text}")
        else:
            print(f" Not handled ComplexType {localName}")

def processElementByName(self, parent, elemName, decend=False):
    print(f"Process Element By Name - Parent {parent.Label} Element Name {elemName}")
    element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
    processElement(self, parent, element, decend)

def addElementProperty(self, parent, name, type_):
    # Maybe call processXsdType direct
    processXsdType(self, parent, name, type_)

def checkName(self, name):
    # FC names cannot contain -
    probChars = "-"

    good = ""
    for i in name:
        if i not in probChars:
            good += i
        else:
            good += ('_')
    return good

def createObjectGroup(self, parent, chkName):
    if parent is not None:
        return parent.newObject("App::DocumentObjectGroup", chkName)
    else:
        return FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", chkName)

    
def processElement(self, parent, element, decend=False):
    #from freecad.openStudio.baseObject import ViewProvider 
    parentType = type(parent)
    name = element.get('name')
    chkName = checkName(self, name)
    print(f"Process Element : {chkName}")
    type_ = element.get('type')
    if type_ is not None:
        addElementProperty(self, parent, chkName, type_)
        return
    else:   # Create as Group Object  
        parent = createObjectGroup(self, parent, chkName)  
        #parent = parent.newObject("App::DocumentObjectGroupPython", name)
        #parent = parent.newObject("App::DocumentObjectGroup", chkName)
        #
        # for gbXML - Object Group alreadt created
        #
        # FC creates unique name so make sure Label reflects name
        setattr(parent,"Label", name)
        for elem in element:
            localName  = elem.xpath('local-name()')
            print(f"localName {localName}")
            if localName == "element":
                continue
            elif localName == "complexType":
                #state = localName
                processComplexType(self, elem, parent, decend)
                break

            # Following ????
            #
            elif localName == "simpleContent":
                #state = localName
                continue
            elif localName == "extension":
                if 'base' in elem.keys:
                    return elem.get('base')
            elif localName == "choice":
                processChoice(self, elem)
                break
            elif localName == "annotation":
                print(f"{localName} : {elem.text}")
            else:
                # annotation - just print
                print(localName)

        return 
        #parentType = type(parent)
        #print(f"Process Element : {name} parent type {parentType}")
        #if isinstance(parent, FreeCAD.Document):
            #obj  = parent.addObject("App::DocumentObjectGroup", name)
        #    obj = parent.addObject("App::DocumentObjectGroupPython", name)
        #else:
            #obj  = parent.Group.addObject("App::DocumentObjectGroup", name)
        #    obj  = parent.newObject("App::DocumentObjectGroup", name)
        #ViewProvider(obj.ViewObject)
        #for elem in element:
        #    localName = elem.xpath('local-name()')
        #    if localName == "element":
        #        print(f"{localName} : {elem.get('ref')}")
        #    elif localName == "complexType":
        #        print("Deal with Complex Type")
        #        return processComplexType(self, elem, obj, decend)
        #    elif localName == "choice":
        #        processChoice(self, elem)
        #    elif localName =="simpleType":
        #        processSimpleType(self, elem, obj)
        #    elif localName == "restriction":
        #        print(f"{localName} : {elem.get('base')}")
        #    elif localName == "attribute":
        #        print(f"{localName} : {elem.get('name')} type {elem.get('type')} use {elem.get('use')}")
        #    elif localName == "enumeration":
        #        print(f"{localName} : {elem.get('value')}")
        #    else:
        #        print(localName)
        #    return None

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
