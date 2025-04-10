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

from freecad.openStudio.gbxml_lxml import gbxml_lxml

class GBXML_file:
    def __init__(self):
        print("Init GDML file")
        self.gbxml = gbxml_lxml()

    def FileDetails(self, filename):
        print(f"Set file details {filename}")
        import os
        split = os.path.splitext(filename)
        self.filename  = filename
        self.pathDir = split[0]
        self.docName = split[1][0]
        self.fileType = os.path.splitext(filename)[1][1:]

    def parseGBXML(self, doc, filename):
        self.FileDetails(filename)
        print(f"Process GBXML file {doc.Name} path {filename} Name{self.docName}")
        self.gbxml.parse(filename)

    def exportSite(self, siteObj):
        print(f"Export Site")
        print(dir(siteObj))
        print([x for x in dir(gbxml) if not x.startswith('_')])
        prints "['AirLoop', \
                'AirLoops', \
                'Campus', \
                'Campuss', \
                'Construction', \
                'Constructions', \
                'DaySchedule', \
                'DaySchedules', \
                'DocumentHistory', \
                'DocumentHistorys', \
                'ExtEquip', \
                'ExtEquips', \
                'HydronicLoop', \
                'HydronicLoops', \
                'IntEquip', \
                'IntEquips', \
                'Layer', \
                'Layers', \
                'LightingControl', \
                'LightingControls', \
                'LightingSystem', \
                'LightingSystems', \
                'Material', \
                'Materials', \
                'Meter', \
                'Meters', \
                'Results', \
                'Resultss', \
                'Schedule', \
                'Schedules', \
                'SimulationParameters', \
                'SimulationParameterss', \
                'SurfaceReferenceLocation', \
                'Weather', \
                'Weathers', \
                'WeekSchedule', \
                'WeekSchedules', \
                'WindowType', \
                'WindowTypes', \
                'Zone', \
                'Zones', \
                'add_AirLoop', 'add_Campus', 'add_Construction', 'add_DaySchedule', 'add_DocumentHistory', 'add_ExtEquip', 'add_HydronicLoop', 'add_IntEquip', 'add_Layer', 'add_LightingControl', 'add_LightingSystem', 'add_Material', 'add_Meter', 'add_Results', 'add_Schedule', 'add_SimulationParameters', 'add_Weather', 'add_WeekSchedule', 'add_WindowType', 'add_Zone', 'add_aecXML', 'add_child', 'addnext', 'addprevious', 'aecXML', 'aecXMLs', 'append', 'areaUnit', 'attrib', 'base', 'clear', 'cssselect', 'engine', 'extend', 'find', 'findall', 'findtext', 'get', 'get_attribute', 'get_attributes', 'get_child', 'get_children', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'id', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'lengthUnit', 'makeelement', 'nntag', 'ns', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'set_attribute', 'sourceline', 'tag', 'tail', 'temperatureUnit', 'text', 'tostring', 'useSIUnitsForResults', 'value', 'values', 'version', 'volumeUnit', 'xpath', 'xsd_schema']"

    
