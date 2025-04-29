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

class BMIclass():

	def __init__(self):
		super().__init__()
		self.Prefix = "BMI_"
		self.GroupLabel = "GBxml"
		self.Group = None
		self.Campus = None
		self.initBMI()

	def initBMI(self):
		#print(f"Create Group")
		#self.Group = App.ActiveDocument.addObject('App::DocumentObjectGroup', self.Prefix)
		self.initLXML()
		self.parse_xsd()

	def initLXML(self):
		import os
		print(f"Init lxml Class")
		self.ns = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
		self.Resources = os.path.join(App.getUserAppDataDir(), "Mod", \
			"OpenStudioWorkBench","freecad", "openStudio","Resources")
		self.xsd_file = os.path.join(self.Resources,"GBxml.xsd")

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

	def createGBxmlStructure(self):
		from freecad.openStudio.createStructure import createStructure
		#self.checkGroup()
		createStructure(self)

	def createGBxmlObject(self, obj):
		objType = self.getFCType(obj)
		print(f"Label {obj.Label} Type {objType}")
		while switch (objType):
			if case("Site"):
				self.createIfcSite(obj)
				break

			if case("Space"):		# ?????
				self.getFCTypecreateIfcSpace(obj)
				break

	def createIfcSite(self, srcObj):
		from freecad.openStudio.processSite import processIfcSite

		print(f"Process IFC Site ")
		self.checkCampus(srcObj)
		processIfcSite(self, srcObj)

	def processSimpleTypeIfcSpace(self, srcObj):
		from freecad.openStudio.processSpace import processIfcSpace

		print(f"Process IFC Space ")
		processSpace(self, srcObj)

	def copyParametersSameName(self, srcObj, trtObj):
		"""
		Properties of Target Obj are created from parsing GBxml.xsd
		"""
		
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

	def checkCampus(self, srcObj):
		print(f"Check Campus {self.Campus}")
		if self.Campus is None:
			self.createCampus(self.Prefix+srcObj.Label, srcObj)

	def createCampus(self, name, sObj):
		from freecad.openStudio.Campus_Feature import CampusFeatureClass
		import FreeCAD
		doc = FreeCAD.ActiveDocument
		# Part::Feature or App::Feature or App::Group ?
		#self.Campus = doc.addObject("App::FeaturePython", "Campus")
		self.Campus = doc.addObject("App::DocumentObjectGroup", self.Prefix+"Campus") 
		CampusFeatureClass(self.Campus, sObj)
		#self.add2group(self.Campus)
		self.updateView()

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