#!/usr/bin/env python3.11
"""
Usage: python createXSDobjects.py <xsd_file> <target_name>

This script parses the given XSD file (using lxml), finds the element with the
specified name and its sub-elements, then outputs a Python file named
target_name.py. The generated code defines a classs that, when attached
to a FreeCAD FeaturePython object, creates properties (mapping XSD types to
FreeCAD properties) and provides a Qt dialog (using PySide2) to edit those values.
"""

from lxml import etree
import sys

# Mapping of basic XSD types to FreeCAD property types.
XSD_TO_FC_MAP = {
    'string': 'App::PropertyString',
    'int': 'App::PropertyInteger',
    'integer': 'App::PropertyInteger',
    'float': 'App::PropertyFloat',
    'double': 'App::PropertyFloat',
    'decimal': 'App::PropertyFloat',
    'boolean': 'App::PropertyBool'
}

def parseXSD(xsd_file, output_filename):
# Parse the XML
	print(f"Parse XSD {xsd_file} to {output_filename}")
	tree = etree.parse(xsd_file)
	root = tree.getroot()
	# Or, if you have a string, use etree.fromstring() instead
	# Iterate over all elements in the document
	fp = open(output_filename,"w")
	for elem in tree.iter():
		name = elem.get('name')
		if name is not None:
			eType = elem.get('type')
			print(f"=== {name} type {eType}")
			#print(dir(elem))
			# Must be a better way
			choice = False
			nameEnum = []
			for subElem in elem.iter():
				#print(subElem)
				#print(subElem.tag)
				subName = subElem.xpath('local-name()')
				if subName == "restriction":
					subType = subElem.get("base")
					print(f"name : {subName} type :{subType}")
					if subType == "xsd:NMTOKEN":
						print(f"Start enum {name}")
						nameEnum = []
				elif subName == "enumeration":
					value =  subElem.get('value')
					print(f"name : {subName} value :{value}")
					nameEnum.append(value)
				elif subName == 'element':
					elemType = subElem.get('type')
					if elemType == "xsd:string":
						print("Process Element ??")
					ref = subElem.get('ref')
					minOccurs = subElem.get('minOccurs')
					maxOccurs = subElem.get('maxOccurs')
					print(f"=====> name : {subName} ref :{ref}")
				elif subName == 'choice':
					minOccurs =  subElem.get('minOccurs')
					maxOccurs =  subElem.get('maxOccurs')
					print(f"=====> name : {subName} minOccurs {minOccurs} maxOccurs {maxOccurs}")
					choice = True
				elif subName == 'attribute':
					id = subElem.get('id')
					attrtype = subElem.get('type') 
					print(f"{subName} {id} type{attrtype}")
				elif subName == 'extension':
					base = subElem.get('base')
					attrtype = subElem.get('type')
					if base == "xsd:decimal":
						print("Process Element ??")
				elif len(nameEnum) > 0:
						print(f"enum {subName}")
				

if len(sys.argv) < 3:
	print("Usage: python createXSDobjects.py <xsd_file> <target_name>");	
xsd_file = sys.argv[1]
output_filename = sys.argv[2]
print(f"xsd processing {xsd_file} to {output_filename}")
parseXSD(xsd_file, output_filename)
print(f"xsd processed {xsd_file} to {output_filename}")

