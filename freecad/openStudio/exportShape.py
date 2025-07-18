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
#                                                                          *
############################################################################

import FreeCAD, FreeCADGui

from PySide import QtGui, QtCore

# Step 1: Define an Enum
#class ExportOptions():
#    Brep = 1
#    Sketch = 2

# Step 2: Create the Enumeration Dialog
class TestEnumComboDialog(QtGui.QDialog):
	def __init__(self, enum_list, parent=None):
		super(TestEnumComboDialog, self).__init__(parent)
		self.enum_list = enum_list
		self.selected_enum = None

		self.setWindowTitle("Select Type of Export")
		self.setMinimumWidth(300)
		self.acceptlayout = QtGui.QtWidgets.QVBoxLayout(self)
		self.list_widget = QtGui.QComboBox()
		for item in self.enum_list:
			self.list_widget.addItem(item)
		self.layout.addWidget(self.list_widget)

		self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
		self.buttons.accepted.connect(self.accept)
		self.buttons.rejected.connect(self.reject)
		self.layout.addWidget(self.buttons)
		
	def accept(self):
		selected_name = self.combo.currentText()
		self.selected_enum = self.enum_class[selected_name]
		super(TestEnumComboDialog, self).accept()

	def get_selection(self):
	    return self.selected_enum


from PySide import QtWidgets, QtGui, QtCore
import FreeCADGui as Gui

class EnumComboBoxWidget(QtGui.QWidget):
	def __init__(self, enum_list, parent=None):
		super(EnumComboBoxWidget, self).__init__(parent)
		self.enum_list = enum_list
		self.combo = QtGui.QComboBox()
        #self.enum_class = QtCore.AlignmentFlag  # Change this to the desired enum
		self.populate_enum_values()
        
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.combo)
		self.setLayout(layout)

	def populate_enum_values(self):
		self.combo.clear()
		for value in self.enum_list:
			self.combo.addItem(value.name, value)

	def get_selected_enum(self):
		return self.combo.currentData()


# Show the widget in FreeCAD's main window
#mw = Gui.getMainWindow()
#widget = EnumComboBoxWidget()
#dock = mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)



def exportDialog(name, Obj):
	#from PySide import QtGui, QtCore

	print(f"Export Shape {name} type{Obj.TypeId}")
	print("Display Dialog")
	ExportOptions = ["Brep", "Sketch", "STL", "STEP"]
	mw = Gui.getMainWindow()
	widget = EnumComboBoxWidget(ExportOptions)
	dock = mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, widget)

	# ExportOptions = ["Brep", "Sketch", "STL", "STEP"]
	#dialog = EnumComboBoxWidget(ExportOptions)
	#print(dialog.exec_())
    #if dialog.exec_() == QtGui.QDialog.Accepted:
    #    selected = dialog.get_selection()
    #    print(f"Selected enum: {selected} ({selected.name})")
    #else:
    #    print("No selection made.")


	# Qt Enumeration
	#
	#
	#	if sel.Object.TypeId == "Mesh::Feature":
        #        shapes2Sketch(sel.Object.Mesh, sel.ObjectName+"Sketch")
        #    else:
        #        if hasattr(sel.Object, "Shape"):                          
        #            shapes2Sketch(sel.Object.Shape, sel.ObjectName+"Sketch")
