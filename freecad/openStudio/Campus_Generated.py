import FreeCAD
from PySide2 import QtWidgets

from freecad.openStudio import baseObject

class CampusGenerated(baseObject):
    def __init__(self, obj):
		super().__init__(obj)
		# Set the element name property
		obj.addProperty("App::PropertyString", "ElementName", "Base", "XSD Element Name")
		obj.ElementName = "Campus"
		# Property for Name
		obj.addProperty("App::PropertyString", "Name", "Base", "Name")
		# Property for Description
		obj.addProperty("App::PropertyString", "Description", "Base", "Description")
		# Property for Location
		obj.addProperty("App::PropertyString", "Location", "Base", "Location")
		# Property for Building
		obj.addProperty("App::PropertyString", "Building", "Base", "Building")
		# Property for Surface
		obj.addProperty("App::PropertyString", "Surface", "Base", "Surface")
		# Property for YearModeled
		obj.addProperty("App::PropertyString", "YearModeled", "Base", "YearModeled")
		# Property for DaylightSavings
		obj.addProperty("App::PropertyString", "DaylightSavings", "Base", "DaylightSavings")
		# Property for Life
		obj.addProperty("App::PropertyString", "Life", "Base", "Life")
		# Property for AltEnergySource
		obj.addProperty("App::PropertyString", "AltEnergySource", "Base", "AltEnergySource")
		# Property for ShellGeometry
		obj.addProperty("App::PropertyString", "ShellGeometry", "Base", "ShellGeometry")
		# Property for Vegetation
		obj.addProperty("App::PropertyString", "Vegetation", "Base", "Vegetation")
		# Property for Transportation
		obj.addProperty("App::PropertyString", "Transportation", "Base", "Transportation")
        # Property for MeterId
		obj.addProperty("App::PropertyString", "MeterId", "Base", "MeterId")
        # Property for ExtEquipId
		obj.addProperty("App::PropertyString", "ExtEquipId", "Base", "ExtEquipId")
		# Property for Lighting
		obj.addProperty("App::PropertyString", "Lighting", "Base", "Lighting")
		# Property for LightControlId
		obj.addProperty("App::PropertyString", "LightControlId", "Base", "LightControlId")
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


