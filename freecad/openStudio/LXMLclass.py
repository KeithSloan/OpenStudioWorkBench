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
		print("================================================")
		print("================================================")
		print(f"Parsed {fileName}")
		print("================================================")
		print("================================================")
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
		print(f"getSet {obj.Label} element {element} key {key}")
		if hasattr(obj, key):
			prop = obj.getPropertyByName(key)
			value = element.get(key)
			print(f"Property {key} type {type(prop)}")
			if isinstance(prop, bool):
				print("Boolean")
				if value == "True":
					value = True
				else:
					value = False
			print(f"Set {obj.Label} Value {key} property {prop} Value {value}")
			setattr(obj, key, value)

	def processKeys(self, obj, element, elemName):
		print(f"processKeys - Set Keys {obj.Label} elemName {elemName}")
		for key in element.keys():
			#self.getSetValue(obj, elemName, key)
			self.getSetValue(obj, key, element.get(key))
		print("keys all set")
	
	def setElementValues(self, parent, element):
		# Values maybe in Group
		elemName = self.cleanTag(element)
		print(f"Set Element Values {parent.Label} elemName {elemName}")
		# Values maybe in Group
		gbObj = self.objectInGroup(parent, elemName)
		if gbObj is not None: # set found object
			print(f"Yes {elemName} is in Group")
			#self.setElementValues(gbObj, element)
			self.getSetValue(gbObj, self.cleanName(elemName), element.text)
		else:
			#pass
			self.processKeys(parent, element, elemName)
			#self.getSetValue(parent, elemName, element.text)
		
	def getSetValue(self, obj, elemName, value):
		print(f'getSetValue {obj.Label} element "{elemName}" value "{value}"')
		if hasattr(obj, elemName):
			prop = obj.getPropertyByName(elemName)
			print(f"Property Type of {elemName} {type(prop)}")
			if isinstance(prop, bool):
				print("Boolean")
				if value == "True":
					value = True
				else:
					value = False
			elif isinstance(prop, int):
				value = int(value)
			elif isinstance(prop, float):
				value = float(value)
			print(f"Set {obj.Label} Value {elemName} property {prop} Value {value}")
			try:
				setattr(obj, elemName, value)
			except ValueError:
				print(f"Invalid Value {value} for {elemName} property {prop}") 
	
	def setValue(self, obj, element):
		elemName = self.cleanTag(element)
		print(f"Set Value obj {obj.Label} ElemName {elemName}")

	def checkIfElementAttribute(self, parent, element, elemName):
		print(f"Is elemName {elemName} an attribute of parent {parent.Label} ?")
		if hasattr(parent, elemName):
			print(f"{elemName} === Yes === is an attribute of {parent.Label} Value {element.text}")
			#type_ = type(parent.elemName)
			#print(f"Type {type_}")
			#setattr(parent, elemName, (type_) element.text)
			self.getSetValue(parent, elemName, element.text)

	def checkIfElementInParentGroup(self, parent, element, elemName):		# Example Area in Building
		print(f"Check if Element {elemName} in Parent Group {parent.Label}")
		obj = self.objectInGroup(parent, elemName)
		if obj is not None:
			self.checkIfElementAttribute(obj, element, elemName)

	def cleanTag(self, element):
		elemName = element.tag
		idx = elemName.find('}')
		if idx > 0:
			elemName = elemName[idx+1:]
		print(f"Cleaned Tag {elemName}")
		return elemName

	def cleanName(self, name):
		# If only one prob char recode
		# FC names cannot contain -
		probChars = "-"
		good = ""
		for i in name:
			if i not in probChars:
				good += i
			else:
				good += ('_')
		return good

	def checkName(self, element):
		# Return Cleaned Name
		#	elemName 	: Element Name
		#   idType 		: [ "id", "zoneIdRef", "surfaceIdRef"]
		#	id			: id or False
		idTypes = ["id", "zoneIdRef", "surfaceIdRef"]
		elemName = self.cleanTag(element)
		print(f"elemName {elemName}")
		for key in element.keys():
			if key in idTypes:
				return elemName, element.get(key)
		else:
			return self.cleanName(elemName), False
	
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

	def objectInGroup(self, parent, name):
		print(f"Is Object {name} in Group {parent.Label}")
		#self.printGroup(parent)
		if hasattr(parent, "Group"):
			for obj in parent.Group:
				if '_' not in obj.Label:
					if obj.Label.startswith(name):
						print(f"Found {name} in {parent.Label}")
						return obj
			#if name in parent.Group:
			#	return parent.Group.index(name)
		print(f"{name} Not Found in {parent.Label} Group")
		return None

	def locateLastInGroup(self, grpObj, name):
		# New item will be added as last
		# Need to locate the previous last item starting with name
		if hasattr(grpObj, "Group"):
			# Range needs to go to zero
			# print(f"Range {range(len(grpObj.Group) - 2, -1, -1)}")
			for i in range(len(grpObj.Group) - 2, -1, -1):
				print(f"i {i}")
				objName = grpObj.Group[i].Label
				print(f"objName : {objName}")  
				if objName.startswith(name):
					print(f"Found {objName} at {i}")
					return i
		print(f"locateLastinGroup : {name} Not Found in {grpObj.Label} Group")
		return None

	def reorderGroup(self, grpObj, name):
		print(f"ReorderGroup {grpObj.Label} length {len(grpObj.Group)}")
		if hasattr(grpObj, "Group"):
			if len(grpObj.Group) > 1:
				num = self.locateLastInGroup(grpObj, name)
				for i in range(len(grpObj.Group) - num - 2):
					# Access last in Group
					obj = grpObj.Group[num + 1]
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

	def findObjectInGroup(self, parent, elemName, id):
		#
		# A name cleaned from element.tag is either
		#
		#	An initialise but not populated Group Object
		# 	A property of the parent
		# 
		print(f"Find Object : Parent {parent.Label} Name {elemName} id {id}")
		print(f"Parent Group {self.groupLabels(parent)}")
		gbObj = self.objectInGroup(parent, elemName) 
		# Check attribute or in Group First?
		#
		# if gbObj is None:	# That means structure name used before
		#   so create new Obj and use
		if gbObj is None:
			print(f"{elemName} Not found in parent group {parent.Label}")
			print("Create New Object from Xrb")
			# Create a New Group and initialise structure
			# Need to access via self.gbXrb
			#from freecad.openStudio.processXrb import processXrbElementByName
			gbObj  = self.gbXrb.processXrbElementByName(parent, elemName)
			# Reorder group to keep togther
			self.reorderGroup(parent, elemName)
		#	if id is not None:
		#		baseName object already exists change label and use
		#		gbObj.Label = name + '__' + id
		#if id is not None and elemName not in ["Campus"]:
		if id and elemName != "Campus":
			print(f"Change Label {id}")
			gbObj.Label = elemName + '__' + id
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
		elemName, id = self.checkName(element)
		if elemName == "AirLoop":
			print(f"AirLoop id {id}")
			#breakpoint()
		#print(f"Find Check Process Element :  parent {label} Element {element}")
		print(f"Find Check Process Element :  parent {label} element {elemName}")
		#treatDiff = ["PolyLoop",
		#			"CartesianPoint",
		#			"Coordinate",
		#treatDiff = ["Coordinate",
		#			"CartesianPoint",
		#]
		# ,
		#			"SpaceBoundary"
		#]
		#if elemName in treatDiff:
		#	return
		#
		#
		# If subFlag then has id so find and use or create new and use.
		if id:
			gbObj = self.findObjectInGroup(parent, elemName, id)
			# process element and children
			#self.processElementAndChildren(parent, element)

			if self.processElement(gbObj, element, elemName, id) == False:
			#elf.checkIfElementAttribute(parent, element, elemName)
			#	#if id is not None:
			#	#gbObj.Label = chkName + '__' + id
				print(f"Process Children")
				for elem in element.iterchildren():
					#print(f'{elem} parent{elem.getparent()}')
					#self.processElement(gbObj, elem)
					#self.setElementValues(parent, element)
					self.findCheckProcessElement(gbObj, elem)
		else:
			print(f"Element {elemName} with no Id")
			gbObj = parent
			if self.processElement(gbObj, element) == False:
				self.processChildren(gbObj, element)
		
	def processChildren(self, parent, element):
		print(f"Process Children II of parent {parent.Label}")
		for elem in element.iterchildren():
			elemName = self.cleanTag(element)
			obj = self.objectInGroup(parent, elemName)
			if obj is None:			# Not in parent Group - Cartesian Point, Coordinate
				obj = parent		# value for PolyLoop in Parent Group, Also  various xxxxGeometry							
			self.processElement(obj, elem)
		return True

	def processElementAndChildren(self, parent, element, decend=False):
		elemName = self.cleanTag(element)
		print(f"Process Element & Children : Parent {parent.Label} Element {elemName}")
		self.processElement(parent, element, elemName, decend)
		for elem in element.iterchildren():
			print(f'{elem} parent{elem.getparent()}')
			self.findCheckProcessElement(parent, elem)
			#self.processElement(parent, elem)
		return True

	def processPolyLoop(self, parent, element, elemName):
		# Should check
		print(f"Process PolyLoop: - parent {parent.Label} elemName {elemName} Group {parent.Label}")
		polyLoopObj  = self.objectInGroup(parent, elemName)
		return self.processPolyLoopObj(polyLoopObj, element, elemName)
	
	def processPolyLoopObj(self, polyLoopObj, element, elemName):
		print(f"Process PolyLoopObj : {polyLoopObj.Label} elemName {elemName}")
		for cn, elem in enumerate(element.iterchildren()):
			#elemName = self.cleanTag(elem)
			#print(f"{elemName}")
			self.processCartesianPoint(polyLoopObj, elem)
		polyLoopObj.Proxy.addCartesianPointCount(polyLoopObj, cn+1)
		return True

	def processCartesianPoint(self, polyLoop, element):
		print(f"Process Cartesian Point  - polyLoop {polyLoop.Label}")
		#print(dir(polyLoop))
		#print(dir(polyLoop.Proxy))
		#polyLoop.PointsCount = 5
		vector = []
		for cn, elem in enumerate(element.iterchildren()):
			# Cartesian Points
			vector.append(float(elem.text))
		print(f"Add Cartesian {vector}")
		# # polyLoop.Proxy.PointsList = [FreeCAD.Vector(11,12,13)]
		# Feature Python Methods are in Proxy, Variables are Not.
		polyLoop.Proxy.addCartesianPoint(polyLoop, vector)
		#print(f"Points List {polyLoop.PointsList}")
		return True

	def processCordinate(self, parent, element):
		print(f"Process Cordinate Point - parent {parent.Label}")
		# check PolyLoop
		for elem in element.iterchildren():
			print(elem.text)

	def processPlanar(self, parent, element, elemName):
		print(f"Process Planer : Parent  {parent.Label} Group {self.groupLabels(parent)}")
		# enumerate or always only one PolyLoop
		planarObj  = self.objectInGroup(parent, elemName)
		print(f"planarObj {planarObj.Label}")
		for cn, elem in enumerate(element.iterchildren()):
			elemName = self.cleanTag(elem)
			print(f"Plannar Element {elemName}")
			if elemName == "PolyLoop":
				polyLoopObj = self.gbXrb.createPolyLoop(planarObj)
				#print(f"PolyLoop {planarObj}")
				self.processPolyLoopObj(polyLoopObj, elem, elemName)
			else:
				print(f"Non PolyLoop")
		return True

	def processShell(self, parent, element, elemName, id):
		print(f"Process Shell : Parent  {parent.Label} Group {self.groupLabels(parent)}")
		if id is not None:
			self.Label = id
		#shellObj  = self.objectInGroup(parent, elemName)
		for cn, elem in enumerate(element.iterchildren()):
			elemName = self.cleanTag(elem)
			print(f"Process Shell Element {elemName}")
			if elemName == "ClosedShell":
				print(f"Set Shell Closed")
				parent.Proxy.setShellIsClosed()
				self.processClosedShell(parent, elem, elemName)
		#	print(f"Process Shell Element {elem}")
		print(f"End Process Shell")
		return True

	def processClosedShell(self, parent, element, elemName):
		print(f"Process Closed Shell : Parent  {parent.Label} Grouo {self.groupLabels(parent)}")
		for cn, elem in enumerate(element.iterchildren()):
			elemName = self.cleanTag(elem)
			print(f"Process Shell Element {elemName}")
			if elemName == "PolyLoop":
				print(f"PolyLoop")
				polyLoopObj = self.gbXrb.createPolyLoop(parent)
				self.processPolyLoopObj(polyLoopObj, elem, elemName)
		print(f"End Process Closed Shell")
		return True

	#def processSpaceBoundary(self, parent, element, elemName, id):
	#	# setProperties(self, surfaceIdRef, isSecondaryLevelBoundary):
	#	print(f"Process Space Boundary : Parent  {parent.Label} Grouo {self.groupLabels(parent)}")
	#
	#	print(f"End Process Closed Shell")
	#	return False # Does not process children

	def processElement(self, parent, element, elemName = None, id=False, decend=False):
		# Returns True if all children processed
    	#from freecad.openStudio.baseObject import ViewProvider
		#print(f"Process Element :  parent {parent}")
		if elemName is None:
			elemName = self.cleanTag(element)
		print(f"Process Element : Parent {parent.Label} Element {elemName}")
		if elemName == "AirLoop":
			print("AirLoop")
			#breakpoint()
		if elemName in ["Cordinate", "ClosedShell", "PolyLoop", "CartesianPoint"]:		# Already dealt with
			return True
		elif elemName == "PlanarGeometry":
			self.processPlanar(parent, element, elemName)
			return True
		elif elemName == "ShellGeometry":
			self.processShell(parent, element, elemName, id)
			return True
		#elif elemName == "SpaceBoundary":
		#	self.processSpaceBoundary(parent, element, elemName, id)
		#	return False
		if id:
			self.processKeys(parent, element, elemName)
		self.setElementValues(parent, element)			# Issue with Standard test ExtEquipId
		self.checkIfElementAttribute(parent, element, elemName)
		#elf.checkIfElementInParentGroup(parent, element, elemName)		# Example Area in Building
		print(f"End Process Element {elemName}")
		return False

	def processSiblings(self, parent, element):
		print(f"process Siblings - parent {parent.Label} element {self.cleanTag(element)}")
		for elem in element.itersiblings():
			self.processElement(parent, elem)
