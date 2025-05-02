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

import FreeCAD as App

class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))

class LXMLclass():

	def __init__(self):
		super().__init__()
		self.gbXML = None		# gbXML Element

	def initLXML(self, fileName):
		print(f"Init lxml Class")
		self.fileName = fileName
		try:
			from lxml import etree
			#from xml import etree

			print(f"Running with etree.ElementTree (import limitations)\n")

			self.parser = etree.XMLParser(ns_clean=True)
			self.tree = etree.parse(fileName, self.parser)
			self.root = self.tree.getroot()
        
		except ImportError:
			try:
				import xml.etree.ElementTree as etree
				print("Rnning with etree.ElementTree (import limitations)\n")
	
				self.tree = etree.parse(filename)
				self.root = self.tree.getroot()
			except:
				print('No lxml or xml')
		
	def processGbXml(self):
		from freecad.openStudio.processXrb import processXrbElement, processXrbElementByName
		print(f"Process GbXml {self.fileName}")
		self.gbXML = processXrbElementByName(self, "gbXML") 
