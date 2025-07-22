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
__title__ = "FreeCAD - Convert GBXML to IDF"
__author__ = "Keith Sloan <ipad2@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/OpenStudioWorkBench"]

import FreeCAD, FreeCADGui
import sys, os

#import copy

if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

def open(filename):
    "called when freecad opens a file."
    global doc
    print(f"Opening : {filename}")
    docName = os.path.splitext(os.path.basename(filename))[0]
    if filename.lower().endswith(".gbxml") or filename.lower().endswith(".xml"):
        # import cProfile, pstats
        # profiler = cProfile.Profile()
        # profiler.enable()
        doc = FreeCAD.newDocument(docName)
        convertGbXML2IDF(doc,filename)
        # profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        # stats.print_stats()

def insert(filename, docName):
    "called when freecad imports a file"
    print("Insert filename : " + filename + " docname : " + docName)
    try:
        doc = FreeCAD.getDocument(docName)
    except NameError:
        doc = FreeCAD.newDocument(docName)
    if filename.lower().endswith(".gbxml") or filename.lower().endswith(".xml"):
        # False flag indicates import
        convertGbXML2IDF(doc, filename)


def convertGbXML2IDF(docName, fileName ): #importFlag, fileName):
    # Debugging
    # from sys import breakpointhook

    from freecad.gbXML2IDF.gbxmlconvertor import convert
	
    print(f"Convert GbXml file path {fileName}")
    #gbXmlxml.processGbXml(docName, fileName)
