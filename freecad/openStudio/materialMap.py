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

__title__ = "FreeCAD OpenStudio - MaterialMap"
__author__ = "Keith Sloan"
__url__ = ["http://www.freecadweb.org"]

import FreeCAD
import FreeCADGui

# from PySide2 import QtGui, QtCore
from PySide import QtGui, QtCore

if FreeCADGui:
    try:
        _encoding = QtGui.QApplication.UnicodeUTF8

        def translate(context, text):
            "convenience function for Qt translator"
            return QtGui.QApplication.translate(context, text, None, _encoding)
    except AttributeError:
        def translate(context, text):
            "convenience function for Qt translator"
            return QtGui.QApplication.translate(context, text, None)




def resetMaterialMap():
    print('Reset Material Map')
    #global workBenchColourMap
    #try:
    #    del workBenchColourMap
    #except NameError:
    #    pass

    #workBenchColourMap = GDMLColourMap(FreeCADGui.getMainWindow())


def showMaterialMap():
    print('Display Material Map')
    #workBenchColourMap.show()


def lookupMateria(col):
    # global workBenchColourMap
    print('Lookup Material')
    #try:
    #    mat = workBenchColourMap.lookupColour(col)

    # except NameError:
    #    workBenchColourMap = GDMLColourMap(FreeCADGui.getMainWindow())
    #    mat = workBenchColourMap.lookupColour(col)

    #return mat

class Material(QtGui.QLineEdit):

    def __init__(self, name):
        super().__init__()
        
        #self.setAutoFillBackground(True)
       
        #self.setStyleSheet("QPushButton {border-color: black; border: 2px;}")
        self.insert(name)
        self.setReadOnly(True)
        self.update()


class Id(QtGui.QLineEdit):

    def __init__(self, id):
        super().__init__()
        self.insert(id)
        self.setReadOnly(True)


class MaterialMapEntry(QtGui.QWidget):

    def __init__(self, id, name, material):
        super().__init__()
        print(f"Material Map Entry - id : {id} Name : {name}")
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(Id(id))
        self.hbox.addWidget(Material(name))
        self.setLayout(self.hbox)

    def dataPicker(self):
        print('DataPicker')


class MaterialMapList(QtGui.QScrollArea):

    #def __init__(self, matList):
    def __init__(self):
        super().__init__()
        # Scroll Area which contains the widgets, set as the centralWidget
        # Widget that contains the collection of Vertical Box
        self.widget = QtGui.QWidget()
        #self.matList = matList
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QtGui.QVBoxLayout()
        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

    def addEntry(self, id, name, material):
        print('Add Entry')
        #matWidget = GDMLMaterial(self.matList, mat)
        self.vbox.addWidget(MaterialMapEntry(id, name, material))

    def getMaterial(self, index):
        # print(dir(self.vbox))
        item = self.vbox.itemAt(index).widget()
        # item.dumpObjectTree()
        # cb = item.findChild(QtGui.QComboBox,'GDMLMaterial')
        cb = item.findChildren(QtGui.QComboBox)[0]
        m = cb.currentText()
        print(m)
        return(m)

    def setMaterial(self, index, mat):
        item = self.vbox.itemAt(index).widget()
        cb = item.findChildren(QtGui.QComboBox)[0]
        matIndex = cb.findText(mat)
        if matIndex != -1:
            cb.setCurrentIndex(matIndex)


class MaterialMapDialog(QtGui.QDialog):
    def __init__(self, parent):
        super(MaterialMapDialog, self).__init__(parent, QtCore.Qt.Tool)
        self.initUI()

    def initUI(self):
        from freecad.openStudio.osmMaterial import printOSMmaterials
        printOSMmaterials()
        
        self.result = userCancelled
        # create our window
        # define window           xLoc,yLoc,xDim,yDim
        self.setGeometry(150, 450, 650, 550)
        self.setWindowTitle("Map gbXML Material to IFX Materials")
        self.setMouseTracking(True)
        self.buttonNew = QtGui.QPushButton(translate('gbXML', 'New'))
        self.buttonNew.clicked.connect(self.onNew)
        self.buttonLoad = QtGui.QPushButton(translate('gbXML', 'Load'))
        self.buttonLoad.clicked.connect(self.onLoad)
        self.buttonSave = QtGui.QPushButton(translate('gbXML', 'Save'))
        self.buttonSave.clicked.connect(self.onSave)
        self.buttonScan = QtGui.QPushButton(translate('gbXML', 'Scan'))
        self.buttonScan.clicked.connect(self.onScan)
        headerLayout = QtGui.QHBoxLayout()
        headerLayout.addWidget(self.buttonNew)
        headerLayout.addWidget(self.buttonLoad)
        headerLayout.addWidget(self.buttonSave)
        headerLayout.addWidget(self.buttonScan)
        self.materialsLayout = QtGui.QGridLayout()
        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.addLayout(headerLayout)
        mainLayout.addLayout(self.materialsLayout)
        #self.mapList = MaterialMapList(self.matList)
        self.mapList = MaterialMapList()
        self.materialMapDict = {}
        self.scanDocument(1)
        print(self.materialMapDict)
        # create Labels & add scrollList
        self.label1 = self.mapList
        self.materialsLayout.addWidget(self.label1, 0, 0)
        #  cancel button
        cancelButton = QtGui.QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.setAutoDefault(True)
        self.materialsLayout.addWidget(cancelButton, 2, 1)

        # OK button
        okButton = QtGui.QPushButton('Set Materials', self)
        okButton.clicked.connect(self.onOk)
        self.materialsLayout.addWidget(okButton, 2, 0)
        # now make the window visible
        self.setLayout(mainLayout)
        self.show()

    def scanDocument(self, action):
        doc = FreeCAD.ActiveDocument
        print('Active')
        print(doc)
        if doc is None:
            return
        # print(dir(doc))
        if hasattr(doc, 'Objects'):
            # print(doc.Objects)
            # self.colorList = []
            for obj in doc.Objects:
                # print(dir(obj))
                # ToDo - Betters to set type in gbXML file
                if obj.Label.startswith("Material") and obj.ValueSet:
                    if action == 1:  # Build Map
                        print(f"Material id {obj.id} Name {obj.Name}")
                        #self.addMaterial2Map(obj.colour, obj.Name, material)
                        self.addMaterial2Map(obj.id, obj.Name, "Material")

                    elif action == 2:  # Update Object Material
                        pass
                        #if hasattr(obj, 'Shape'):
                        #                mapIdx = self.colorDict[colhex]
                        #                print(f'Found {colhex} : id {mapIdx}')
                        #                print(obj.Label)
                        #                m = self.mapList.getMaterial(mapIdx)
                        #                # Only add
                        #                if not hasattr(obj, 'material'):
                        #                    obj.addProperty("App::PropertyEnumeration",
                        #                                    "material", "GDML", "Material")
                        #                    obj.material = self.matList
                        #                # Ignore GDML objects which will have Proxy
                        #                if not hasattr(obj, 'Proxy'):
                        #                    obj.material = self.matList.index(
                        #                        m)

    def addMaterial2Map(self, id, name, material):
        self.mapList.addEntry(id, name, material)

    def lookupColour(self, col):
        print('Lookup Colour')
        idx = self.colorList.index(col)
        print(idx)
        entry = self.mapList.vbox.itemAt(idx).widget()
        print(entry)
        mat = entry.hbox.itemAt(1).widget().currentText()
        print(mat)
        return mat

    def onCancel(self):
        self.result = userCancelled
        self.close()

    def onOk(self):
        self.result = userOK
        print('Set Materials')
        self.scanDocument(2)
        # self.close()

    def onNew(self):
        print('onNew')

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16)
                     for i in range(0, lv, lv // 3))

    def onLoad(self):
        import csv
        import os 
        print('onLoad')
        #processXML(FreeCAD.ActiveDocument, joinDir(
        #    'Resources/MapMaterials.xml'))
        # reset mapList
        self.mapList = MaterialMapList(self.matList)
        with open(os.path.join('Resources/ColorDict.csv'), 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                colhex = row[0]
                colour = self.hex_to_rgb(colhex)
                print(f'colour : {colour}')
                material = row[1]
                print(row)
                print(row[1])
                idx = self.matList.index(row[1])
                self.addColour2Map(colour, colhex, material)
                self.colorDict.update([(colhex, idx)])
                self.mapList.setMaterial(i, material)

    def onSave(self):
        import os 
        print('onSave')
        # Save materials
        #from .exportGDML import exportMaterials
        
        # matGrp = FreeCAD.ActiveDocument.getObject('Materials')
        #if matGrp is not None:
        #    exportMaterials(matGrp, joinDir('Resources/MapMaterials.xml'))
        # Save Color Dictionary
        f = open(os.path.join('Resources/ColorDict.csv'), 'w')
        for key, value in self.colorDict.items():
            print(f'key {key} value {value}')
            print(self.mapList.getMaterial(value))
            f.write(f'{key},{self.mapList.getMaterial(value)}\n')
        f.close()

    def onScan(self):
        print('onScan')
        self.scanDocument(1)
        print('Update Layout')
        self.coloursLayout.update()

    #def getGDMLMaterials(self):
    #    print('getGDMLMaterials')
    #    matList = []
    #    doc = FreeCAD.activeDocument()
    #    try:
    #        materials = doc.Materials
    #        geant4 = doc.Geant4
    #        g4Mats = doc.getObject('G4Materials')

    #   except:
    #        from .importGDML import processXML
    #        from .init_gui import joinDir

    #        print('Load Geant4 Materials XML')
    #        processXML(doc, joinDir("Resources/Geant4Materials.xml"))
    #        materials = doc.Materials
    #    try:
    #        if materials is not None:
    #            for m in materials.OutList:
    #               matList.append(m.Label)
    #            # print(matList)
    #    except:
    #        pass

    #   try:
    #        if g4Mats is not None:
    #            for m in g4Mats.OutList:
    #                matList.append(m.Label)
    #            # print(matList)
    #    except:
    #        pass

    #   return matList


# Class definitions

# Function definitions

# Constant definitions
global userCancelled, userOK
userCancelled = "Cancelled"
userOK = "OK"
