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


from lxml import etree

class GbxmlExporter:

    from lxml import etree

class GbxmlExporter:
    def __init__(self, root_tag="gbXML", ns="http://www.gbxml.org/schema"):
        """
        Create a new gbXML document with a default namespace.
        """
        self.ns = ns
        self.root = etree.Element(root_tag, nsmap={None: ns})
        self.tree = etree.ElementTree(self.root)

    def add_element(self, parent, tag, text=None, attrib=None):
        """
        Add an element to the XML.
        :param parent: Parent element (or None for root).
        :param tag: Tag name (no namespace needed).
        :param text: Optional text value.
        :param attrib: Optional dict of attributes.
        """
        if attrib is None:
            attrib = {}

        target_parent = parent if parent is not None else self.root
        element = etree.SubElement(target_parent, tag, attrib)

        if text is not None:
            element.text = str(text)

        return element

    def add_material(self, mat_id, name, thickness=None, conductivity=None, density=None, specific_heat=None):
        """
        Add a gbXML Material element with optional properties.
        """
        mat = self.add_element(self.root, "Material", attrib={"id": mat_id})
        self.add_element(mat, "Name", name)
        if thickness is not None:
            self.add_element(mat, "Thickness", thickness)
        if conductivity is not None:
            self.add_element(mat, "Conductivity", conductivity)
        if density is not None:
            self.add_element(mat, "Density", density)
        if specific_heat is not None:
            self.add_element(mat, "SpecificHeat", specific_heat)
        return mat

    def writeTree(self, filepath, pretty=True, xml_declaration=True, encoding="UTF-8"):
        """
        Save the XML to file.
        """
        self.tree.write(filepath, pretty_print=pretty, xml_declaration=xml_declaration, encoding=encoding)



"""
# class gbxml_lxml():
    global ET                # Is there a better way ???
#    from lxml import etree as ET
    import os

    def __init__(self):
        super().__init__()
        self.gbXML = self.gbXMLelement()
        self.tree = ET.ElementTree(self.gbXML)

    def getTree(self):
        return self.tree

    def setFileDetails(self, path):
        self.filepath = path

    def gbXMLelement(self):
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

    def addSubElement(self, element, name):
        #print(f"Add SubElement : {name}")
        return ET.SubElement(element, name)


    def writeElementTree(self, pathname, ext="xml"):
        #fpath = os.path.join(path, sname+'_'+type)
        print(f"writing file : {pathname}")
        #ET.ElementTree(elem).write(fpath+'.'+ext)
        #ET.ElementTree(self.gbXML).write(fpath+'.'+ext)
        ET.indent(self.tree, space="\t", level=0)
        self.tree.write(pathname, encoding="utf-8")
"""