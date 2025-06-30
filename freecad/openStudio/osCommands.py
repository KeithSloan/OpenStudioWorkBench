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
		from freecad.openStudio.XrbClass import XrbClass
		self.XrbClass = XrbClass()
		#for obj in FreeCADGui.Selection.getSelection():
		print("Add gbxml properties")
		selectEx = FreeCADGui.Selection.getSelectionEx()
		if len(selectEx) > 0:
			sel = selectEx[0]
			#self.XrbClass.createGBxmlObject(sel.Object)
			self.XrbClass.processBIMobject(sel.Object)

		#for sel in selectEx:
		#	print("Add gbxml properties")
		#	self.bmiClass.createGBxmlObject(sel.Object)
		return

	def addXrbClass(self, obj):
		self.XrbClass.addClass(obj)


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
		from freecad.openStudio.XrbClass import XrbClass
		self.XrbClass = XrbClass()
		#for obj in FreeCADGui.Selection.getSelection():
		print("Build gbxml Group Structure")
		self.XrbClass.createGBxmlStructure()
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

class CreateIFcFeature:
	def Activated(self):
		from freecad.openStudio.createIFcClass import CreateIFCclass
		print(f"Create IFc Class")
		self.createIfc = CreateIFCclass()
		self.createIfc.processSelection()
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "CreateIFcFeature",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
                "CreateIFcFeature", "Create IFc Feature"
                ),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "CreateIFcFeature", "Create IFc Feature"
                ),
            }

class ExportGeometryFeature:

	def Activated(self):
		from freecad.openStudio.exportShape import exportDialog
		
		print("Export Geometry")
		#   for obj in FreeCADGui.Selection.getSelection()
		selectEx = FreeCADGui.Selection.getSelectionEx()
		for sel in selectEx :
			print(f"Selected-Ex {sel.ObjectName} {sel.Object.TypeId}")
			if hasattr(sel, 'PartShape'):
				if sel.ShapeValid == 0:		# Unset
					# Calc Shape
					pass
				if sel.ShapeValid == 1:
					exportDialog(sel.ObjectName, sel.Object)
	     
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "ExportGeometry",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
                "ExportGeometry", "Export Geometry"
                ),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "ExportGeometry", "Export Geometry"
                ),
            }


class RunEnergyModelFeature:
	def Activated(self):
		print("Run Energy Model")
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "RunEnergyModel",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
                "RunEnergyModel", "Run Energy Model"
                ),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "RunEnergyModel", "Run Energy Model"
                ),
            }

class EditTemplateFeature:
	def Activated(self):
		from freecad.openStudio.editFile import editFile
		print("EditTemplate : IDF_template.idf")
		editFile("IDF_template.idf")
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "EditTemplate",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
				"EditTemplate", "Edit Template"
				),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "EditTemplate", "Edit Template"
                ),
            }


class EditMaterialMapFeature:
	def Activated(self):
		from freecad.openStudio.editFile import editFile
		print("EditMaterialMap : material_data.csv")
		editFile("material_data.csv")
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "EditMaterialMap",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
				"EditMaterial", "Edit Material Map"
				),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "EditMaterial", "Edit Material Map"
                ),
			}

class EditScheduleFeature:
	def Activated(self):
		from freecad.openStudio.editFile import editFile
		print("EditSchedule : IDF_schedules.idf")
		editFile("IDF_schedules.idf")
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "EditSchedule",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
				"EditSchedule", "Edit Schedule"
				),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "EditSchedule", "Edit Schedule"
                ),
			}

class EditIDFSpaceFeature:
	def Activated(self):
		from freecad.openStudio.editFile import editFile
		print("EditIDFSpace : space_data.csv")
		editFile("space_data.csv")
		
	def IsActive(self):
		if FreeCAD.ActiveDocument is None:
			return False
		else:
			return True
			
	def GetResources(self):
		return {
            "Pixmap": "EditIDFSpaceMap",
            "MenuText": QtCore.QT_TRANSLATE_NOOP(
				"EditIDFSpace", "Edit IDF Space Map"
				),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP(
                "EditIDFSpace", "Edit IDF Space Map"
                ),
			}		

class IdfGroupFeature:
    """Group of To IDF Commands"""
            
    def GetCommands(self):
        """Tuple of Commands"""
        return ("RunEnergyModelCmd", "EditTemplateCmd", "EditMaterialMapCmd", "EditScheduleCmd", "EditIDFSpaceCmd")

    def GetResources(self):
        """Set icon, menu and tooltip."""

        return {
            "Pixmap": "IDFeditGroup",
            "MenuText": QtCore.QT_TRANSLATE_NOOP("Edit IDF Group", "IDF Group"),
            "ToolTip": QtCore.QT_TRANSLATE_NOOP("Edit IDF Group", " Group of Gmsh Commands"
            ),
        }

    def IsActive(self):
        """Return True when this command should be available."""
        if FreeCAD.ActiveDocument is None:
            return False
        else:
            return True
			

FreeCADGui.addCommand("IdfGroupCmd", IdfGroupFeature())
FreeCADGui.addCommand("RunEnergyModelCmd", RunEnergyModelFeature())
FreeCADGui.addCommand("EditTemplateCmd", EditTemplateFeature())
FreeCADGui.addCommand("EditMaterialMapCmd", EditMaterialMapFeature())
FreeCADGui.addCommand("EditScheduleCmd", EditScheduleFeature())
FreeCADGui.addCommand("EditIDFSpaceCmd", EditIDFSpaceFeature())
FreeCADGui.addCommand("addGBxmlCmd", AddGBxmlFeature())
FreeCADGui.addCommand("buildGBxmlCmd", BuildGBxmlFeature())
FreeCADGui.addCommand("createIFcCmd", CreateIFcFeature())
FreeCADGui.addCommand("syncGBxmlCmd", SyncGBxmlFeature())
FreeCADGui.addCommand("exportGeometryCmd", ExportGeometryFeature())
