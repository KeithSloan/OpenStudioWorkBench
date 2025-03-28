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
#    Takes as input a Volume Name, GDML file  and outputs                  *
#              a directory structure starting at the specified Volume Name *
#                                                                          *
#                                                                          *
#    python3 buildDirStruct.py <parms> <Volume> <gdml_file> <Out_dir>      *
#                                                                          *
#       parms for future use ( use 1 for now )                             *
#       Volume    : Name of Volume to be extracted                         *
#       gdml_file : Source GDML file                                       *
#       Out_dir   : Output Directory                                       *
#                                                                          *
#  Where each Volume, Assembly is created as a sub directory               *
#                                                                          *
#           volumeName.gdml                                                *
#           volumeName_define.xml                                          *
#           volumeName_materials.xml                                       *
#           volumeName_solids.xml                                          *
#           volumeName_struct.xml                                          *
#           volumeName_setup.xml                                           *
#           < sub Volumes/Assemblies >                                     *
#                                                                          *
############################################################################

import FreeCAD, FreeCADGui
import sys, os
#from freecad.openStudio import skp_lxml
#import copy


if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


def getType(obj):
    if obj.TypeId == "Part::FeaturePython":
        if hasattr(obj, "Proxy"):
            if hasattr(obj.Proxy, "Type"):
                return obj.Proxy.Type
    else:
        return obj.TypeId

def processSpaceSketch(wallObj, sketch):
    for sObj in sketch.Geometry:
        print(sObj.TypeId)
        gType = sObj.TypeId
        #while switch(gType):
        #    if case("Part::GeomLineSegment"):
        #        print(f"{sObj.StartPoint} , {sObj.EndPoint}")
        #
        #    print(f"{gType} Not yet handled")
        #    return
        if gType == "Part::GeomLineSegment":
            print(f"{sObj.StartPoint} , {sObj.EndPoint}")
        else:
            print(f"{gType} Not yet handled")


def processWall(wObj):
    if hasattr(wObj, "Base"):
        print(wObj.Base)
        if wObj.Base is not None:
            if wObj.Base.TypeId == "Sketcher::SketchObject":
                processSpaceSketch(wObj, wObj.Base)

def getFace(obj, fName):
    print(f"{obj.Label} Get Face {fName}")

def processBoundaryObjFaces(objFaces):
    # objFaces - tuples
    print(f"objFaces {objFaces}")
    processWall(objFaces[0])
    #for wObj in objFaces(0): 
    #    processWall(wObj)

    #print(f"{obj.Label} type {getType(obj)}")
    #for fn in fNames:
    #    face = getFace(obj, fn)

def processBoundaries(bObjs):
    print(bObjs)
    for b in bObjs :
        processBoundaryObjFaces(b)
    #print(boundType)

def processSpace(sObj):
    if hasattr(sObj, "Boundaries"):
        processBoundaries(sObj.Boundaries)

def processExport(obj):
    objType = getType(obj)
    print(f"Label {obj.Label} Type {objType}")
    while switch (objType):
        if case("Space"):
            print(f"Space")
            processSpace(obj)
             
        return

def export(exportList, filename):
    "called when FreeCAD exports a file"

    # process Objects
    print("\nStart OpenStudio Export skp xml 0.1\n")
    print(f"Open Output File : ExportList {exportList}")
    for e in exportList:
        processExport(e)


def exportEntity(dirPath, elemName, elem):
    import os
    global gdml, docString

    etree.ElementTree(elem).write(os.path.join(dirPath, elemName))
    docString += '<!ENTITY '+elemName+' SYSTEM "'+elemName+'">\n'
    gdml.append(etree.Entity(elemName))




