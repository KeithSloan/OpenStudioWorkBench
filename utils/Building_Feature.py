import FreeCAD
from PySide2 import QtWidgets

class BuildingFeature:
    def __init__(self, obj):
        # Set the element name property
        obj.addProperty("App::PropertyString", "ElementName", "Base", "XSD Element Name")
        obj.ElementName = "Building"
        # Property for Name
        obj.addProperty("App::PropertyString", "Name", "Base", "Name")
        # Property for Description
        obj.addProperty("App::PropertyString", "Description", "Base", "Description")
        # Property for StreetAddress
        obj.addProperty("App::PropertyString", "StreetAddress", "Base", "StreetAddress")
        # Property for Area
        obj.addProperty("App::PropertyString", "Area", "Base", "Area")
        # Property for Space
        obj.addProperty("App::PropertyString", "Space", "Base", "Space")
        # Property for AverageNumberOfFloors
        obj.addProperty("App::PropertyString", "AverageNumberOfFloors", "Base", "AverageNumberOfFloors")
        # Property for InfiltrationFlow
        obj.addProperty("App::PropertyString", "InfiltrationFlow", "Base", "InfiltrationFlow")
        # Property for ShellGeometry
        obj.addProperty("App::PropertyString", "ShellGeometry", "Base", "ShellGeometry")
        # Property for SpaceBoundary
        obj.addProperty("App::PropertyString", "SpaceBoundary", "Base", "SpaceBoundary")
        # Property for Lighting
        obj.addProperty("App::PropertyString", "Lighting", "Base", "Lighting")
        # Property for IntEquipId
        obj.addProperty("App::PropertyString", "IntEquipId", "Base", "IntEquipId")
        # Property for MeterId
        obj.addProperty("App::PropertyString", "MeterId", "Base", "MeterId")
        # Property for PeakDomesticHotWaterFlow
        obj.addProperty("App::PropertyString", "PeakDomesticHotWaterFlow", "Base", "PeakDomesticHotWaterFlow")
        # Property for BuildingStorey
        obj.addProperty("App::PropertyString", "BuildingStorey", "Base", "BuildingStorey")
        obj.Proxy = self

    @staticmethod
    def createDialog(obj):
        class ParameterDialog(QtWidgets.QDialog):
            def __init__(self, obj):
                super().__init__()
                self.obj = obj
                self.setWindowTitle(f"Edit Parameters: {obj.Label}")
                layout = QtWidgets.QFormLayout()
                self.inputs = {}
                for prop in obj.PropertiesList:
                    if prop == "ElementName":
                        continue
                    value = getattr(obj, prop, "")
                    prop_type = obj.getTypeIdOfProperty(prop)
                    if prop_type in ["App::PropertyFloat", "App::PropertyDistance"]:
                        input_field = QtWidgets.QDoubleSpinBox()
                        input_field.setValue(float(value))
                        input_field.setDecimals(6)
                    elif prop_type == "App::PropertyInteger":
                        input_field = QtWidgets.QSpinBox()
                        input_field.setValue(int(value))
                    elif prop_type == "App::PropertyBool":
                        input_field = QtWidgets.QCheckBox()
                        input_field.setChecked(bool(value))
                    elif prop_type == "App::PropertyEnumeration":
                        input_field = QtWidgets.QComboBox()
                        input_field.addItems(obj.getEnumerationsOfProperty(prop))
                        input_field.setCurrentText(str(value))
                    else:
                        input_field = QtWidgets.QLineEdit(str(value))
                    self.inputs[prop] = input_field
                    layout.addRow(prop, input_field)
                ok_button = QtWidgets.QPushButton("OK")
                ok_button.clicked.connect(self.apply_changes)
                layout.addWidget(ok_button)
                self.setLayout(layout)

            def apply_changes(self):
                for prop, input_field in self.inputs.items():
                    prop_type = self.obj.getTypeIdOfProperty(prop)
                    if prop_type in ["App::PropertyFloat", "App::PropertyDistance"]:
                        setattr(self.obj, prop, input_field.value())
                    elif prop_type == "App::PropertyInteger":
                        setattr(self.obj, prop, input_field.value())
                    elif prop_type == "App::PropertyBool":
                        setattr(self.obj, prop, input_field.isChecked())
                    elif prop_type == "App::PropertyEnumeration":
                        setattr(self.obj, prop, input_field.currentText())
                    else:
                        setattr(self.obj, prop, input_field.text())
                FreeCAD.ActiveDocument.recompute()
                self.accept()
        dialog = ParameterDialog(obj)
        dialog.exec_()

def create_feature_object(obj_name):
    obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", obj_name)
    BuildingFeature(obj)
    FreeCAD.ActiveDocument.recompute()
    return obj