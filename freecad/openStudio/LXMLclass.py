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
			self.XmlRoot = self.tree.getroot()
			self.gbXML = self.XmlRoot
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

		print(f"Process GbXml File {fileName}")
		self.gbXrb.checkGBxml()
		self.parseLXML(fileName)

	def processGbXml(self):
		print(f"Process Parsed GbXml")
		self.processGbXmlElement()
		for tags in self.gbXML.iter():
			print(f"Print tag {tags}")

	def findAddObject(self, parent, baseName, Label):
		import FreeCAD
		from freecad.openStudio.processXrb import processXrbElementByName
		print(f"Find Add Object : Parent {parent.Label} baseName {baseName} Label {Label}")
		# If baseName object already exists change label and use
		# Else create new object
		Objs = FreeCAD.ActiveDocument.getObjectsByLabel(baseName)
		print(f"Objs {Objs}")
		fullLabel = baseName + ' : ' + Label
		print(f"Full Name {fullLabel}")
		if len(Objs) == 0:
			gbObj = processXrbElementByName(self, parent, baseName, decend=False)
		else:
			gbObj = Objs[0] 
		#setattr(gbObj, "Label", fullLabel)
		gbObj.Label = fullLabel
		return gbObj

	def findObject(self, name):
		import FreeCAD
		from freecad.openStudio.processXrb import processXrbElementByName
		print(f"Find Object : Name {name}")
		# If baseName object already exists change label and use
		# Else create new object
		doc = FreeCAD.ActiveDocument
		Objs = doc.getObjectsByLabel(name)
		print(f"Objs {Objs}")
		#fullLabel = baseName + ' : ' + Label
		#ullLabel = name
		#print(f"Full Name {fullLabel}")
		if len(Objs) == 0:
			# Add new and create properties
			gbObj = processXrbElementByName(self, doc, name, decend=False)
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

	def setElementValues(self, name, parameters, element):
		obj = self.findObject(name)
		for key in element.keys():
			self.getSet(obj, element, key)

	def processGbXmlElement(self):
		parameters = [
			"useSIUnitsForResults",
			"temperatureUnit",
			"lengthUnit",
			"areaUnit",
			"SquareFeet",
			"volumeUnit",
			"CubicFeet", 
			"version"
		]
		self.setElementValues("gbXML", parameters, self.gbXML)

	def findAndProcessSubElement(self, parent, elemName):
    	#element = self.xmlRoot.find('element[@name="'+elemName+'"]', namespaces=self.ns)
		element = self.xmlRoot.find('element[@name="'+elemName+'"]')
		self.processSubElements(parent, element)

	def	processSubElements(self, parent, elemName):
		return processElement(self, parent, element, decend=False)

	def processElementByName(self, parent, elemName):
		print(f"Process Element By Name - Parent {parent.Label} Element Name {elemName}")
		element = self.xmlRoot.find('element[@name="'+elemName+'"]')
		return self.processElement(parent, element)

	def processElement(self, parent, element, decend=False):
    	#from freecad.openStudio.baseObject import ViewProvider
		parentType = type(parent)
		name = element.get('name')
    	#chkName = checkName(self, name)
		# chkName = name
		print(f"Process Element : {chkName}")
		type_ = element.get('type')
    	#if type_ is not None:
        #addElementProperty(self, parent, chkName, type_)
    	#else:   # Create as Group Obje
    