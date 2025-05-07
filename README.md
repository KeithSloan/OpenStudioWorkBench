# OpenStudio Workbench

## ( FreeCAD workbench to add facilities for OpenStudio & EnergyPlus )

This is ane experimental workbench looking to create valid input
for OpenStudio & EnergyPlus

Rename to BIM or BEM workbench ?

## Installation

It can be installed via the [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons) (from Tools menu)


## Alternative Installation

Clone into FreeCAD's Mod directory see https://wiki.freecadweb.org/Installing_more_workbenches

   * Change to FreeCAD Mod directory
   * **git clone https://github.com/KeithSloan/OpenStudioWorkBench.git

* Start/Restart FreeCAD

Investingating creating the data as per OpenStudio's Skectcher plug
and gbxml.

## FreeCAD setting
  Set the FreeCAD Preference for Document - Allow duplicate object labels in one document

## Gui Icons

    * Build GBxml Group Structure ( For testing )
      - Create GBxml structure from GBxml.xsd  : Elements - hard coded - Element depends on Branch
          - Branches
             * Cost
             * LighteningSystem
             * MinFlow

    * Add GBxml - Properties ( under development )
      - Select FC object, create GBxml structure and set some property values
      - Currently Implemented
          * Select BMI Site
              - Creates GbXML structure
                   - Campus
                   - Building
                   - Building Storey

    * Import gbXML file
      - Currently 
          * need to eemove first xml line ( Need to fix )
          * Just processes top level
          * Need to fix setvaklues
          * Look at Grouping items

    * Sync GBxml - Properties ( to be developed )
      - Sync FC object Properties with GBxml structure

    * Export GBxml - Export GBxml structure to gbxml file ( to be developed )

    * Import Weather - ToDo

## Info

Energy+.idd         # from Energy Plus - (Single file subdirectory ?)
SketchUpPlugin.xml  # SketchUpPluginPolicy.xml from Open Studio sketchup plus
