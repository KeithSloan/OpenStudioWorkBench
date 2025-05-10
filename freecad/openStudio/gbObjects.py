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

from freecad.openStudio.baseObject import baseObjectClass

class PolyLoopClass(baseObjectClass):

    def __init__(self, obj):
        super().__init__(obj, "PolyLoopClass")
        """Init"""
        self.obj = obj

    def initPoly(self):
        self.obj.addProperty("App::PropertyVectorList", "Coordinates","GbXml","Coordinate Points")

    def addCordinateVector(self, v):
        self.Cordinates.append(v)

    def addCordinates(self, X, Y, Z=0.0):
        import FreeCAD
        v = FreeCAD.Vector(X, Y, Z)
        self.Cordinates.append(v)