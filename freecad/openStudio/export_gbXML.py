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
# *                                                                         
# *   Process Document and where                                                                   *
# *                                                                         *
# *                                                                         *
# *                                                                         *
############################################################################*

import FreeCAD, FreeCADGui
import sys, os
#from freecad.openStudio import skp_lxml
#import copy


if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here


#from freecad.openStudio.gbxml_lxml import gbxml_lxml
#from freecad.openStudio.docTree_gbxml import buildDocTree

#global gbXML
#gbXML = gbxml_lxml()

####
#    gbxml = ET.Element(
#        "gbXML",
#         attrib={
#
#    <?xml version="1.0"?>
#<gbXML useSIUnitsForResults="false" temperatureUnit="C" lengthUnit="Feet" 
#areaUnit="SquareFeet" volumeUnit="CubicFeet" version="0.37" xmlns="http://www.gbxml.org/schema">
####


#def processExportActiveDocument(filename):
#    import FreeCAD
#
#    for obj in FreeCAD.ActiveDocument.Objects:
#        print(obj.Label)
#        if hasattr(obj, "Valueset"):
#            print("Value Set")

def exportObj(exporter, elemGrp, Obj):
    print(f"ExportObj {elemGrp} Object {Obj.Label}")
    if hasattr(Obj, "ValueSet"):
        #print(f"Object {obj.Label} Value Set")
        if Obj.ValueSet :
            print(f"Object : {Obj.Label} - Values Set")
            #for prop in Obj.PropertiesList:
            #    group = Obj.getGroupOfProperty(prop)
            #    if group == "gbXML":
            #        print(f"Property {prop} is in Group {group}")
            #        attr = str(getattr(Obj, prop))
            #        #elemGrp.set(prop, attr)

        # Now process Group
        # if Obj.ValueSet : ????
        if hasattr(Obj,"Group"):
            print(f"Process {Obj.Label} Group ")
            for obj in Obj.Group:
                print(f"Process Group {obj.Label}")
                print(f"Add SubElement {obj.Label} to {elemGrp} ")
                # add_element(self, parent, tag, text=None, attrib=None, ns="gbxml"):
                newElemGrp = exporter.add_element(elemGrp, obj.Label)
                exportObj(exporter, newElemGrp, obj)

def exportSelection(filename, obj):
    from freecad.openStudio.GbxmlExporterClass import GbxmlExporter  
    print(obj.Label)
    # Set gbXML structure on each export
    exporter = GbxmlExporter()
    exportObj(exporter, exporter.root, obj)
    #gbXML.writeElementTree(filename, gbXML, type, elem, ext="xml")
    exporter.writeTree(filename)


def export(exportList, filename):

    "called when FreeCAD exports a file"
    # from freecad.openStudio import gbxml_lxml
    # process Objects
    print("\nStart Export gbxml 0.1\n")
    print(f"Open Output File : {filename} ExportList {exportList}")
    #gbXML.setFileDetails(filename)
    exportSelection(filename, exportList[0])
    #processExportActiveDocument(filename)