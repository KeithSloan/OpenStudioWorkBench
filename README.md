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

## Gui Icons

    * Build GBxml Group Structure ( For testing )
      - Create GBxml structure from hard coded Element - Element depends on Branch
          - Branch Cost

    * Add GBxml - Properties ( under development )
      - Select FC object, create GBxml structure and set property values

    * Sync GBxml - Properties ( to be developed )
      - Sync FC object Properties with GBxml structure

    * Export GGxml - Export GBxml structure to gbxml file ( to be developed )


## Info

Energy+.idd         # from Energy Plus - (Single file subdirectory ?)
SketchUpPlugin.xml  # SketchUpPluginPolicy.xml from Open Studio sketchup plus
