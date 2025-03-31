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
# *                                                                         *                                                                  *
# *   FreeCAD does not provide an easy way to access the document           •
# *   structure as it controlled by ViewProviders                           •
# *                                                                         *
# *   buildDocTree - buids doc structure using Qt info                      *
# *                                                                         *
# *         Based on version in GDML Workbench                              *                                                                *
# *         Code copyright Munther Hindo see GDML Workbench                 *                                                       *
# *                                                                         *
# *                                                                         *
############################################################################*
__title__ = "FreeCAD - GBXML BuildDoc Tree"
__author__ = "Keith Sloan <ipad2@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

import FreeCADGui
import FreeCAD as App

from PySide import QtWidgets 

def buildDocTree():     # Munther Hindi
    #global childObjects
    childObjects = {}  # dictionary of list of child objects for each object
    # TypeIds that should not go in to the tree
    #skippedTypes = ["App::Origin", "Sketcher::SketchObject", "Part::Compound"]
    skippedTypes = ["App::Origin", "Part::Compound"]

    def addDaughters(item: QtWidgets.QTreeWidgetItem):
        print (f"--------addDaughters {item.text(0)}")
        objectLabel = item.text(0)
        object = App.ActiveDocument.getObjectsByLabel(objectLabel)[0]
        if object not in childObjects:
            childObjects[object] = []
        for i in range(item.childCount()):
            childItem = item.child(i)
            treeLabel = childItem.text(0)
            try:
                childObject = App.ActiveDocument.getObjectsByLabel(treeLabel)[0]
                objType = childObject.TypeId
                if objType not in skippedTypes:
                    childObjects[object].append(childObject)
                    addDaughters(childItem)
            except Exception as e:
                print(e)
        #return
        return childObjects