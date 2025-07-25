# Right after surface.setSpace(space):
if "windows" in surface_data:
    for window_data in surface_data["windows"]:
        win_pts = openstudio.Point3dVector()
        for x, y, z in window_data["vertices"]:
            win_pts.append(openstudio.Point3d(x, y, z))

        window = openstudio.model.SubSurface(win_pts, model)
        window.setSurface(surface)
        window.setSubSurfaceType("FixedWindow")  # or "OperableWindow"
