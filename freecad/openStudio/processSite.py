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

def processAreas(self, grp):
	print(f"Process Areas")

def processAxes(self, grp):
	print(f"Process Axes")

def processTerrain(self, grp):
	print(f"Process Terrain")	

def processBuilding(self, obj):
	print(f"Process Building {obj.Label}")
	#processIfcGroup(self, obj)
	for obj in obj.Group:
		#processBuildingPart(obj)
		print(f"{obj.Label}")
		processIfcType(self, obj)

def processBuildingElement(self, obj):
	print(f"Process Building Element")

def processBeams(self, obj):
	print(f"Process Beams")

def processCurtainWall(self, obj):
	print(f"Process Curtain Wall")

def processDoor(self, obj):
	print(f"Process Door")

#def processEntranceStairs(obj):
#	print(f"Process Entrance Stairs")

#def processGardenStairs(obj):
#	print(f"Process Garden Stairs")

def processSlab(self, obj):
	print(f"Process Slab")

def processStair(self, obj):
	print(f"Process Stair")

def processWall(self, obj):
	print(f"Process Wall")

def processWindow(self, obj):
	print(f"Process Window")


#def processPartGroup(Obj):
#	print(f"Process Part Group {Obj.Label} {Obj}")
#	for obj in Obj.Group:
#		print(f"{obj.Label} {type(obj)}")
		

#def OldprocessBuildingPart(Obj):
#	# Not Good to rely on label as Labels can be edited
#	# Label should at least be set to Read Only
#	print(f"Process Building Part {Obj.Label} {Obj}")
#	if hasattr(Obj,"Group"):
#		processPartGroup(Obj)
#		for obj in Obj.Group:
#			if obj.Label == "Beams":
#				processBeams(obj)
#			elif obj.Label == "Doors":
#				processDoors(obj)
#			elif obj.Label == "Entrance stairs":
#				processEntranceStairs(obj)
#			elif obj.Label == "Garden stairs":
#				processGardenStairs(obj)
#			elif obj.Label == "Slabs":
#				processSlabs(obj)
#			elif obj.Label == "Stairs":
#				processStairs(obj)
#			elif obj.Label == "Walls":
#				processWalls(obj)
#			elif obj.Label == "Windows":
#				processWindows(obj)
#			else:
#				print(f"BuildPart Group {obj.Label} Item Not Handled")

#def processBuildingPart(Obj):
#	# Not Good to rely on label as Labels can be edited
#	# Label should at least be set to Read Only
#	print(f"Process Building Part {Obj.Label} {Obj}")
#	if hasattr(Obj, "IfcType"):
#		if Obj.IfcType == "Building Storey":
#			processBuildingStorey(Obj)
#		else:
#			print(f"Building Part IfcType {Obj.IfcType} Not Handled")
#	else:
#		print(f"BuildPart Part {Obj.Label} Item Not Handled")

def processIfcGroup(self, ifcObj):
	if hasattr(ifcObj, "Group"):
		print(f"Process Ifc Group")
		for obj in ifcObj.Group:
			if hasattr(obj,"IfcType"):
				processIfcType(self, obj)

			elif hasattr(obj, "Group"):
				# Not Good to rely on Labels as Label Names can be edited?
				# Label should at least be set to Read Only
				if obj.Label == "Axes":
					processAxes(self, obj.Group)

				elif obj.Label == "Terrain":
					processTerrain(self, obj.Group)

				elif obj.Label == "Areas":
					processAreas(self, obj.Group)

				else:
					print(f"{obj.Label} Not Handled - processIfcGroup")

def processIfcType(self,obj):
	print(f"Process IfcType  {obj.IfcType} Label {obj.Label}")
	if obj.IfcType == "Building":
		processBuilding(self, obj)
	elif obj.IfcType == "Building Storey":
		processBuildingStorey(self, obj)
	elif obj.IfcType == "Building Element Proxy":
		processBuildingElement(self, obj)
	elif obj.IfcType == "Beams":
		processBeams(self, obj)
	elif obj.IfcType == "Curtain Wall":
		processCurtainWall(self,obj)
	elif obj.IfcType == "Door":
		processDoor(self, obj)
	elif obj.IfcType == "Slab":
		processSlab(self, obj)
	elif obj.IfcType == "Stair":
		processStair(self, obj)
	elif obj.IfcType == "Wall":
		processWall(self, obj)
	elif obj.IfcType == "Window":
		processWindow(self, obj)
		
	else:
		print(f"Process IfcType {obj.IfcType} Not Handled")			

def processBuildingStorey(self, Obj):
	print(f"Process Building Storey {Obj.Label} {Obj}")
	if hasattr(Obj,"Group"):
		for obj in Obj.Group:
			processIfcGroup(self, obj)


# 	processSite(BMIclass, CampusObj, siteObj)
def processIfcSite(self, siteObj):
	self.checkCampus(siteObj)
	print(f"Process Site {self}  {siteObj}")
	if hasattr(siteObj,"Group"):
		processIfcGroup(self, siteObj)
	print(dir(self.Campus.LinkedObj))
	#self.copyParametersSameName(siteObj,self.Campus)