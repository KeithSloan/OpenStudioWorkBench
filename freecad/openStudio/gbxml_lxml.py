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

        print("init gbxml lxml")
        #self.gbxml = xgbxml.create_gbXML()
        # docString ?? default defintion !!!
        self.docString = ''
        self.gbxml = xgbxml.create_gbXML()
        # uses xgbxml to generate a lxml parser to read gbXML version 0.37
        #self.parser = self.gbxml.get_parser(version='0.37')
        self.parser = xgbxml.get_parser("0.37")
    
    def setFileDetails(self, filename):
        import os
        split = os.path.splitext(filename)
        self.filename  = filename
        self.pathDir = split[0]
        self.docName = split[1][0]
        self.fileType = os.path.splitext(filename)[1][1:]

    def parseGBXML(self, doc, filename):
        from lxml import etree
        #self.setFileDetails(filename)
        print(f"Parse file {filename}")   
        self.tree = etree.parse(filename, self.parser)
        self.gbxml = self.tree.getroot()
    
    def export(self, filename):
        self.tree = self.gbxml.getroottree()
        self.tree.write(filename)

    def exportSite(self, siteObj):
        print(dir(siteObj))
        print(f"Campus {dir('Campus')}")
        self.campus=self.gbxml.add_Campus(id='my_campus')
        building1=self.campus.add_Building(id='my_building1')
        #print([x for x in dir(self.gbxml) if not x.startswith('_')])
        #prints "['AirLoop', 'AirLoops', 'Campus', 'Campuss', 'Construction', 'Constructions', 'DaySchedule', 'DaySchedules', 'DocumentHistory', 'DocumentHistorys', 'ExtEquip', 'ExtEquips', 'HydronicLoop', 'HydronicLoops', 'IntEquip', 'IntEquips', 'Layer', 'Layers', 'LightingControl', 'LightingControls', 'LightingSystem', 'LightingSystems', 'Material', 'Materials', 'Meter', 'Meters', 'Results', 'Resultss', 'Schedule', 'Schedules', 'SimulationParameters', 'SimulationParameterss', 'SurfaceReferenceLocation', 'Weather', 'Weathers', 'WeekSchedule', 'WeekSchedules', 'WindowType', 'WindowTypes', 'Zone', 'Zones', 'add_AirLoop', 'add_Campus', 'add_Construction', 'add_DaySchedule', 'add_DocumentHistory', 'add_ExtEquip', 'add_HydronicLoop', 'add_IntEquip', 'add_Layer', 'add_LightingControl', 'add_LightingSystem', 'add_Material', 'add_Meter', 'add_Results', 'add_Schedule', 'add_SimulationParameters', 'add_Weather', 'add_WeekSchedule', 'add_WindowType', 'add_Zone', 'add_aecXML', 'add_child', 'addnext', 'addprevious', 'aecXML', 'aecXMLs', 'append', 'areaUnit', 'attrib', 'base', 'clear', 'cssselect', 'engine', 'extend', 'find', 'findall', 'findtext', 'get', 'get_attribute', 'get_attributes', 'get_child', 'get_children', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'id', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'lengthUnit', 'makeelement', 'nntag', 'ns', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'set_attribute', 'sourceline', 'tag', 'tail', 'temperatureUnit', 'text', 'tostring', 'useSIUnitsForResults', 'value', 'values', 'version', 'volumeUnit', 'xpath', 'xsd_schema']"
        self.tree=self.gbxml.getroottree()
        self.tree.write(self.filename, pretty_print=True)

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