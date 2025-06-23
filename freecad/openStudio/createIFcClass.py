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

# import FreeCAD as App
import Arch, FreeCAD, FreeCADGui
from nativeifc import ifc_tools

#building = Arch.makeBuilding()

class CreateIFCclass():
	def __init__(self):
		self.doc = FreeCAD.ActiveDocument
		self.project = ifc_tools.create_document(self.doc)
		self.site = Arch.makeSite()
		self.site = ifc_tools.aggregate(self.site, self.project)

	def processSelection(self):
		print("Process Selection")
		sel = FreeCADGui.Selection.getSelection()
		if sel is not None:
			print(f"Selection {sel}")
			for grp in sel:
				if hasattr(grp, "Group"):
					print(f"Selected {grp.Label}")
					if grp.Label == "Campus":
						self.createSiteFromCampus(grp)
					elif grp.Label.startswith("Building"):
						self.createBuilding()

	def createSiteFromCampus(self, campus):
		print("Create Site from Campus")
		print(dir(self.site))
		print(dir(campus))
	
	def createBuilding(self):
		print("Create IFC Building")
	
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

	def checkName(self, element):
		pass
		# Return Cleaned Name
		#	elemName 	: Element Name
		#   idType 		: [ "id", "zoneIdRef", "surfaceIdRef"]
		#	id			: id or False
		#idTypes = ["id", "zoneIdRef", "surfaceIdRef"]
		#elemName = self.cleanTag(element)
		#print(f"elemName {elemName}")
		#for key in element.keys():
		#	if key in idTypes:
		#		return elemName, element.get(key)
		#else:
		#	return self.cleanName(elemName), False
	
	