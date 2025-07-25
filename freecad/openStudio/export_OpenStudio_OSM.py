import openstudio

def create_openstudio_model_from_gbxml(zones_data, output_dir="output"):
    model = openstudio.model.Model()

    # --- 🧱 Create Default Constructions ---
    construction_set = openstudio.model.DefaultConstructionSet(model)
    model.getBuilding().setDefaultConstructionSet(construction_set)

    material = openstudio.model.StandardOpaqueMaterial(model, "MediumRough", "Concrete", 0.2, 1.4, 2200, 900)
    wall_construction = openstudio.model.Construction(model)
    wall_construction.insertLayer(0, material)
    surface_constructions = openstudio.model.DefaultSurfaceConstructions(model)
    surface_constructions.setWallConstruction(wall_construction)
    construction_set.setDefaultExteriorSurfaceConstructions(surface_constructions)

    # --- ⏰ Create Default Schedules ---
    schedule_ruleset = openstudio.model.ScheduleRuleset(model, 1.0)
    schedule_ruleset.setName("Always On")

    # --- 🔥 Internal Load Definitions ---
    people_def = openstudio.model.PeopleDefinition(model)
    people_def.setName("People Def")
    people_def.setPeoplePerFloorArea(0.1)

    lights_def = openstudio.model.LightsDefinition(model)
    lights_def.setName("Lights Def")
    lights_def.setWattsperSpaceFloorArea(10)

    equipment_def = openstudio.model.ElectricEquipmentDefinition(model)
    equipment_def.setName("Equip Def")
    equipment_def.setWattsperSpaceFloorArea(8)

    # --- ♻️ Loop Through Zones ---
    for zone_data in zones_data:
        # Create Thermal Zone and Space
        thermal_zone = openstudio.model.ThermalZone(model)
        thermal_zone.setName(zone_data["name"])

        space = openstudio.model.Space(model)
        space.setThermalZone(thermal_zone)
        space.setName(f"{zone_data['name']}_space")

        # Add Internal Loads
        people = openstudio.model.People(people_def)
        people.setSpace(space)
        people.setNumberofPeopleSchedule(schedule_ruleset)

        lights = openstudio.model.Lights(lights_def)
        lights.setSpace(space)
        lights.setSchedule(schedule_ruleset)

        equipment = openstudio.model.ElectricEquipment(equipment_def)
        equipment.setSpace(space)
        equipment.setSchedule(schedule_ruleset)

        # Create Surfaces
        for surface_data in zone_data["surfaces"]:
            pts = openstudio.Point3dVector()
            for x, y, z in surface_data["vertices"]:
                # Assume input in meters; convert from mm if needed
                pts.append(openstudio.Point3d(x, y, z))

            surface = openstudio.model.Surface(pts, model)
            surface.setSurfaceType(surface_data["type"])
            surface.setOutsideBoundaryCondition(surface_data["outside_boundary_condition"])
            surface.setSpace(space)

    # --- 🌬️ Add Ideal Air Loads ---
    for zone in model.getThermalZones():
        zone.setUseIdealAirLoads(True)

    # --- 💾 Save OSM & Translate to IDF ---
    osm_path = openstudio.path(f"{output_dir}/model.osm")
    model.save(osm_path, True)
    print(f"✅ OSM saved to: {osm_path}")

    translator = openstudio.energyplus.ForwardTranslator()
    idf = translator.translateModel(model)

    idf_path = openstudio.path(f"{output_dir}/model.idf")
    idf.save(idf_path, True)
    print(f"✅ IDF saved to: {idf_path}")

    return model

