import time
import os
import numpy as np
import pandas as pd
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

project_name = 'coaxial_antenna'
data_dir = os.path.join(cst_dir, f'Data/{project_name}')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


fmin_time_file_name = f'{project_name}-fmin-runid-time-mesh-step.txt'
fmin_time_csvfile_name = f'{project_name}-fmin-time-mesh-step.csv'
fmin_time_file_path = os.path.join(data_dir, fmin_time_file_name)
fmin_time_csvfile_path = os.path.join(data_dir, fmin_time_csvfile_name)

freq_samples = 1
run_samples = 1
all_samples = run_samples * freq_samples
# to store fmin, run ID, time(s), mesh number, time steps, time delta(as)
freq_run_time = np.zeros((all_samples, 6))
f_max = 10
with open(fmin_time_file_path, 'a') as f:
    f.write("fmin   run ID  time(s)   mesh number   time steps   time delta(as)\n")
    f.write("------------------------------------------------------------------\n")

    for f_min_indx, f_min in enumerate(np.linspace(0, 9, num=freq_samples, endpoint=True)):
        for run_num in range(run_samples):
            # dictionary form of parameters
            para_dict = {
                'Probe_L': 25,
                'Coax_L': 25,
                'Probe_R': 0.43,
                'Coax_Outer_Ri': 1,
                'Coax_Outer_Ro': 1.2,
                'fmin': f_min,
                'fmax': f_max,
                'fctr': '(fmin+fmax)/2',
            }

            # define a CST instance and creat a new mws project
            test = cst_interface.cst()


            # pass parameters to the CST file
            for para in para_dict:
                par_value = para_dict[para]
                test.store_para(para, par_value)
                # exec(para + '=par_value')
            # update the structure with parameters
            test.update_para()
            # use default settings for antenna design
            test.horn_antenna_template()
            # # tune off working plane
            # test.working_plane_status(False)
            # # set units
            # test.unit('mm', 'GHz', 'ns')
            # # set background
            # test.background_vacuum()
            # # set boundary
            # test.boundaries_same(_boundary_type="expanded open", _xsymmetry="none", _ysymmetry="none", _zsymmetry="none")
            # set pml type
            test.pml_specails(_pml_type='Center', f_for_open_space='fctr')

            # set frequency
            test.freq_range('fmin', 'fmax')  # either string or number for fmin and fmax
            # creat component
            test.create_component('Ant')
            test.create_cylinder("Ant", "Probe", "PEC", "Probe_R", "0", 'z',
                         0, "Coax_L+Probe_L", 0, 0)
            test.create_cylinder("Ant", "Coax", "PEC", "Coax_Outer_Ro", "Coax_Outer_Ri", 'z',
                         0, "Coax_L", 0, 0)
            # define port
            test.define_wg_port_free(_port_num=1, _label_name='', _folder_name='', _mode_num=1, _adjust_pol=False,
                             _pol_ang=0, _ref_dist=0, _orientation='zmin', _xmin='-Coax_Outer_Ri', _xmax='Coax_Outer_Ri',
                             _ymin='-Coax_Outer_Ri', _ymax="Coax_Outer_Ri", _zmin=0, _zmax=0)

            # define monitors
            test.define_efield_monitor_fdomain('fctr')
            test.define_hfield_monitor_fdomain('fctr')
            test.define_far_filed_monitor('fctr')

            # define solver parameters
            # test.define_default_solver_para(_port_name='All')


            # save CST file first
            test.saveas_cst(cst_dir + f'/{project_name}.cst')
            # store number of mesh cells as a CST parameter
            test.store_mesh_nums()
            test.update_para()
            vars_all = test.get_parameters()
            vars_dict = dict(zip(vars_all[0], vars_all[1]))
            mesh_num = int(vars_dict['Mesh_Num_Total'])
            # run CST
            cstrun_start_time = time.time()
            test.run_cst()
            cstrun_elapsed_time = time.time() - cstrun_start_time
            run_time = round(cstrun_elapsed_time,2)
            file_dir = os.path.join(data_dir, f"{project_name}-input_signal_{f_min}GHz.txt")
        # if run_num == 0:
            test.export_ascii_1d(SelectTreeItem="1D Results\Port signals\i1", file_path= file_dir)
            input_signal=pd.read_csv(file_dir, skiprows=[0, 1], delim_whitespace=True, header=None)
            time_steps = input_signal.shape[0] # steps of discrete time
            # time delta, origianly in ns
            time_delta = int(input_signal.diff(axis=0).iat[1,1] * 1e9) 
            # store all wanted info to a ndarray
            freq_run_indx = f_min_indx * run_samples + run_num
            freq_run_time[freq_run_indx, 0] = f_min
            freq_run_time[freq_run_indx, 1] = run_num
            freq_run_time[freq_run_indx, 2] = run_time
            freq_run_time[freq_run_indx, 3] = mesh_num
            freq_run_time[freq_run_indx, 4] = time_steps
            freq_run_time[freq_run_indx, 5] = time_delta
            print(f'For fmin={f_min}GHz & run_ID={run_num}, overall time: {run_time}s, meshes: {mesh_num}, timesteps: {time_steps}, timedelta: {time_delta}as')
            time.sleep(5)
            # quit
            test.quit_cst()
            f.write(f'{f_min}GHz    {run_num}     {run_time}        {mesh_num}         {time_steps}          {time_delta}' + "\n")
freq_time_mesh_pd = pd.DataFrame(freq_run_time)
# average time for each time step
# freq_time_mesh_pd[6] = freq_time_mesh_pd[2] / freq_time_mesh_pd[4]
freq_time_mesh_mean = freq_time_mesh_pd.groupby(0)[[2,3,4,5]].mean()
freq_time_mesh_mean.columns = ['time(s)','mesh number','time steps','time delta(as)']
freq_time_mesh_mean.index=[f'{item}GHz' for item in freq_time_mesh_mean.index]
freq_time_mesh_mean.to_csv(fmin_time_csvfile_path)
###############################################################################
elapsed_time = time.time() - start_time
print(f'Overall time for this script is: {elapsed_time:.1f}s')
print('Finished all!')