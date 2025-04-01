# import packages
from xgbxml import get_parser
from xgbxml import geometry_functions, gbxml_functions, render_functions from lxml import etree
import matplotlib.pyplot as plt
import copy
import math
from uuid import uuid4

# uses xgbxml to generate a lxml parser to read gbXML version 0.37
parser=get_parser(version='0.37')

# opens the file using the custom lxml parser
fp='23-013 WH Swan Hill_Mass_23-08-30.xml' tree=etree.parse(fp,parser) gbxml=tree.getroot()
# renders the Campus element
ax=gbxml.Campus.render()
ax.figure.set_size_inches(8, 8)
ax.set_title(fp)
plt.show()

#
<Surface xmlns="http://www.gbxml.org/schema" id="f20a7dbc-94d5-43ee-bf64-748c3e61658b">
  <AdjacentSpaceId spaceIdRef="aim2197"/>
  <PlanarGeometry>
    <PolyLoop>
      <CartesianPoint>
        <Coordinate>72.2287629</Coordinate>
        <Coordinate>-0.3141381</Coordinate>
        <Coordinate>0.0</Coordinate>
      </CartesianPoint>
      <CartesianPoint>
        <Coordinate>72.2287629</Coordinate>
        <Coordinate>-0.4999998</Coordinate>
        <Coordinate>0.0</Coordinate>
      </CartesianPoint>
      <CartesianPoint>
        <Coordinate>72.0986211</Coordinate>
        <Coordinate>-0.4999998</Coordinate>
        <Coordinate>0.0</Coordinate>
      </CartesianPoint>
    </PolyLoop>
  </PlanarGeometry>
</Surface>

<Surface xmlns="http://www.gbxml.org/schema" id="407a76aa-3287-4b5e-ac62-0440fb629f72">
  <AdjacentSpaceId spaceIdRef="aim2553"/>
  <AdjacentSpaceId spaceIdRef="aim7413"/>
  <PlanarGeometry>
    <PolyLoop>
      <CartesianPoint>
        <Coordinate>80.2291667</Coordinate>
        <Coordinate>14.5625</Coordinate>
        <Coordinate>10.0</Coordinate>
      </CartesianPoint>
      <CartesianPoint>
        <Coordinate>80.0208333</Coordinate>
        <Coordinate>14.5625</Coordinate>
        <Coordinate>10.0</Coordinate>
      </CartesianPoint>
      <CartesianPoint>
        <Coordinate>80.0208333</Coordinate>
        <Coordinate>16.020833</Coordinate>
        <Coordinate>10.0</Coordinate>
      </CartesianPoint>
      <CartesianPoint>
        <Coordinate>80.2291667</Coordinate>
        <Coordinate>16.020833</Coordinate>
        <Coordinate>10.0</Coordinate>
      </CartesianPoint>
    </PolyLoop>

# Recheck gaps
# identify gaps in surfaces of building
gaps=gbxml.Campus.Building.get_gaps_in_surfaces()
gaps

# writes the gbXML etree to a local file
tree.write('23-013 WH Swan Hill_Mass_23-08-30-UPDATED.xml', pretty_print=True)


### Question: For my university thesis work I have to create a lot of different GBXML models (around 18000). No way I can do that without code. This is what I came up with (I attached only a part of it; FloorR, WallsR, RoofR are lists to set R value of corresponding elements):

### Setting Energy Analysis parameters ###

opt=Analysis.EnergyAnalysisDetailModelOptions()
opt.EnergyModelType=Analysis.EnergyModelType.BuildingElement
opt.ExportMullions=False
opt.IncludeShadingSurfaces=False
opt.SimplifyCurtainSystems=True
opt.Tier=Analysis.EnergyAnalysisDetailModelTier.SecondLevelBoundaries

### loop over all R-value combinations and create models ###

t=Transaction(doc,"R change")
c=Transaction(doc,"model creation")

for i in range(len(FloorR)):
  for j in range(len(WallsR)):
    for k in range(len(RoofR)):
    t.Start()
    Floor.Set(FloorR[i]/0.3048)  #R-value change for floor
    Wall.Set(WallsR[j]/0.3048)#R-value change for Walls
    Roof.Set(RoofR[k]/0.3048)#R-value change for roof
    t.Commit()
    t.Dispose()

    c.Start()
    model=Analysis.EnergyAnalysisDetailModel.Create(doc, opt)
    model.TransformModel()
    GBopt=GBXMLExportOptions()
    GBopt.ExportEnergyModelType=ExportEnergyModelType.BuildingElement
    doc.Export("C:\Users\Миша\Desktop\ASD","0"+","+str(0.2/FloorR[i])+","+str(0.3/WallsR[j])+","+str(0.3/RoofR[k]), GBopt)
    c.Commit()

###
EnergyAnalysisDetailModelOptions.ExportMullions = False

  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  AttributeError: static property 'ExportMullions' of 'EnergyAnalysisDetailModelOptions' 
  can only be assigned to through a type, not an instance
###

#Answer: A nice example of Python EnergyAnalysisDetailModelOptions administration is discussed in the export of multiple gbXML models.

The relevant code snippet is this:

### Setting Energy Analysis parameters ###

opt=Analysis.EnergyAnalysisDetailModelOptions()
opt.EnergyModelType=Analysis.EnergyModelType.BuildingElement
opt.ExportMullions=False
opt.IncludeShadingSurfaces=False
opt.SimplifyCurtainSystems=True
opt.Tier=Analysis.EnergyAnalysisDetailModelTier.SecondLevelBoundaries