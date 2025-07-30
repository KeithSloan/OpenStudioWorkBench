# Deliverables

# Basic OpenStudio .osm Material Library File
# Includes common materials like:
# Concrete (light/heavy)
# Insulation
# Gypsum
# Brick
# Wood
# Glass (optional)

# FreeCAD Qt Dialog (MaterialMapperDialog)
# Lists gbXML materials
# Allows mapping to:
# Standard material from .osm
# Or Custom material (fields: Thickness, Conductivity, Density, Cp)
# "Save" button stores the mapping
# Code to Load .osm Material Library
# Returns a list of (name, object) pairs for use in the UI
# Code to Generate OpenStudio Materials from Mapping
# Clones standard material or creates custom one

#  How This Will Work in Your FreeCAD Workbench

# gbxml_materials = [{"id": "mat001", "name": "Concrete"}, ...] is passed to the dialog.
# User sees each material and chooses standard/custom.
# material_mapping = dialog.get_mapping() returns the final dict.
# You use this mapping to build materials in OpenStudio.

Sample .osm Library of Standard Materials

A minimal OpenStudio material library containing common opaque materials:

Concrete (Lightweight)
Concrete (Heavyweight)
Brick – Clay
Gypsum Board – Plaster
Wood (Softwood)
Insulation (Fiberglass)
Glass – Clear
You can use this .osm as a "standards library" to load into your FreeCAD plugin.


