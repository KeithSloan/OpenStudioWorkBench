import FreeCAD
FreeCAD.addImportType("OpenStudio Sketch Plugin gbXML (*.gbXML)","freecad.openStudio.import_gbXML")
FreeCAD.addImportType("OpenStudio Sketch Plugin xml (*.xml)","freecad.openStudio.import_gbXML")
FreeCAD.addImportType("Convert gbXML to IDF (*.gbXML)","freecad.openStudio.convert_gbXML2IDF")
FreeCAD.addImportType("Convert gbXML to IDF (*.xml)","freecad.openStudio.convert_gbXML2IDF")
FreeCAD.addImportType("MGVisschers IFC to gbXML (*.ifc)","freecad.openStudio.import_IFC_gbXML")
FreeCAD.addExportType("OpenStudio Sketch Plugin gbXML (*.xml)","freecad.openStudio.export_gbXML")
