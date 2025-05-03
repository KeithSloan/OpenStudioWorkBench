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
	
				self.tree = etree.parse(filename)
				self.XmlRoot = self.tree.getroot()
			except:
				print('No lxml or xml')
		
	def parseGbXmlFile(self, fileName): 

		print(f"Parse GbXml File {fileName}")
		# Create Structure
		self.gbXrb.checkGBxml()
		# Parse the file
		self.parseLXML(fileName)

	def processGbXml(self, docName, gbXmlObj):
		print(f"Process Parsed gbXML")
		# Structure is created so now process
		#self.processGbXmlElement()
		#for tags in self.gbXML.iter():
		#	print(f"Print tag {tags}")
		#processElementByName(self, parent, "gbXML")
		#self.setElementValues(gbXmlObj, self.gbXML)
		#self.processElementByName(gbXmlObj,"gbXML")
		#print(dir(self.gbXML))
		#self.processElement(gbXmlObj, self.gbXML)
		#for elem in self.gbXML.iter:
		#	self.processElement(gbXmlObj,"gbXML", self.gbXML)
		for element in self.gbXML.iter():
			self.findCheckProcessElement(docName, element)

	def findObject(self, gbObj, name, id):
		import FreeCAD
		from freecad.openStudio.processXrb import processXrbElementByName
		print(f"Find Object : Name {name} id {id}")
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
				processXrbElementByName(self, gbObj, name)
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
		print(f"CheckName tag {element.tag} {element}")
		elemName = element.tag
		idx = elemName.find('}')
		if idx > 0:
			elemName = elemName[idx+1:]
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
		if parent is not None:
			return parent.newObject("App::DocumentObjectGroup", chkName)
		else:
			return FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", chkName)

	def processElementByName(self, parent, elemName):
		print(f"Process Element By Name - Parent {parent.Label} Element Name {elemName}")
		element = self.xmlRoot.find('element[@name="'+elemName+'"]')
		return self.processElement(parent, element)

	
	def findCheckProcessElement(self, parent, element):
		label = parent
		if hasattr(parent, "Label"):
			label = parent.Label
		print(f"Find Check Process Element :  parent {label} Element {element}")
		chkName, id = self.checkName(element)
		gbObj = self.findObject(parent, chkName, id)
		self.processElement(gbObj, element)
		if id is not None:
			gbObj.Label = chkName + '__' + id
	
	def processElement(self, parent, element, decend=False):
    	#from freecad.openStudio.baseObject import ViewProvider
		print(f"Process Element :  parent {parent} Element {element}")
		parentType = type(parent)
		# chkName = name
		print(f"Process Element : Parent {parent.Label} {element.tag}")
		#type_ = element.get('type')
		#if type_ is not None:
		#	self.addElementProperty(parent, chkName, type_)
		#else:   # Create as Group Object
	