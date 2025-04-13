import FreeCAD

from freecad.openStudio.Campus_Generated  import CampusGeneratedClass

class CampusFeatureClass(CampusGeneratedClass):
	def __init__(self, obj):
		super().__init__(obj)
		print("Campus Feature")

	def create_from_ifc_obj(self, obj):
		pass

	def create_from_arch_obj(self, obj):
		pass

	def sync(self):
		pass

	def export(self):
		pass

	#def create_feature_object(self, obj_name):

	#	obj = FreeCAD.ActiveDocument.addObject("App::FeaturePython", obj_name)
	#	CampusFeature(obj)
	#	#FreeCAD.ActiveDocument.recompute()
	#	return obj
