# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2025 Keith Sloan <ipad2@sloan-home.co.uk>               *
# *                 Maarten Visschers <maartenvisschers@hotmail.com>        *
# *                                                                         *                                                                    *
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
# *     Frontend for Maarten Visschers IFC to gbXML converter               *
# *    https://github.com/MGVisschers/IFC-to-gbXML-converter/tree/master    *
# *                                                                         *
# *   Acknowledgements :                                                    *
# *                                                                         *      
# *                                                                         *
############################################################################*
__title__ = "FreeCAD - Front end to Maarten Visschers IFC to gbXML importer"
__author__ = "Keith Sloan <ipad2@sloan-home.co.uk>"
__url__ = ["https://github.com/KeithSloan/FreeCAD_GDML"]

import FreeCAD
import os, sys, pathlib, tempfile

if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

from freecad.openStudio.import_gbXML import processGbXmlFile
#sys.path.append("../IFC-to-gbXML-converter")
# Need to access parent
child_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(child_dir, '../IFC-to-gbXML-converter'))
sys.path.append(parent_dir)
# print(sys.path)

import ifcgbxml

def open(filename):
    "called when freecad opens a file."
    global doc
    print(f"Open : {filename}")
    docName = os.path.splitext(os.path.basename(filename))[0]
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as gbXMLfile:
        #gbXMLname = os.path.join(tmpdir, docName + '.gbXML')
        print(f"gbXML fileName {gbXMLfile.name}")
        if filename.lower().endswith(".ifc"):
            # profiler = cProfile.Profile()
            # profiler.enable()
            doc = FreeCAD.newDocument(docName)
            ifcgbxml.convertIfc2gbXML(filename, gbXMLfile.name)
            processGbXmlFile(doc, False, gbXMLfile)
            #tmpdir.cleanup()        
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
    with tempfile.NamedTemporaryFile() as gbXMLfile:
        try:
            doc = FreeCAD.getDocument(docName)
        except NameError:
            doc = FreeCAD.newDocument(docName)
        if filename.lower().endswith(".ifc"):
            # False flag indicates import
            ifcgbxml.convert_IFC_to_gbXML(filename, gbXMLfile.name)
            processGbXmlFile(doc, False, gbXMLfile)
            #tmpdir.cleanup()  
        
    #elif filename.lower().endswith(".xml"):
    #    processXML(doc, filename)

def processGbXmlFile(docName, importFlag, fileName):
    # Debugging
    # from sys import breakpointhook
    from freecad.openStudio.XrbClass import XrbClass
    from freecad.openStudio.LXMLclass import LXMLclass
	
    print(f"Process GbXml file {docName} path {fileName}")
    gbXmlXrb = XrbClass()
    gbXmlXrb.checkGBxml()
    gbXmlxml = LXMLclass(gbXmlXrb)
    gbXmlxml.processGbXml(docName, fileName)
    
