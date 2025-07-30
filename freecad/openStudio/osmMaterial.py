# libpath ~/OpenAStudio/Materials.osm

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

def apply_material_mapping_to_model(mapping, standard_library, model):
    for mat_id, data in mapping.items():
        if data["type"] == "standard":
            name = data["name"]
            lib_material = next((m for n, m in standard_library if n == name), None)
            if lib_material:
                model_material = lib_material.clone(model).to_StandardOpaqueMaterial().get()
                print(f"✔ Imported standard material: {name}")
        elif data["type"] == "custom":
            props = data["properties"]
            mat = openstudio.model.StandardOpaqueMaterial(model)
            mat.setName(f"Custom_{mat_id}")
            mat.setThickness(props["Thickness"])
            mat.setThermalConductivity(props["Conductivity"])
            mat.setDensity(props["Density"])
            mat.setSpecificHeat(props["Specific Heat"])
            print(f"✏️ Created custom material for {mat_id}")


