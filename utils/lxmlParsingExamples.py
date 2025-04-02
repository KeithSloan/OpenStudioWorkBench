#!/usr/bin/env python
"""
Usage: python generate_feature.py <xsd_file> <element_name>

This script parses the given XSD file (using lxml), finds the element with the
specified name and its sub-elements, then outputs a Python file named
<element_name>_Feature.py. The generated code defines a class that, when attached
to a FreeCAD FeaturePython object, creates properties (mapping XSD types to
FreeCAD properties) and provides a Qt dialog (using PySide2) to edit those values.
"""

from lxml import etree
#import sys

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
# Parse the XML
tree = etree.parse('your_document.xml')
# Or, if you have a string, use etree.fromstring() instead

# Iterate over all elements in the document
for element in tree.iter():
    print(element.tag)  # Print the tag name of each element
    
# Iterate only over elements with the tag 'item'
for element in tree.iter('item'):
    print(element.tag, element.text)  # Print tag name and text of each 'item' element

# Find all elements with the tag 'item' regardless of their position in the document
for element in tree.xpath('//item'):
    print(element.tag, element.text)

# Find all 'item' elements that are direct children of the 'container' element
for element in tree.xpath('/container/item'):
    print(element.tag, element.text)

# Find all 'item' elements under 'container' using ElementPath
for element in tree.findall('.//container/item'):
    print(element.tag, element.text)

current_element = tree.find('.//item')

# Iterate over next siblings
while current_element is not None:
    print(current_element.tag)
    current_element = current_element.getnext()

# Reset current_element to some item for this example
current_element = tree.find('.//item')

# Iterate over previous siblings
while current_element is not None:
    print(current_element.tag)
    current_element = current_element.getprevious()

### gblxml

from lxml import etree
import xgbxml

parser=xgbxml.get_parser()  # default is gbXML version 6.01

tree=etree.parse('my_gbxml_file.xml', parser)
gbxml=tree.getroot()

### For reading gblxml

from lxml import etree
import xgbxml

parser=xgbxml.get_parser()  # default is gbXML version 6.01

tree=etree.parse('gbXMLStandard.xml', parser)
gbxml=tree.getroot()
buildings=gbxml.Campus.Buildings

print(buildings)
# prints "gbCollection(<Building (id="aim0013")>)"

print(type(buildings))
# prints "<class 'xgbxml.xgbxml.gbCollection'>"





    xsd_file = sys.argv[1]
    element_name = sys.argv[2]
    #code = generate_feature_class(xsd_file, element_name)
    #output_filename = f"{element_name}_Feature.py"
    #with open(output_filename, "w") as f:
    #    f.write(code)
    #print(f"Generated code written to {output_filename}")

