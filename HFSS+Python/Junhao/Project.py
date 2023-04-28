# -*- coding: utf-8 -*-
from win32com import client
import os


def Prj(_phase1, _phase2, _phase3, _phase4, _phase5, _phase6, _phase7, _phase8):
    oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
    oDesktop = oAnsoftApp.GetAppDesktop()
    oDesktop.OpenProject("C:/Users/tee/PycharmProjects/Prj2.aedt")
    oProject = oDesktop.SetActiveProject("Prj2")
    oDesign = oProject.SetActiveDesign("HFSSDesign1")
    oModule = oDesign.GetModule("Solutions")
    oModule.EditSources(
        [
            [
                "IncludePortPostProcessing:=", True,
                "SpecifySystemPower:=", False
            ],
            [
                "Name:=", "lumpedPort1:1",
                "Magnitude:=", '1W',
                "Phase:=", str(_phase1) + "deg"
            ],
            [
                "Name:=", "lumpedPort2:1",
                "Magnitude:=", '1W',
                "Phase:=", str(_phase2) + "deg"
            ],
            [
                "Name:=", "lumpedPort3:1",
                "Magnitude:=", '1W',
                "Phase:=", str(_phase3) + "deg"
            ],
            [
                "Name:=", "lumpedPort4:1",
                "Magnitude:=", '1W',
                "Phase:=", str(_phase4) + "deg"
            ],
            [
                "Name:="	, "lumpedPort5:1",
                "Magnitude:="	, '1W',
                "Phase:="		, str(_phase5) + "deg"
                    ],
                [
                        "Name:="		, "lumpedPort6:1",
                        "Magnitude:="	,  '1W',
                        "Phase:="		, str(_phase6) + "deg"
                    ],
                [
                        "Name:="		, "lumpedPort7:1",
                        "Magnitude:="	, '1W',
                        "Phase:="		, str(_phase7) + "deg"
                    ],
                [
                        "Name:="		, "lumpedPort8:1",
                        "Magnitude:="	, '1W',
                        "Phase:="		, str(_phase8) + "deg"
                    ]
            ])
    oModule = oDesign.GetModule("ReportSetup")
    oModule.ExportToFile("Gain Plot 2", "C:/Users/tee/PycharmProjects/Gain Plot 2.csv")
    oProject.save()
    oDesktop.CloseProject("Prj2")


def Parametric(_name, _var, _start, _end, _step):
    _path = os.getcwd()
    _path = os.path.join(_path, 'Prj{}.aedt'.format(_name))
    _start = str(_start) + "mm"
    _end = str(_end) + "mm"
    _step = str(_step) + "mm"
    oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
    oDesktop = oAnsoftApp.GetAppDesktop()
    oDesktop.OpenProject(_path)
    oProject = oDesktop.SetActiveProject('Prj{}'.format(_name))
    oDesign = oProject.SetActiveDesign("HFSSDesign1")
    oModule = oDesign.GetModule("Optimetrics")
    oModule.InsertSetup("OptiParametric",
                        [
                            "NAME:ParametricSetup1",
                            "IsEnabled:="	, True,
                            [
                                "NAME:ProdOptiSetupDataV2",
                                "SaveFields:="		, False,
                                "CopyMesh:="		, False,
                                "SolveWithCopiedMeshOnly:=", True
                            ],
                            [
                                "NAME:StartingPoint"
                            ],
                            "Sim. Setups:="		, ["Setup1"],
                            [
                                "NAME:Sweeps",
                                [
                                    "NAME:SweepDefinition",
                                    "Variable:="		, str(_var),
                                    "Data:="		, "LIN {} {} {}".format(_start, _end, _step),
                                    "OffsetF1:=", False,
                                    "Synchronize:="	, 0
                                ]
                            ],
                            [
                                "NAME:Sweep Operations"
                            ],
                            [
                                "NAME:Goals"
                            ]
                        ])
    oProject.save()
    oDesktop.CloseProject('Prj{}'.format(_name))


def Optimization(_name, _var, _start, _min, _max):
    _path = os.getcwd()
    _path = os.path.join(_path, 'Prj{}.aedt'.format(_name))
    oAnsoftApp = client.Dispatch('AnsoftHfss.HfssScriptInterface')
    oDesktop = oAnsoftApp.GetAppDesktop()
    oDesktop.OpenProject(_path)
    oProject = oDesktop.SetActiveProject('Prj{}'.format(_name))
    oDesign = oProject.SetActiveDesign("HFSSDesign1")
    oProject.ChangeProperty(
        ["NAME:AllTabs",
         ["NAME:ProjectVariableTab",
          ["NAME:PropServers", "ProjectVariables"],
          ["NAME:ChangedProps",
           ["NAME:{}".format(_var), ["NAME:Optimization", "Included:=", True]],
           ["NAME:{}".format(_var), ["NAME:Optimization", "Min:=", str(_min) + "mm"]],
           ["NAME:{}".format(_var), ["NAME:Optimization", "Max:=", str(_max) + "mm"]]]]
         ])
    oModule = oDesign.GetModule("Optimetrics")
    oModule.InsertSetup("OptiOptimization",
                        ["NAME:OptimizationSetup1", "IsEnabled:=", True,
                         ["NAME:ProdOptiSetupDataV2", "SaveFields:=", False, "CopyMesh:=", False,
                          "SolveWithCopiedMeshOnly:=", True
                          ],
                         ["NAME:StartingPoint", "{}:=".format(_var), str(_start) + "mm"], "Optimizer:=", "SNLP",
                         ["NAME:AnalysisStopOptions", "StopForNumIteration:=", True, "StopForElapsTime:=", False,
                          "StopForSlowImprovement:=", False, "StopForGrdTolerance:=", False,
                          "MaxNumIteration:=", 15, "MaxSolTimeInSec:=", 3600,
                          "RelGradientTolerance:=", 0, "MinNumIteration:=", 10
                          ], "CostFuncNormType:=", "L2", "PriorPSetup:=", "", "PreSolvePSetup:=", True,
                         ["NAME:Variables", "{}:=".format(_var),
                          ["i:=", True, "int:=", False, "Min:=", str(_min) + "mm", "Max:=", str(_max) + "mm",
                           "MinStep:=", "0.01mm", "MaxStep:=", "0.1mm", "MinFocus:=", str(_min) + "mm", "MaxFocus:=",
                           str(_max) + "mm"]], ["NAME:LCS"],
                         ["NAME:Goals",
                          ["NAME:Goal", "ReportType:=", "Modal Solution Data", "Solution:=", "Setup1 : LastAdaptive",
                           ["NAME:SimValueContext"],
                           "Calculation:=", "dB(S(lumpedPort1,lumpedPort1))", "Name:=",
                           "dB(S(lumpedPort1,lumpedPort1))",
                           ["NAME:Ranges", "Range:=",
                            ["Var:=", "Freq", "Type:=", "rd", "Start:=", "2.44GHz", "Stop:=", "2.44GHz",
                             "DiscreteValues:=", "2.44GHz"]
                            ], "Condition:=", "Minimize",
                           ["NAME:GoalValue", "GoalValueType:=", "Independent", "Format:=", "Real/Imag",
                            "bG:=", ["v:=", "[0;]"]], "Weight:=", "[1;]"
                           ]
                          ],
                         "Acceptable_Cost:=", 0, "Noise:=", 0.0001,
                         "UpdateDesign:=", False, "UpdateIteration:=", 5,
                         "KeepReportAxis:=", True, "UpdateDesignWhenDone:=", True
                         ])
    oProject.save()
    # oDesktop.CloseProject('Prj{}'.format(_name))


if __name__ == '__main__':
    Prj(0, 0, 0, 0, 0, 0, 0, 0)
    # Parametric(2, 'w', 50, 60, 2.5)
    # Optimization(2, 'w', 56, 56.5, 58.5)
