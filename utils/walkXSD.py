#!/usr/bin/python

#
# Go through an XSD, listing attributes and entities
#

import argparse
from lxml import etree

def do_element(elmnt):
     nam = elmnt.get('name')
     if len(elmnt) != 0:
        # Entity
        print("Entity: ", nam, " Type: ",elmnt.get('type','None'))
     else:
        # Attribute
        if nam != None:
             print("Attrib: ", nam, " Type: ",elmnt.get('type','None') )

def main():
    parser = argparse.ArgumentParser(prog='test')
    parser.add_argument('-d',action='store_true',help='debugging')

    parser.add_argument('infile')
    args = parser.parse_args()

    xsd_prs = etree.XMLParser(remove_blank_text=True)
    xsd_doc = etree.parse(args.infile, xsd_prs)
    xsd_doc.xinclude()

    walkall = xsd_doc.getiterator()
    for elmnt in walkall:
        do_element(elmnt)

if __name__ == "__main__":
    main()
