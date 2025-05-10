# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2025 Keith Sloan <ipad2@sloan-home.co.uk>               *
# *                                                                         *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# *   Acknowledgements :                                                    *
# *                                                                         *
# *   Takes as input a Volume Name, GDML file  and outputs                  *
# *             a directory structure starting at the specified Volume Name *
# *                                                                         *
# *                                                                         *
# *                                                                         *
# *                                                                         *
############################################################################*

import FreeCAD as App

class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

class XrbClass():
    
    def __init__(self):
        super().__init__()
        self.Prefix = "BMI_"
        self.gbObj = None		# gbXML object
        self.gbXML = None
        self.initLxsd()

        #def initXrd(self):
        #	#print(f"Create Group")
        #	#self.Group = App.ActiveDocument.addObject('App::DocumentObjectGroup', self.Prefix)
        #	self.initLxsd()

    def initLxsd(self):
        import os
        print(f"Init lxsd Class")
        self.Campus = None		# Campus one per BMI
        self.ns = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
        self.Resources = os.path.join(App.getUserAppDataDir(), "Mod", \
			"OpenStudioWorkBench","freecad", "openStudio","Resources")
        self.xsd_file = os.path.join(self.Resources,"GBxml.xsd")
        self.parse_xsd()
        
    def checkGBxml(self):
        if self.gbXML is None:
            self.createGBxml()

    def createGBxml(self):
        #
        # Used by checkGbxml if self.gbXML has not yet been created
        #
		#from freecad.openStudio.processXrb import processXrbElement
        import FreeCAD
		#self.gbObj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", 'gbXML')
        self.gbXML = self.xmlRoot.find('./xsd:element[@name="gbXML"]', namespaces=self.ns)
        self.processXrbElement(None, self.gbXML, decend=False)
		
    def createGBxmlProcessObj(self):
		#from freecad.openStudio.processXrb import processXrbElement
        import FreeCAD
		#self.gbObj = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroupPython", 'gbXML')
        self.gbXML = self.xmlRoot.find('./xsd:element[@name="gbXML"]', namespaces=self.ns)
        self.gbXMLobj = self.processXrbElement(None, self.gbXML)
    
    def initIfc2gbxml(self):
        self.ifc2gbxmlDict = {
			"Site: Campus",
			"Terrain: xxxxx"
			"Building: Building",
			"Building Part: yyyyy ",
			"Walls: wwwww",
			"Slabs: ssss",
			"Beams: bbbbb",
			"Stairs: sssss",
			"2D Plan View: zzzz",
			"Surface: sssss",
			"Layer: lllll",
		}
        
    def parse_xsd(self):
        print("Parse GBxml xsd")
    	# Define a function to parse the XSD schema and extract the elements and their properties
        from lxml import etree as ET

        self.etree = ET.parse(self.xsd_file)
        self.xmlRoot = self.etree.getroot()
        # Define the namespace for XSD elements
		#    namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
    	#gbXML = root.find('./xsd:element[@name="gbXML"]', namespaces)

    def add2group(self, obj):
        self.checkGroup()
        self.Group.addObject(obj)

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
        self.processXrbElement(obj, self.gbXML, decend=False)
        return obj

    def createGBxmlStructure(self):
		#from freecad.openStudio.processXrb import createStructure
		#self.checkGroup()
        self.gbXMLobj = self.createStructure()
        
    def findAddObject(self, parent, baseName, Label):
        import FreeCAD
        #from freecad.openStudio.processXrb import processXrbElementByName
        print(f"Find Add Object : Parent {parent.Label} baseName {baseName} Label {Label}")
        # If baseName object already exists change label and use
        # Else create new object
        Objs = FreeCAD.ActiveDocument.getObjectsByLabel(baseName)
        print(f"Objs {Objs}")
        fullLabel = baseName + ' : ' + Label
        print(f"Full Name {fullLabel}")
        if len(Objs) == 0:
            #parent = parent.newObject("App::DocumentObjectGroup", fullLabel)
            exit
            gbObj = self.processXrbElementByName(parent, baseName, decend=False)
        else:
            gbObj = Objs[0] 
        #setattr(gbObj, "Label", fullLabel)
        gbObj.Label = fullLabel
        return gbObj

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
            "xsd:date": "App::PropertyString",      # Appears no App::PropertyDate in FreeCAD
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
            chkName = self.checkName(name)
            print(f"Add property {chkName} to {obj.Label} type {type_}")
            obj.addProperty(FC_Type, chkName, "GBxml")
            return True
        else:
            print("Not Single processXsdType {type_}")
            return False
            # Could be Enum
            # 
    def createPolyLoop(self, parent):
        from freecad.openStudio.gbObjects import PolyLoopClass
        # Treat PolyLoop Custom Object
        
        print(f"Create PolyLoop : Parent {parent.Label}")
        obj = parent.newObject("App::FeaturePython", "PolyLoop")
        PolyLoopClass(obj)
        return None

    def processXrbElementByRef(self, parent, element, decend=False):
        if 'ref' in element.keys():
            elemName = element.get('ref')
            print(f"Process Element By Ref - Parent {parent.Label} Element Name {elemName}")
            self.processXrbElementByName(parent, elemName)
        else:
            print(f"Process by Ref : But no Ref")

    def processXrbElementByName(self, parent, elemName, decend=False):
        print(f"Process Element By Name - Parent {parent.Label} Element Name {elemName}")
        # Here or in Choice
        if elemName == "PolyLoop":
            return self.createPolyLoop(parent)
        else:
            element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
            return self.processXrbElement(parent, element, decend)
            
    def processXrbElement(self, parent, element, decend=False):
        #from freecad.openStudio.baseObject import ViewProvider 
        parentType = type(parent)
        name = element.get('name')
        chkName = self.checkName(name)
        print(f"Process Element : {chkName}")
        type_ = element.get('type')
        if type_ is not None:
            self.addElementProperty(parent, chkName, type_)
        else:   # Create as Group Object  
            parent = self.createObjectGroup(parent, chkName)
            # FC creates unique name so make sure Label reflects name
            #setattr(parent,"Label", name)  
            setattr(parent,"Label", name)
        #parent = parent.newObject("App::DocumentObjectGroupPython", name)
        #parent = parent.newObject("App::DocumentObjectGroup", chkName)
        #
        # for gbXML - Object Group already created
        #
        for elem in element:
            localName  = elem.xpath('local-name()')
            print(f"localName {localName}")
            if localName == "element":
                pass
                #if 'ref' in elem.keys:
                #    prop = elem.get('ref')
                #    setattr(parent,prop,"")
            elif localName == "complexType":
                #state = localName
                self.processComplexType(elem, parent, decend)
                break

            # Following ????
            #
            # 
            elif localName == "simpleContent":
                #state = localName
                continue
            elif localName == "extension":
                if 'base' in elem.keys:
                    return elem.get('base')
            elif localName == "choice":
                self.processChoice(self, elem)
                break
            elif localName == "annotation":
                print(f"{localName} : {elem.text}")
            else:
                # annotation - just print
                print(localName)
        return parent
        #return

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
                #
                # Should handling of decend be im processXrbElement
                #
                # Following Code ??
                #    "TheProperty" introduced by VSCodium???
                #if not decend:
                #    parent.ThePropertyName = None
                #else:
                #    parent.ThePropertyName = self.findAndProcessSubElement(self, parent, elemName)
                #
            elif localName == "all":
                self.processAll(parent, elem)
            elif localName == "choice":
                #self.processChoice(parent, elem, decend)
                self.processChoice(parent, elem, decend=False)
            elif localName == "attribute":
                self.processAttribute(parent, elem)
            elif localName == "simpleContent":
                self.processSimpleType(parent, elem)
            #
            # Following ??
            #
            elif localName == "restriction":
                print(f"{localName} : {elem.get('base')}")
                self.processRestriction(parent, elem)
            elif localName == "enumeration":
                print(f"{localName} : {elem.get('value')}")
            elif localName == "documentation":
                print(f"{localName} : {elem.text}")
            else:
                print(f" Not handled ComplexType {localName}")

    def processSimpleTypeByName(self, parent, elemName):
        print(f"Process SingleType By Name {elemName}")
        element = self.xmlRoot.find('./xsd:simpleType[@name="'+elemName+'"]', namespaces=self.ns)
        print(f"Process SingleType By Name - Found {element}")
        return self.processSimpleType(parent, element)

    def processSimpleType(self, parent, element):
        print(f"Process <=== SimpleType ===> Parent Name {parent.Label}")
        # SimpleType - should only be one elem
        for elem in element:
            localName = elem.xpath('local-name()')
            if localName == "extension":
                self.processExtension(parent, elem)
            elif localName == "restriction":
                return self.processRestriction(parent, elem)
            elif localName == "union":
                return list(self.processUnion(parent, elem))
            else:
                print(f"Not handled - simpleType {localName}")

    def processAll(self, parent, element):
        print(f"Process xsd:All Parent {parent.Label}")
        for elem in element.xpath('./xsd:*', namespaces=self.ns):
            localName = elem.xpath('local-name()')
            print(f"localName {localName}")
            if localName == "element":
                print(f"Process by Ref {elem.get('ref')}")
                self.processXrbElementByRef(parent, elem)
            else:
                print(f"Process All {localName} Not Handled")
        print(f"End Process All")
                
    def processChoice(self, parent, element, decend):
        print(f"Process Choice <=== choice ===> Parent {parent.Label}")
        #for subElem in element.findall('./xsd:element', namespaces):
        for elem in element.xpath('./xsd:*', namespaces=self.ns):
            localName = elem.xpath('local-name()')
            if localName == "element":
                elemName = elem.get('ref')
                #type_ = getElementTypeByName(self, elem.get('ref'))
                #print(f"Choice : {localName} : {elemName} <=== {type_} ===>")
                print(f"Choice : {localName} : {elemName} Parent {parent.Label}")
                # Here or in processXrbElementByName ??
                if elemName == "PolyLoop":
                    print(f"process PolyLoop")
                    self.createPolyLoop(parent)
                    break
                else:
                    #parent = parent.newObject("App::DocumentObjectGroupPython", name)
                    #newParent = addProperty(self, parent, elemName, type_, decend
                    #
                    #print(f"Parent Before {parent} {parent.Label}")
                    self.processXrbElementByName(parent, elemName, decend)
                    #print(f"Parent After {parent} {parent.Label}")
                    #self.processXrbElementByName(parent, elemName)
            else:
                print(f"Not handled Choice {localName}")
        print(f"End Process Choice <=== choice ===> Parent {parent.Label}")

    def processUnion(self, parent, element):
        # return set for unique values
        memberTypes = element.get('memberTypes')
        print(f"Process Union : parent {parent.Label} memberTypes [{memberTypes}]")
        if memberTypes is not None:
            # Use set for unique values
            XsdEnumLst = []
            for member in memberTypes.split(' '):
                XsdEnumLst.extend(self.processSimpleTypeByName(parent, member))
            print(XsdEnumLst)
            return set(XsdEnumLst)
        else:
            print("Not handled process Union")

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
                    XsdEnumLst = self.processSimpleType(parent, elem)
                elif localName == "documentation":
                    print(f"Attribute - documentatton {elem.text}")
                else:
                    print(f"Not  Handled - Process Attribute {localName}")
                    break
                print(f"Add Enumertion Property to {parent.Label} name {elemName} length {len(XsdEnumLst)}")
                print(f"XsdEnumLst {XsdEnumLst}")
                eNumObj = parent.addProperty("App::PropertyEnumeration", elemName, "GBxml", elemName+"Desctription")
                setattr(eNumObj, elemName, XsdEnumLst) 

    # Check for eNum types are enumerations in restricted in simplType
    #eNumList = processSimpleTypeByName(self, parent, typeName)
        elif not self.processXsdType(parent, elemName, typeName):
            element = self.xmlRoot.find('./xsd:simpleType[@name="'+typeName+'"]', namespaces=self.ns)
            print(f"Process XsdType - Found {element}")
            XsdEnumLst = self.processSimpleType(parent, element)
            print(f"Add Enumertion Property to {parent.Label} name {elemName} length {len(XsdEnumLst)}")
            eNumObj = parent.addProperty("App::PropertyEnumeration", elemName, "GBxml", elemName+"Desctription")
            setattr(eNumObj, elemName, XsdEnumLst)        
        else:
            print("Not Handled Process Attribute")

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

    def processExtension(self, parent, element):
        varType = element.get('base')
        print(f"Process Extension - Type {varType} Parent {parent.Label}")
        self.processXsdType(parent, parent.Label, varType)
        #processRestriction(self, parent, elem)
        for elem in element:
            localName = elem.xpath('local-name()')
            if localName == "attribute":
                self.processAttribute(parent, elem)
            else:
                print(f"Not Handled -  Extension {localName}")

    def addElementProperty(self, parent, name, type_):
        # Maybe call processXsdType direct
        self.processXsdType(parent, name, type_)
     
    def processBIMobject(self, obj):
        from freecad.openStudio.processIfc import processIfcSite

        print(f"Process IFC Site ")
        objType = self.getFCType(obj)
        print(f"Label {obj.Label} Type {objType}")
        while switch (objType):
            if case("Site"):
                print(f"Process IFC Site ")        
                processIfcSite(self, obj)
                break

            if case("Space"):		# ?????
                self.getFCTypecreateIfcSpace(obj)
                break

    def processIfcSpace(self, srcObj):
        from freecad.openStudio.processSpace import processIfcSpace

        print(f"Process IFC Space ")
        processIfcSpace(self, srcObj)

    def copyParametersSameName(self, srcObj, trtObj):
        ###
	    # Properties of Target Obj are created from parsing GBxml.xsd
	    ###
        print(f"Copy Properties with same Name {srcObj.Label} {trtObj.Label}/n")
        print(f"Source Prop {srcObj.PropertiesList}/n/n")
        commonList = []
        for p in srcObj.PropertiesList:
            if p in trtObj.PropertiesList:
                commonList.append(p)
                try:
                    trtObj.p = p    
                except:
                    pass
        print(f"Common List {commonList}")

    def checkGroup(self):
    	import FreeCAD
    	doc = FreeCAD.ActiveDocument
    	grps = doc.getObjectsByLabel(self.GroupLabel)
    	if len(grps) == 0 or self.Group is None:
    		self.Group = doc.addObject("App::DocumentObjectGroup", self.GroupLabel)


    def createObjectGroup(self, parent, chkName):
        import FreeCAD
        if parent is not None:
            return parent.newObject("App::DocumentObjectGroup", chkName)
        else:
            return FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", chkName)

    def findAndProcessSubElement(self, parent, elemName):
        element = self.xmlRoot.find('./xsd:element[@name="'+elemName+'"]', namespaces=self.ns)
        return self.processXrbElement(parent, element, decend=False)


	#def checkCampus(self, srcObj):
	#	print(f"Check Campus {self.Campus}")
	#	if self.Campus is None:
	#		self.createCampus(self.Prefix+srcObj.Label, srcObj)

	#def createCampus(self, name, sObj):
	#	from freecad.openStudio.Campus_Feature import CampusFeatureClass
	#	#import FreeCAD
	#	self.checkGBxml()
	#	#doc = FreeCAD.ActiveDocument
	#	# Part::Feature or App::Feature or App::Group ?
	#	#self.Campus = doc.addObject("App::FeaturePython", "Campus")
	#	self.Campus = self.gbXML("App::DocumentObjectGroup", self.Prefix+"Campus") 
	#	CampusFeatureClass(self.Campus, sObj)
	#	#self.add2group(self.Campus)
	#	self.updateView()

    def getFCType(self, obj):
    	if obj.TypeId == "Part::FeaturePython":
    		if hasattr(obj, "Proxy"):
    			if hasattr(obj.Proxy, "Type"):
    				return obj.Proxy.Type
    	else:
    		return obj.TypeId

    def updateView(self):
    	import FreeCADGui
    	App.ActiveDocument.recompute()
    	if App.GuiUp:
    		FreeCADGui.SendMsgToActiveView("ViewFit")