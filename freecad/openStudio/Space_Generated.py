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
from freecad.openStudio.baseObject import baseObject

class SpaceGenerated(baseObject):
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
