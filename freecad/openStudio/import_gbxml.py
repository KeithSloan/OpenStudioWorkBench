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
__title__ = "FreeCAD - GBXML importer"
__author__ = "Keith Sloan <ipad2@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

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

#from freecad.openStudio.gbxml_lxml import gbxml_lxml
from freecad.openStudio.gbxml_lxml import gbxml_lxml

#def open(filename, processType=1, prompt=True):
def open(filename):
    "called when freecad opens a file."
    global doc
    print(f"Open : {filename}")
    docName = os.path.splitext(os.path.basename(filename))[0]
    if filename.lower().endswith(".xml"):

        # import cProfile, pstats
        # profiler = cProfile.Profile()
        # profiler.enable()
        doc = FreeCAD.newDocument(docName)
        # prompt = True
        #if processType == 2:
        #    prompt = False
        #processGBXML(doc, True, filename, prompt, processType, False)
        #gdml_file.FileDetails(filename)
        my_gbxml = gbxml_lxml()
        my_gbxml.parseGBXML(doc, filename)
        # profiler.disable()
        # stats = pstats.Stats(profiler).sort_stats('cumtime')
        # stats.print_stats()

    #elif filename.lower().endswith(".xml"):
    #    try:
    #        doc = FreeCAD.ActiveDocument()
    #        print("Active Doc")

    #   except:
    #        print("New Doc")
    #        doc = FreeCAD.newDocument(docName)

     #   processXML(doc, filename)

def insert(filename, docName):
    "called when freecad imports a file"
    print("Insert filename : " + filename + " docname : " + docName)
    global doc

    # print(f'volDict : {volDict}')
    #groupname = os.path.splitext(os.path.basename(filename))[0]
    try:
        doc = FreeCAD.getDocument(docName)
    except NameError:
        doc = FreeCAD.newDocument(docName)
    if filename.lower().endswith(".gbxml"):
        # False flag indicates import
        #processGDXML(doc, False, filename, True, 1, False)
        gl  = gbxml_lxml()
        #gdml_file.setFileDetails(filename)
        gl.parseGBXML(doc, filename)
        #processGBXML(doc, filename, docName)

    #elif filename.lower().endswith(".xml"):
    #    processXML(doc, filename)
