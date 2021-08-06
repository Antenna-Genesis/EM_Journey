"""
CST2019 Python API
by Kai Lu, Apr. 22, 2020
kai.lu@my.cityu.edu.hk
"""
from win32com.client import Dispatch


class cst:

    # other templates
    # \CST STUDIO SUITE 2019\Library\Post Processing Templates
    # \CST STUDIO SUITE 2019\Online Help\vba
    def __init__(self, *args):
        import sys
        # Launch CST Studio
        self.cst_obj = Dispatch('CSTStudio.Application')
        if len(args) == 0:
            self.new_mws()
            # Created a new mws
        elif len(args) == 1:
            # print(args, len(args))
            self.open_mws(args[0])  # args is a tuple
            # Opened an existing mws
        else:
            sys.exit("To define a CST class, provide path of an existing CST file or make a blank one.")

    def new_mws(self):
        # creat a new CST file
        self.mws = self.cst_obj.NewMWS()

    def open_mws(self, _cst_file_path):
        # open an existing CST file
        self.mws = self.cst_obj.openFile(_cst_file_path)

    def saveas_cst(self, _cst_file_path):
        # Save CST project
        self.mws._FlagAsMethod('SaveAs')
        self.mws.SaveAs(_cst_file_path, True)

    def save_cst(self):
        # Save CST project
        self.mws._FlagAsMethod('Save')
        self.mws.Save()

    def run_cst(self):
        # Run simulation
        self.mws.Solver.Start

    def rebuild(self):
        # use Rebuild to retian the last simulation only
        # All results will be deleted.
        self.mws._FlagAsMethod('Rebuild')
        self.mws.Rebuild()

    # does not work
    # def set_quiet_Mode(self):
    #     # When flag is set to True message boxes are suppressed.
    #     self.mws._FlagAsMethod('SetQuietMode')
    #     self.mws.SetQuietMode(True)

    def quit_cst(self):
        # Quit CST
        self.mws._FlagAsMethod('Quit')
        self.mws.Quit()

    def unit(self, _geometry, _frequency, _time):
        # Setup the units
        _cst_macro_script = f'''
With Units 
    .Geometry "{_geometry}" 
    .Frequency "{_frequency}" 
    .Time "{_time}" 
End With 
'''
        self.add_to_history(f"Define Units: {_frequency}, {_geometry}, {_time}", _cst_macro_script)

    def free_macro(self, _macro_script, _macro_name):
        _cst_macro_script = f'''
{_macro_script}
'''
        self.add_to_history(f"(*) {_macro_name}", _cst_macro_script)

    def zoom_structure(self):
        _cst_macro_script = f'Plot.ZoomToStructure'
        self.add_to_history("ZoomToStructure", _cst_macro_script)
        # self.mws._FlagAsMethod('Plot')
        # self.mws.Plot.ZoomToStructure

    def freq_range(self, _fmin, _fmax):
        _cst_macro_script = f'''
With Solver
    .FrequencyRange "{_fmin}", "{_fmax}"
End With
'''
        self.add_to_history(f"Define frequency range: {_fmin} - {_fmax}", _cst_macro_script)

    def working_plane_status(self, _true_or_false):
        # Switch working plane on or off
        _cst_macro_script = f'Plot.DrawWorkplane "{_true_or_false}"'
        self.add_to_history("Switch Working Plane", _cst_macro_script)

    def background_vacuum(self):
        # other background setting need to created separately
        _cst_macro_script = f'''
With Background 
     .Type "Normal" 
     .Epsilon "1.0" 
     .Mue "1.0" 
     .XminSpace "0.0" 
     .XmaxSpace "0.0" 
     .YminSpace "0.0" 
     .YmaxSpace "0.0" 
     .ZminSpace "0.0" 
     .ZmaxSpace "0.0" 
End With 
'''
        self.add_to_history("Set background material to vacuum", _cst_macro_script)

    def background_pec(self):
        # other background setting need to created separately
        _cst_macro_script = f'''
With Background 
     .Type "PEC" 
     .Epsilon "1.0" 
     .Mue "1.0" 
     .XminSpace "0.0" 
     .XmaxSpace "0.0" 
     .YminSpace "0.0" 
     .YmaxSpace "0.0" 
     .ZminSpace "0.0" 
     .ZmaxSpace "0.0" 
End With 
'''
        self.add_to_history("Set background material to vacuum", _cst_macro_script)

    def boundaries_same(self, _boundary_type="expanded open",
                        _xsymmetry="none", _ysymmetry="none", _zsymmetry="none"):
        # other boundary settings need to created separately
        _cst_macro_script = f'''
With Boundary
    .Xmin "{_boundary_type}"
    .Xmax "{_boundary_type}"
    .Ymin "{_boundary_type}"
    .Ymax "{_boundary_type}"
    .Zmin "{_boundary_type}"
    .Zmax "{_boundary_type}"
    .Xsymmetry "{_xsymmetry}"
    .Ysymmetry "{_ysymmetry}"
    .Zsymmetry "{_zsymmetry}"
End With
'''
        self.add_to_history("Set boundaries and symmetries", _cst_macro_script)

    def boundaries_free(self, _xmin="expanded open", _xmax="expanded open", _ymin="expanded open",
                        _ymax="expanded open",
                        _zmin="expanded open", _zmax="expanded open", _xsym="none", _ysym="none", _zsym="none"):
        '''
        :param _xmin: "electric", "magnetic", "expanded open", "open", "periodic", "conducting wall" etc.
        :param _xmax:
        :param _ymin:
        :param _ymax:
        :param _zmin:
        :param _zmax:
        :param _xsym: "electric", "magnetic", "none"
        :param _ysym: "electric", "magnetic", "none"
        :param _zsym: "electric", "magnetic", "none"
        :return:
        '''
        _cst_macro_script = f'''
With Boundary
     .Xmin "{_xmin}"
     .Xmax "{_xmax}"
     .Ymin "{_ymin}"
     .Ymax "{_ymax}"
     .Zmin "{_zmin}"
     .Zmax "{_zmax}"
     .Xsymmetry "{_xsym}"
     .Ysymmetry "{_ysym}"
     .Zsymmetry "{_zsym}"
     .ApplyInAllDirections "False"
End With
'''
        self.add_to_history("(*) Set Free Boundaries", _cst_macro_script)

    def pml_specails(self, _pml_type='CenterNMonitors', f_for_open_space='fc'):
        _cst_macro_script = f'''
With Boundary
    .ReflectionLevel "0.0001" 
    .MinimumDistanceType "Fraction" 
    .MinimumDistancePerWavelengthNewMeshEngine "4" 
    .MinimumDistanceReferenceFrequencyType "{_pml_type}"
    .FrequencyForMinimumDistance "{f_for_open_space}" 
    .SetAbsoluteDistance "0.0" 
End With    
'''
        self.add_to_history(f"Set PML type as {_pml_type}", _cst_macro_script)

    def create_component(self, _component_name):
        _cst_macro_script = f'''
With Component
    .New "{_component_name}"
End With
'''
        self.add_to_history(f"New Component: {_component_name}", _cst_macro_script)

    def pick_face(self, _component_name, _structure_name, _face_id):
        _cst_macro_script = f'''
With Pick
   .PickFaceFromId "{_component_name}:{_structure_name}", "{_face_id}"
End With
'''
        self.add_to_history(f"Pick Face: {_component_name}-{_structure_name}-{_face_id}", _cst_macro_script)

    def set_edge(self, _point1, _point2):
        _cst_macro_script = f'''
Pick.AddEdge "{_point1[0]}", "{_point1[1]}", "{_point1[2]}", "{_point2[0]}", "{_point2[1]}", "{_point2[2]}" 
'''
        self.add_to_history(f"Add Edge", _cst_macro_script)

    def extrude(self, _component_name, _structure_name, _extrude_material, _extrude_height, _taper_angle=0):
        _cst_macro_script = f'''
With Extrude
    .Name "{_structure_name}"
    .Component "{_component_name}"
    .Material "{_extrude_material}"
    .Mode "Picks"
    .Height "{_extrude_height}"
    .Taper "{_taper_angle}"
    .UsePicksForHeight "False"
    .DeleteBaseFaceSolid "False"
    .ClearPickedFace "True"
    .Create 
End With
'''
        self.add_to_history(f"Extrude: {_component_name}-{_structure_name}", _cst_macro_script)

    def rotate(self, _component_name, _structure_name, _rotate_material, _rotate_ang, _taper_angle=0):
        _cst_macro_script = f'''
With Rotate 
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}" 
     .NumberOfPickedFaces "1" 
     .Material "{_rotate_material}" 
     .Mode "Picks" 
     .Angle "{_rotate_ang}" 
     .Height "0.0" 
     .RadiusRatio "1.0" 
     .TaperAngle "{_taper_angle}" 
     .NSteps "0" 
     .SplitClosedEdges "True" 
     .SegmentedProfile "False" 
     .DeleteBaseFaceSolid "True" 
     .ClearPickedFace "True" 
     .SimplifySolid "True" 
     .UseAdvancedSegmentedRotation "True" 
     .CutEndOff "True" 
     .Create 
End With 
'''
        self.add_to_history(f"Rotate: {_component_name}-{_structure_name}", _cst_macro_script)

    def extrude_face(self, _component_name, _structure_name,
                     _extrude_material="Vacuum", _extrude_height=10,
                     _twist_ang=0, _taper_angle=0):
        _cst_macro_script = f'''
With Extrude
    .Reset 
    .Name "{_structure_name}"
    .Component "{_component_name}"
    .Material "{_extrude_material}"
    .Mode "Picks"
    '.Mode "MultiplePicks" '
    .Height "{_extrude_height}"
    .Twist "{_twist_ang}"
    .Taper "{_taper_angle}"
    .UsePicksForHeight "False"
    .DeleteBaseFaceSolid "False"
    .ClearPickedFace "True"
    .Create 
End With
'''
        self.add_to_history(f"Extrude: {_component_name}-{_structure_name}", _cst_macro_script)

    def analytica_face(self, _component_name,
                       _structure_name,
                       _material="PEC",
                       _x_expr='5*Cos(v) + Cos(u+v)',
                       _y_expr='5*Sin(v) + Sin(u+v)',
                       _z_expr='v',
                       _u_range=[0, 1], _v_range=[0, 1]):
        _cst_macro_script = f'''
With AnalyticalFace
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}" 
     .Material "{_material}" 
     .LawX "{_x_expr}" 
     .LawY "{_y_expr}" 
     .LawZ "{_z_expr}" 
     .ParameterRangeU "{_u_range[0]}", "{_u_range[1]}" 
     .ParameterRangeV "{_v_range[0]}", "{_v_range[1]}" 
     .Create
End With
'''
        self.add_to_history(f"Create Analytical Face: {_component_name}-{_structure_name}", _cst_macro_script)

    def define_curve_from_edge(self, _structure_name, _curve_name):
        _cst_macro_script = f'''
With EdgeCurve
     .Reset 
     .Name "{_structure_name}" 
     .Curve "{_curve_name}" 
     .Create
End With
'''
        self.add_to_history(f"Define Curve from Edge: {_curve_name}-{_structure_name}", _cst_macro_script)

    def extrude_curve(self, _component_name, _structure_name, _extrude_material,
                      _extrude_height, _curve_name, _twist_angle=0, _taper_angle=0):
        _cst_macro_script = f'''
With ExtrudeCurve
    .Reset 
    .Name "{_structure_name}"
    .Component "{_component_name}"
    .Material "{_extrude_material}"
    .Thickness "{_extrude_height}"
    .Twistangle "{_twist_angle}" 
    .Taperangle "{_taper_angle}"
    .DeleteProfile "True" 
    .Curve "{_curve_name}" 
    .Create 
End With
'''
        self.add_to_history(f"Extrude Curve: {_component_name}-{_structure_name}", _cst_macro_script)

    def boolean_add(self, _component1, _structure1, _component2, _structure2):
        _cst_macro_script = f'''
With Solid
    .Add "{_component1}:{_structure1}", "{_component2}:{_structure2}"
End With
'''
        self.add_to_history(f"Boolean Add Shapes: {_component1}:{_structure1}, {_component2}:{_structure2}",
                            _cst_macro_script)

    def boolean_subtract(self, _component1, _structure1, _component2, _structure2):
        _cst_macro_script = f'''
With Solid
    .Subtract "{_component1}:{_structure1}", "{_component2}:{_structure2}"
End With
'''
        self.add_to_history(f"Boolean Subtract Shapes: {_component1}:{_structure1}, {_component2}:{_structure2}",
                            _cst_macro_script)

    def boolean_insert(self, _component1, _structure1, _component2, _structure2):
        _cst_macro_script = f'''
With Solid
    .Insert "{_component1}:{_structure1}", "{_component2}:{_structure2}"
End With
'''
        self.add_to_history(f"Boolean Insert Shapes: {_component1}:{_structure1}, {_component2}:{_structure2}",
                            _cst_macro_script)

    def boolean_intersect(self, _component1, _structure1, _component2, _structure2):
        _cst_macro_script = f'''
With Solid
    .Intersect "{_component1}:{_structure1}", "{_component2}:{_structure2}"
End With
'''
        self.add_to_history(f"Boolean Intersect Shapes: {_component1}:{_structure1}, {_component2}:{_structure2}",
                            _cst_macro_script)

    def boolean(self, _boolean_type, _component1, _structure1, _component2, _structure2):
        _cst_macro_script = f'''
With Solid
    .{_boolean_type} "{_component1}:{_structure1}", "{_component2}:{_structure2}"
End With
'''
        self.add_to_history(f"Boolean {_boolean_type} Shapes: {_component1}:{_structure1}, {_component2}:{_structure2}",
                            _cst_macro_script)

    def shell(self, _component, _structure, _wall_thickness, _shell_type="Outside"):
        _cst_macro_script = f'''
With Solid
    .AdvancedShell "{_component}:{_structure}", "{_shell_type}", "{_wall_thickness}"
End With
'''
        self.add_to_history(f"Shell Object: {_component}-{_structure}", _cst_macro_script)

    def pick_point(self, _component, _structure, _point_id):
        _cst_macro_script = f'''
With Pick
    .PickEndpointFromId "{_component}:{_structure}", "{_point_id}"
End With
'''
        self.add_to_history(f"Pick Points: {_component}-{_structure}-{_point_id}", _cst_macro_script)

    def define_wg_port_picks(self, _port_number, _modes_num,
                             _polarization_angle=0, _ref_plane_dist=0, _orientation='zmin'):
        _cst_macro_script = f'''
With Port
    .Reset 
    .PortNumber "{_port_number}"
    .NumberOfModes "{_modes_num}"
    .AdjustPolarization False 
    .PolarizationAngle "{_polarization_angle}"
    .ReferencePlaneDistance "{_ref_plane_dist}"
    .Coordinates "Picks"
    .Orientation "{_orientation}"
    .PortOnBound "True"
    .ClipPickedPortToBound "False"
    .Create 
End With
'''
        self.add_to_history(f"Define Waveguide Port: {_port_number}", _cst_macro_script)

    def clear_picks(self):
        _cst_macro_script = f'''
With Pick
    .ClearAllPicks 
End With
'''
        self.add_to_history(f"Clear All Picks", _cst_macro_script)

    def define_wg_port_free(self, _port_num=1, _label_name='', _folder_name='', _mode_num=1, _adjust_pol=False,
                            _pol_ang=0, _ref_dist=0, _orientation='zmin', _xmin=0, _xmax=0, _ymin=0, _ymax=0,
                            _zmin=0, _zmax=0):
        _cst_macro_script = f'''
With Port 
     .Reset 
     .PortNumber "{_port_num}" 
     .Label "{_label_name}" 
     .Folder "{_folder_name}" 
     .NumberOfModes "{_mode_num}" 
     .AdjustPolarization "{_adjust_pol}" 
     .PolarizationAngle "{_pol_ang}" 
     .ReferencePlaneDistance "{_ref_dist}" 
     .TextSize "50" 
     .TextMaxLimit "1" 
     .Coordinates "Free" 
     .Orientation "{_orientation}" 
     .PortOnBound "False" 
     .ClipPickedPortToBound "False" 
     .Xrange "{_xmin}", "{_xmax}" 
     .Yrange "{_ymin}", "{_ymax}" 
     .Zrange "{_zmin}", "{_zmax}" 
     .XrangeAdd "0.0", "0.0" 
     .YrangeAdd "0.0", "0.0" 
     .ZrangeAdd "0.0", "0.0" 
     .SingleEnded "False" 
     .WaveguideMonitor "False" 
     .Create 
End With 
'''
        self.add_to_history(f"Define Waveguide Port: {_port_num}", _cst_macro_script)

    def define_discreteport_free(self, _port_num=1, _label_name='', _folder_name='', _xmin=0, _xmax=0,
                                 _ymin=0, _ymax=0, _zmin=0, _zmax=0, _invert_direction=False):
        _cst_macro_script = f'''
With DiscretePort 
     .Reset 
     .PortNumber "{_port_num}" 
     .Type "SParameter" 
     .Label "{_label_name}" 
     .Folder "{_folder_name}" 
     .Impedance "50.0" 
     .VoltagePortImpedance "0.0" 
     .Voltage "1.0" 
     .Current "1.0" 
     .SetP1 "False", "{_xmin}", "{_ymin}", "{_zmin}" 
     .SetP2 "False", "{_xmax}", "{_ymax}", "{_zmax}" 
     .InvertDirection "{_invert_direction}" 
     .LocalCoordinates "False" 
     .Monitor "True" 
     .Radius "0.0" 
     .Wire "" 
     .Position "end1" 
     .Create 
End With
'''
        self.add_to_history(f"Define Discrete Port: {_port_num}", _cst_macro_script)

    def transform_shift(self, _obj='Port1', _x_shift=0, _y_shift=0, _z_shift=0, _keep_old=True,
                        _repetitions=1, _dest_comp='', _dest_material='', _obj_type='Port'):
        """
        To shift a single object
        :param _dest_material:
        :param _dest_comp:
        :param _obj: 'Port1' or "WG:WG_Tube_1"
        :param _x_shift:
        :param _y_shift:
        :param _z_shift:
        :param _keep_old: keep the original one or not
        :param _repetitions:
        :param _obj_type: 'Shape', 'Port', or 'Mixed'
        for mixed,    use  .AddName "solid$WG:WG_Ridge_Inner"  after .Name
        :return:
        """
        if _obj is None:
            _obj = 'Port1'

        _cst_macro_script = f'''
With Transform 
     .Reset 
     .Name "{_obj}"
     .Vector "{_x_shift}", "{_y_shift}", "{_z_shift}" 
     .UsePickedPoints "False" 
     .InvertPickedPoints "False" 
     .MultipleObjects "{_keep_old}" 
     .GroupObjects "False" 
     .Repetitions "{_repetitions}" 
     .MultipleSelection "False" 
     .Destination "{_dest_comp}" 
     .Material "{_dest_material}" 
     .Transform "{_obj_type}", "Translate" 
End With 
'''
        self.add_to_history(f"Shift {_obj}", _cst_macro_script)

    def transform_rotate(self, _obj='Port1', _x_center=0, _y_center=0, _z_center=0,
                         _x_rot_ang=0, _y_rot_ang=0, _z_rot_ang=0, _keep_old=True,
                         _repetitions=1, _dest_comp='', _dest_material='', _obj_type='Port'):
        _cst_macro_script = f'''
With Transform 
     .Reset 
     .Name "{_obj}" 
     .Origin "Free" 
     .Center "{_x_center}", "{_y_center}", "{_z_center}" 
     .Angle "{_x_rot_ang}", "{_y_rot_ang}", "{_z_rot_ang}" 
     .MultipleObjects "{_keep_old}" 
     .GroupObjects "False" 
     .Repetitions "{_repetitions}" 
     .MultipleSelection "False" 
     .Destination "{_dest_comp}" 
     .Material "{_dest_material}" 
     .Transform "{_obj_type}", "Rotate" 
End With 
'''
        self.add_to_history(f"Rotate {_obj}", _cst_macro_script)

    def transform_mirror(self, _obj='WG:WG_Ridge_Inner', _center_x=0, _center_y=0, _center_z=0, _normalplane_x=0,
                         _normalplane_y=0, _normalplane_z=0, _keep_old=True,
                         _repetitions=1, _dest_comp='', _dest_material='', _obj_type='Shape'):
        '''

        :param _obj: "WG:WG_Ridge_Inner" or "Port1"
        :param _center: such as "0", "10", "0"
        :return:
        '''
        _cst_macro_script = f'''
With Transform 
     .Reset 
     .Name "{_obj}" 
     .Origin "Free" 
     .Center "{_center_x}", "{_center_y}", "{_center_z}" 
     .PlaneNormal "{_normalplane_x}", "{_normalplane_y}", "{_normalplane_x}" 
     .MultipleObjects "{_keep_old}" 
     .GroupObjects "False" 
     .Repetitions "{_repetitions}" 
     .MultipleSelection "False" 
     .Destination "{_dest_comp}" 
     .Material "{_dest_material}" 
     .Transform "{_obj_type}", "Mirror" 
End With 
'''
        self.add_to_history(f"Mirror {_obj}", _cst_macro_script)

    def define_efield_monitor_fdomain(self, _frequency):
        _cst_macro_script = f'''
With Monitor
    .Reset 
    .Name "e-field (f={_frequency})"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Efield"
    .Frequency "{_frequency}"
    .Create 
End With
'''
        self.add_to_history(f"Define E-field Monitor FD: {_frequency}", _cst_macro_script)

    def define_hfield_monitor_fdomain(self, _frequency):
        _cst_macro_script = f'''
With Monitor
    .Reset 
    .Name "h-field (f={_frequency})"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Hfield"
    .Frequency "{_frequency}"
    .Create 
End With
'''
        self.add_to_history(f"Define H-field Monitor FD: {_frequency}", _cst_macro_script)

    def define_efield_monitor_tdomain(self, _time_step):
        _cst_macro_script = f'''
With Monitor
    .Reset 
    .Name "e-field (t=0..end({_time_step}))"
    .Dimension "Volume"
    .Domain "Time"
    .FieldType "Efield"
    .Tstart "0"
    .Tstep "{_time_step}"
    .Tend "0"
    .Create     
End With
'''
        self.add_to_history(f"Define Transient E-field Monitor", _cst_macro_script)

    def define_far_filed_monitor(self, _frequency):
        _cst_macro_script = f'''
With Monitor
    .Reset 
    .Name "farfield (f={_frequency})"
    .Dimension "Volume"
    .Domain "Frequency"
    .FieldType "Farfield"
    .Frequency "{_frequency}"
    .Create 
End With
'''
        self.add_to_history(f"Define Far-field Monitor: {_frequency}", _cst_macro_script)

    def define_solver_para(self, _calculation_type='TD-S', _stimulation_port='All',
                           _stimulation_mode="All", _steady_state_limit="-40", _adaptive_port_meshing=False):
        _cst_macro_script = f'''
With Solver
    .CalculationType "{_calculation_type}"
    .StimulationPort "{_stimulation_port}"
    .StimulationMode "{_stimulation_mode}"
    .SteadyStateLimit "{_steady_state_limit}"
    .AdaptivePortMeshing {_adaptive_port_meshing}
End With
'''
        self.add_to_history(f"Define Solver Parameters", _cst_macro_script)

    def define_default_solver_para(self, _port_name='All'):
        _cst_macro_script = f'''
Mesh.SetCreator "High Frequency" 
With Solver 
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "{_port_name}"
     .StimulationMode "All"
     .SteadyStateLimit "-40"
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
'''
        self.add_to_history(f"Set Default Solver Parameters", _cst_macro_script)

    def vswr_display(self):
        _cst_macro_script = f'''
With PostProcess1D
    .ActivateOperation "VSWR", "True"
End With
'''
        self.add_to_history(f"(*) Show VSWR", _cst_macro_script)

    def yz_display(self):
        _cst_macro_script = f'''
With PostProcess1D
    .ActivateOperation "yz-matrices", "True"
End With
'''
        self.add_to_history(f"(*) Show Y and Z Matrix", _cst_macro_script)

    def define_free_ff_cut(self, _plane_type, _plane_ang, _ang_step):
        """
        :param _ang_step: number in deg
        :param _plane_ang: number in deg
        :param _plane_type: "lateral"
        :return: none
        """
        _cst_macro_script = f'''
With FarfieldPlot
    .ClearCuts 
    .AddCut "{_plane_type}", "{_plane_ang}", "{_ang_step}"
End With
'''
        self.add_to_history(f"(*) Define Far Field Cut for {_plane_type}={_plane_ang} deg", _cst_macro_script)

    def define_typical_ff_cuts(self):
        _cst_macro_script = f'''
With FarfieldPlot
    .ClearCuts ' lateral=phi, polar=theta
    .AddCut "lateral", "0", "1"
    .AddCut "lateral", "90", "1"
    .AddCut "polar", "90", "1"
End With
'''
        self.add_to_history(f"(*) Define Typical Far Field Cuts for phi=0&90 deg, theta=90 deg", _cst_macro_script)

    def new_fun_template(self):
        _cst_macro_script = f'''
With PostProcess1D
    .ActivateOperation "yz-matrices", "True"
End With
'''
        self.add_to_history(f"(*) Show Y and Z Matrix", _cst_macro_script)

    def export_ascii_1d(self, SelectTreeItem="1D Results\Port signals\i1",
                        file_path="D:\CST_Projects\Temp\input_signal.txt"):
        _cst_macro_script = f'''
SelectTreeItem ("{SelectTreeItem}")
With ASCIIExport
    .Reset
    .FileName ("{file_path}")
    .Execute
End With
'''
        self.add_to_history(f"(*) Exported {SelectTreeItem} as {file_path}", _cst_macro_script)

    def store_para(self, _para_name, _par_value):
        # define/change a parameter to a CST file
        self.mws._FlagAsMethod('StoreParameter')
        self.mws.StoreParameter(_para_name, _par_value)

    def get_parameters(self):
        # define/change a parameter to a CST file
        self.mws._FlagAsMethod('GetNumberOfParameters')
        self.para_num = int(self.mws.GetNumberOfParameters())
        para_names_list = []
        para_values_list = []
        para_exprs_list = []
        for para_indx in range(self.para_num):
            pass
            self.mws._FlagAsMethod('GetParameterName')
            _para_names = self.mws.GetParameterName(para_indx)
            self.mws._FlagAsMethod('GetParameterNValue')
            _para_values = self.mws.GetParameterNValue(para_indx)
            self.mws._FlagAsMethod('GetParameterSValue')
            _para_exprs = self.mws.GetParameterSValue(para_indx)
            para_names_list.append(_para_names)
            para_values_list.append(_para_values)
            para_exprs_list.append(_para_exprs)
        return para_names_list, para_values_list, para_exprs_list

    def update_para(self):
        self.mws._FlagAsMethod('RebuildOnParametricChange')
        self.mws.RebuildOnParametricChange(False, False)

    def store_mesh_nums(self):
        _cst_macro_script = f'''
Mesh.Update
If DoesParameterExist ("Mesh_Num_Total") Then
        DeleteParameter ("Mesh_Num_Total")
End If
If DoesParameterExist ("Mesh_Min_Length") Then
        DeleteParameter ("Mesh_Min_Length")
End If
If DoesParameterExist ("Mesh_Max_Length") Then
        DeleteParameter ("Mesh_Max_Length")
End If
MakeSureParameterExists("Mesh_Num_Total", Mesh.GetNumberOfMeshCells)
MakeSureParameterExists("Mesh_Min_Length", Mesh.GetMinimumEdgeLength)
MakeSureParameterExists("Mesh_Max_Length", Mesh.GetMaximumEdgeLength)
'StoreParameter("Mesh_Num_Total", Mesh.GetNumberOfMeshCells)
'StoreParameter("Mesh_Min_Length", Mesh.GetMinimumEdgeLength)
'StoreParameter("Mesh_Max_Length", Mesh.GetMaximumEdgeLength)
'Returns the total number of mesh cells (may be either hexahedral elements or tetrahedrons).
'Returns the minimum edge length of the currently chosen mesh.
'Returns the maximum edge length of the currently chosen mesh.
'''
        self.add_to_history(f"Store Pivot Mesh Info to Parameter List", _cst_macro_script)

    def enable_tlm_solver(self):
        _cst_macro_script = f'''
With Mesh
     .MeshType "HexahedralTLM"
End With

With MeshSettings
     .SetMeshType "HexTLM"'
End With
        '''
        self.add_to_history(f"Enable TLM Solver and Mesh", _cst_macro_script)

    def add_to_history(self, _script_line_name, _script_lines):
        self.mws._FlagAsMethod("AddToHistory")
        self.mws.AddToHistory(_script_line_name, _script_lines)

    def create_brick(self, _component_name, _structure_name, _material_name,
                     _x_min, _x_max, _y_min, _y_max, _z_min, _z_max):
        # define a brick
        # e.g. cstbrick("a", "b", "c", "-waveguide_width/2", 20, -30, 40, -50, 60)
        _cst_macro_script = f'''
With Brick
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}"
     .Material "{_material_name}"
     .Xrange "{_x_min}", "{_x_max}"
     .Yrange "{_y_min}", "{_y_max}" 
     .Zrange "{_z_min}", "{_z_max}"
     .Create
End With
'''
        self.add_to_history(f'Define Brick: {_component_name} - {_structure_name}', _cst_macro_script)

    def create_cone(self, _component_name, _structure_name, _material_name,
                    _bottom_r, _top_r, _axis, _cone_min_position, _cone_max_position, _cone_center_u, _cone_center_v):
        _cst_macro_script = f'''
With Cone 
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}" 
     .Material "{_material_name}" 
     .BottomRadius "{_bottom_r}" 
     .TopRadius "{_top_r}" 
     .Axis "{_axis}" 
     .Zrange "{_cone_min_position}", "{_cone_max_position}" 
     .Xcenter "{_cone_center_u}" 
     .Ycenter "{_cone_center_v}" 
     .Segments "0" 
     .Create 
End With
'''
        self.add_to_history(f'Define Cone: {_component_name} - {_structure_name}', _cst_macro_script)

    def create_cylinder(self, _component_name, _structure_name, _material_name, _outer_r, _inner_r, _axis,
                        _cylinder_min_position, _cylinder_max_position, _cylinder_center_u, _cylinder_center_v):
        if _axis == 'z':
            range_name = 'Zrange'
            u_center = 'Xcenter'
            v_center = 'Ycenter'
        elif _axis == 'x':
            range_name = 'Xrange'
            u_center = 'Ycenter'
            v_center = 'Zcenter'
        elif _axis == 'y':
            range_name = 'Yrange'
            u_center = 'Zcenter'
            v_center = 'Xcenter'
        _cst_macro_script = f'''
With Cylinder 
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}" 
     .Material "{_material_name}" 
     .OuterRadius "{_outer_r}" 
     .InnerRadius "{_inner_r}" 
     .Axis "{_axis}" 
     .{range_name} "{_cylinder_min_position}", "{_cylinder_max_position}" 
     .{u_center} "{_cylinder_center_u}" 
     .{v_center} "{_cylinder_center_v}" 
     .Segments "0" 
     .Create 
End With 
'''
        self.add_to_history(f'Define Cylinder: {_component_name} - {_structure_name}', _cst_macro_script)

    def create_ecylinder(self, _component_name, _structure_name, _material_name, _x_r, _y_r, _axis,
                         _cylinder_min_position, _cylinder_max_position, _cylinder_center_u, _cylinder_center_v):
        if _axis == 'z':
            range_name = 'Zrange'
            u_center = 'Xcenter'
            v_center = 'Ycenter'
        elif _axis == 'x':
            range_name = 'Xrange'
            u_center = 'Ycenter'
            v_center = 'Zcenter'
        elif _axis == 'y':
            range_name = 'Yrange'
            u_center = 'Zcenter'
            v_center = 'Xcenter'
        _cst_macro_script = f'''
With ECylinder 
     .Reset 
     .Name "{_structure_name}" 
     .Component "{_component_name}" 
     .Material "{_material_name}" 
     .Xradius "{_x_r}" 
     .Yradius "{_y_r}" 
     .Axis "{_axis}" 
     .{range_name} "{_cylinder_min_position}", "{_cylinder_max_position}" 
     .{u_center} "{_cylinder_center_u}" 
     .{v_center} "{_cylinder_center_v}" 
     .Segments "0" 
     .Create 
End With 
'''
        self.add_to_history(f'Define Elliptical Cylinder: {_component_name} - {_structure_name}', _cst_macro_script)

    def polygon3D(self, _curve_name, _polygon_name, point_list):
        _cst_macro_points = ''
        for xyz in point_list:
            _cst_macro_points += f'     .Point "{xyz[0]}", "{xyz[1]}", "{xyz[2]}" \n'

        _cst_macro_script = f'''
With Polygon3D 
     .Reset 
     .Version 10 
     .Name "{_polygon_name}" 
     .Curve "{_curve_name}"
''' + _cst_macro_points + '''
     .Create 
End With 
'''
        self.add_to_history(f"Define 3D Polygon {_curve_name}:{_polygon_name}", _cst_macro_script)

    def analytical_curve(self, _curve_name, _analytical_name, _x_expr,
                         _y_expr, _z_expr, _tmin, _tmax):
        _cst_macro_script = f'''
With AnalyticalCurve
     .Reset 
     .Name "{_analytical_name}" 
     .Curve "{_curve_name}" 
     .LawX "{_x_expr}" 
     .LawY "{_y_expr}" 
     .LawZ "{_z_expr}" 
     .ParameterRange "{_tmin}", "{_tmax}" 
     .Create
End With
'''
        self.add_to_history(f"Define Analytical Curve :{_curve_name}:{_analytical_name}", _cst_macro_script)

    def polygon(self, _curve_name, _polygon_name, point_list):
        _cst_macro_points = ''
        for xy in point_list:
            _cst_macro_points += f'     .Point "{xy[0]}", "{xy[1]}" \n'

        _cst_macro_script = f'''
With Polygon
     .Reset 
     .Name "{_polygon_name}" 
     .Curve "{_curve_name}"
''' + _cst_macro_points + '''
     .Create 
End With 
'''
        self.add_to_history(f"Define Polygon", _cst_macro_script)

    def covercurve(self, _component_name, _sheet_name, _material, _curve_name):
        _cst_macro_script = f'''
With CoverCurve
     .Reset 
     .Name "{_sheet_name}" 
     .Component "{_component_name}" 
     .Material "{_material}" 
     .Curve "{_curve_name}" 
     .DeleteCurve "True" 
     .Create
End With
'''
        self.add_to_history(f"Cover Curve by Sheet {_component_name}:{_sheet_name}", _cst_macro_script)

    def delete(self, _component_name, _structure_name):
        _cst_macro_script = f'''
Solid.Delete "{_component_name}:{_structure_name}" 
'''
        self.add_to_history(f"Delete {_component_name}:{_structure_name}", _cst_macro_script)

    def horn_antenna_template(self):
        _cst_macro_script = f'''
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

Mesh.FPBAAvoidNonRegUnite "True"
Mesh.ConsiderSpaceForLowerMeshLimit "False"
Mesh.MinimumStepNumber "5"

With Mesh
     .MeshType "PBA"
     '.MeshType "HexahedralTLM"
     .SetCreator "High Frequency"
End With

With MeshSettings
     .SetMeshType "Hex"
     '.SetMeshType "HexTLM"'
     .Set "RatioLimitGeometry", "20"
     .Set "Version", 1%
End With

'set the solver type
ChangeSolverType("HF Time Domain")
'----------------------------------------------------------------------------
'''
        self.add_to_history(f'Use Horn Antenna Template', _cst_macro_script)


if __name__ == '__main__':
    import time
    import os

    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')
    ###############################################################################
    # define CST file folder
    cst_dir = r'C:\CST_Projects\Temp'
    if not os.path.exists(cst_dir):
        os.makedirs(cst_dir)

    # dictionary form of parameters
    para_dict = {
        'taper_angle': 30,
        'horn_length': 30,
        'wall_thickness': 2.0,
        'waveguide_width': 20,
        'waveguide_height': 10,
        'fmin': '160/waveguide_width',
        'fmax': '200/waveguide_width',
        'fctr': '180/waveguide_width',
        'f1': 'fmin',
        'f2': '0.5*(fctr+fmin)',
        'f4': '0.5*(fctr+fmax)',
        'f5': 'fmax',
    }

    # define a CST instance
    test = cst()
    # # creat a new mws project
    # test.new_mws()
    # pass parameters to the CST file
    for para in para_dict:
        par_value = para_dict[para]
        test.store_para(para, par_value)
        # exec(para + '=par_value')
    # update the structure with parameters
    test.update_para()

    vars_all = test.get_parameters()
    vars_dict = dict(zip(vars_all[0], vars_all[1]))
    # extract all Parameters from CST ans store name/value in a dict
    # prj_vars = SimpleNamespace(**para_dict)
    # # works well only for direct definitions, not equations

    # #  apply a template for some basic settings
    # test.horn_antenna_template()

    # change some settings separately
    # tune off working plane
    test.working_plane_status(False)
    # set units
    test.unit('mm', 'GHz', 'ns')
    # set background
    test.background_vacuum()
    # set boundary
    test.boundaries_same(_boundary_type="expanded open", _xsymmetry="magnetic", _ysymmetry="electric",
                         _zsymmetry="none")
    # set pml type
    test.pml_specails(_pml_type='CenterNMonitors', f_for_open_space='fctr')

    # set frequency
    test.freq_range(vars_dict['fmin'], vars_dict['fmax'])  # either string or number for fmin and fmax
    # creat component
    test.create_component('Component1')
    # creat brick
    test.create_brick("Component1", "Solid1", "PEC", "-waveguide_width/2", "waveguide_width/2",
                      "-waveguide_height/2", "waveguide_height/2", 0, 6)
    # pick face
    test.pick_face("Component1", "Solid1", "1")
    # extrude
    test.extrude('Component1', 'Solid2', 'PEC', 'horn_length', vars_dict['taper_angle'])
    # add Solid1 and Solid2
    test.boolean_add("Component1", "Solid1", "Component1", "Solid2")
    # pick face 5 & 8
    test.pick_face("Component1", "Solid1", "5")
    test.pick_face("Component1", "Solid1", "8")
    # shell solid1
    test.shell("Component1", "Solid1", 'wall_thickness', _shell_type="Outside")
    # pick points 13, 15, and 16
    test.pick_point("Component1", "Solid1", '13')
    test.pick_point("Component1", "Solid1", '15')
    test.pick_point("Component1", "Solid1", '16')
    # define port
    test.define_wg_port_picks(1, 1, _polarization_angle=0, _ref_plane_dist=0, _orientation='zmin')
    # clear picks
    test.clear_picks()
    # define monitors
    test.define_efield_monitor_fdomain('fctr')
    test.define_hfield_monitor_fdomain('fctr')
    test.define_far_filed_monitor('fctr')
    test.define_efield_monitor_tdomain(0.02)
    # define solver parameters
    test.define_default_solver_para(_port_name='All')
    # display vswr and yz matrix
    test.vswr_display()
    test.yz_display()
    # show typical far-field cuts
    test.define_typical_ff_cuts()
    # save CST file first
    test.saveas_cst(cst_dir + '/test.cst')
    # run CST
    cstrun_start_time = time.time()
    test.run_cst()
    cstrun_elapsed_time = time.time() - cstrun_start_time
    print(f'Overall running time of this project is {cstrun_elapsed_time:.3f}s')
    # quit
    test.quit_cst()
    ###############################################################################
    elapsed_time = time.time() - start_time
    print(f'Overall time for this script is: {elapsed_time:.3f}s')
    print('Finished all!')
