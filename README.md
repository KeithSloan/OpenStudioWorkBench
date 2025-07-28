# OpenStudio Workbench

## ( FreeCAD workbench to add facilities for OpenStudio & EnergyPlus )

This is ane experimental workbench looking to create valid input
for OpenStudio & EnergyPlus

Rename to BIM or BEM workbench ?


# IMPORTANT 

Due to an error by the developer in the original choice of tab name installation via the 
Addon Manager and using the standard manual installation results in the workbench being installed in different locations. If you have an installed version that is less than 0.2
then you need to unstall and then re install the workbench once the change in tab name has
been merged into the main FreeCAD.

## Installation

It can be installed via the [Addon Manager](https://github.com/FreeCAD/FreeCAD-addons) (from Tools menu)


## Alternative Installation

Clone into FreeCAD's Mod directory see https://wiki.freecadweb.org/Installing_more_workbenches

   * Change to FreeCAD Mod directory
   * git clone https://github.com/KeithSloan/OpenStudioWorkBench.git

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
                   
    * Sync GBxml - Properties ( to be developed )
      - Sync FC object Properties with GBxml structure

                   
## Import Functions

    * Import gbXML file
      - Currently 
          Group GBxsd - Just parsed from GBxml.xsd
          Group gbXML - Values have been set on import

      - Look at creating dictionary from GBxml.xsd
        or leave and goback to build FC Objects from preprocess.

      -ToDo
        Create FC Shapes for Geometry and check with imported data
        
    * Import ifc file
      - Import Ifc file using Maarten Visschers - ifc to gbXML converter
          https://github.com/MGVisschers/IFC-to-gbXML-converter
          Maintained by Bruno Postle
          https://github.com/brunopostle/IFC-to-gbXML-converter
          Current fork pull request to be made.
          https://github.com/KeithSloan/IFC-to-gbXML-converter

          On import should get a Frame prompt
          
          ![Screenshot] https://github.com/user-attachments/assets/64fe0bbd-6b72-4a1e-958b-c766655d218d

          Click Okay to convert Ifc to gbXML and import 

    * Branch gbXML2IDF

       submodule add https://github.com/KeithSloan/gbXML2IDF which is a fork of https://github.com/Udaragithub/gbXML2IDF

       Has facility to use external editor for 
         - IDF_template.IDF
         - IDF_Schedules.IDF
         - material_data.csv
         - space_data.csv

        ToDo
          - Create files baaed on gbXML source i.e. Avoid hand editing step 
              - Providing mapping gbXML materials to IDF Materials
              - Providing mapping gbXML Space to iDF Space
              
          - Run Energy Model
           

   ## Other Functions
   
    * Export GBxml - Export GBxml structure to gbxml file ( to be developed )

    * Import Weather - ToDo

## Info

Energy+.idd         # from Energy Plus - (Single file subdirectory ?)
SketchUpPlugin.xml  # SketchUpPluginPolicy.xml from Open Studio sketchup plus
