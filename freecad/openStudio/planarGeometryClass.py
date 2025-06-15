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

# class BaseClass():
#	def __init__(self, obj, type_):
#		super().__init__()
#		self.obj = obj
#		obj.Proxy = self
#		obj.Proxy.Type = type_

# def addBaseProperties(self):
#        self.obj.addProperty("Part::PropertyPartShape", "Shape", "PartShape", "Base")
#        self.obj.addProperty("App::PropertyEnumeration", "ShapeValid", "ShapeValid", "Base")
#        self.obj.ShapeValid = ["UnSet", "Valid", "InValid"]
#        self.obj.ShapeValid = "UnSet"
#        self.obj.addProperty("App::PropertyBoolean", "CalcShape", "Compute FC Shape", "Base")        

from freecad.openStudio.baseObject import BaseClass

class PlanarGeometryClass(BaseClass):
	def __init__(self, obj):
		super().__init__(obj, "PlanarGeometry")
		self.initPlanarGeometry()
		#self.sketch = None
				
	def initPlanarGeometry(self):
		print(f"Init PolyLoop Class")
		self.addBaseProperties()
		#self.PointsCount = 
		#self.PointsList = self.obj.addProperty("App::PropertyVectorList","PointsList","gbXml","Cartesian Points")
		#self.PointsList = []

	#def addPolyLoopObject(self, parent):
	#	# Add new FC object to parentself.obj.addProperty("App::PropertyInteger","PointsCount","gbXml","Points Count")
	#	print(f"Add PolyLoop Object")
	#	self.obj = parent.newObject("App::PythonFeature","PolyLoop")

	#def addCartesianPoint(self, polyLoop, vector):
	#	# Need to be passed polyLoop !!! ??
	#	# self will be definition - polyLoop will be instance
	#	import FreeCAD
	#	#print(dir(self))
	#	#print(f"add Cartesian - self {self} polyLoop {polyLoop}")
	#	print(f"addCartesian - Vector passed {vector}")
	#	#print(f"Before Points List {polyLoop.PointsList}")
	#	#print(type(polyLoop.PointsList))
	#	vecList = polyLoop.PointsList
	#	vecList.append(FreeCAD.Vector(vector[0], vector[1], vector[2]))
	#	polyLoop.PointsList = vecList
	#	#polyLoop.PointsList = [FreeCAD.Vector(4,5,6)]
	#	#print(f"After Points List {polyLoop.PointsList}")

	#def addCartesianPointCount(self, polyLoop, count):
	#	print(f"Add points count {self.obj.Label} {count}")
	#	polyLoop.PointsCount = count

	def calcShape(self):		# Called from onChange in BaseClass
		import Part
		print(f"Planar Geometry calcShape")
		ln = len(self.obj.Group)
		if ln == 1:
			pl = self.obj.Group[0]
			print(f"PolyLoop {pl.Label}")
			if len(pl.PointsList) > 3:
				# Add a Point to Close Shape
				shapePoints = pl.PointsList + pl.PointsList[:1]
				#shapePoints = pl.PointsList.append(pl.PointsList[1:])
				print(f"shapePoints {shapePoints}")
				try:
					shapeWire = Part.makePolygon(shapePoints)
				except:
					print("Invalid PolyGon")
					self.obj.ShapeValid = "InValid"
					return
				try:
					self.PartShape = Part.makeFace(shapeWire)
				except:
					print("Invalid Face")
					self.obj.ShapeValid = "InValid"
					return
				self.obj.ShapeValid = "Valid"
				if not hasattr(self.obj,"Area"):
					self.Area = self.obj.addProperty("App::PropertyFloat","Area","Base","Area of PlanarGeometry")
				print(f"PartShape Area {self.PartShape.Area}")
				self.obj.Area = self.PartShape.Area
		elif ln > 1:
			print("Not yet handled : calcShape planarGeometry")

	def returnQtDialog(self):
		# Or QtFrame ??
		# ToDo
		pass

	def pushBIM(self):
		# ToDo ??
		pass

	def pushIfc(self):
		# ToDo ??
		pass

	def createNewSketch(self):
		# ToDo
		pass

	def add2Sketch(self):
		if self.sketch is None:
			self.sketch = self.createNewSketch()
		# ToDo
		# Add to sketch Geometry
		# Add to sketch Constraints
		pass

	def add2Draft(self):
		# ToDo ??
		pass