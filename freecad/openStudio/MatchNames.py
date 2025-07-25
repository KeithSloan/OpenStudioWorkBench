# Match CSV Names to Standard OSM Materials

standard_materials = load_standard_materials("StandardMaterials.osm")
std_names = [name.lower() for name, _ in standard_materials]

from difflib import get_close_matches

def match_material_to_library(material_name, std_names):
    matches = get_close_matches(material_name.lower(), std_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

csv_materials = load_csv_materials("material_data.csv")

mapping = {}

for mat in csv_materials:
    best_match = match_material_to_library(mat["name"], std_names)
    if best_match:
        mapping[mat["id"]] = {"type": "standard", "name": best_match}
    else:
        # Fallback to prompt user later for custom values
        mapping[mat["id"]] = {
            "type": "custom",
            "properties": {
                "Thickness": None,
                "Conductivity": None,
                "Density": None,
                "Specific Heat": None
            }
        }

