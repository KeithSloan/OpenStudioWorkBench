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

class LXMLclass():
	#from BMIclass import BMIclass
	# xmlns="http://www.gbxml.org/schema"
	#from freecad.openStudio.processSite import processSite

	def __init__(self, gbXrb):
		super().__init__()
		self.gbXrb = gbXrb
		self.gbXML = None		# gbXML Element

	def parseLXML(self, fileName):
		print(f"Init lxml Class")
		
		self.fileName = fileName
		try:
			from lxml import etree
			#from xml import etree

			print(f"Running with lxml etree\n")

			self.parser = etree.XMLParser(ns_clean=True, encoding="utf-8")
			self.tree = etree.parse(fileName, self.parser)
			self.xmlRoot = self.tree.getroot()
			self.gbXML = self.xmlRoot
			print(f"GBXML {self.gbXML}")
			print(f"keys {self.gbXML.keys()}")
			print(f"values {self.gbXML.values()}")
        
		except ImportError:
			try:
				import xml.etree.ElementTree as etree
				print("Rnning with etree.ElementTree (import limitations)\n")
	
				self.tree = etree.parse(fileName)
				self.XmlRoot = self.tree.getroot()
			except:
				print('No lxml or xml')
		
	def parseGbXmlFile(self, fileName): 

		print(f"Parse GbXml File {fileName}")
		# Create Structure
		self.gbXrb.checkGBxml()
		# Parse the file
		self.parseLXML(fileName)

	def processGbXml(self, docName, fileName):
		# Structure created from xsd
		# Assume more info than gbXml
		# Structure is created so now parse and process file
		#
		print(f"Parsed {fileName}")
		self.parseGbXmlFile(fileName)
		self.rootGbXML = self.gbXmlGroup()
		self.processElementAndChildren(self.rootGbXML, self.gbXML)

	def gbXmlGroup(self):
		import FreeCAD
		doc = FreeCAD.ActiveDocument
		print(f"Root Objects {doc.RootObjects}")
		for obj in doc.RootObjects:
			print(obj.Label)
			if obj.Label == "gbXML":
				return obj	

	def findObjectInDoc(self, gbObj, name, id):
		import FreeCAD
		#from freecad.openStudio.processXrb import processXrbElementByName
		# Need to access via self.gbXrb
		print(f"Find Object In Doc : Name {name} id {id}")
		# If baseName object already exists change label and use
		# Else create new object
		if id is not None:
			doc = FreeCAD.ActiveDocument
			Objs = doc.getObjectsByLabel(name)
			print(f"Objs {Objs}")
			#fullLabel = baseName + ' : ' + Label
			#ullLabel = name
			#print(f"Full Name {fullLabel}")
			if len(Objs) == 0 :
				# Add new and create properties
				gbObj = self.createObjectGroup(gbObj, name)
				self.gbXrb.processXrbElementByName(self, gbObj, name)
			else:
				gbObj = Objs[0] 
		#setattr(gbObj, "Label", fullLabel)
		#gbObj.Label = fullLabel
		return gbObj

	def getSet(self, obj, element, key):
		if hasattr(obj, key):
			prop = obj.getPropertyByName(key)
			print(f"Property {key} type {type(prop)}")
			if isinstance(prop, bool):
				print("Boolean")
				if prop == "True":
					prop = True
				else:
					prop = False
			setattr(obj, key, prop)

	def setElementValues(self, obj, element):
		print(f"Set Element Values {obj.Label}")
		for key in element.keys():
			self.getSet(obj, element, key)

	#def processGbXmlElement(self):
	#	parameters = [
	#		"useSIUnitsForResults",
	#		"temperatureUnit",
	#		"lengthUnit",
	#		"areaUnit",
	#		"SquareFeet",
	#		"volumeUnit",
	#		"CubicFeet", 
	#		"version"
	#	]
	#	self.setElementValues("gbXML", parameters, self.gbXML)

	#def findAndProcessSubElement(self, parent, elemName):
    #	#element = self.xmlRoot.find('element[@name="'+elemName+'"]', namespaces=self.ns)
	#	element = self.xmlRoot.find('element[@name="'+elemName+'"]')
	#	self.processSubElements(parent, element)

	#def	processSubElements(self, parent, elemName):
	#	return processElement(self, parent, element, decend=False)

	def checkName(self, element):
		singleElements = ["Campus"]
		#print(f"CheckName tag {element.tag} {element}")
		elemName = element.tag
		idx = elemName.find('}')
		if idx > 0:
			elemName = elemName[idx+1:]
		print(f"CheckName  {elemName}")
		if elemName in singleElements:
			return elemName, None
		if 'id' in element.keys():
			return elemName, element.get('id')
		# FC names cannot contain -
		probChars = "-"
		good = ""
		for i in elemName:
			if i not in probChars:
				good += i
			else:
				good += ('_')
		return good, None
	
	def createObjectGroup(self, parent, chkName):
		import FreeCAD
		if parent is not None:
			return parent.newObject("App::DocumentObjectGroup", chkName)
		else:
			return FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", chkName)

	def processElementByName(self, parent, elemName):
		print(f"Process Element By Name - Parent {parent.Label} Element Name {elemName}")
		element = self.xmlRoot.find('element[@name="'+elemName+'"]')
		return self.processElement(parent, element)

	def printGroup(self, grpObj, msg=None):
		if msg is not None:
			print(f"======= {msg} ======")
		if hasattr(grpObj, "Group"):
			for obj in grpObj.Group:
				print(obj.Label)

	def groupLabels(self, grpObj):
		if hasattr(grpObj, "Group"):
			lst = []
			for obj in grpObj.Group:
				lst.append(obj.Label)
			return lst

	def objectInGroup(self, grpObj, name):
		if hasattr(grpObj, "Group"):
			for obj in grpObj.Group:
				if name == obj.Label:
					print(f"Found {name} {obj}")
					return obj
		print(f"{name} Not Found")
		return None

	def locateLastInGroup(self, grpObj, name):
		if hasattr(grpObj, "Group"):
			print(f"Range {range(len(grpObj.Group) - 2, 0, -1)}")
			for i in range(len(grpObj.Group) - 2, 0, -1):
				objName = grpObj.Group[i].Label  
				if objName.startswith(name):
					print(f"Found {objName} at {i}")
					return i
		print(f"{name} Not Found")
		return None

	def reorderGroup(self, grpObj, name):
		import FreeCAD
		doc = FreeCAD.ActiveDocument
		if hasattr(grpObj, "Group"):
			if len(grpObj.Group) > 1:
				num = self.locateLastInGroup(grpObj, name)
				for i in range(len(grpObj.Group) - num - 2):
					# Access last but one member of Group
					obj = grpObj.Group[num+1]
					print(f"Move {i} {obj.Label}")
					# Removed from Group
					grpObj.removeObject(obj)
					# Add to tail of Group
					grpObj.addObject(obj)
						

	def addObject2Group(self, parent, name):
		print(f"addObject2Group parent {parent.Label} Name {name}")
		if hasattr(parent, "Group"):
			gbObj = parent.newObject("App::DocumentObjectGroup", name)
			parent.Group.append(gbObj)
			return gbObj
		else:
			print(f"Failed to add to group {parent.Label}")

	def insertObject2Group(self, parent, name):
		import FreeCAD
		print(f"inserObject2Group parent {parent.Label} Name {name}")
		if hasattr(parent, "Group"):
	#		#idx = self.locateInGroup(parent, name)
	#		self.printGroup(parent, "Before create")
			gbObj = parent.newObject("App::DocumentObjectGroup", name)
			self.reorderGroup(parent, name)

	def findObject(self, parent, name, id):
		#
		# A name cleaned from element.tag is either
		#
		#	An initialise but not populated Group Object
		# 	A property of the parent
		# 
		import FreeCAD
		print(f"Find Object : Parent {parent.Label} Name {name} id {id}")
		print(f"Parent Group {self.groupLabels(parent)}")
		gbObj = self.objectInGroup(parent, name) 
		# if gbObj is None:	# That means structure name used before
		#   so create new Obj and use
		if gbObj is None:
			# Else create a New Group and initialise structure
			print(f"Not found create new gbObj")
			# Need to access via self.gbXrb
			#from freecad.openStudio.processXrb import processXrbElementByName
			gbObj  = self.gbXrb.processXrbElementByName(parent, name)
			# Reorder group to keep togther
			self.reorderGroup(parent, name)
		#	if id is not None:
		#		baseName object already exists change label and use
		#		gbObj.Label = name + '__' + id
		if id is not None:
			gbObj.Label = name + '__' + id
		return gbObj
			
	def findCheckProcessElement(self, parent, element):
		#
		# A name cleaned from element.tag is either
		#
		#	An initialise but not popluated Group Object
		# 	A property of the parent
		#  
		label = parent
		if hasattr(parent, "Label"):
			label = parent.Label
		#print(f"Find Check Process Element :  parent {label} Element {element}")
		print(f"Find Check Process Element :  parent {label}")
		chkName, id = self.checkName(element)
		# If id is None Property
		if id is not None:
			gbObj = self.findObject(parent, chkName, id)
			gbObj.Label = chkName + '__' + id
			self.processElement(gbObj, element)
			#print(dir(element))
			exit
			for elem in element.iterchildren():
				print(f'{elem} parent{elem.getparent()}')
				self.findCheckProcessElement(gbObj, elem)
	
	def processElementAndChildren(self, parent, element, decend=False):
		self.processElement(parent, element, decend)
		for elem in element.iterchildren():
			print(f'{elem} parent{elem.getparent()}')
			self.findCheckProcessElement(parent, elem)

	def processElement(self, parent, element, decend=False):
    	#from freecad.openStudio.baseObject import ViewProvider
		#print(f"Process Element :  parent {parent} Element {element}")
		print(f"Process Element :  parent {parent}")
		parentType = type(parent)
		# chkName = name
		print(f"Process Element : Parent {parent.Label} {element.tag}")
		self.setElementValues(parent, element)
		#type_ = element.get('type')
		#if type_ is not None:
		#	self.addElementProperty(parent, chkName, type_)
		#else:   # Create as Group Object
	