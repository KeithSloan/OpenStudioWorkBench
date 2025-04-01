#!/usr/bin/env python
"""
Usage: python generate_feature.py <xsd_file> <element_name>

This script parses the given XSD file (using lxml) and finds the element with the
specified name. It handles both complex types with subelements and complex types with
simpleContent extensions. For simpleContent, it creates a property with the element’s
name (e.g. “Area”) for the base value (mapped from xsd:decimal to a float) and for attributes
(such as “unit”), it renames them (e.g. “unit” becomes “AreaType”) and maps to a FreeCAD enumeration.
The generated code is written to <element_name>_Feature.py.
"""

from lxml import etree
import sys

# Mapping of basic XSD types to FreeCAD property types.
# (FreeCAD doesn’t support a decimal property, so we map decimal to float)
XSD_TO_FC_MAP = {
    'string': 'App::PropertyString',
    'int': 'App::PropertyInteger',
    'integer': 'App::PropertyInteger',
    'float': 'App::PropertyFloat',
    'double': 'App::PropertyFloat',
    'decimal': 'App::PropertyFloat',
    'boolean': 'App::PropertyBool'
}

def resolve_xsd_type(custom_type, root):
    """
    Attempt to resolve a custom XSD type to its base type.
    Searches for a global simpleType with matching local-name.
    Returns the base type (lowercased) if found, otherwise returns custom_type in lowercase.
    """
    st = root.find(f".//*[local-name()='simpleType'][@name='{custom_type}']")
    if st is not None:
        restriction = st.find("*[local-name()='restriction']")
        if restriction is not None:
            base = restriction.get("base")
            if base:
                return base.split(':')[-1].strip().lower()
    return custom_type.lower()

def generate_feature_class(xsd_file, element_name):
    tree = etree.parse(xsd_file)
    root = tree.getroot()

    # Use XPath with local-name() to find the target element regardless of prefix.
    elems = root.xpath(f"//*[local-name()='element' and @name='{element_name}']")
    if not elems:
        print(f"Element '{element_name}' not found in {xsd_file}")
        sys.exit(1)
    elem = elems[0]
    
    properties = []  # List of tuples: (property_name, fc_property_type, enumeration_values)

    # Try to detect a simpleContent extension using XPath.
    ext_nodes = elem.xpath("./*[local-name()='complexType']/*[local-name()='simpleContent']/*[local-name()='extension']")
    if ext_nodes:
        extension = ext_nodes[0]
        # Process the base type.
        base = extension.get("base")
        if base:
            base_type = base.split(':')[-1].strip().lower()
            # For our purposes, treat 'decimal' as float.
            if base_type == "decimal":
                base_type = "float"
            if base_type not in XSD_TO_FC_MAP:
                base_type = resolve_xsd_type(base_type, root)
        else:
            base_type = 'string'
        fc_prop_type = XSD_TO_FC_MAP.get(base_type, 'App::PropertyString')
        # Use the element name as the property name.
        properties.append((element_name, fc_prop_type, None))
        
        # Process attributes within the extension.
        attr_nodes = extension.xpath("./*[local-name()='attribute']")
        for attr in attr_nodes:
            attr_name = attr.get("name")
            # Rename "unit" to "<ElementName>Type" (e.g. "AreaType")
            if attr_name == "unit":
                attr_prop_name = element_name + "Type"
            else:
                attr_prop_name = attr_name
            attr_type = attr.get("type")
            enum_values = None
            if attr_type:
                attr_type = attr_type.split(':')[-1].strip().lower()
                if attr_type not in XSD_TO_FC_MAP:
                    attr_type = resolve_xsd_type(attr_type, root)
            else:
                attr_type = 'string'
            # If the type ends with "enum", force an enumeration property.
            if attr_type.endswith("enum"):
                fc_prop_type_attr = "App::PropertyEnumeration"
            else:
                fc_prop_type_attr = XSD_TO_FC_MAP.get(attr_type, 'App::PropertyString')
            properties.append((attr_prop_name, fc_prop_type_attr, enum_values))
    else:
        # Fallback: process subelements in a sequence.
        subelements = elem.xpath(".//*[local-name()='element']")
        for sub in subelements:
            prop_name = sub.get('name') or sub.get('ref')
            if not prop_name:
                continue

            xsd_type = sub.get('type')
            enum_values = None

            if xsd_type:
                xsd_type = xsd_type.split(':')[-1].strip().lower()
                if xsd_type not in XSD_TO_FC_MAP:
                    xsd_type = resolve_xsd_type(xsd_type, root)
            else:
                simpleType = sub.find("*[local-name()='simpleType']")
                if simpleType is not None:
                    restriction = simpleType.find("*[local-name()='restriction']")
                    if restriction is not None:
                        base = restriction.get('base')
                        if base:
                            xsd_type = base.split(':')[-1].strip().lower()
                        enums = restriction.findall("*[local-name()='enumeration']")
                        if enums:
                            enum_values = [e.get('value') for e in enums]
                if not xsd_type:
                    xsd_type = 'string'
            
            if enum_values:
                fc_prop_type = 'App::PropertyEnumeration'
            else:
                fc_prop_type = XSD_TO_FC_MAP.get(xsd_type, 'App::PropertyString')
            properties.append((prop_name, fc_prop_type, enum_values))

    # For debugging: print detected properties.
    for prop in properties:
        print(f"Detected property '{prop[0]}' with XSD type mapping '{prop[1]}' and enum_values={prop[2]}")

    # Build the generated Python code.
    lines = []
    lines.append("import FreeCAD")
    lines.append("from PySide2 import QtWidgets")
    lines.append("")
    lines.append(f"class {element_name}Feature:")
    lines.append("    def __init__(self, obj):")
    lines.append("        # Set the element name property")
    lines.append("        obj.addProperty(\"App::PropertyString\", \"ElementName\", \"Base\", \"XSD Element Name\")")
    lines.append(f"        obj.ElementName = \"{element_name}\"")
    for prop_name, fc_prop_type, enum_values in properties:
        comment = f"Property for {prop_name}"
        if fc_prop_type == "App::PropertyEnumeration" and enum_values is not None:
            lines.append(f"        # {comment} (Enumeration: {', '.join(enum_values)})")
            lines.append(f"        obj.addProperty(\"{fc_prop_type}\", \"{prop_name}\", \"Base\", \"{prop_name}\")")
            lines.append(f"        obj.setPropertyEnumValues(\"{prop_name}\", {enum_values})")
        else:
            lines.append(f"        # {comment}")
            lines.append(f"        obj.addProperty(\"{fc_prop_type}\", \"{prop_name}\", \"Base\", \"{prop_name}\")")
    lines.append("        obj.Proxy = self")
    lines.append("")
    lines.append("    @staticmethod")
    lines.append("    def createDialog(obj):")
    lines.append("        class ParameterDialog(QtWidgets.QDialog):")
    lines.append("            def __init__(self, obj):")
    lines.append("                super().__init__()")
    lines.append("                self.obj = obj")
    lines.append("                self.setWindowTitle(f\"Edit Parameters: {obj.Label}\")")
    lines.append("                layout = QtWidgets.QFormLayout()")
    lines.append("                self.inputs = {}")
    lines.append("                for prop in obj.PropertiesList:")
    lines.append("                    if prop == \"ElementName\":")
    lines.append("                        continue")
    lines.append("                    value = getattr(obj, prop, \"\")")
    lines.append("                    prop_type = obj.getTypeIdOfProperty(prop)")
    lines.append("                    if prop_type in [\"App::PropertyFloat\", \"App::PropertyDistance\"]:")
    lines.append("                        input_field = QtWidgets.QDoubleSpinBox()")
    lines.append("                        input_field.setValue(float(value))")
    lines.append("                        input_field.setDecimals(6)")
    lines.append("                    elif prop_type == \"App::PropertyInteger\":")
    lines.append("                        input_field = QtWidgets.QSpinBox()")
    lines.append("                        input_field.setValue(int(value))")
    lines.append("                    elif prop_type == \"App::PropertyBool\":")
    lines.append("                        input_field = QtWidgets.QCheckBox()")
    lines.append("                        input_field.setChecked(bool(value))")
    lines.append("                    elif prop_type == \"App::PropertyEnumeration\":")
    lines.append("                        input_field = QtWidgets.QComboBox()")
    lines.append("                        input_field.addItems(obj.getEnumerationsOfProperty(prop))")
    lines.append("                        input_field.setCurrentText(str(value))")
    lines.append("                    else:")
    lines.append("                        input_field = QtWidgets.QLineEdit(str(value))")
    lines.append("                    self.inputs[prop] = input_field")
    lines.append("                    layout.addRow(prop, input_field)")
    lines.append("                ok_button = QtWidgets.QPushButton(\"OK\")")
    lines.append("                ok_button.clicked.connect(self.apply_changes)")
    lines.append("                layout.addWidget(ok_button)")
    lines.append("                self.setLayout(layout)")
    lines.append("")
    lines.append("            def apply_changes(self):")
    lines.append("                for prop, input_field in self.inputs.items():")
    lines.append("                    prop_type = self.obj.getTypeIdOfProperty(prop)")
    lines.append("                    if prop_type in [\"App::PropertyFloat\", \"App::PropertyDistance\"]:")
    lines.append("                        setattr(self.obj, prop, input_field.value())")
    lines.append("                    elif prop_type == \"App::PropertyInteger\":")
    lines.append("                        setattr(self.obj, prop, input_field.value())")
    lines.append("                    elif prop_type == \"App::PropertyBool\":")
    lines.append("                        setattr(self.obj, prop, input_field.isChecked())")
    lines.append("                    elif prop_type == \"App::PropertyEnumeration\":")
    lines.append("                        setattr(self.obj, prop, input_field.currentText())")
    lines.append("                    else:")
    lines.append("                        setattr(self.obj, prop, input_field.text())")
    lines.append("                FreeCAD.ActiveDocument.recompute()")
    lines.append("                self.accept()")
    lines.append("        dialog = ParameterDialog(obj)")
    lines.append("        dialog.exec_()")
    lines.append("")
    lines.append("def create_feature_object(obj_name):")
    lines.append("    obj = FreeCAD.ActiveDocument.addObject(\"App::FeaturePython\", obj_name)")
    lines.append(f"    {element_name}Feature(obj)")
    lines.append("    FreeCAD.ActiveDocument.recompute()")
    lines.append("    return obj")
    
    generated_code = "\n".join(lines)
    return generated_code

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_feature.py <xsd_file> <element_name>")
        sys.exit(1)
    
    xsd_file = sys.argv[1]
    element_name = sys.argv[2]
    code = generate_feature_class(xsd_file, element_name)
    output_filename = f"{element_name}_Feature.py"
    with open(output_filename, "w") as f:
        f.write(code)
    print(f"Generated code written to {output_filename}")
