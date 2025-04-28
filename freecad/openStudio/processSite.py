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

#if open.__module__ in ['__builtin__', 'io']:
#    pythonopen = open # to distinguish python built-in open function from the one declared here

class switch(object):
	value = None

	def __new__(class_, value):
		class_.value = value
		return True

def case(*args):
	return any((arg == switch.value for arg in args))

#def initIfc2gbxml(self):
#	self.ifc2gbxmlDict = {
#		"Site: Campus",
#		"Terrain: xxxxx"
#		"Building: Building",
#		"Building Part: yyyyy ",
#		"Walls: wwwww",
#		"Slabs: ssss",
#		"Beams: bbbbb",
#		"Stairs: sssss",
#		"2D Plan View: zzzz",
#		"Surface: sssss",
#		"Layer: lllll",
#		}

def processAreas(grp):
	print(f"Process Areas")

def processAxes(grp):
	print(f"Process Axes")

def processBuilding(obj):
	for obj in obj.Group:
		processBuildingPart(obj)

def processBuildingPart(obj):
	print(f"{obj.Label} {obj}")

def processTerrain(grp):
	print(f"Process Terrain")	

def processIfcGroup(self, ifcObj):
	for obj in ifcObj.Group:
		if hasattr(obj,"IfcType"):
			print(f"Process {obj.Label} IfcType {obj.IfcType}")
			if obj.IfcType == "Building":
				processBuilding(obj)

		elif hasattr(obj, "Group"):
			# Better to use some type?
			if obj.Label == "Axes":
				processAxes(obj.Group)

			elif obj.Label == "Terrain":
				processTerrain(obj.Group)

			elif obj.Label == "Areas":
				processAreas(obj.Group)

			else:
				print(f"{obj.Label} Not Handled - processIfcGroup")

			

#	processSite(BMIclass, CampusObj, siteObj)
def processIfcSite(self, siteObj):
	self.checkCampus(siteObj)
	print(f"Process Site {self}  {siteObj}")
	if hasattr(siteObj,"Group"):
		processIfcGroup(self, siteObj)
	print(dir(self.Campus.LinkedObj))
	#self.copyParametersSameName(siteObj,self.Campus)