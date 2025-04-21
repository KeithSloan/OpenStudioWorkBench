# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2025 Keith Sloan <keith@sloan-home.co.uk>              *
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
# *                                                                        *
# **************************************************************************

__title__ = "FreeCAD GBxml Workbench - GUI Commands"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

from PySide import QtGui, QtCore
from PySide.QtCore import Qt

import FreeCAD, FreeCADGui

class AddGBxmlFeature:
	def Activated(self):
		from freecad.openStudio.BMIclass import BMIclass
		self.bmiClass = BMIclass()
		#for obj in FreeCADGui.Selection.getSelection():
		print("Add gbxml properties")
		selectEx = FreeCADGui.Selection.getSelectionEx()
		if len(selectEx) > 0:
			sel = selectEx[0]
			self.bmiClass.createGBxmlObject(sel.Object)
		#for sel in selectEx:
		#	print("Add gbxml properties")
		#	self.bmiClass.createGBxmlObject(sel.Object)
		return

	def addBMIclass(self, obj):
		self.bmiClass.addClass(obj)


	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True

	def GetResources(self):
		return {
			"Pixmap": "AddGBxmlFeature",
			"MenuText": QtCore.QT_TRANSLATE_NOOP(
				"AddGBxmlFeature", "Add gbxml Properites"
			),
			"ToolTip": QtCore.QT_TRANSLATE_NOOP(
				"AddGBxmlFeature", "Add gbxml Properties"
			),
		}

class BuildGBxmlFeature:
	def Activated(self):
		from freecad.openStudio.BMIclass import BMIclass
		self.bmiClass = BMIclass()
		#for obj in FreeCADGui.Selection.getSelection():
		print("Build gbxml Group Structure")
		self.bmiClass.createGBxmlStructure()
		return

	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True

	def GetResources(self):
		return {
			"Pixmap": "BuildGBxmlFeature",
			"MenuText": QtCore.QT_TRANSLATE_NOOP(
				"BuildGBxmlFeature", "Build GBxml Group Structure"
			),
			"ToolTip": QtCore.QT_TRANSLATE_NOOP(
				"BuildGBxmlFeature", "Build GBxml Group Structure"
			),
		}

class SyncGBxmlFeature:
	def Activated(self):
		print(f"Sync activated")

	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True

	def GetResources(self):
		return {
			"Pixmap": "SyncGBxmlFeature",
			"MenuText": QtCore.QT_TRANSLATE_NOOP(
				"SyncGBxmlFeature", "Sync gbxml Properites"
			),
			"ToolTip": QtCore.QT_TRANSLATE_NOOP(
				"SyncGBxmlFeature", "Sync gbxml Properties"
			),
		}

FreeCADGui.addCommand("buildGBxmlCmd", BuildGBxmlFeature())
FreeCADGui.addCommand("addGBxmlCmd", AddGBxmlFeature())
FreeCADGui.addCommand("syncGBxmlCmd", SyncGBxmlFeature())
