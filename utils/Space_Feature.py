import FreeCAD
from PySide2 import QtWidgets

class SpaceFeature:
    def __init__(self, obj):
        # Set the element name property
        obj.addProperty("App::PropertyString", "ElementName", "Base", "XSD Element Name")
        obj.ElementName = "Space"
        # Property for Name
        obj.addProperty("App::PropertyString", "Name", "Base", "Name")
        # Property for Description
        obj.addProperty("App::PropertyString", "Description", "Base", "Description")
        # Property for Lighting
        obj.addProperty("App::PropertyString", "Lighting", "Base", "Lighting")
        # Property for LightingControl
        obj.addProperty("App::PropertyString", "LightingControl", "Base", "LightingControl")
        # Property for InfiltrationFlow
        obj.addProperty("App::PropertyString", "InfiltrationFlow", "Base", "InfiltrationFlow")
        # Property for PeopleNumber
        obj.addProperty("App::PropertyString", "PeopleNumber", "Base", "PeopleNumber")
        # Property for PeopleHeatGain
        obj.addProperty("App::PropertyString", "PeopleHeatGain", "Base", "PeopleHeatGain")
        # Property for LightPowerPerArea
        obj.addProperty("App::PropertyString", "LightPowerPerArea", "Base", "LightPowerPerArea")
        # Property for EquipPowerPerArea
        obj.addProperty("App::PropertyString", "EquipPowerPerArea", "Base", "EquipPowerPerArea")
        # Property for AirChangesPerHour
        obj.addProperty("App::PropertyString", "AirChangesPerHour", "Base", "AirChangesPerHour")
        # Property for Area
        obj.addProperty("App::PropertyString", "Area", "Base", "Area")
        # Property for Temperature
        obj.addProperty("App::PropertyString", "Temperature", "Base", "Temperature")
        # Property for Volume
        obj.addProperty("App::PropertyString", "Volume", "Base", "Volume")
        # Property for PlanarGeometry
        obj.addProperty("App::PropertyString", "PlanarGeometry", "Base", "PlanarGeometry")
        # Property for ShellGeometry
        obj.addProperty("App::PropertyString", "ShellGeometry", "Base", "ShellGeometry")
        # Property for AirLoopId
        obj.addProperty("App::PropertyString", "AirLoopId", "Base", "AirLoopId")
        # Property for HydronicLoopId
        obj.addProperty("App::PropertyString", "HydronicLoopId", "Base", "HydronicLoopId")
        # Property for MeterId
        obj.addProperty("App::PropertyString", "MeterId", "Base", "MeterId")
        # Property for IntEquipId
        obj.addProperty("App::PropertyString", "IntEquipId", "Base", "IntEquipId")
        # Property for AirLoopEquipmentId
        obj.addProperty("App::PropertyString", "AirLoopEquipmentId", "Base", "AirLoopEquipmentId")
        # Property for HydronicLoopEquipmentId
        obj.addProperty("App::PropertyString", "HydronicLoopEquipmentId", "Base", "HydronicLoopEquipmentId")
        # Property for CADObjectId
        obj.addProperty("App::PropertyString", "CADObjectId", "Base", "CADObjectId")
        # Property for TypeCode
        obj.addProperty("App::PropertyString", "TypeCode", "Base", "TypeCode")
        # Property for SpaceBoundary
        obj.addProperty("App::PropertyString", "SpaceBoundary", "Base", "SpaceBoundary")
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
    SpaceFeature(obj)
    FreeCAD.ActiveDocument.recompute()
    return obj