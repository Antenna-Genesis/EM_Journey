# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:36:11 2020

This program is writing for Ansys HFSS software. It possesses three parts including the basic software operations,
advanced data post-process, and optimization algorithms. Maybe it will also have some GUI design and others.

This is the first part ---Class HFSS, which mainly includes the basic software operations.
To make it easier to use these functions, there are examples for each function.
Hope you will have a pleasant experience!

The program starts from 18th NOV. 2020 at City University of HK. Here we have a group of partners (Garen, Tinger, Indigo, and Leo), Hope we can complete
this huge project. Best regards to us. If you have any questions, please email to Chen.Yang@my.cityu.edu.hk

@author: cyang58
"""

from win32com import client
import os
import re

class HFSS:
######################################################################
# Launch ANSYS Electronics Desktop
######################################################################
    def init(self):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oDesktop.RestoreWindow()
        self.oProject = self.oDesktop.GetActiveProject()
        self.oDesign = self.oProject.GetActiveDesign()
#        self.oDesign = self.oProject.SetActiveDesign()
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5

    def launch(self):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oDesktop.RestoreWindow()
        self.oProject = self.oDesktop.NewProject()
        self.oProject.InsertDesign('HFSS', 'HFSSDesign1', 'DrivenModal1', '')
        self.oDesign = self.oProject.SetActiveDesign("HFSSDesign1")
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5

    def openProject(self, Path, Projectname):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oDesktop.RestoreWindow()
        if Path=="":
            self.oProject = self.oDesktop.OpenProject(Projectname + ".aedt")
        else:
            self.oProject = self.oDesktop.OpenProject(Path+"//"+Projectname+".aedt")
        self.oDesign = self.oProject.GetActiveDesign()
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5

    def openProjectwithdesign(self, Path, Projectname, Designname):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oDesktop.RestoreWindow()
        self.oProject = self.oDesktop.OpenProject(Path+"//"+Projectname+".aedt")
        self.oDesign = self.oProject.SetActiveDesign(Designname)
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5

    def activeDesign(self, Designname) :
        self.oDesign = self.oProject.SetActiveDesign(Designname)
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')
        self.transparency = 0.5


######################################################################
# Set variable         unit: 'mm' 'deg' or ''
# Change variable value
#Example:
#setVariable('a', 22.86,'mm')  setVariable('b', 25,'deg') setVariable('c', 0.3,'')
#changeVariablevalue('Xc', 10,'mm')
######################################################################

    def setVariable(self, Var_name, Var_value, unit):
        self.oDesign.ChangeProperty(["NAME:AllTabs",
                               ["NAME:LocalVariableTab",
                               ["NAME:PropServers", "LocalVariables"],
                               ["NAME:NewProps",
                               ['NAME:' + Var_name, "PropType:=", "VariableProp", "UserDef:=", True, "Value:=", str(Var_value)+' '+ unit]]]])

    def changeVariablevalue(self, Var_name, Var_value, unit):
        self.oDesign.ChangeProperty(
    	                      ["NAME:AllTabs",["NAME:LocalVariableTab",["NAME:PropServers", "LocalVariables"],
                              ["NAME:ChangedProps",
    				          ["NAME:"+Var_name,"Value:=", str(Var_value) + unit]]]])

    def getVariablevalue(self,Var_name):
        value=self.oDesign.GetVariableValue(Var_name)
        return value

    def convertVariabletovalueandunit(self,Var_name):
        val=float(re.findall(r"\-?\d+\.?\d*",Var_name)[0])
        unit=''.join(re.findall(r'[A-Za-z]', Var_name))
        return val,unit


######################################################################
# Create box, Cylinder,Regularpolyhedron         Material: 'defined material'
# Example:
#      createBox('0mm','0mm','0mm','10mm','20mm','30mm', 'DR', 'DK10')
#      createCylinder('0mm','0mm','0mm','3mm','3mm','Z','Cylinder1','vacuum')
#      createRegularpolyhedron('0mm','0mm','0mm','3mm','3mm','0mm','300mm',7,'Z','Cylinder10','vacuum')
######################################################################

    def createBox(self, Xposition,YPosition,ZPosition, Xsize,Ysize,Zsize, Name, Material,SolveIn):
        if SolveIn=="F":
                Flag=False
        else:
                Flag=True
        self.oEditor.CreateBox(
                          ["NAME:BoxParameters", "XPosition:=", Xposition, "YPosition:=" , YPosition, "ZPosition:=" , ZPosition,
                                                 "XSize:=", Xsize, "YSize:=", Ysize, "ZSize:=", Zsize],
                          ["NAME:Attributes", "Name:=", Name, "Flags:=", "", "Color:=", "(143 175 143)", "Transparency:=", 0,
                           "PartCoordinateSystem:=", "Global", "UDMId:=", "", "MaterialValue:=", '"\"' + Material+'\""', "SurfaceMaterialValue:=", "\"\"",
                           "SolveInside:=", Flag, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

    def createCylinder(self, XCenter,YCenter,ZCenter,Radius,Height,WhichAxis,Name,Material,SolveIn):
        if SolveIn=="F":
                Flag=False
        else:
                Flag=True
        self.oEditor.CreateCylinder(
    	          	          ["NAME:CylinderParameters","XCenter:=", XCenter,"YCenter:=", YCenter,"ZCenter:=", ZCenter, "Radius:=", Radius,
    		                   "Height:=", Height, "WhichAxis:=", WhichAxis,  "NumSides:=", "0",],
    		                  ["NAME:Attributes","Name:=", Name,"Flags:=", "","Color:=", "(143 175 143)","Transparency:=", 0, "PartCoordinateSystem:=", "Global","UDMId:=", "",
    			               "MaterialValue:=" ,'"\"' + Material+'\""', "SurfaceMaterialValue:=", "\"\"", "SolveInside:=", Flag, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

    def createPolyprism(self, XCenter,YCenter,ZCenter,Radius,Height,WhichAxis,SideNumber,Name,Material,SolveIn):
        if SolveIn=="F":
                Flag=False
        else:
                Flag=True
        self.oEditor.CreateCylinder(
    	          	          ["NAME:CylinderParameters","XCenter:=", XCenter,"YCenter:=", YCenter,"ZCenter:=", ZCenter, "Radius:=", Radius,
    		                   "Height:=", Height, "WhichAxis:=", WhichAxis,  "NumSides:=", SideNumber,],
    		                  ["NAME:Attributes","Name:=", Name,"Flags:=", "","Color:=", "(143 175 143)","Transparency:=", 0, "PartCoordinateSystem:=", "Global","UDMId:=", "",
    			               "MaterialValue:=" ,'"\"' + Material+'\""', "SurfaceMaterialValue:=", "\"\"", "SolveInside:=", Flag, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

    def createSphere(self, XCenter,YCenter,ZCenter,Radius,Name,Material,SolveIn):
        if SolveIn=="F":
                Flag=False
        else:
                Flag=True
        self.oEditor.CreateSphere(
	          	             ["NAME:SphereParameters","XCenter:=", XCenter,"YCenter:=", YCenter,"ZCenter:=", ZCenter, "Radius:=", Radius],
    		                  ["NAME:Attributes","Name:=", Name,"Flags:=", "","Color:=", "(143 175 143)","Transparency:=", 0, "PartCoordinateSystem:=", "Global","UDMId:=", "",
    			               "MaterialValue:=" ,'"\"' + Material+'\""', "SurfaceMaterialValue:=", "\"\"", "SolveInside:=", Flag, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False, "IsLightweight:=", False])

    def createRegularpolyhedron(self, XCenter,YCenter,ZCenter,XStart,YStart,ZStart,Height,NumSides,WhichAxis,Name,Material,SolveIn):
        if SolveIn=="F":
                Flag=False
        else:
                Flag=True
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oEditor.CreateRegularPolyhedron(
    	                               ["NAME:PolyhedronParameters","XCenter:=", XCenter,"YCenter:=", YCenter,"ZCenter:=", ZCenter, "XStart:=", XStart, "YStart:=", YStart, "ZStart:=", ZStart,
    		                            "Height:=", Height, "NumSides:=", NumSides, "WhichAxis:=", WhichAxis],
    	                               ["NAME:Attributes","Name:=", Name,"Flags:=", "","Color:=", "(143 175 143)","Transparency:=", 0,"PartCoordinateSystem:=", "Global","UDMId:=", "",
    		                            "MaterialValue:=", '"\"' + Material+'\""',"SurfaceMaterialValue:=", "\"\"","SolveInside:=", Flag, "IsMaterialEditable:=", True,"UseMaterialAppearance:=", False,"IsLightweight:=", False])

    def createSpherenonmodel(self, XCenter,YCenter,ZCenter,Radius,Name):
        self.oEditor.CreateSphere(
	          	             ["NAME:SphereParameters","XCenter:=", XCenter,"YCenter:=", YCenter,"ZCenter:=", ZCenter, "Radius:=", Radius],
		                     ["NAME:Attributes","Name:=", Name,"Flags:=", "NonModel#","Color:=", "(143 175 143)","Transparency:=", 0, "PartCoordinateSystem:=", "Global","UDMId:=", "",
			                  "MaterialValue:=" , "\"vacuum\"", "SurfaceMaterialValue:=", "\"\"", "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False, "IsLightweight:=", False])

    def createRectangle(self,Xposition,YPosition,ZPosition, Width, Height, Whichaxis, Name ):
        self.oEditor.CreateRectangle(
                                ["NAME:RectangleParameters", "IsCovered:=", True, "XStart:=", Xposition, "YStart:=", YPosition, "ZStart:=", ZPosition,
		                         "Width:=", Width, "Height:=", Height, "WhichAxis:=", Whichaxis],
	                            ["NAME:Attributes", "Name:=", Name, "Flags:=", "", "Color:=", "(143 175 143)", "Transparency:=", 0,
		                         "PartCoordinateSystem:=", "Global", "UDMId:=", "", "MaterialValue:=", "\"vacuum\"", "SurfaceMaterialValue:=", "\"\"",
                                 "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False, "IsLightweight:=", False])

    def createCircle(self, XCenter,YCenter,ZCenter,Radius,Whichaxis,Name):
        self.oEditor.CreateCircle(
                                ["NAME:CircleParameters", "IsCovered:=", True, "XCenter:=", XCenter, "YCenter:=", YCenter, "ZCenter:=", ZCenter,
		                         "Radius:=", Radius, "WhichAxis:=", Whichaxis, "NumSegments:=", "0"],
	                            ["NAME:Attributes", "Name:=", Name, "Flags:=", "", "Color:=", "(143 175 143)", "Transparency:=", 0,
		                         "PartCoordinateSystem:=", "Global", "UDMId:=", "", "MaterialValue:=", "\"vacuum\"", "SurfaceMaterialValue:=", "\"\"",
                                 "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False, "IsLightweight:=", False])



######################################################################





######################################################################
# Add dielectric material  Loss_tan is set as 2.4 GHz
# Change material of a Object
#
# Example:
#                addMaterial('DK10', 10, 0.0032)
#                changeMaterial('Cylinder1', 'DK10')
######################################################################

    def addMaterial(self, Name, DK, Loss_tan):
        oDefinitionManager = self.oProject.GetDefinitionManager()
        oDefinitionManager.AddMaterial(
                                       ['NAME:' + Name,"CoordinateSystemType:=", "Cartesian","BulkOrSurfaceType:=", 1,
                                       ["NAME:PhysicsTypes","set:=", ["Electromagnetic"]],
    	        	                    "permittivity:=", str(DK),
    		                            "dielectric_loss_tangent:=", str(Loss_tan),
                        		        "delta_H_freq:=", "2400000000" ])

    def changeMaterial(self, Object, Material):
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oEditor.ChangeProperty(
    	                       ["NAME:AllTabs",
    	                       ["NAME:Geometry3DAttributeTab",["NAME:PropServers", Object],
    		                   ["NAME:ChangedProps",["NAME:Material","Value:=", "\"" + Material + "\""]]]])


######################################################################
# Create air box (region)  and Set region as radiation boundary
#
# Example:
#                createRegion('40mm')
#                assignRadiationRegion()
######################################################################
    def createRegion(self, Var_region):
        self.oEditor.CreateRegion(
                            ["NAME:RegionParameters", "+XPaddingType:=", "Absolute Offset", "+XPadding:=", Var_region, "-XPaddingType:=", "Absolute Offset", "-XPadding:=", Var_region,
                             "+YPaddingType:=", "Absolute Offset", "+YPadding:=", Var_region, "-YPaddingType:=", "Absolute Offset", "-YPadding:=", Var_region,
                             "+ZPaddingType:=", "Absolute Offset", "+ZPadding:=", Var_region, "-ZPaddingType:=", "Absolute Offset", "-ZPadding:=", Var_region],
                            ["NAME:Attributes", "Name:=", "Region", "Flags:=", "Wireframe#", "Color:=", "(143 175 143)", "Transparency:=", 0, "PartCoordinateSystem:=", "Global","UDMId:=", "",
                             "MaterialValue:="	, "\"vacuum\"", "SurfaceMaterialValue:=", "\"\"", "SolveInside:=", True, "IsMaterialEditable:=", True, "UseMaterialAppearance:=", False])

    def assignRadiationRegion(self):
        self.oModule.AssignRadiation(
                               ["NAME:Rad1", "Objects:=", ["Region"], "IsFssReference:=", False, "IsForPML:=", False])


######################################################################
# Set an analysis setup       Centerfreuency: '3.5GHz'
# Set an Sweep analysis       Sweep_type: 'Discrete' 'Fast'
# Solve an  analysis setup
# Example:
#                insertSetup('Setup6', '3.5GHz')
#                insertFrequencysweep('Setup6', '6GHz', '20GHz', '100MHz', 'Fast')
#                solve('Setup1')
######################################################################
    def insertSetup(self, Setupname,Centerfreuency):
        NAME = 'NAME:' + Setupname
        self.oModule = self.oDesign.GetModule("AnalysisSetup")
        self.oModule.InsertSetup("HfssDriven",
                           [NAME,"AdaptMultipleFreqs:=", False, "Frequency:=", Centerfreuency,"MaxDeltaE:=", 0.02,"MaximumPasses:=", 15,"MinimumPasses:=", 1,
            		       "MinimumConvergedPasses:=", 1,"PercentRefinement:=", 30, "IsEnabled:=", True,"BasisOrder:=", 1,"DoLambdaRefine:=", True,"DoMaterialLambda:=", True,
                           "SetLambdaTarget:=", False,"Target:=", 0.3333,"UseMaxTetIncrease:=", False,"UseDomains:=", False,"UseIterativeSolver:=", False,
                           "SaveRadFieldsOnly:="	, False,"SaveAnyFields:="	, True,"IESolverType:="	, "Auto","LambdaTargetForIESolver:=", 0.15,"UseDefaultLambdaTgtForIESolver:=", True])

    def insertFrequencysweep(self, Setupname, Minfrequency, Maxfrequency, Step, Sweep_type):
        self.oModule = self.oDesign.GetModule("AnalysisSetup")
        self.oModule.InsertFrequencySweep(Setupname,
    	                            ["NAME:Sweep", "IsEnabled:=", True, "RangeType:=", "LinearStep", "RangeStart:=", Minfrequency,
    		                         "RangeEnd:=", Maxfrequency, "RangeStep:=", Step, "Type:=", Sweep_type, "SaveFields:=", True, "SaveRadFields:=", False, "ExtrapToDC:=", False])

    def solve(self, Setupname):
        self.oDesktop.RestoreWindow()
        self.oDesign.Analyze(Setupname)


######################################################################
# Set up a Far-field Radiation Sphere
# Example:
#       insertRadiationsphere()
######################################################################
    def insertRadiationsphere(self):
        self.oModule = self.oDesign.GetModule("RadField")
        self.oModule.InsertFarFieldSphereSetup(
                                          ["NAME:Infinite Sphere1", "UseCustomRadiationSurface:=", False, "ThetaStart:=", "-180deg","ThetaStop:=", "180deg", "ThetaStep:=", "3deg",
                                           "PhiStart:=", "0deg", "PhiStop:=", "360deg", "PhiStep:=", "3deg", "UseLocalCS:=", False])

######################################################################
# Copy a Object
# Example:
#       copy('Cylinder1')
######################################################################
    def copy(self, Object):
        self.oEditor.Copy(["NAME:Selections", "Selections:=", Object])
        self.oEditor.Paste()

######################################################################
# Unite Object1 with Object2
# Example:
#       unitef('Cylinder1','Cylinder2')  Don't keep Object2
#       unitet('Cylinder1','Cylinder2')  Keep Object2
######################################################################
    def unitef(self, Object1,Object2):
        self.oEditor.Unite(["NAME:Selections", "Selections:=", Object1 + ',' + Object2],
                      ["NAME:UniteParameters", "KeepOriginals:=", False])
    def unitet(self, Object1,Object2):
        self.oEditor.Unite(["NAME:Selections", "Selections:=", Object1 + ',' + Object2],
                      ["NAME:UniteParameters", "KeepOriginals:=", True])


######################################################################
# Subtract Object1 by Object2
# Example:
#       subtractf('Cylinder1','Cylinder2')  Don't keep Object2
#       subtractt('Cylinder1','Cylinder2')  Keep Object2
######################################################################
    def subtractf(self, Object1,Object2):
        self.oEditor.Subtract(["NAME:Selections", "Blank Parts:=", Object1, "Tool Parts:=", Object2],
                         ["NAME:SubtractParameters", "KeepOriginals:=", False])
    def subtractt(self, Object1,Object2):
        self.oEditor.Subtract(["NAME:Selections", "Blank Parts:=", Object1, "Tool Parts:=", Object2],
                         ["NAME:SubtractParameters", "KeepOriginals:=", True])


######################################################################
# Connect Object1 by Object2
# Example:
#       connect( 'Cylinder1','Cylinder2')
######################################################################
    def connect(self, Object1,Object2):
        self.oEditor.Connect(["NAME:Selections", "Selections:=", Object1 + ',' + Object2])


######################################################################
# Intersect Object1 with Object2
# Example:
#       intersectf('Cylinder1','Cylinder2')  Don't keep Object2
#       intersectt('Cylinder1','Cylinder2')  Keep Object2
######################################################################
    def intersectf(self, Object1,Object2):
        self.oEditor.Intersect(["NAME:Selections", "Selections:=", Object1 + ',' + Object2],
                          ["NAME:IntersectParameters", "KeepOriginals:=", False])

    def intersectt(self, Object1,Object2):
        self.oEditor.Intersect(["NAME:Selections", "Selections:=", Object1 + ',' + Object2],
                          ["NAME:IntersectParameters", "KeepOriginals:=", True])


######################################################################
# Basic operation: Move, Rotate, and Mirror
# Example:
#       rotate('Cylinder1','Z','30deg')
#       move('Cylinder1','10mm','30mm','20mm',)
#       mirror('Cylinder1','10mm','30mm','20mm','0mm','1mm','0mm')
######################################################################
    def rotate(self, Object,RotateAxis,RotateAngle):
        self.oEditor.Rotate(["NAME:Selections", "Selections:=", Object,  "NewPartsModelFlag:=", "Model"],
                       ["NAME:RotateParameters", "RotateAxis:=", RotateAxis, "RotateAngle:=", RotateAngle])

    def move(self, Object,VectorX,VectorY,VectorZ):
        self.oEditor.Move(["NAME:Selections", "Selections:=", Object,  "NewPartsModelFlag:=", "Model"],
                     ["NAME:TranslateParameters", "TranslateVectorX:=", VectorX, "TranslateVectorY:=", VectorY,"TranslateVectorZ:=", VectorZ])

    def mirror(self, Object,BaseX,BaseY,BaseZ,NormalX,NormalY,NormalZ):
        self.oEditor.Mirror(["NAME:Selections", "Selections:=", Object,  "NewPartsModelFlag:=", "Model"],
                       ["NAME:MirrorParameters", "MirrorBaseX:="	, BaseX,
                                                 "MirrorBaseY:="	, BaseY,
    		                                     "MirrorBaseZ:="	, BaseZ,
                                                 "MirrorNormalX:="	, NormalX,
                                                 "MirrorNormalY:="	, NormalY,
    		                                     "MirrorNormalZ:="	, NormalZ])

######################################################################
# Duplicate operation: Move, Rotate, and Mirror
# Example:
#       duplicateRotate('Cylinder1','Z','30deg',3)
#       duplicateMove('Cylinder1','10mm','0mm','0mm',6)
#       duplicateMirror('Cylinder1','0mm','0mm','0mm','0mm','0mm','1mm')
######################################################################
    def duplicateRotate(self, Object,RotateAxis,RotateAngle,Number,CreateNewObject):
        if CreateNewObject=="T":
                Flag=True
        else:
                Flag=False
        self.oEditor.DuplicateAroundAxis(["NAME:Selections", "Selections:=", Object, "NewPartsModelFlag:=", "Model"],
    	                           ["NAME:DuplicateAroundAxisParameters", "CreateNewObjects:=", Flag,
                                                                            "WhichAxis:=", RotateAxis,
                                                                            "AngleStr:=", RotateAngle,
                                                                            "NumClones:=", Number],
    	                           ["NAME:Options", "DuplicateAssignments:=", True],
    	                           ["CreateGroupsForNewObjects:=", False])

    def duplicateRotatenonmodel(self, Object,RotateAxis,RotateAngle,Number,CreateNewObject):
        if CreateNewObject=="T":
                Flag=True
        else:
                Flag=False
        self.oEditor.DuplicateAroundAxis(["NAME:Selections", "Selections:=", Object, "NewPartsModelFlag:=", "NonModel"],
    	                           ["NAME:DuplicateAroundAxisParameters", "CreateNewObjects:=", Flag,
                                                                            "WhichAxis:=", RotateAxis,
                                                                            "AngleStr:=", RotateAngle,
                                                                            "NumClones:=", Number],
    	                           ["NAME:Options", "DuplicateAssignments:=", True],
    	                           ["CreateGroupsForNewObjects:=", False])

    def duplicateMove(self, Object,VectorX,VectorY,VectorZ,Number,CreateNewObject):
        if CreateNewObject=="T":
                Flag=True
        else:
                Flag=False
        self.oEditor.DuplicateAlongLine(["NAME:Selections", "Selections:=", Object,"NewPartsModelFlag:=", "Model"],
    	                           ["NAME:DuplicateToAlongLineParameters", "CreateNewObjects:=", Flag,
                                                                             "XComponent:=", VectorX,
                                                                             "YComponent:=", VectorY,
                                                                             "ZComponent:=", VectorZ,
                                                                             "NumClones:=", Number],
    	                           ["NAME:Options", "DuplicateAssignments:=", True],
    	                           ["CreateGroupsForNewObjects:=", False])

    def duplicateMirror(self, Object,BaseX,BaseY,BaseZ,NormalX,NormalY,NormalZ,CreateNewObject):
        self.oEditor.DuplicateMirror(["NAME:Selections", "Selections:=", Object,  "NewPartsModelFlag:=", "Model"],
                                ["NAME:DuplicateToMirrorParameters", "DuplicateMirrorBaseX:=", BaseX,
                                                                     "DuplicateMirrorBaseY:=", BaseY,
    		                                                         "DuplicateMirrorBaseZ:=", BaseZ,
                                                                     "DuplicateMirrorNormalX:=", NormalX,
                                                                     "DuplicateMirrorNormalY:=", NormalY,
    		                                                         "DuplicateMirrorNormalZ:=", NormalZ],
            	                ["NAME:Options", "DuplicateAssignments:=", True],
    	                        ["CreateGroupsForNewObjects:=", False])

######################################################################
# get Face ID by position and object
# Example:
#       GetFacebyposition('Port','Monopole_position','0mm','-Feed_height')

######################################################################

    def getFacebyposition(self, Object, Xposition, Yposition, Zposition):
        faceid=self.oEditor.GetFaceByPosition(["NAME:FaceParameters", "BodyName:=", Object, "XPosition:=", Xposition, "YPosition:=", Yposition, "ZPosition:=", Zposition])
        return faceid

######################################################################
# Assign boundary: Perfect E, Perfect H, Radiation, Master, Slave
# Example:
#       assignHertziandipolewave('0mm','Dipole_position','0mm','0.1mm')
#       assignPlanewave('Dipole_position','Dipole_position','Dipole_position')
#       assignCylindricalwave('0mm','Dipole_position','0mm','0.1mm')
######################################################################

    def assignPerfectE(self, Object, PEC_name):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignPerfectE(
	                     ["NAME:"+PEC_name, "Objects:=", [Object], "InfGroundPlane:=", False])

    def assignMaster(self, Masterboundaryname, FaceID, Originx, Originy, Originz, Uposx, Uposy, Uposz):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignMaster(["NAME:"+Masterboundaryname, "Faces:=", [FaceID],
		                 ["NAME:CoordSysVector",
			              "Origin:=", [str(Originx), str(Originy),str(Originz)],
			              "UPos:=", [str(Uposx), str(Uposy),str(Uposz)]
                          ],"ReverseV:=", False])

    def assignSlave(self, Slaveboundaryname, Masterboundaryname, FaceID, Originx, Originy, Originz, Uposx, Uposy, Uposz, Scan_phi, Scan_theta):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignSlave(["NAME:"+Slaveboundaryname, "Faces:=", [FaceID],
		                  ["NAME:CoordSysVector",
		                   "Origin:=", [str(Originx), str(Originy),str(Originz)],
			               "UPos:=", [str(Uposx), str(Uposy),str(Uposz)]],
		                   "ReverseV:=", True, "Master:=", Masterboundaryname,
		                   "UseScanAngles:=", True,
		                   "Phi:=", Scan_phi,
		                   "Theta:=", Scan_theta])

######################################################################
# Assign Excitation_incident wave: Hertziandipole wave, Plane wave, Cylindrical wave,
# Example:
#       assignHertziandipolewave('0mm','Dipole_position','0mm','0.1mm')
#       assignPlanewave('Dipole_position','Dipole_position','Dipole_position')
#       assignCylindricalwave('0mm','Dipole_position','0mm','0.1mm')
######################################################################
    def assignHertziandipolewave(self, OriginX,OriginY,OriginZ,SphereRadius):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignHertzianDipoleWave(
    	                                ["NAME:IncHDWave1", "IsCartesian:=", True, "EoX:=", "0", "EoY:=", "0", "EoZ:=", "1",
    		                             "kX:=", "0", "kY:=", "0", "kZ:=", "1", "OriginX:=", OriginX, "OriginY:=", OriginY, "OriginZ:=", OriginZ,
    		                             "SphereRadius:=", SphereRadius, "IsElectricDipole:=", True])

    def assignPlanewave(self, OriginX,OriginY,OriginZ):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignPlaneWave(
    	                       ["NAME:IncPWave1", "IsCartesian:=", True, "EoX:=", "1", "EoY:=", "0", "EoZ:=", "0",
    		                    "kX:=", "0", "kY:=", "0", "kZ:=", "1", "OriginX:=", OriginX, "OriginY:=", OriginY, "OriginZ:=", OriginZ,
    		                    "IsPropagating:=", True, "IsEvanescent:=", False, "IsEllipticallyPolarized:=", False])
    #                            "IsPropagating:=", False, "IsEvanescent:=", False, "IsEllipticallyPolarized:=", True, "PolarizationAngle:=", "0deg","PolarizationRatio:=", "1"])

    def assignCylindricalwave(self, OriginX,OriginY,OriginZ,SphereRadius):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignCylindricalWave(
    	                             ["NAME:IncCWave1","IsCartesian:=", True,"EoX:=", "1","EoY:=", "0","EoZ:=", "0",
    		                          "kX:=", "0","kY:=", "0","kZ:=", "1","OriginX:=", OriginX,"OriginY:=", OriginY,"OriginZ:=", OriginZ,"CylinderRadius:=", SphereRadius])



######################################################################
# Assign Excitation: Wave port, Floquet port, Lumped port,
# Example
#       assignHertziandipolewave('0mm','Dipole_position','0mm','0.1mm')
#       assignPlanewave('Dipole_position','Dipole_position','Dipole_position')
#       getFaceidfromposition('Port','Monopole_position','0mm','-Feed_height')
######################################################################
#def getFaceidfromposition(Object,Positionx,Positiony,Positionz):
#    self.oEditor.GetFaceByPosition(
#                              ["NAME:FaceParameters", "BodyName:=", Object, "XPosition:=", Positionx, "YPosition:=", Positiony, "ZPosition:=", Positionz])
#
#
#top_face_id = self.oEditor.GetFaceByPosition(["NAME:FaceParameters", "BodyName:=", "Box", "XPosition:=", "0mm", "YPosition:=", "0mm", "ZPosition:=", "100mm"])

    def assignWaveport(self, FaceID,Startx,Starty,Startz,Endx,Endy,Endz):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignWavePort(
    	                      ["NAME:1", "Faces:=", [FaceID], "NumModes:=", 1, "UseLineModeAlignment:=", False, "DoDeembed:=", False, "RenormalizeAllTerminals:=", True,
    		                  ["NAME:Modes",["NAME:Mode1","ModeNum:=", 1,"UseIntLine:=", True,
                              [ "NAME:IntLine", "Start:=", [str(Startx), str(Starty),str(Startz)], "End:=", [str(Endx), str(Endy), str(Endz)]],
    				           "AlignmentGroup:=", 0, "CharImp:=", "Zpi"]], "ShowReporterFilter:=", False, "ReporterFilter:="	, [True], "UseAnalyticAlignment:=", False])

    def assignWaveportwithname(self, Portname, FaceID,Startx,Starty,Startz,Endx,Endy,Endz):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignWavePort(
    	                      ["NAME:"+Portname, "Faces:=", [FaceID], "NumModes:=", 1, "UseLineModeAlignment:=", False, "DoDeembed:=", False, "RenormalizeAllTerminals:=", True,
    		                  ["NAME:Modes",["NAME:Mode1","ModeNum:=", 1,"UseIntLine:=", True,
                              [ "NAME:IntLine", "Start:=", [str(Startx), str(Starty),str(Startz)], "End:=", [str(Endx), str(Endy), str(Endz)]],
    				           "AlignmentGroup:=", 0, "CharImp:=", "Zpi"]], "ShowReporterFilter:=", False, "ReporterFilter:="	, [True], "UseAnalyticAlignment:=", False])

    def assignWaveportdeembed(self, FaceID,Startx,Starty,Startz,Endx,Endy,Endz,Deembeddistance):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignWavePort(
    	                      ["NAME:1", "Faces:=", [FaceID], "NumModes:=", 1, "UseLineModeAlignment:=", False, "DoDeembed:=", True, "DeembedDist:=", Deembeddistance, "RenormalizeAllTerminals:=", True,
    		                  ["NAME:Modes",["NAME:Mode1","ModeNum:=", 1,"UseIntLine:=", True,
                              [ "NAME:IntLine", "Start:=", [str(Startx), str(Starty),str(Startz)], "End:=", [str(Endx), str(Endy), str(Endz)]],
    				           "AlignmentGroup:=", 0, "CharImp:=", "Zpi"]], "ShowReporterFilter:=", False, "ReporterFilter:="	, [True], "UseAnalyticAlignment:=", False])

    def assignFloquetportdeembed(self, Portname, FaceID, Deembeddistance,Astartx,Astarty,Astartz,Aendx,Aendy,Aendz,
                                 Bstartx,Bstarty,Bstartz,Bendx,Bendy,Bendz,Scan_phi,Scan_theta):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignFloquetPort(
	                              ["NAME:"+Portname, "Faces:=", [FaceID], "NumModes:=", 2, "DoDeembed:=", True, "DeembedDist:=", Deembeddistance, "RenormalizeAllTerminals:=", True,
		                          ["NAME:Modes", ["NAME:Mode1", "ModeNum:=", 1, "UseIntLine:=", False, "CharImp:=", "Zpi"],[ "NAME:Mode2", "ModeNum:=", 2, "UseIntLine:=", False, "CharImp:=", "Zpi"]],
		                           "ShowReporterFilter:=", False, "ReporterFilter:=", [False,False], "UseScanAngles:=", True, "Phi:=", Scan_phi, "Theta:=", Scan_theta,
#                                   		                           "ShowReporterFilter:=", False, "ReporterFilter:=", [False,False], "UseScanAngles:=", True, "Phi:=", Scan_phi, "Theta:=", Scan_theta,
		                          ["NAME:LatticeAVector", "Start:=", [str(Astartx), str(Astarty),str(Astartz)], "End:=", [str(Aendx), str(Aendy), str(Aendz)]],
		                          ["NAME:LatticeBVector", "Start:=", [str(Bstartx), str(Bstarty),str(Bstartz)], "End:=", [str(Bendx), str(Bendy), str(Bendz)]],
		                          ["NAME:ModesList", ["NAME:Mode", "ModeNumber:=", 1, "IndexM:=", 0, "IndexN:=", 0, "KC2:=", 0, "PropagationState:=", "Propagating", "Attenuation:=", 0, "PolarizationState:=", "TE", "AffectsRefinement:=", True],
			                      ["NAME:Mode", "ModeNumber:=", 2, "IndexM:=", 0, "IndexN:=", 0, "KC2:=", 0, "PropagationState:=", "Propagating", "Attenuation:=", 0, "PolarizationState:=", "TM", "AffectsRefinement:=", True]]])
    def assignlumpport(self,port,name,sx,sy,sz,ex,ey,ez):
        self.oModule = self.oDesign.GetModule("BoundarySetup")
        self.oModule.AssignLumpedPort(
            [
                "NAME:"+name,
                "Objects:="		, [port],
                "RenormalizeAllTerminals:=", True,
                "DoDeembed:="		, False,
                [
                    "NAME:Modes",
                    [
                        "NAME:Mode1",
                        "ModeNum:="		, 1,
                        "UseIntLine:="		, True,
                        [
                            "NAME:IntLine",
                            "Start:="		, [sx,sy,sz],
                            "End:="			, [ex,ey,ez]
                        ],
                        "CharImp:="		, "Zpi",
                        "AlignmentGroup:="	, 0,
                        "RenormImp:="		, "50ohm"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [True],
                "FullResistance:="	, "50ohm",
                "FullReactance:="	, "0ohm"
            ])







######################################################################
# Adjust view: Fit all,
# Example
#
######################################################################

    def fitAll(self):
        self.oEditor.FitAll()

######################################################################
# EditSources:
# Example
#
######################################################################

    def editSources(self, Portname, Magnitude, Phase):
        self.oModule = self.oDesign.GetModule("Solutions")
        self.oModule.EditSources(
	                      [["IncludePortPostProcessing:=", False, "SpecifySystemPower:=", False],
		                  ["Name:=", Portname+":1", "Magnitude:=", str(Magnitude)+"W", "Phase:=", str(Phase)+"deg"]])





######################################################################
# Create report: S parameter,
# Creat Farfield report: Radiation pattern,
# Delete Allreports
# Example
#       createSpreport('Sparameter','Setup1')
#       createRectangulzrfarfieldpreport('RadiationPattern','Setup1','All', 0,'10Ghz') #Phi=0 plane
#       deleteAllreports()
######################################################################

    # def createSpreport(self, Reportname,Setupname,Result_items):
    #     self.oModule = self.oDesign.GetModule("ReportSetup")
    #     self.oModule.CreateReport(Reportname, "Modal Solution Data", "Rectangular Plot", Setupname+": Sweep",
    # 	["Domain:=", "Sweep"], ["Freq:=", ["All"]],
    # 	["X Component:=", "Freq", "Y Component:=", Result_items], [])
    def createSpreport(self, Reportname: object, Setupname: object, Result_items: object) :
        # self.oModule = self.oDesign.GetModule("ReportSetup")
        # self.oModule.CreateReport(Reportname, "Modal Solution Data", "Rectangular Plot", Setupname+": Sweep",
        # ["Domain:=", "Sweep"], ["Freq:=", ["All"]],
        # ["X Component:=", "Freq", "Y Component:=", Result_items], [])
        self.oModule = self.oDesign.GetModule("ReportSetup")
        self.oModule.CreateReport(Reportname, "Modal Solution Data", "Rectangular Plot", "setup1 : Sweep",
            [
                "Domain:="		, "Sweep"
            ],
            [
                "Freq:="		, ["All"]
            ],
            [
                "X Component:="		, "Freq",
                "Y Component:="		, ["dB(S(1,1))"]
            ], [])
    def createRectangulzrfarfieldpreport(self, Reportname,Setupname,Theta, Phi,Freq):
        if Theta=='All':
            theta='All'
            phi=str(Phi)+'deg'
            X_Component='Theta'
#            reportname=Reportname+' Phi= '+str(Phi)+' deg'
            item=[ "Theta:=", [theta], "Phi:=", [phi], "Freq:=", [Freq]]
        else:
            theta=str(Theta)+'deg'
            phi='All'
            X_Component='Phi'
#            reportname=Reportname+' Theta= '+str(Theta)+' deg'
            item=[ "Phi:=", [phi], "Theta:=", [theta],  "Freq:=", [Freq]]
        self.oModule = self.oDesign.GetModule("ReportSetup")
        self.oModule.CreateReport(Reportname, "Far Fields", "Rectangular Plot", Setupname+" : LastAdaptive",
	                         [ "Context:=", "Infinite Sphere1"],
	                         item,
                        	 ["X Component:=", X_Component, "Y Component:=", ["mag(GainTotal)"]])

    def deleteAllreports(self):
        self.oModule = self.oDesign.GetModule("ReportSetup")
        self.oModule.DeleteAllReports()


######################################################################
# Export field result: 'Complex E field.fld', Plane wave, Cylindrical wave,
# Example:
#       result_path = r'C:\Users\cyang58\Desktop\Python for HFSS\Result'
#       Filename='Complex E field.fld'
#       exportField('ComplexMag_E', result_path, Filename)
#
#
#
#
#Field calculator commands
######################################################################
    def exportField(self, Fieldtype, Savepath, Savefilename, Xmin, Xmax, Xstep, Ymin, Ymax, Ystep, Zmin, Zmax, Zstep):
        self.oModule = self.oDesign.GetModule("FieldsReporter")
        self.oModule.CopyNamedExprToStack(Fieldtype)
        self.oModule.ExportOnGrid(Savepath+"\\"+Savefilename+".fld",
                            [str(Xmin), str(Ymin), str(Zmin)], [str(Xmax), str(Ymax), str(Zmax)], [str(Xstep), str(Ystep), str(Zstep)], "Setup1 : LastAdaptive",
    	                    ["Freq:=", "3.5GHz", "Phase:=", "0deg"],
                            True, "Cartesian", ["0mm", "0mm", "0mm"], False)

    def calculateEfieldvalueintegrate(self,Fieldtype, Object, Savepath, Savefilename):
        self.oModule = self.oDesign.GetModule("FieldsReporter")
        self.oModule.CopyNamedExprToStack(Fieldtype)
        self.oModule.EnterVol(Object)
        self.oModule.CalcOp("Integrate")
        self.oModule.ClcEval("Setup1 : LastAdaptive",
	                        ["Freq:=", "3.5GHz", "Phase:=", "0deg"])
        self.oModule.CalculatorWrite(Savepath+"\\"+Savefilename+".fld",
                                    ["Solution:=", "Setup1 : LastAdaptive"],
	                                ["Freq:=", "3.5GHz", "Phase:=", "0deg"])

    def calculateVolumeintegrate(self, Object, Savepath, Savefilename):
        self.oModule = self.oDesign.GetModule("FieldsReporter")
        self.oModule.EnterScalar(1)
        self.oModule.EnterVol(Object)
        self.oModule.CalcOp("Integrate")
        self.oModule.ClcEval("Setup1 : LastAdaptive",
	                        ["Freq:=", "3.5GHz", "Phase:=", "0deg"])
        self.oModule.CalculatorWrite(Savepath+"\\"+Savefilename+".fld",
                                    ["Solution:=", "Setup1 : LastAdaptive"],
	                                ["Freq:=", "3.5GHz", "Phase:=", "0deg"])
######################################################################

######################################################################
# Export report: s parameter,
# Example:
#       result_path = r'C:/Users/YANG Chen/Desktop/Python for HFSS/Result'
#       Filename='S Parameter Plot 1.csv'
#       exportTofile('Sparameter', result_path, Filename)
#
######################################################################


    def exportTofile(self, Reportname, Savepath, Savefilename):
        self.oModule = self.oDesign.GetModule("ReportSetup")
        self.oModule.ExportToFile(Reportname, Savepath+"\\"+Savefilename)


#    def exportTofile(self, Reportname, Savepath, Savefilename, Save_num):
#        if not os.path.exists(Savepath):
#                os.makedirs(Savepath)
#        Savefilename = Savefilename + str(Save_num)+'.CSV'
#        self.oModule = self.oDesign.GetModule("ReportSetup")
#        self.oModule.ExportToFile(Reportname, os.path.join(Savepath, Savefilename))

    def exportTosnp(self, Savepath, Savefilename, Save_num):
        self.oModule = self.oDesign.GetModule("Solutions")
        if not os.path.exists(Savepath):
            os.makedirs(Savepath)
        Savefilename = Savefilename + str(Save_num)+'.s1p'
        self.oModule.ExportNetworkData("", ["Setup1:Sweep"], 3, Savepath+"\\"+Savefilename, ["All"], True, 50, "S", -1, 0, 15,True, True, False )
        '''
        oModule.ExportNetworkData("Model parameter", ["Setup name"], <FileFormat> 2 : Tab delimited spreadsheet format (.tab)
                                                                                  3 : Touchstone (.sNp)
                                                                                  4 : CitiFile (.cit)
                                                                                  7 : Matlab (.m)
                                                                                  8 : Terminal Z0 spreadsheet,
                                                                                  Savepath and filename,
                                                                                  Frequency---["All"],
                                                                                  Specifies whether to renormalize the data before export---True,
                                                                                  Real impedance value in ohms---50,
                                                                                  <DataType> Type: "S", "Y", or "Z"---"S",
                                                                                  -1,
                                                                                  <ComplexFormat> Type: "0", "1", or "2" 0 = Magnitude/Phase.  1= Real/Imaginary.  2= db/Phase.---0,
                                                                                  15,  True, True, False )
        '''

######################################################################
#Command of project
# Example:
#       result_path = r'C:\Users\cyang58\Desktop\Python for HFSS\Result'
#       Filename='Complex E field.fld'
#       exportField('ComplexMag_E', result_path, Filename)
#
#########################################################################
    def saveProjectdefault(self):
        base_path = os.getcwd()
        prj_num = 1
        while True:
                path = os.path.join(base_path, 'Prj{}.hfss'.format(prj_num))
                if os.path.exists(path):
                    prj_num += 1
                else:
                    break
        self.oProject.SaveAs(path, True)

    def saveProject(self, result_path, file_name):
        base_path = result_path
        while True:
                base_name = file_name+'.hfss'
                path = os.path.join(base_path, base_name)
                if os.path.exists(path):
                    file_name = file_name+"_1"
                    base_name = file_name+'.hfss'
                    path = os.path.join(base_path, base_name)
                else:
                    break
        self.oProject.SaveAs(path, True)

    def closeProject(self):
        self.oDesktop.GetActiveProject()
        self.oDesktop.CloseProject (str(self.oProject.GetName()))
        self.oDesktop.QuitApplication()
        del self.oModule
        del self.oEditor
        del self.oDesign
        del self.oProject
        del self.oDesktop
        del self.oAnsoftApp

    def closeAnsysapp(self):
        self.oDesktop.QuitApplication()
        del self.oModule
        del self.oEditor
        del self.oDesign
        del self.oProject
        del self.oDesktop
        del self.oAnsoftApp
