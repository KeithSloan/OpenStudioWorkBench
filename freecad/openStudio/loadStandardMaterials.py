def get_standard_material_names(lib_path):
    import openstudio

    translator = openstudio.osversion.VersionTranslator()
    path = openstudio.path(lib_path)
    loaded_model = translator.loadModel(path)
    if loaded_model.is_initialized():
        model = loaded_model.get()
        materials = model.getStandardOpaqueMaterials()
        return [(mat.nameString(), mat) for mat in materials]
    return []
# You’ll store the list of (name, material_object) for mapping later.

# Update the Qt UI to Support Both Options
# Replace plain QListWidget with a per-material mapping panel:

# Material Label
# QComboBox with options:
# Standard Materials (loaded from .osm)
# "Custom" option
# If "Custom" is selected:
# Show editable fields for thickness, etc.

# On Save — Store Result As One Of:
# "standard_material_name" → for library reference
# "custom" → with user-defined values

material_mapping = {
    "mat001": {
        "type": "standard",
        "name": "Concrete - Heavyweight"
    },
    "mat002": {
        "type": "custom",
        "properties": {
            "Thickness": 0.15,
            "Conductivity": 1.4,
            "Density": 2200,
            "Specific Heat": 900
        }
    }
}
