import FreeCAD
import sys
from PySide2 import QtWidgets

def create_parameter_dialog(obj):
    """Create a Qt dialog to set parameters of a FeaturePython object."""
    class ParameterDialog(QtWidgets.QDialog):
        def __init__(self, obj):
            super().__init__()
            self.obj = obj
            self.setWindowTitle(f"Edit Parameters: {obj.Label}")
            layout = QtWidgets.QFormLayout()
            self.inputs = {}
            
            for prop in obj.PropertiesList:
                if prop != "ElementName":  # Skip the element name
                    value = getattr(obj, prop, "")
                    input_field = QtWidgets.QLineEdit(str(value))
                    self.inputs[prop] = input_field
                    layout.addRow(prop, input_field)
            
            self.ok_button = QtWidgets.QPushButton("OK")
            self.ok_button.clicked.connect(self.apply_changes)
            layout.addWidget(self.ok_button)
            
            self.setLayout(layout)
        
        def apply_changes(self):
            for prop, input_field in self.inputs.items():
                setattr(self.obj, prop, input_field.text())
            FreeCAD.ActiveDocument.recompute()
            self.accept()
    
    dialog = ParameterDialog(obj)
    dialog.exec_()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <feature_python_object_name>")
        sys.exit(1)
    
    obj_name = sys.argv[1]
    obj = FreeCAD.ActiveDocument.getObject(obj_name)
    if obj:
        create_parameter_dialog(obj)
    else:
        print(f"Object '{obj_name}' not found in the FreeCAD document.")

