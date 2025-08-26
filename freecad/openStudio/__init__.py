import FreeCAD
FreeCAD.addImportType("OpenStudio Sketch Plugin gbXML (*.gbXML)","freecad.openStudio.import_gbXML")
FreeCAD.addImportType("OpenStudio Sketch Plugin xml (*.xml)","freecad.openStudio.import_gbXML")
FreeCAD.addImportType("MGVisschers IFC to gbXML (*.ifc)","freecad.openStudio.import_IFC_gbXML")
FreeCAD.addImportType("MGVisschers Convert IFC to gbXML (*.ifc)","freecad.openStudio.convert_IFC_gbXML")
FreeCAD.addExportType("OpenStudioWorkBench export to gbXML (*.gbXML)","freecad.openStudio.export_gbXML")
FreeCAD.addExportType("OpenStudioWorkBench export to gbXML (*.xml)","freecad.openStudio.export_gbXML")
FreeCAD.addExportType("OpenStudioWorkBench export IFC to gbXML (*.gbXML)","freecad.openStudio.export_ifc2gbXML")
FreeCAD.addExportType("OpenStudioWorkBench export IFC to gbXML (*.xml)","freecad.openStudio.export_ifc2gbXML")