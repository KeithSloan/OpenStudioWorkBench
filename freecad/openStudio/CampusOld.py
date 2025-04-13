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

class baseObject:
    def __init__(self, obj):
        """Init"""
        self.possibleProp = []
        self.currentProp = []
        self.linkedObject = None
    
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
                except e:
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

#class Campus(baseObject):
#    def __init__(self,  obj, id):
#        super().__init__()
        #obj.addProperty("App::PropertyFloat", "x", "GDMLBox", "Length x").x = x
        #obj.addProperty("App::PropertyFloat", "y", "GDMLBox", "Length y").y = y
        #obj.addProperty("App::PropertyFloat", "z", "GDMLBox", "Length z").z = z
        #obj.addProperty(
        #    "App::PropertyEnumeration", "lunit", "GDMLBox", "lunit"
        #obj.addProperty(
        #    "App::PropertyEnumeration", "material", "GDMLBox", "Material"
        #)
        #setMaterial(obj, material)
        #if FreeCAD.GuiUp:
        #    updateColour(obj, colour, material)
        #    # Suppress Placement - position & Rotation via parent App::Part
        #    # this makes Placement via Phyvol easier and allows copies etc

        # One change of FreeCAD changed PythonFeaturs use of Proxy so set Type in bothe
 #       self.Type = "Campus"
 #       self.id = id
 #       obj.Proxy = self
 #       obj.Proxy.Type = "Campus"

        #<Location>
        #<StationId IDType="WMO">53158_2004</StationId>
        #<ZipcodeOrPostalCode>00000</ZipcodeOrPostalCode>
        #<Longitude>-71.033</Longitude>
        #<Latitude>42.213</Latitude>
        #<Elevation>154</Elevation>
        #<CADModelAzimuth>0</CADModelAzimuth>
        #<Name>Boston, MA</Name>
        


class  Building(baseObject):
    def __init__(self, obj, buildingType, id):
        super().__init__()
        self.buildingType = buildingType
        self.id = id
        # One change of FreeCAD changed PythonFeaturs use of Proxy so set Type in bothe
        self.Type = "Building"
        obj.Proxy = self
        obj.Proxy.Type = "Campus"
        # If id is not passed use ufa?
        # <StreetAddress>Boston, MA</StreetAddress>
        #<Area>6664.153</Area>


class Space(baseObject):
    def __init__(self, obj, spaceType, zoneIdRef, lightScheduleIdRef):
        super().__init__()
        self.spaceType = spaceType
        self.zoneIdRef = zoneIdRef
        self.lightScheduleIdRef = lightScheduleIdRef
        #<PeopleNumber unit="NumberOfPeople">2.85822</PeopleNumber>
        #<PeopleHeatGain unit="BtuPerHourPerson" heatGainType="Total">0</PeopleHeatGain>
        #<PeopleHeatGain unit="BtuPerHourPerson" heatGainType="Latent">0</PeopleHeatGain>
        #<PeopleHeatGain unit="BtuPerHourPerson" heatGainType="Sensible">0</PeopleHeatGain>
        #<LightPowerPerArea unit="WattPerSquareFoot">1.1</LightPowerPerArea>
        #<EquipPowerPerArea unit="WattPerSquareFoot">0.54</EquipPowerPerArea>
        #
        #
        #
        # The following can change sp set on export
        #
        #<Area>404.9365</Area>
        #Area>404.9365</Area>
        #<Volume>4458.979</Volume>
