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
############################################################################

import FreeCAD, FreeCADGui

from freecad.openStudio.BMIclass import BMIinfo

#if open.__module__ in ['__builtin__', 'io']:
#    pythonopen = open # to distinguish python built-in open function from the one declared here

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

def addGBxml(obj):
	objType = getType(obj)
	print(f"Label {obj.Label} Type {objType}")
	while switch (objType):
		if case("Space"):
			print(f"Space")
			processSpace(obj)
			bmiClass.add(obj)
             
		return

# process Objects
print("\nStart OpenStudio Add gbxml properties 0.1\n")
doc = FreeCAD.ActiveDocument
global bmiClass
bmiClass = BMIinfo()
if doc is not None:
	bmiClass = BMIinfo()
	for obj in doc.RootObjects:
		addGBxml(obj)
