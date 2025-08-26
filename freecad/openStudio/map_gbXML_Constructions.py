### Add Real Constructions from gbXML or OpenStudio Library

# Assuming gbXML materials/constructions are matched to names in OpenStudio’s library:

def load_construction_by_name(model, name):
    path = openstudio.path("/path/to/your/construction_library.osm")
    translator = openstudio.osversion.VersionTranslator()
    lib_model = translator.loadModel(path).get()

    for cons in lib_model.getConstructions():
        if cons.nameString() == name:
            return cons.clone(model).to_Construction().get()
    return None

# Apply to walls/roofs:
wall_construction = load_construction_by_name(model, "Steel Framed Wall R-13")
surface.setConstruction(wall_construction)

# Add Real HVAC System (e.g. Packaged Rooftop Unit)

# For now, let’s use HVAC Templates — this gives you working systems without full node-by-node modeling.

# Insert This After All Zones Are Create

from openstudio.model import addSystemType1

openstudio.model.addSystemType1(model)  # System Type 1 = Packaged Single Zone AC

