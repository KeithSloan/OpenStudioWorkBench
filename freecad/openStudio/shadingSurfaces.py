# Add Shading Surfaces (Context Geometry)

# FreeCAD geometry outside the thermal zones (trees, neighboring buildings) can become ShadingSurfaceGroup.

# Example:

shading_group = openstudio.model.ShadingSurfaceGroup(model)
shading_group.setName("ContextBuilding")

pts = openstudio.Point3dVector()
pts.append(openstudio.Point3d(15, 0, 0))
pts.append(openstudio.Point3d(20, 0, 0))
pts.append(openstudio.Point3d(20, 5, 10))
pts.append(openstudio.Point3d(15, 5, 10))

shading_surface = openstudio.model.ShadingSurface(pts, model)
shading_surface.setShadingSurfaceGroup(shading_group)

