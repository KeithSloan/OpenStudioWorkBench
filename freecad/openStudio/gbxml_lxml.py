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

import FreeCAD, FreeCADGui
import sys, os
#from freecad.openStudio import skp_lxml
#import copy


if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here


class gbxml_lxml():
    from lxml import etree as ET
    global ET                # Is there a better way ???
    import os

    def __init__(self):
        super().__init__()
        self.gbXML = self.init_gbXML()

    def setFileDetails(self, path):
        self.filepath = path

    def init_gbXML(self):
        NS = "http://www.w3.org/2001/XMLSchema-instance"                       
        location_attribute = "{%s}noNamespaceSchemaLocation" % NS              
        # For some reason on my system around Sep 30, 2024, the following url is unreachable,       
        # I think because http:// is no longer accepted, so use https:// instead. DID NOT WORK!,
        # although wget of url works. I don't know what's going on
        gbXML = ET.Element(
            "gbXML",
                attrib={
                    location_attribute: "https://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd" 
                },
            )
        return gbXML 


    #def writeElementTree(self, path, sname, type, elem, ext="xml"):

    def writeElementTree(self, pathname, ext="xml"):
        #fpath = os.path.join(path, sname+'_'+type)
        print(f"writing file : {pathname}")
        #ET.ElementTree(elem).write(fpath+'.'+ext)
        #ET.ElementTree(self.gbXML).write(fpath+'.'+ext)
        ET.ElementTree(self.gbXML).write(pathname)