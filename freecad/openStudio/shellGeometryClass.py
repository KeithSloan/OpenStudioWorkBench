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

class ShellGeometryClass(BaseClass):
	def __init__(self, obj):
		super().__init__(obj, "ShellGeometry")
		self.initShellGeometry()
				
	def initShellGeometry(self):
		print(f"Init Shell Geometry Class")
		self.addBaseProperties()
		self.ClosedShell = self.obj.addProperty("App::PropertyBool","ClosedShell","gbXml","Shell is Closed")
		self.ClosedShell = False

	def setShellIsClosed(self):
		print(f"Set Shell is Closed")
		self.ClosedShell = True
		print(f"Closed shell {self.ClosedShell}")

	def calcShape(self):		# Called from onChange in BaseClass
		import Part
		print(f"Shell Geometry calcShape")
		if self.ClosedShell:
			print("Create Closed Shell")
			print("Not yet handled : calcShape ShellGeometry")
		else:
			print("Not yet handled : calcShape ShellGeometry")

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