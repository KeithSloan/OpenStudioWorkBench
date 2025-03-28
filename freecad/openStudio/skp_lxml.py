# **************************************************************************
# *                                                                        *
# *   Copyright (c) 2025 Keith Sloan <keith@sloan-home.co.uk>              *
# *                                                                        *
# *                                                                        *
# *   This program is free software; you can redistribute it and/or modify *
# *   it under the terms of the GNU Lesser General Public License (LGPL)   *
# *   as published by the Free Software Foundation; either version 2 of    *
# *   the License, or (at your option) any later version.                  *
# *   for detail see the LICENCE text file.                                *
# *                                                                        *
# *   This program is distributed in the hope that it will be useful,      *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
# *   GNU Library General Public License for more details.                 *
# *                                                                        *
# *   You should have received a copy of the GNU Library General Public    *
# *   License along with this program; if not, write to the Free Software  *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
# *   USA                                                                  *
# *                                                                        *
# *   Acknowledgements :                                                   *
#                                                                          *
#    Takes as input a Volume Name, GDML file  and outputs                  *
#              a directory structure starting at the specified Volume Name *
#                                                                          *
#                                                                          *
#    python3 buildDirStruct.py <parms> <Volume> <gdml_file> <Out_dir>      *
#                                                                          *
#       parms for future use ( use 1 for now )                             *
#       Volume    : Name of Volume to be extracted                         *
#       gdml_file : Source GDML file                                       *
#       Out_dir   : Output Directory                                       *
#                                                                          *
#  Where each Volume, Assembly is created as a sub directory               *
#                                                                          *
#           volumeName.gdml                                                *
#           volumeName_define.xml                                          *
#           volumeName_materials.xml                                       *
#           volumeName_solids.xml                                          *
#           volumeName_struct.xml                                          *
#           volumeName_setup.xml                                           *
#           < sub Volumes/Assemblies >                                     *
#                                                                          *
############################################################################
import sys, os
from lxml import etree
import copy


if open.__module__ in ['__builtin__', 'io']:
    pythonopen = open # to distinguish python built-in open function from the one declared here

def export(exportList, filename):
    "called when FreeCAD exports a file"

    # process Objects
    print("\nStart OpenStudio Export skp xml 0.1\n")
    print("Open Output File")

class gdml_lxml() :
    def __init__(self, filename):
        try:
            from lxml import etree
            print('Running with lxml.etree\n')
            print(filename)
            parser = etree.XMLParser(resolve_entities=True)
            self.root = etree.parse(filename, parser=parser)

        except ImportError:
            try:
                import xml.etree.ElementTree as etree
                print("Rnning with etree.ElementTree (import limitations)\n")
                self.tree = etree.parse(filename)
                self.root = self.tree.getroot()
            except:
                print('No lxml or xml')

        self.define    = self.root.find('define')
        self.materials = self.root.find('materials')
        self.solids    = self.root.find('solids')
        self.structure = self.root.find('structure')
        #self.volAsmDict = {}  # Can have number of PhysVols that refer to same
        # Needs to be in VolAsm   
        self.VolAsmStructDict = {}

    def printElement(self, elem):
        import lxml.html as html
        print(html.tostring(elem))


    def printMaterials(self):
        import lxml.html as html
        print(html.tostring(self.materials))


    #def printMaterial(self, mat):
    #    import lxml.html as html
    #    print(html.tostring(mat))


    def printName(self, elem):
        name = elem.attrib.get('name')
        print(f"{elem} : {name}")


    #def checkVolAsmDict(self, name):
    #    # print(f"Check Vol Asm Dict {self.volAsmDict}")
    #    if name in self.volAsmDict.keys():
    #        return False        # No need to process
    #    return True             # NEED to process


    #def addVolAsmDict(self, name, elem):
    #    self.volAsmDict[name] = elem


    def addVolAsmStructDict(self, name, elem):
        self.VolAsmStructDict[name] = elem


    def getRawVolAsmStruct(self, vaname):
        newStruct = copy.deepcopy(self.structure)
        struct = newStruct.find(f"*[@name='{vaname}']")
        return struct


    def getVolAsmStruct(self, vaname):
        # Needs to be structure and sub volumes 
        # So cannot just use structure in source#
        print(f"VolAsmStructDict {self.VolAsmStructDict.keys()}")
        ret = self.VolAsmStructDict[vaname]
        if ret is not None:
            return ret
        else:
            print(f"{vaname} not found in Dict")    


    def getPosition(self, posName):
        return self.define.find(f"position[@name='{posName}']")


    def getRotation(self, rotName):
        return self.define.find(f"rotation[@name='{rotName}']")


    def getSolid(self, sname):
        self.solids = self.root.find('solids')
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        # self.printElement(self.solids)
        # return self.solids.find(f"*[@name='{sname}']")
        ret = self.solids.find(f"*[@name='{sname}']")
        print(f"getSolid : {self.solids} {len(self.solids)} {sname}")
        if ret is not None:
            self.printElement(ret)
        print(ret)
        return ret

    def getMaterials(self):
        return(self.materials)

#   No Longer used
#    def processElement(self, volAsm, elem):
#        print(f"Process Element : {elem}")
#        elemXml = self.materials.find(f"*[@name='{elem}']")
#        if elemXml is not None:
#            # <- make a deep copy of the found elemen
#            newelemXml = copy.deepcopy(elemXml)
#            print(f"Element : {elemXml.get('name')}")
#            #matxml.append(newelemXml)
#            self.materials.append(newelemXml)
#            volAsm.newMaterials.append(newelemXml)


    def processMaterial(self, volAsm, mat):
        #print(f"Process Material  {mat} {volAsm}")
        # Mat Material could be Element | Material
        # Find should find and copy type
        print(f"Process Material  {mat}")
        matXml = self.materials.find(f"*[@name='{mat}']")
        print(f"matXml {matXml}")
        if matXml is not None:
            # <- make a deep copy of the found material element
            newmatXml = copy.deepcopy(matXml)
            #self.printMaterial(newmatXml)
            volAsm.newMaterials.append(newmatXml)


    def processMaterials(self, volAsm, matList):
        print(f"Process Materials {matList} {volAsm}")
        #print(f"Process Materials {matList}")
        for mat in matList:
            newMat = self.processMaterial(volAsm, mat)
            #        if newMat is not None:
            #            while volAsm is not None:
            #print(f"insert into Materials XML {volAsm.newMaterials}")
            #volAsm.newMaterials.append(newMat)
            #                volAsm = volAsm.getParent()


    def checkAddMaterial(self, volAsm, name):
        exists = volAsm.newMaterials.find(f"*[@name='{name}']")
        if exists is None:
            matXml = self.materials.find(f"*[@name='{name}']")
            self.processMaterial(volAsm, name)

    def processMaterialsElements(self, volAsm, matList):
        # Need to process before processMaterials
        # List may contain Elements or Materials with Elements
        #(fraction/composite
        #print(f"Process Material Elements : {volAsm}")
        for mat in matList:
            matXml = self.materials.find(f"*[@name='{mat}']")
            print(f"matXml type {matXml.tag}")
            if matXml is not None:
                print(f"matXml type {matXml.tag}")
                if matXml.tag in ['element','isotope']:
                    name = matXml.get('name')
                    self.checkAddMaterial(volAsm, name)
                elif matXml.tag == 'material':
                    for fractXml in matXml.findall("fraction"):
                        ref = fractXml.get("ref")
                        print(f"Faction ref {ref}")
                        self.checkAddMaterial(volAsm, ref)

                    for compXml in matXml.findall("composite"):
                        ref = compXml.get("ref")
                        print(f"Composite ref {ref}")
                        self.checkAddMaterial(volAsm, ref)

                else:
                    print(f"Not a valid Material Tag")       


    def checkBooleanSolids(self, volAsm, solidXml):
        #print(f"{solidXml}")
        #print(solidXml.attrib)
        #print(solidXml.keys)
        #print(dir(solidXml))
        tag = solidXml.tag
        if tag == 'union' or tag == 'subtraction' or tag == 'intersection':
            for child in solidXml:
                if child.tag == "first" or child.tag == "second":
                    solidRef = child.attrib.get("ref")
                    print(f"Solid Ref {solidRef}")
                    self.processSolid(volAsm, solidRef)

        elif tag == 'multiUnion':
            for child in solidXml:
                if child.tag == 'multiUnionNode':
                    for el in child:
                        if el.tag == 'solid':
                            solidRef = el.attrib.get("ref")            
                            print(f"Solid Ref {solidRef}")
                            self.processSolid(volAsm, solidRef)

    def processSolid(self, volAsm, sname):
        solidXml = self.solids.find(f"*[@name='{sname}']")
        #print(f"solidXml {solidXml}")
        newSolidXml = copy.deepcopy(solidXml)
        if newSolidXml is not None:
            volAsm.newSolids.append(newSolidXml)
            self.checkBooleanSolids(volAsm, newSolidXml)


    def processSolids(self, volAsm, solidList):
        #print(f"Process Solids {solidList} {volAsm}")
        print(f"Process Solids {solidList}")
        for sname in solidList:
            self.processSolid(volAsm, sname)


    def processPosDefine(self, volAsm, pos):
        posXml = self.define.find(f"*[@name='{pos}']")
        #print(f"posXml {posXml}")
        newPosXml = copy.deepcopy(posXml)
        if newPosXml is not None:
            volAsm.newDefine.append(newPosXml)


    def processPosDefines(self, volAsm, definePosList):
        #print(f"Process Solids {definePosList} {volAsm}")
        #print(f"Process Pos defines {definePosList}")
        if len(definePosList) > 0:
            for pos in definePosList:
                self.processPosDefine(volAsm, pos)


    def processRotDefine(self, volAsm, rot):
        rotXml = self.define.find(f"*[@name='{rot}']")
        #print(f"rotXml {rotXml}")
        newRotXml = copy.deepcopy(rotXml)
        if newRotXml is not None:
            volAsm.newDefine.append(newRotXml)


    def processRotDefines(self, volAsm, defineRotList):
        #print(f"Process Solids {definePosList} {volAsm}")
        #print(f"Process Rot defines {defineRotList}")
        if len(defineRotList) > 0:
            for rot in defineRotList:
                self.processRotDefine(volAsm, rot)


    # def addEntity(self, elemName, xmlFile) :
    #    self.docString += "<!ENTITY " + elemName + ' SYSTEM "' + xmlFile+'">\n'
    #    self.gdml.append(etree.Entity(elemName))

    # def closeElements(self) :
    #    self.docString += ']\n'

    def writeGDML(self, path, vname):
        # indent(iself.gdml)
        etree.ElementTree(self.gdml).write(os.path.join(path, vname+'.gdml'), \
               doctype = self.docString.encode('UTF-8'))


def exportEntity(dirPath, elemName, elem):
    import os
    global gdml, docString

    etree.ElementTree(elem).write(os.path.join(dirPath, elemName))
    docString += '<!ENTITY '+elemName+' SYSTEM "'+elemName+'">\n'
    gdml.append(etree.Entity(elemName))


if len(sys.argv) < 5:
    print ("Usage: sys.argv[0] <parms> <Volume> <in_file> <Out_directory> <materials>")
    print("/n For parms the following are or'ed together")
    print(" For future")
    sys.exit(1)

parms = int(sys.argv[1])
vName = sys.argv[2]
iName = sys.argv[3]
oName = sys.argv[4]

print('\nExtracting Volume : '+vName+' from : '+iName+' to '+oName)
checkDirectory(oName)
path = os.path.join(oName,vName)
checkDirectory(path)
lxml = gdml_lxml(iName)
volasm = VolAsm(vName, None)
volasm.processVolAsm(lxml, path, vName)
# setup = etree.Element('setup', {'name':'Default', 'version':'1.0'})
# etree.SubElement(setup,'world', { 'ref' : volList[-1]})



