#!/usr/bin/env python
"""
Usage: python generate_feature.py <xsd_file> <element_name>

This script parses the given XSD file (using lxml), finds the element with the
specified name and its sub-elements, then outputs a Python file named
<element_name>_Feature.py. The generated code defines a class that, when attached
to a FreeCAD FeaturePython object, creates properties (mapping XSD types to
FreeCAD properties) and provides a Qt dialog (using PySide2) to edit those values.
"""

from lxml import etree
import sys

# Mapping of basic XSD types to FreeCAD property types.
XSD_TO_FC_MAP = {
    'string': 'App::PropertyString',
    'int': 'App::PropertyInteger',
    'integer': 'App::PropertyInteger',
    'float': 'App::PropertyFloat',
    'double': 'App::PropertyFloat',
    'decimal': 'App::PropertyFloat',
    'boolean': 'App::PropertyBool'
}

def resolve_xsd_type(custom_type, root, ns):
    """
    Attempt to resolve a custom XSD type to its base type.
    Looks up a global xs:simpleType with name == custom_type.
    Returns the base type in lowercase (e.g. "int") if found,
    otherwise returns custom_type in lowercase.
    """
    st = root.find(f".//xs:simpleType[@name='{custom_type}']", namespaces=ns)
    if st is not None:
        restriction = st.find("xs:restriction", namespaces=ns)
        if restriction is not None:
            base = restriction.get("base")
            if base:
                return base.split(':')[-1].strip().lower()
    return custom_type.lower()

def generate_feature_class(xsd_file, element_name):
    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    tree = etree.parse(xsd_file)
    root = tree.getroot()

    # Locate the target element by its name.
    elems = root.xpath(f".//xs:element[@name='{element_name}']", namespaces=ns)
    if not elems:
        print(f"Element '{element_name}' not found in {xsd_file}")
        sys.exit(1)
    elem = elems[0]

    # Look for the complexType inside the element.
    ct = elem.find('xs:complexType', namespaces=ns)
    print(f"ComplexType {elem.find('xs:complexType', namespaces=ns)}")
    if (elem.find('xs:complexType', namespaces=ns)) is None:
        print(f"Element '{element_name}' does not have a complexType definition.")
        sys.exit(1)
    print(f"Complex Type {ct}")
    sc = ct.find('xs:SimpleContent', namespaces=ns)
    if sc is not None:
        scExt = sc.find('xs:Extension', namespaces=ns)
        if scExt is not None:
            if scExt is not None:
                scBase = scExt.get('base')
                print(f"scBase {scBase}")
            


    # Find sub-elements (assumed to be in a sequence)
    subelements = (elem.find('xs:complexType', namespaces=ns)).xpath(".//xs:element", namespaces=ns)
    properties = []  # Each property is (name, fc_property_type, enumeration_values)

    print(f"subelemnts {subelements}")
    for sub in subelements:
        # Try to get the 'name' attribute; if not available, try 'ref'
        prop_name = sub.get('name') or sub.get('ref')
        if not prop_name:
            continue

        # Determine the XSD type.
        xsd_type = sub.get('type')
        enum_values = None

        if xsd_type:
            # Remove namespace prefix if any, strip whitespace, and lower-case the type.
            xsd_type = xsd_type.split(':')[-1].strip().lower()
            # If the type is not in our mapping, try to resolve it.
            if xsd_type not in XSD_TO_FC_MAP:
                xsd_type = resolve_xsd_type(xsd_type, root, ns)
        else:
            # Look for an inline simpleType with restrictions (possibly enumerations)
            simpleType = sub.find('xs:simpleType', namespaces=ns)
            if simpleType is not None:
                restriction = simpleType.find('xs:restriction', namespaces=ns)
                if restriction is not None:
                    base = restriction.get('base')
                    if base:
                        xsd_type = base.split(':')[-1].strip().lower()
                    enums = restriction.findall('xs:enumeration', namespaces=ns)
                    if enums:
                        enum_values = [e.get('value') for e in enums]
            # Default to string if no type was found.
            if not xsd_type:
                xsd_type = 'string'
        
        # Debug: Uncomment the following line to print detected types.
        print(f"Detected property '{prop_name}' with XSD type '{xsd_type}' and enum_values={enum_values}")
        
        # Determine FreeCAD property type.
        if enum_values:
            fc_prop_type = 'App::PropertyEnumeration'
        else:
            fc_prop_type = XSD_TO_FC_MAP.get(xsd_type, 'App::PropertyString')

        properties.append((prop_name, fc_prop_type, enum_values))

    # Build the generated Python code as a list of lines.
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
            # We assume a custom method to set enumeration values exists.
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

