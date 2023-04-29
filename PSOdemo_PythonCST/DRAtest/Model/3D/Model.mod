'# MWS Version: Version 2020.0 - Sep 25 2019 - ACIS 29.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 2 fmax = 5
'# created = '[VERSION]2020.0|29.0.1|20190925[/VERSION]


'@ use template: Antenna - Planar_2.cfg

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
'set the units
With Units
    .Geometry "mm"
    .Frequency "GHz"
    .Voltage "V"
    .Resistance "Ohm"
    .Inductance "H"
    .TemperatureUnit  "Kelvin"
    .Time "ns"
    .Current "A"
    .Conductance "Siemens"
    .Capacitance "F"
End With
'----------------------------------------------------------------------------
Plot.DrawBox True
With Background
     .Type "Normal"
     .Epsilon "1.0"
     .Mu "1.0"
     .XminSpace "0.0"
     .XmaxSpace "0.0"
     .YminSpace "0.0"
     .YmaxSpace "0.0"
     .ZminSpace "0.0"
     .ZmaxSpace "0.0"
End With
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "none"
     .Ysymmetry "none"
     .Zsymmetry "none"
End With
' optimize mesh settings for planar structures
With Mesh
     .MergeThinPECLayerFixpoints "True"
     .RatioLimit "20"
     .AutomeshRefineAtPecLines "True", "6"
     .FPBAAvoidNonRegUnite "True"
     .ConsiderSpaceForLowerMeshLimit "False"
     .MinimumStepNumber "5"
     .AnisotropicCurvatureRefinement "True"
     .AnisotropicCurvatureRefinementFSM "True"
End With
With MeshSettings
     .SetMeshType "Hex"
     .Set "RatioLimitGeometry", "20"
     .Set "EdgeRefinementOn", "1"
     .Set "EdgeRefinementRatio", "6"
End With
With MeshSettings
     .SetMeshType "HexTLM"
     .Set "RatioLimitGeometry", "20"
End With
With MeshSettings
     .SetMeshType "Tet"
     .Set "VolMeshGradation", "1.5"
     .Set "SrfMeshGradation", "1.5"
End With
' change mesh adaption scheme to energy
' 		(planar structures tend to store high energy
'     	 locally at edges rather than globally in volume)
MeshAdaption3D.SetAdaptionStrategy "Energy"
' switch on FD-TET setting for accurate farfields
FDSolver.ExtrudeOpenBC "True"
PostProcess1D.ActivateOperation "vswr", "true"
PostProcess1D.ActivateOperation "yz-matrices", "true"
With FarfieldPlot
	.ClearCuts ' lateral=phi, polar=theta
	.AddCut "lateral", "0", "1"
	.AddCut "lateral", "90", "1"
	.AddCut "polar", "90", "1"
End With
'----------------------------------------------------------------------------
With MeshSettings
     .SetMeshType "Hex"
     .Set "Version", 1%
End With
With Mesh
     .MeshType "PBA"
End With
'set the solver type
ChangeSolverType("HF Time Domain")
'----------------------------------------------------------------------------

'@ new component: component1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Component.New "component1"

'@ define cylinder: component1:solid1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "Ground_radius" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "-Ground_height", "0" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ define cylinder: component1:Feed_innner

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "Feed_innner" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "Mono_r" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "-Feed_h", "0" 
     .Xcenter "Mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ define cylinder: component1:Feed

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "Feed" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "2.03" 
     .InnerRadius "mono_r" 
     .Axis "z" 
     .Zrange "-Feed_h", "0" 
     .Xcenter "mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ rename block: component1:Feed to: component1:Feed_mid

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solid.Rename "component1:Feed", "Feed_mid"

'@ delete shape: component1:Feed_mid

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solid.Delete "component1:Feed_mid"

'@ define material: material1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Material 
     .Reset 
     .Name "material1"
     .Folder ""
     .Rho "0.0"
     .ThermalType "Normal"
     .ThermalConductivity "0"
     .SpecificHeat "0", "J/K/kg"
     .DynamicViscosity "0"
     .Emissivity "0"
     .MetabolicRate "0.0"
     .VoxelConvection "0.0"
     .BloodFlow "0"
     .MechanicsType "Unused"
     .FrqType "all"
     .Type "Normal"
     .MaterialUnit "Frequency", "GHz"
     .MaterialUnit "Geometry", "mm"
     .MaterialUnit "Time", "ns"
     .MaterialUnit "Temperature", "Kelvin"
     .Epsilon "2.08"
     .Mu "1"
     .Sigma "0"
     .TanD "0.0"
     .TanDFreq "0.0"
     .TanDGiven "False"
     .TanDModel "ConstTanD"
     .EnableUserConstTanDModelOrderEps "False"
     .ConstTanDModelOrderEps "1"
     .SetElParametricConductivity "False"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .SigmaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstTanD"
     .EnableUserConstTanDModelOrderMu "False"
     .ConstTanDModelOrderMu "1"
     .SetMagParametricConductivity "False"
     .DispModelEps  "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "Nth Order"
     .MaximalOrderNthModelFitEps "10"
     .ErrorLimitNthModelFitEps "0.1"
     .UseOnlyDataInSimFreqRangeNthModelEps "False"
     .DispersiveFittingSchemeMu "Nth Order"
     .MaximalOrderNthModelFitMu "10"
     .ErrorLimitNthModelFitMu "0.1"
     .UseOnlyDataInSimFreqRangeNthModelMu "False"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0", "1", "1" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With

'@ define cylinder: component1:Feed_mid

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "Feed_mid" 
     .Component "component1" 
     .Material "material1" 
     .OuterRadius "2.03" 
     .InnerRadius "mono_r" 
     .Axis "z" 
     .Zrange "-Feed_h", "0" 
     .Xcenter "mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ define cylinder: component1:Feed_outer

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "Feed_outer" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "2.8" 
     .InnerRadius "2.03" 
     .Axis "z" 
     .Zrange "-Feed_h", "-Ground_height" 
     .Xcenter "mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ paste structure data: 1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With SAT 
     .Reset 
     .FileName "*1.cby" 
     .SubProjectScaleFactor "0.001" 
     .ImportToActiveCoordinateSystem "True" 
     .ScaleToUnit "True" 
     .Curves "False" 
     .Read 
End With

'@ boolean subtract shapes: component1:solid1, component1:Feed_mid_1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solid.Subtract "component1:solid1", "component1:Feed_mid_1"

'@ paste structure data: 2

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With SAT 
     .Reset 
     .FileName "*2.cby" 
     .SubProjectScaleFactor "0.001" 
     .ImportToActiveCoordinateSystem "True" 
     .ScaleToUnit "True" 
     .Curves "False" 
     .Read 
End With

'@ boolean subtract shapes: component1:solid1, component1:Feed_innner_1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solid.Subtract "component1:solid1", "component1:Feed_innner_1"

'@ define cylinder: component1:monop

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "monop" 
     .Component "component1" 
     .Material "PEC" 
     .OuterRadius "mono_r" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "0", "mono_h" 
     .Xcenter "mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ define material: material2

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Material 
     .Reset 
     .Name "material2"
     .Folder ""
     .Rho "0.0"
     .ThermalType "Normal"
     .ThermalConductivity "0"
     .SpecificHeat "0", "J/K/kg"
     .DynamicViscosity "0"
     .Emissivity "0"
     .MetabolicRate "0.0"
     .VoxelConvection "0.0"
     .BloodFlow "0"
     .MechanicsType "Unused"
     .FrqType "all"
     .Type "Normal"
     .MaterialUnit "Frequency", "GHz"
     .MaterialUnit "Geometry", "mm"
     .MaterialUnit "Time", "ns"
     .MaterialUnit "Temperature", "Kelvin"
     .Epsilon "10"
     .Mu "1"
     .Sigma "0"
     .TanD "0.0"
     .TanDFreq "0.0"
     .TanDGiven "False"
     .TanDModel "ConstTanD"
     .EnableUserConstTanDModelOrderEps "False"
     .ConstTanDModelOrderEps "1"
     .SetElParametricConductivity "False"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .SigmaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstTanD"
     .EnableUserConstTanDModelOrderMu "False"
     .ConstTanDModelOrderMu "1"
     .SetMagParametricConductivity "False"
     .DispModelEps  "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "Nth Order"
     .MaximalOrderNthModelFitEps "10"
     .ErrorLimitNthModelFitEps "0.1"
     .UseOnlyDataInSimFreqRangeNthModelEps "False"
     .DispersiveFittingSchemeMu "Nth Order"
     .MaximalOrderNthModelFitMu "10"
     .ErrorLimitNthModelFitMu "0.1"
     .UseOnlyDataInSimFreqRangeNthModelMu "False"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0", "1", "1" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With

'@ define cylinder: component1:DR

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "DR" 
     .Component "component1" 
     .Material "material2" 
     .OuterRadius "DR_r" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "0", "DR_h" 
     .Xcenter "0" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ define cylinder: component1:port

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Cylinder 
     .Reset 
     .Name "port" 
     .Component "component1" 
     .Material "material1" 
     .OuterRadius "3" 
     .InnerRadius "0" 
     .Axis "z" 
     .Zrange "-Feed_h", "-Feed_h" 
     .Xcenter "mono_p" 
     .Ycenter "0" 
     .Segments "0" 
     .Create 
End With

'@ boolean insert shapes: component1:DR, component1:monop

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solid.Insert "component1:DR", "component1:monop"

'@ pick end point

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Pick.PickEndpointFromId "component1:port", "1"

'@ define discrete port: 1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With DiscretePort 
     .Reset 
     .PortNumber "1" 
     .Type "SParameter" 
     .Label "" 
     .Folder "" 
     .Impedance "50.0" 
     .VoltagePortImpedance "0.0" 
     .Voltage "1.0" 
     .Current "1.0" 
     .SetP1 "False", "mono_p", "0", "-Feed_h" 
     .SetP2 "False", "mono_p+3", "0.0", "-Feed_h" 
     .InvertDirection "False" 
     .LocalCoordinates "False" 
     .Monitor "True" 
     .Radius "0.0" 
     .Wire "" 
     .Position "end1" 
     .Create 
End With

'@ define frequency range

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solver.FrequencyRange "3", "10"

'@ define time domain solver parameters

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Mesh.SetCreator "High Frequency" 
With Solver 
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "All"
     .StimulationMode "All"
     .SteadyStateLimit "-30"
     .MeshAdaption "False"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

'@ set PBA version

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Discretizer.PBAVersion "2019092520"

'@ delete port: port1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Port.Delete "1"

'@ clear picks

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Pick.ClearAllPicks

'@ pick face

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Pick.PickFaceFromId "component1:port", "3"

'@ define port: 1

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
With Port 
     .Reset 
     .PortNumber "1" 
     .Label "" 
     .Folder "" 
     .NumberOfModes "1" 
     .AdjustPolarization "False" 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .TextMaxLimit "1" 
     .Coordinates "Picks" 
     .Orientation "negative" 
     .PortOnBound "False" 
     .ClipPickedPortToBound "False" 
     .Xrange "7", "13" 
     .Yrange "-3", "3" 
     .Zrange "-9", "-9" 
     .XrangeAdd "0.0", "0.0" 
     .YrangeAdd "0.0", "0.0" 
     .ZrangeAdd "0.0", "0.0" 
     .SingleEnded "False" 
     .WaveguideMonitor "False" 
     .Create 
End With

'@ define frequency range

'[VERSION]2020.0|29.0.1|20190925[/VERSION]
Solver.FrequencyRange "2", "5"

