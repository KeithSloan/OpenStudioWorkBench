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
class QtExportDialog(QtGui.QDialog):
    def __init__(self, enum_class, parent=None):
        super().__init__(parent)
        self.enum_class = enum_class
        self.selected_enum = None

        self.setWindowTitle("Select an Enum Value")
        self.layout = QtGui.QVBoxLayout(self)

        self.label = QtGui.QLabel("Choose a value:")
        self.layout.addWidget(self.label)

        self.list_widget = QtGui.QListWidget()
        for item in enum_class:
            self.list_widget.addItem(item.name)
        self.layout.addWidget(self.list_widget)

        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def accept(self):
        selected = self.list_widget.currentItem()
        if selected:
            self.selected_enum = self.enum_class[selected.text()]
        super().accept()

    def get_selection(self):
        return self.selected_enum


def exportDialog(name, Obj):
	#from PySide import QtGui, QtCore

	print(f"Export Shape {name} type{Obj.TypeId}")
	print("Display Dialog")
	ExportOptions = ["Brep", "Sketch"]
	dialog = QtExportDialog(ExportOptions)
	print(dialog.exec_())
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
