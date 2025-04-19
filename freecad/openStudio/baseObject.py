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

class baseObjectClass:
    def __init__(self, obj, srcObj):
        """Init"""
        import FreeCAD as App

        self.possibleProp = []
        self.currentProp = []
        print(f"Set LinkedObj {srcObj}")
        obj.addProperty("App::PropertyLink", "LinkedObj", "Base", "Initial Source Object" \
            ).LinkedObj = srcObj
        # No Proxy for App::Group ?
        #obj.Proxy = self
    
    def addPossibleProp(self, prop):
        if prop not in self.possibleProp:
            self.possibleProp.append(prop)
            
    def addCurrentProp(self, prop):
        if prop not in self.possibleProp:
            raise ValueError("Invalid Prop")
        self.currentProp.append(prop)

    def updateLinkedProperties(self):
        if self.linkedObject is not None:
            for p in self.linkedObject.PropertiesList:
                print(f"Check and Update {p}")
                try:
                    self.p = self.linkedObject.p
                except:
                    # Check p in AlternateNameDict
                    pass

    def __getstate__(self):
        """
        When saving the document this object gets stored using Python's
		json module.
		Since we have some un-serializable parts here -- the Coin stuff --
		we must define this method
		to return a tuple of all serializable objects or None.
        """
        if hasattr(self, "Type"):  # If not saved just return
            return {"type": self.Type}
        else:
            	pass

    def __setstate__(self, arg):
        """
        When restoring the serialized object from document we have the
		chance to set some internals here.
		Since no data were serialized nothing needs to be done here.
        """
		# Handle bug in FreeCAD 0.21.2 handling of json
		#print(f"setstate : arg {arg} type {type(arg)}")
        if arg is not None and arg != {}:
            if 'type' in arg:
                self.Type = arg["type"]
            else: #elif 'Type' in arg:
                self.Type = arg["Type"]
            #print(self.Type)