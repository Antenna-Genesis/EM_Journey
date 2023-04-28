import time
import sys
import os
import numpy as np
script_dir = os.path.dirname(os.path.realpath(__file__))
# get the dir of the py file
current_dir = script_dir  # get current dir

os.chdir("..")  # go up one dir layer
up_dir = os.getcwd()
from Library import cst_interface

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
    'WG_Tube_R': 5.8,
    'WG_Tube_L': 30,
    'WG_Ridge_W': 1.2,
    'WG_RidgeGap': 2.4,
    'fmin': 2,
    'fmax': 18
}

# define a CST instance and creat a new mws project
cst_temp = cst_interface.cst()

# pass parameters to the CST file
for para in para_dict:
    par_value = para_dict[para]
    cst_temp.store_para(para, par_value)
    # exec(para + '=par_value')
# update the structure with parameters
cst_temp.update_para()

# extract all Parameters from CST ans store name/value in a dict
vars_all = cst_temp.get_parameters()
vars_dict = dict(zip(vars_all[0], vars_all[1]))

# apply a template for some basic settings
cst_temp.horn_antenna_template()
# set PEC boundaries
cst_temp.boundaries_same(_boundary_type="electric", _xsymmetry="none", _ysymmetry="none", _zsymmetry="none")
# set background pec
cst_temp.background_pec()
# set frequency
cst_temp.freq_range('fmin', 'fmax')

# creat component
cst_temp.create_component('WG')
# build shapes
cst_temp.create_cylinder("WG", "WG_Tube", "Vacuum", "WG_Tube_R", "0", 'z',
                         0, "WG_Tube_L", 0, 0)
cst_temp.create_brick("WG", "WG_Ridge", "PEC", "-WG_Ridge_W/2", "WG_Ridge_W/2",
                      "-WG_Tube_R", "-WG_RidgeGap/2", 0, 'WG_Tube_L')

cst_temp.transform_mirror(_obj='WG:WG_Ridge', _center_x=0, _center_y=0, _center_z=0, _normalplane_x=0,
                          _normalplane_y=1, _normalplane_z=0, _keep_old=True,
                          _repetitions=1, _dest_comp='', _dest_material='', _obj_type='Shape')
cst_temp.boolean_add("WG", "WG_Ridge", "WG", "WG_Ridge_1")
cst_temp.boolean_subtract("WG", "WG_Tube", "WG", "WG_Ridge")

# define excitations
cst_temp.define_wg_port_free(_port_num=1, _label_name='', _folder_name='', _mode_num=2, _adjust_pol=False,
                             _pol_ang=0, _ref_dist=0, _orientation='zmin', _xmin='-WG_Tube_R', _xmax='WG_Tube_R',
                             _ymin='-WG_Tube_R', _ymax="WG_Tube_R", _zmin=0, _zmax=0)
cst_temp.define_wg_port_free(_port_num=2, _label_name='', _folder_name='', _mode_num=2, _adjust_pol=False,
                             _pol_ang=0, _ref_dist=0, _orientation='zmax', _xmin='-WG_Tube_R', _xmax='WG_Tube_R',
                             _ymin='-WG_Tube_R', _ymax="WG_Tube_R", _zmin='WG_Tube_L', _zmax='WG_Tube_L')
'''

'''
# define solver parameters
cst_temp.define_default_solver_para(_port_name='1')

# save CST file first
cst_temp.saveas_cst(cst_dir + '/Ridged_Cylindrical_WG_C01D01.cst')
# run CST
cst_temp.run_cst()
# # quit
cst_temp.quit_cst()
###############################################################################
elapsed_time = time.time() - start_time
print(f'Overall time for script is: {elapsed_time:.3f}s')
print('Finished all!')
