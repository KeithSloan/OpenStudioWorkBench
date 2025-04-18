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
		self.Label = "BMIinfo"
		self.GroupLabel = "GBxml"
		self.Group = None
		self.Campus = None

	def initBMI(self):
		print(f"Create Group")
		self.Group = App.ActiveDocument.addObject('App::DocumentObjectGroup', self.label)

	def add2group(self, obj):
		self.checkGroup()
		self.Group.addObject(obj)

	def getType(self, obj):
		if obj.TypeId == "Part::FeaturePython":
			if hasattr(obj, "Proxy"):
				if hasattr(obj.Proxy, "Type"):
					return obj.Proxy.Type
		else:
			return obj.TypeId

	def createGBxmlObject(self, obj):
		from freecad.openStudio.processSite import processSite
		from freecad.openStudio.processSpace import processSpace

		objType = self.getType(obj)
		print(f"Label {obj.Label} Type {objType}")
		while switch (objType):
			if case("Site"):
				print(f"Obj Type Site")
				processSite(self, obj)
				break

			if case("Space"):
				print(f"Space")
				processSpace(obj)
				break

	def checkGroup(self):
		import FreeCAD
		doc = FreeCAD.ActiveDocument
		grps = doc.getObjectsByLabel(self.GroupLabel)
		if len(grps) == 0 or self.Group is None:
			self.Group = doc.addObject("App::DocumentObjectGroup", self.GroupLabel)

	def checkCampus(self, sourceObj):
		#from   freecad.openStudio.Campus_Feature import CampusFeature
		from .Campus_Feature import CampusFeatureClass
		print(f"Check Campus {self.Campus}")
		if self.Campus is None:
			self.createCampus(sourceObj.Label)

	def createCampus(self, name):
		import FreeCAD
		doc = FreeCAD.ActiveDocument
		# Part::Feature or App::Feature or App::Group ?
		#self.Campus = doc.addObject("App::FeaturePython", "Campus")
		self.Campus = doc.addObject("App::DocumentObjectGroup", "Campus") 
		self.add2group(self.Campus)
		self.updateView()

	def updateView(self):
		import FreeCADGui
		App.ActiveDocument.recompute()
		if App.GuiUp:
			FreeCADGui.SendMsgToActiveView("ViewFit")