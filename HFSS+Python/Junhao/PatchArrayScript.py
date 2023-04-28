# -*- coding: utf-8 -*-
from win32com import client
import os


class HFSS:
    def __init__(self):
        self.oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
        self.oDesktop = self.oAnsoftApp.GetAppDesktop()
        self.oProject = self.oDesktop.NewProject()
        self.oProject.InsertDesign('HFSS', 'HFSSDesign1', 'DrivenModal1', '')
        self.oDesign = self.oProject.SetActiveDesign("HFSSDesign1")
        self.oEditor = self.oDesign.SetActiveEditor("3D Modeler")
        self.oModule = self.oDesign.GetModule('BoundarySetup')

    def set_variable(self, _var_name, _var_value):
        _NAME = 'NAME:' + _var_name
        _VALUE = str(_var_value) + 'mm'
        self.oDesign.ChangeProperty(
            ["NAME:AllTabs",
             ["NAME:ProjectVariableTab",
              ["NAME:PropServers", "ProjectVariables"],
              ["NAME:NewProps",
               [_NAME, "PropType:=", "VariableProp", "UserDef:=", True, "Value:=", _VALUE]]]])

    def create_cylinder(self, _name, _var_xp, _var_yp, _var_zp, _var_radius, _var_height, _axis, _mat):
        self.oEditor.CreateCylinder(
            [
                "NAME:CylinderParameters",
                "XCenter:="		, _var_xp,
                "YCenter:="		, _var_yp,
                "ZCenter:="		, _var_zp,
                "Radius:="		, _var_radius,
                "Height:="		, _var_height,
                "WhichAxis:="		, _axis,
                "NumSides:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, _name,
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"" + _mat + "\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def create_rectangle(self, _name, _var_xp, _var_zp, _var_x, _var_y, _axis):
        self.oEditor.CreateRectangle(
            [
                "NAME:RectangleParameters",
                "IsCovered:=", True,
                "XStart:=", _var_xp,
                "YStart:=", '60mm',
                "ZStart:=", _var_zp,
                "Width:=", _var_x,
                "Height:=", _var_y,
                "WhichAxis:=", _axis
            ],
            [
                "NAME:Attributes",
                "Name:=", _name,
                "Flags:=", "",
                "Color:=", "(255 255 143)",
                "Transparency:=", 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:=", "",
                "MaterialValue:=", "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="	, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def create_box(self, _var_xp, _var_yp, _var_z, _name):
        self.oEditor.CreateBox(
            [
                "NAME:BoxParameters",
                "XPosition:=", '-' + _var_xp + '/2',
                "YPosition:=", _var_yp,
                "ZPosition:=", "0mm",
                "XSize:=", _var_xp,
                "YSize:=", _var_yp,
                "ZSize:=", _var_z,
            ],
            [
                "NAME:Attributes",
                "Name:=", _name,
                "Flags:=", "",
                "Color:=", "(143 175 143)",
                "Transparency:=", 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:=", "",
                "MaterialValue:=", "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False
            ])

    def create_cycle(self, _var_zp, _radius):
        self.oEditor.CreateCircle(
            [
                "NAME:CircleParameters",
                "IsCovered:="		, True,
                "XCenter:="		, "0mm",
                "YCenter:="		, "54.8mm",
                "ZCenter:="		, _var_zp,
                "Radius:="		, _radius,
                "WhichAxis:="		, "Y",
                "NumSegments:="		, "0"
            ],
            [
                "NAME:Attributes",
                "Name:="		, "Port",
                "Flags:="		, "",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])

    def create_object_from_faces(self):
        self.oEditor.CreateObjectFromFaces(
            [
                "NAME:Selections",
                "Selections:="	, "GND",
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:Parameters",
                [
                    "NAME:BodyFromFaceToParameters",
                    "FacesToDetach:="	, [7, 464]
                ]
            ],
            [
                "CreateGroupsForNewObjects:=", False
            ])

    def subtract(self, _obj1, _obj2, _bool):
        self.oEditor.Subtract(
            [
                "NAME:Selections",
                "Blank Parts:="	, _obj1,
                "Tool Parts:="		, _obj2
            ],
            [
                "NAME:SubtractParameters",
                "KeepOriginals:=", _bool
            ]
        )

    def duplicate_line(self, _obj, _d, _num):
        self.oEditor.DuplicateAlongLine(
            [
                "NAME:Selections",
                "Selections:="	, _obj,
                "NewPartsModelFlag:="	, "Model"
            ],
            [
                "NAME:DuplicateToAlongLineParameters",
                "CreateNewObjects:="	, True,
                "XComponent:="		, "0mm",
                "YComponent:="		, "0mm",
                "ZComponent:="		, _d,
                "NumClones:="		, _num
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ],
            [
                "CreateGroupsForNewObjects:=", False
            ])

    def wrap_sheet(self):
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_1,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_2,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_3,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_4,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_5,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_6,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )
        self.oEditor.WrapSheet(
            [
                "NAME:Selections",
                "Selections:="		, "patch_7,Substrate"
            ],
            [
                "NAME:WrapSheetParameters",
                "Imprinted:="		, False
            ]
        )

    def set_material(self, _obj, _mat):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        _obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Material",
                            "Value:="	, "\"" + _mat + "\""
                        ]
                    ]
                ]
            ])

    def delete(self, _obj):
        self.oEditor.Delete(
            [
                "NAME:Selections",
                "Selections:="		, _obj
            ])

    def create_region(self, _d):
        self.oEditor.CreateRegion(
            [
                "NAME:RegionParameters",
                "+XPaddingType:=", "Absolute Offset",
                "+XPadding:=", _d,
                "-XPaddingType:=", "Absolute Offset",
                "-XPadding:="	, _d,
                "+YPaddingType:="	, "Absolute Offset",
                "+YPadding:="		, _d,
                "-YPaddingType:="	, "Absolute Offset",
                "-YPadding:="		, _d,
                "+ZPaddingType:="	, "Absolute Offset",
                "+ZPadding:="		, _d,
                "-ZPaddingType:="	, "Absolute Offset",
                "-ZPadding:="		, _d
            ],
            [
                "NAME:Attributes",
                "Name:="	, "Region",
                "Flags:="		, "Wireframe#",
                "Color:="		, "(143 175 143)",
                "Transparency:="	, 0,
                "PartCoordinateSystem:=", "Global",
                "UDMId:="		, "",
                "MaterialValue:="	, "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:="		, True,
                "IsMaterialEditable:="	, True,
                "UseMaterialAppearance:=", False
            ])
        self.oModule.AssignRadiation(
            [
                "NAME:Rad1",
                "Objects:="	, ["Region"],
                "IsFssReference:="	, False,
                "IsForPML:="		, False
            ])

    def assign_perfe(self, _obj1, _obj2):
        self.oModule.AssignPerfectE(
            [
                "NAME:PerfE_GND",
                "Objects:="	, [_obj1, _obj2],
                "InfGroundPlane:="	, False
            ])
        self.oModule.AssignPerfectE(
            [
                "NAME:PerfE_patch",
                "Objects:=", ["patch_1", "patch_2", "patch_3", "patch_4", "patch_5", "patch_6", "patch_7", "patch"],
                "InfGroundPlane:=", False
            ])

    def change_color(self, _obj, _r, _g, _b):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        _obj
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Color",
                            "R:="			, _r,
                            "G:="			, _g,
                            "B:="			, _b
                        ]
                    ]
                ]
            ])

    def assign_port(self, _obj, _start, _end, _name):
        self.oModule.AssignLumpedPort(
            [
                "NAME:1",
                "Objects:="	, [_obj],
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
                            "Start:="		, ["0mm", "54.8mm", str(_start) + "mm"],
                            "End:="			, ["0mm", "54.8mm", str(_end) + "mm"]
                        ],
                        "AlignmentGroup:="	, 0,
                        "CharImp:="		, "Zpi",
                        "RenormImp:="		, "50ohm"
                    ]
                ],
                "ShowReporterFilter:="	, False,
                "ReporterFilter:="	, [True],
                "Impedance:="		, "50ohm"
            ])
        self.oDesign.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:HfssTab",
                    [
                        "NAME:PropServers",
                        "BoundarySetup:1"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Name",
                            "Value:="		, _name
                        ]
                    ]
                ]
            ])

    def edit_sources(self, _mag1, _mag2, _mag3, _mag4, _phase1, _phase2, _phase3, _phase4):
        mod = self.oDesign.GetModule("Solutions")
        mod.EditSources(
            [
                [
                    "IncludePortPostProcessing:=", True,
                    "SpecifySystemPower:="	, False
                ],
                [
                    "Name:="		, "lumpedPort1:1",
                    "Magnitude:="	, str(_mag1) + 'W',
                    "Phase:="		, str(_phase1) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort2:1",
                    "Magnitude:="	, str(_mag2) + 'W',
                    "Phase:="		, str(_phase2) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort3:1",
                    "Magnitude:="	, str(_mag3) + 'W',
                    "Phase:="		, str(_phase3) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort4:1",
                    "Magnitude:="	, str(_mag4) + 'W',
                    "Phase:="		, str(_phase4) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort5:1",
                    "Magnitude:="		, str(_mag4) + 'W',
                    "Phase:="		, str(_phase4) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort6:1",
                    "Magnitude:="		, str(_mag3) + 'W',
                    "Phase:="		, str(_phase3) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort7:1",
                    "Magnitude:="		, str(_mag2) + 'W',
                    "Phase:="		, str(_phase2) + "deg"
                ],
                [
                    "Name:="		, "lumpedPort8:1",
                    "Magnitude:="		, str(_mag1) + 'W',
                    "Phase:="		, str(_phase1) + "deg"
                ]
            ])

    def solve_inside(self, _obj1):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    [
                        "NAME:PropServers",
                        _obj1
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Solve Inside",
                            "Value:="	, False
                        ]
                    ]
                ]
            ])

    def override(self, _bool):
        self.oDesign.SetDesignSettings(
            [
                "NAME:Design Settings Data",
                "Use Advanced DC Extrapolation:=", False,
                "Use Power S:="		, False,
                "Export After Simulation:=", False,
                "Allow Material Override:=", _bool,
                "Calculate Lossy Dielectrics:=", False,
                "Perform Minimal validation:=", False,
                "EnabledObjects:="	, [],
                "Port Validation Settings:=", "Standard"
            ],
            [
                "NAME:Model Validation Settings",
                "EntityCheckLevel:="	, "Strict",
                "IgnoreUnclassifiedObjects:=", False,
                "SkipIntersectionChecks:=", False
            ])

    def insert_setup(self, _freq):
        mod = self.oDesign.GetModule('AnalysisSetup')
        mod.InsertSetup("HfssDriven",
                        [
                            "NAME:Setup1",
                            "AdaptMultipleFreqs:=", False,
                            "Frequency:=", str(_freq) + 'GHz',
                            "MaxDeltaS:="	, 0.02,
                            "PortsOnly:="		, False,
                            "UseMatrixConv:="	, False,
                            "MaximumPasses:="	, 9,
                            "MinimumPasses:="	, 1,
                            "MinimumConvergedPasses:=", 1,
                            "PercentRefinement:="	, 30,
                            "IsEnabled:="		, True,
                            "BasisOrder:="		, 1,
                            "DoLambdaRefine:="	, True,
                            "DoMaterialLambda:="	, True,
                            "SetLambdaTarget:="	, False,
                            "Target:="		, 0.3333,
                            "UseMaxTetIncrease:="	, False,
                            "PortAccuracy:="	, 2,
                            "UseABCOnPort:="	, False,
                            "SetPortMinMaxTri:="	, False,
                            "UseDomains:="		, False,
                            "UseIterativeSolver:="	, False,
                            "SaveRadFieldsOnly:="	, False,
                            "SaveAnyFields:="	, True,
                            "IESolverType:="	, "Auto",
                            "LambdaTargetForIESolver:=", 0.15,
                            "UseDefaultLambdaTgtForIESolver:=", True
                        ])

    def insert_sweep(self, range1, range2):
        mod = self.oDesign.GetModule("AnalysisSetup")
        mod.InsertFrequencySweep("Setup1",
                                 [
                                     "NAME:Sweep",
                                     "IsEnabled:="	, True,
                                     "RangeType:="		, "LinearStep",
                                     "RangeStart:="		, str(range1) + "GHz",
                                     "RangeEnd:="		, str(range2) + "GHz",
                                     "RangeStep:="		, "0.01GHz",
                                     "Type:="		, "Fast",
                                     "SaveFields:="		, True,
                                     "SaveRadFields:="	, False,
                                     "GenerateFieldsForAllFreqs:=", False,
                                     "ExtrapToDC:="		, False
                                 ])

    def insert_field_setup(self):
        mod = self.oDesign.GetModule("RadField")
        mod.InsertFarFieldSphereSetup(
            [
                "NAME:Infinite Sphere1",
                "UseCustomRadiationSurface:=", False,
                "ThetaStart:="	, "-180deg",
                "ThetaStop:="		, "180deg",
                "ThetaStep:="		, "1deg",
                "PhiStart:="		, "0deg",
                "PhiStop:="		, "360deg",
                "PhiStep:="		, "1deg",
                "UseLocalCS:="		, False
            ])
        mod.InsertFarFieldSphereSetup(
            [
                "NAME:xy",
                "UseCustomRadiationSurface:=", False,
                "ThetaStart:="	, "90deg",
                "ThetaStop:="		, "90deg",
                "ThetaStep:="		, "5deg",
                "PhiStart:="		, "0deg",
                "PhiStop:="		, "360deg",
                "PhiStep:="		, "1deg",
                "UseLocalCS:="		, False
            ])
        mod.InsertFarFieldSphereSetup(
            [
                "NAME:xz",
                "UseCustomRadiationSurface:=", False,
                "ThetaStart:="	, "-180deg",
                "ThetaStop:="		, "180deg",
                "ThetaStep:="		, "1deg",
                "PhiStart:="		, "0deg",
                "PhiStop:="		, "0deg",
                "PhiStep:="		, "5deg",
                "UseLocalCS:="		, False
            ]
        )
        mod.InsertFarFieldSphereSetup(
            [
                "NAME:yz",
                "UseCustomRadiationSurface:=", False,
                "ThetaStart:=", "-180deg",
                "ThetaStop:="	, "180deg",
                "ThetaStep:="		, "1deg",
                "PhiStart:="		, "90deg",
                "PhiStop:="		, "90deg",
                "PhiStep:="		, "5deg",
                "UseLocalCS:="		, False
            ])

    def create_report(self):
        mod = self.oDesign.GetModule("ReportSetup")
        mod.CreateReport(
            "S Parameter Plot 1", "Modal Solution Data", "Rectangular Plot", "Setup1 : Sweep",
            [
                "Domain:="		, "Sweep"
            ],
            [
                "Freq:="		, ["All"]
            ],
            [
                "X Component:="		, "Freq",
                "Y Component:="		, ["dB(S(lumpedPort1,lumpedPort1))", "dB(S(lumpedPort2,lumpedPort2))",
                                    "dB(S(lumpedPort3,lumpedPort3))", "dB(S(lumpedPort4,lumpedPort4))",
                                    "dB(S(lumpedPort5,lumpedPort5))", "dB(S(lumpedPort6,lumpedPort6))",
                                    "dB(S(lumpedPort7,lumpedPort7))", "dB(S(lumpedPort8,lumpedPort8))"]
            ], [])
        mod.CreateReport(
            "Gain Plot 1", "Far Fields", "3D Polar Plot", "Setup1 : LastAdaptive",
            [
                "Context:="	, "Infinite Sphere1"
            ],
            [
                "Phi:="			, ["All"],
                "Theta:="		, ["All"],
                "Freq:="		, ["All"]
            ],
            [
                "Phi Component:="	, "Phi",
                "Theta Component:="	, "Theta",
                "Mag Component:="	, ["dB(RealizedGainTotal)"]
            ], [])
        mod.CreateReport(
            "Gain Plot 2", "Far Fields", "Radiation Pattern", "Setup1 : LastAdaptive",
            [
                "Context:="	, "yz"
            ],
            [
                "Theta:="		, ["All"],
                "Phi:="			, ["All"],
                "Freq:="		, ["All"]
            ],
            [
                "Ang Component:="	, "Theta",
                "Mag Component:="	, ["dB(RealizedGainTotal)"]
            ], [])
        mod.CreateReport(
            "Gain Plot 3", "Far Fields", "Radiation Pattern", "Setup1 : LastAdaptive",
            [
                "Context:="	, "xz"
            ],
            [
                "Theta:="		, ["All"],
                "Phi:="		,     ["All"],
                "Freq:="		, ["All"]
            ],
            [
                "Ang Component:="	, "Theta",
                "Mag Component:="	, ["dB(RealizedGainTotal)"]
            ], [])
        mod.CreateReport(
            "Realized Gain Plot 1", "Far Fields", "Rectangular Plot", "Setup1 : LastAdaptive",
            [
                "Context:="		, "yz"
            ],
            [
                "Theta:="		, ["All"],
                "Phi:="			, ["All"],
                "Freq:="		, ["All"]
            ],
            [
                "X Component:="		, "Theta",
                "Y Component:="		, ["dB(RealizedGainTotal)"]
            ], [])

    def csv(self, _path, _bool):
        if _bool is False:
            _path = os.getcwd()
        mod = self.oDesign.GetModule("ReportSetup")
        _path = os.path.join(_path, 'Gain Plot 1.csv')
        mod.ExportToFile(
            "Gain Plot 1", _path)
        _path = os.path.join(_path, 'Gain Plot 2.csv')
        mod.ExportToFile(
            "Gain Plot 2", _path)
        _path = os.path.join(_path, 'Gain Plot 3.csv')
        mod.ExportToFile(
            "Gain Plot 3", _path)
        _path = os.path.join(_path, 'S Parameter Plot 1.csv')
        mod.ExportToFile(
            "S Parameter Plot 1", _path)

    def save(self):
        _base_path = os.getcwd()
        _prj_num = 1
        while True:
            _path = os.path.join(_base_path, 'Prj{}.aedt'.format(_prj_num))
            if os.path.exists(_path):
                _prj_num += 1
            else:
                break
        self.oProject.SaveAs(_path, True)

    def run(self):
        self.oDesktop.RestoreWindow()
        self.oDesign.AnalyzeAll()
