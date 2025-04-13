import FreeCAD
from PySide2 import QtWidgets

from freecad.openStudio.Campus_Generated  import CampusGenerated

class CampusFeature(CampusGenerated):
    def __init__(self, obj):
		super().__init__(obj)
		pass
	

	def create_from_ifc_obj(self, obj):
		pass

	def create_from_arch_obj(self, obj):
		pass

	def sync(self):
		pass

	def export(self):
		pass

	def create_feature_object(self, obj_name):
		obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", obj_name)
		CampusFeature(obj)
		FreeCAD.ActiveDocument.recompute()
		return obj
