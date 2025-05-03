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

def findAddObject(self, parent, baseName, Label):
	from freecad.openStudio.processXrb import processXrbElementByName
	print(f"Find Add Object : Parent {parent.Label} baseName {baseName} Label {Label}")
	# If baseName object already exists change label and use
	# Else create new object
	Objs = FreeCAD.ActiveDocument.getObjectsByLabel(baseName)
	print(f"Objs {Objs}")
	fullLabel = baseName + ' : ' + Label
	print(f"Full Name {fullLabel}")
	if len(Objs) == 0:
		#gbObj = parent.newObject("App::DocumentObjectGroup", fullLabel)
		gbObj = processXrbElementByName(self, parent, baseName, decend=False)
	else:
		gbObj = Objs[0] 
	#setattr(gbObj, "Label", fullLabel)
	gbObj.Label = fullLabel
	return gbObj

def processBuilding(self, parent, obj):
	print(f"Process Building {parent.Label} {obj.Label}")
	parent = findAddObject(self, parent, "Building", obj.Label)
	#processIfcGroup(self, obj)
	for obj in obj.Group:
		#processBuildingPart(obj)
		print(f"{obj.Label}")
		processIfcType(self, parent, obj)
	parent.Name = obj.Label
	parent.id = obj.GlobalId

def processBuildingStorey(self, parent, Obj):
	print(f"Process Building Storey {parent} {Obj.Label}")
	parent = findAddObject(self, parent, "BuildingStorey", Obj.Label)
	if hasattr(Obj,"Group"):
		for obj in Obj.Group:
			processIfcGroup(self, parent, obj)
		parent.Name = Obj.Label
		parent.id = Obj.GlobalId

def processBuildingElement(self, obj):
	print(f"Process Building Element {obj.Label}")

def processBeams(self, obj):
	print(f"Process Beams {obj.Label}")

def processCurtainWall(self, obj):
	print(f"Process Curtain Wall {obj.Label}")

def processDoor(self, obj):
	print(f"Process Door {obj.Label}")

def processSlab(self, obj):
	print(f"Process Slab {obj.Label}")

def processStair(self, obj):
	print(f"Process Stair")

def processWall(self, gbObj, obj):
	import Part
	from  FreeCAD import Vector
	print(f"Process Wall {obj.Label} Name {obj.Name}")
	print(f"Bounding Box {obj.Shape.BoundBox} ZMin {obj.Shape.BoundBox.ZMin} ")
	print(f"GbObj {gbObj.Label} {gbObj.Group}")
	#print(dir(gbObj))
	# Use Name as Labels not unique
	#gbObj = findAddObject(self, gbObj, "Wall", obj.Name)
	# number of ways Walls can be created so try using Shape
	# All edges where Z component is same as MinZ from BoundingBoc
	wZ = obj.Shape.BoundBox.ZMin
	#Level = gbObj.Group[gbObj.Group.index("Level")]
	Level = gbObj.Group[0]
	if hasattr(Level,"Level"):
		setattr(Level,"Level",wZ)
		setattr(Level,"unit","Meters")
	#PlanarGeometry = gbObj.Group[gbObj.Group.index("PlanarGeometry")]
	PlanarGeometry = gbObj.Group[1]
	# PolyLoop is a Sketch
	PolyLoop = PlanarGeometry.Group[0]
	baseLevel =[]
	for v in obj.Shape.Vertexes:
		if v.Z == wZ:
			print(f"Add Coordinates {v.X} {v.Y} {v.Z}")
			baseLevel.append(Vector((v.X),(v.Y),(v.Z)))
	for i in range(len(baseLevel)):
		PolyLoop.addGeometry(Part.LineSegment(baseLevel[i-1],baseLevel[i]))

	#			setattr(PolyLoop.CartesianPoint,"X",v.X)
	#			setattr(PolyLoop.CartesianPoint,"Y",v.Y)
	#			PolyLoop.addGeometry(Part.LineSegment(i))




###	###
	if hasattr(obj, "Base"):
		print(f"Base Type {type(obj.Base)}")
	if hasattr(obj, "Width") and hasattr(obj, "Length"):
		print(f"Wall gbObj {gbObj} {obj.Length} x {obj.Width}")
		exit
	else:
		if hasattr(obj,"Subtractions"):
			print(f"Subtractions Type {type(object.Subtractions)}")
		if hasattr(obj,"Additions"):
			print(f"Additions Type {type(obj.Additions)}")
		if hasattr(obj,"ArchSketchData"):
			print(f"Arch Sketch Edges {obj.ArchSketchEdges}")
###	###	



def processWindow(self, obj):
	print(f"Process Window {obj.Label}")

def processIfcGroup(self, gbObj, ifcObj):
	if hasattr(ifcObj, "Group"):
		print(f"Process Ifc Group {ifcObj.Label}")
		for obj in ifcObj.Group:
			if hasattr(obj,"IfcType"):
				processIfcType(self, gbObj, obj)

			elif obj.TypeId == "Part::FeaturePython":
				if hasattr(obj, "ArrayType"):
					print(f"ArrayType : {obj.ArrayType}")

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

def processIfcType(self, gbObj, ifcObj):
	print(f"Process IfcType  {ifcObj.IfcType} Label {ifcObj.Label}")
	if ifcObj.IfcType == "Building":
		processBuilding(self, gbObj, ifcObj)
	elif ifcObj.IfcType == "Building Storey":
		processBuildingStorey(self, gbObj, ifcObj)
	elif ifcObj.IfcType == "Building Element Proxy":
		processBuildingElement(self, ifcObj)
	elif ifcObj.IfcType == "Beams":
		processBeams(self, ifcObj)
	elif ifcObj.IfcType == "Curtain Wall":
		processCurtainWall(self,ifcObj)
	elif ifcObj.IfcType == "Door":
		processDoor(self, ifcObj)
	elif ifcObj.IfcType == "Slab":
		processSlab(self, ifcObj)
	elif ifcObj.IfcType == "Stair":
		processStair(self, ifcObj)
	elif ifcObj.IfcType == "Wall":
		processWall(self, gbObj, ifcObj)
	elif ifcObj.IfcType == "Window":
		processWindow(self, ifcObj)
		
	else:
		print(f"Process IfcType {ifcObj.IfcType} Not Handled")			

def get_FC_Object(self, name):
	import freecad
	return FreeCAD.ActiveDocument.getObject(name)

# 	processSite(BMIclass, CampusObj, siteObj)
def processIfcSite(self, siteObj):
	self.checkGBxml()
	CampusObj = get_FC_Object(self, "Campus")
	print(f"Process Site {self}  {siteObj}")
	if hasattr(siteObj,"Group"):
		processIfcGroup(self, CampusObj, siteObj)
	#print(dir(self.Campus.LinkedObj))
	#self.copyParametersSameName(siteObj,self.Campus)
