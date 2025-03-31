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


class gbxml_lxml() :
    def __init__(self):
        import xgbxml

        self.gbxml = xgbxml.create_gbXML()
        # docString ?? default defintion !!!
        self.docString = ''
        # uses xgbxml to generate a lxml parser to read gbXML version 0.37
        self.parser=self.gbxml.get_parser(version='0.37')

    def setFileDetails(self, filename):
        import os
        split = os.path.splitext(fileame)
        self.filename  = filename
        self.pathDir = split[0]
        self.docName = split[1][0]
        self.fileType = os.path.splitext(filename)[1][1:]

    def parse(self, filename):
        self.setFileDetails(filename)   
            
        from self.gbxml import etree
        print('Running with gbxml.etree\n')
        print(filename)
        #parser = etree.XMLParser(resolve_entities=True)
        self.root = etree.parse(filename, parser=self.parser)

    def export(self, filename):
        self.tree = self.gbxml.getroottree()
        self.tree.write(filename)

    def printElement(self, elem):
        import gbxml.html as html
        print(html.tostring(elem))
    
    def appendEntity(self, filename, elemName):
        self.exportdocString += "<!ENTITY " + elemName + ' SYSTEM "' + filename + '">\n'
        #self.gbxml.append(ET.Entity(elemName))
        #self.tree.ElementTree(elem).write(os.path.join(self.dirPath, elem))


    def printMaterials(self):
        import lxml.html as html
        print(html.tostring(self.materials))

    def printName(self, elem):
        name = elem.attrib.get('name')
        print(f"{elem} : {name}")