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

class BaseClass():
	def __init__(self):
		super().__init__()

class PolyLoopClass(BaseClass):
    
	def __init__(self):
		super().__init__()
		self.initPolyLoop()
		self.PointsList = []
		self.sketch = None
		
	def initPolyLoop(self):
		print(f"Init PolyLoop Class")

	def addPolyLoopObject(self, parent):
		# Add new FC object to parent
		self.obj = parent.newObject("App::PythonFeature","PolyLoop")

	def addCartesianPoint(self, x, y, z=0.0):
		import FreeCAD
		self.PointsList.append(FreeCAD.Vector(x, y, z))

	def processCartesanPointElement(self,elem):
		# ToDo
		pass

	def returnQtDialog(self):
		# Or QtFrame ??
		# ToDo
		pass

	def add2BIM(self):
		# To Do ??
		pass

	def returnIfc(self):
		# To Do ??
		pass

	def createNewSketch(self):
		# To Do
		pass

	def add2Sketch(self):
		if self.sketch is None:
			self.sketch = self.createNewSketch()
		# To Do
		# Add to sketch Geometry
		# Add to sketch Constraints
		pass

	def add2Draft(self):
		# To Do ??
		pass
