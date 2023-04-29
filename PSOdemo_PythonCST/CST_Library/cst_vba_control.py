# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:44:17 2020

@author: Kai
"""
import warnings
import sys
import os
import numpy as np
import itertools
import pandas as pd
# import h5py
# from scipy import interpolate
# from skrf import Network
import json
import shutil
import time


def convert_seconds(seconds):
    h = int(seconds//(60*60))
    m = int((seconds-h*60*60)//60)
    s = seconds-(h*60*60)-(m*60)
    return [h, m, s]


def cst_para_study(_cst_dir=r"C:\CST_Projects\Twist_Horn_2020",
                   _cst_project_name='Ridged_WG_C01D01',
                   _snp_rawfile_dir='Export',
                   _snp_rawfile_name='S-Parameters_S2,1',
                   _snp_file_format='txt',
                   _h5_enable=False,
                   _rad_enable=False,
                   _para_name_list=['Launcher_RidgeW', 'Launcher_RidgeGap'],
                   _para_value_list=[np.around(np.linspace(3, 4.5, 4, endpoint=True), decimals=2),
                                     np.around(np.linspace(0.5, 1, 1, endpoint=True), decimals=2), ]):
    '''
    h5 file and rad file handling is not ready
    '''


    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')
    ######################################################################

    # close this cst file before you start
    cst_file = os.path.join(_cst_dir, _cst_project_name + '.cst')
    # folder containing result files from CST
    data_dir = os.path.join(_cst_dir, f'Data/{_cst_project_name}')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # command to run CST from command window
    cst_Command = '"C:\Program Files (x86)\CST STUDIO SUITE 2019\CST DESIGN ENVIRONMENT.exe"'
    # define vbs script for parameter control
    cst_VbaScript = os.path.join(data_dir, _cst_project_name + "_vba_script.bas")
    
    
    # folder containing exported touchstone files directly from CST
    snpPath_raw = os.path.join(*[_cst_dir, _cst_project_name, _snp_rawfile_dir])
    
    # file name: MWS-run-0001
    # snp_filename_raw = 'S-Parameters_S2,1.txt'
    snp_filename_rawpath = os.path.join(snpPath_raw, f'{_snp_rawfile_name}.{_snp_file_format}')
    
    # # h5 file to be further processed
    # h5Path = os.path.join(data_dir, "H5")
    # if not os.path.exists(h5Path):
    #     os.makedirs(h5Path)
    # h5file_fullpath = os.path.join(h5Path, cst_project_name + ".h5")
    
    # snp folder to contain all snp files with RunID as names
    snp_dir = os.path.join(data_dir, "Snp")
    if not os.path.exists(snp_dir):
        os.makedirs(snp_dir)


    if len(_para_name_list) != len(_para_value_list):
        warnings.warn('para_name_list and para_value_list must have same dimension!')
        sys.exit()
    # generate all parameter combinations
    para_com_list = list(itertools.product(*_para_value_list))
    
    # generate DataFrame to store all sets of parameters
    para_pd = pd.DataFrame(para_com_list, columns=_para_name_list)
    para_all = os.path.join(data_dir, "all_paras.csv")
    para_pd.to_csv(para_all)
    
    # read or generate DataFrame to store the good parameters
    para_good_store = os.path.join(data_dir, "good_paras.csv")
    if os.path.isfile(para_good_store):
        para_pd_good = pd.read_csv(para_good_store)
        # remove the first column
        para_pd_good.drop(para_pd_good.columns[0], axis=1, inplace=True)
    else:
        para_pd_good = pd.DataFrame(columns=_para_name_list)
    
    # convert to new dictionary format for iteration
    # this line can be omitted if you use DataFrame directly
    para_dict_all = para_pd.to_dict('index')

    # make an intro file to store the history of parametric study
    # it applies for all results from the same parametric study
    intro_snpfile_name = 'RunID-Parameters.txt'
    intro_snpfile_path =  os.path.join(snp_dir, intro_snpfile_name)   
    # open(intro_snpfile_path, 'w').close() # empty the file 
    with open(intro_snpfile_path, 'a') as f:
        f.write('RunID  ->' + '  Parameters' + f"  {_para_name_list}" + " \n")

    run_id = 0
    # loop all sets of parameters
    for simu_indx, para_dict in para_dict_all.items():
        # store current parameters into a DataFrame
        current_para_set = pd.DataFrame([para_dict])
        # check whether the current set of parameters has been simulated
        current_para_in = pd.merge(para_pd_good, current_para_set, how='right', indicator='Exist')
        if current_para_in['Exist'][0] == 'both':
            print(f'Results of {para_dict} are ready, skip this parameter set.')
        else:
            cst_simu_start_time = time.time()
            run_id += 1
            para_pd_good = para_pd_good.append(para_dict, ignore_index=True)
            print(f'RunID: {run_id} -> {para_dict} -> parameter set: {simu_indx}')
            
            # empty results of snp and rad
            shutil.rmtree(snpPath_raw, ignore_errors=True)
            with open(cst_VbaScript, "w") as fvba:
                fvba.write('Sub Main\n')
                fvba.write('   OpenFile("' + cst_file + '")\n')
                for para in para_dict:
                    par_value = para_dict[para]
                    fvba.write(f'   StoreDoubleParameter "{para}", {par_value} \n')
                
                fvba.write('   RebuildOnParametricChange(True, True)\n')  # False, False
                fvba.write('   Solver.Start\n')
                fvba.write('End Sub\n')
            # calculate cst model
            os.system(cst_Command + " -m " + cst_VbaScript)
            # pause 5 second to release mws
            time.sleep(5)
            
            # store parameter information into a list and then a file name
            all_para_list = [f'{simu_indx}={para}' for simu_indx, para in para_dict.items()]
            # convert list to string
            all_para_info = ','.join(all_para_list)
            snp_filename_newpath = os.path.join(snp_dir, f'{all_para_info}.{_snp_file_format}')
            # copy snp result to a data folder
            shutil.copy(snp_filename_rawpath, snp_filename_newpath)
            #
            # with h5py.File(os.path.join(h5Path, cst_project_name + ".h5"), "a") as fileHandle:
            #     # create the root group in hdf5 output file given by the run_id 
            #     run_id_grp = fileHandle.create_group(str(run_id))
            #     snp_grp = run_id_grp.create_group(str('Snp'))
        
            #     # define atributes for this group
            #     metadata = {'Date': time.time(),
            #         'User': 'Kai',
            #         'OS': os.name}
            #     run_id_grp.attrs.update(metadata)
        
            #     # save the relevant parameters in the run_id root group
            #     para_set = run_id_grp.create_dataset('Parameters', data=json.dumps(para_dict), dtype=dt)
            #     para_set_value = para_set[()]
               
            #     # to verify the parameter info are stored successfully
            #     para_set_verify = json.loads(para_set_value)
    
            # record the information of parametric study for later study
            with open(intro_snpfile_path, 'a') as f:
                f.write(f"{run_id}         ->  {para_dict} -> simu_indx index {simu_indx}\n")
    
            cstrun_elapsed_time = time.time() - cst_simu_start_time
            run_time = round(cstrun_elapsed_time, 2)
            # count simulation times
            print(f"Finished number {run_id} (simu_indx index = {simu_indx}) of all simulations, in {run_time}s")
    # store simulated parameter sets
    para_pd_good.to_csv(para_good_store)
    ######################################################################
    elapsed_time = time.time() - start_time
    print('Overall time for this parametric study is: {}s'.format(elapsed_time))

def cst_para_pd(_cst_dir=r"C:\CST_Projects\Twist_Horn_2020",
                _cst_project_name='Ridged_WG_C01D01',
                _snp_rawfile_dir='Export',
                _snp_rawfile_name='S-Parameters_S1,1',
                _snp_file_format='txt',
                _h5_enable=False,
                _rad_enable=False,
                _para_pd=pd.DataFrame([[0, 1], [2, 3], [4, 5]], columns=['a', 'b'])):
    '''
    h5 file and rad file handling is not ready
    '''

    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')
    ######################################################################

    # close this cst file before you start
    cst_file = os.path.join(_cst_dir, _cst_project_name + '.cst')
    # folder containing result files from CST
    data_dir = os.path.join(_cst_dir, f'Data/{_cst_project_name}')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # command to run CST from command window
    cst_Command = '"C:\Program Files (x86)\CST STUDIO SUITE 2019\CST DESIGN ENVIRONMENT.exe"'
    # define vbs script for parameter control
    cst_VbaScript = os.path.join(data_dir, _cst_project_name + "_vba_script.bas")
    
    # folder containing exported touchstone files directly from CST
    snpPath_raw = os.path.join(*[_cst_dir, _cst_project_name, _snp_rawfile_dir])
    
    # snp_filename_raw = 'S-Parameters_S2,1.txt' or 'MWS-run-0001'
    snp_filename_rawpath = os.path.join(snpPath_raw, f'{_snp_rawfile_name}.{_snp_file_format}')
    
    # snp folder to contain all snp files with RunID as names
    snp_dir = os.path.join(data_dir, "Snp")
    if not os.path.exists(snp_dir):
        os.makedirs(snp_dir)

    # store all sets of parameters
    para_all = os.path.join(data_dir, "all_paras.csv")
    _para_pd.to_csv(para_all)
    
    # read or generate DataFrame to store the good parameters
    para_good_store = os.path.join(data_dir, "good_paras.csv")
    if os.path.isfile(para_good_store):
        para_pd_good = pd.read_csv(para_good_store)
        # remove the first column
        para_pd_good.drop(para_pd_good.columns[0], axis=1, inplace=True)
    else:
        para_pd_good = pd.DataFrame(columns=_para_pd.columns)

    # make an intro file to store the history of parametric study
    # it applies for all results from the same parametric study
    intro_snpfile_name = 'RunID-Parameters.txt'
    intro_snpfile_path =  os.path.join(snp_dir, intro_snpfile_name)   
    # open(intro_snpfile_path, 'w').close() # empty the file 
    with open(intro_snpfile_path, 'a') as f:
        f.write(f'RunID  ->  Parameters -> {_snp_rawfile_name}\n')
    
    para_set_indx_all = _para_pd.index
    run_id = 0
    # loop all sets of parameters
    for para_set_indx in para_set_indx_all:
        # store current parameters into a DataFrame
        current_para_set = _para_pd.iloc[para_set_indx, :].to_frame().T
        # store parameter information into a list and then a file name
        all_para_list = [f'{para}={current_para_set.at[para_set_indx, para]}' for para in current_para_set.columns]
        # convert list to string
        all_para_info = ','.join(all_para_list)
        
        # check whether the current set of parameters has been simulated
        para_check = pd.merge(para_pd_good, current_para_set, how='right', indicator='Exist')
        if para_check['Exist'][0] == 'both':
            print(f'Results of {all_para_info} are ready, skip this parameter set.')
        else:
            cst_simu_start_time = time.time()
            run_id += 1
            para_pd_good = para_pd_good.append(current_para_set)
            
            print(f'RunID: {run_id} -> {all_para_info} -> parameter set: {para_set_indx}')
            
            # empty results of snp and rad
            shutil.rmtree(snpPath_raw, ignore_errors=True)
            # write bas file with a new parameter set
            with open(cst_VbaScript, "w") as fvba:
                fvba.write('Sub Main\n')
                fvba.write('   OpenFile("' + cst_file + '")\n')
                for para in current_para_set.columns:
                    par_value = current_para_set.at[para_set_indx, para]
                    fvba.write(f'   StoreDoubleParameter "{para}", {par_value} \n')
                
                fvba.write('   RebuildOnParametricChange(True, True)\n')  # False, False
                fvba.write('   Solver.Start\n')
                fvba.write('End Sub\n')
            # run cst model
            os.system(cst_Command + " -m " + cst_VbaScript)
            # pause 5 second to release mws
            time.sleep(5)
            
            snp_filename_new_dir = os.path.join(snp_dir, f'{all_para_info}.{_snp_file_format}')
            try:
                # copy snp result to a data folder
                shutil.copy(snp_filename_rawpath, snp_filename_new_dir)
    
                with open(intro_snpfile_path, 'a') as f:
                    f.write(f"{run_id}         ->  {all_para_info} -> parameter set: {para_set_indx}\n")
        
                
                # store simulated parameter sets
                para_pd_good.to_csv(para_good_store)
            except Exception as inst:
                # print(type(inst))    # the exception instance
                # print(inst.args)     # arguments stored in .args
                print(inst)          # __str__ allows args to be printed directly,
                                     # but may be overridden in exception subclasses
                # x, y = inst.args     # unpack args
                # print('x =', x)
                # print('y =', y)
            run_time = time.time() - cst_simu_start_time
            hh, mm, ss = convert_seconds(run_time)
            # count simulation times
            print(f"Finished number {run_id} of all simulations, in {hh}h:{mm}m:{ss:.2f}s")
    ######################################################################
    elapsed_time = time.time() - start_time
    hh, mm, ss = convert_seconds(elapsed_time)
    print(f'Overall time for this parametric study is: {hh}h:{mm}m:{ss:.2f}s')


if __name__ == '__main__':
    
    # define parameter ranges and sampling points
    para_name_list = ['Launcher_RidgeW', 
                      'Launcher_RidgeGap', ]
    para_value_list = [np.around(np.linspace(3, 4.5, 4, endpoint=True), decimals=2),
                       np.around(np.linspace(0.5, 0.7, 1, endpoint=True), decimals=2),]
    if len(para_name_list) != len(para_value_list):
        warnings.warn('para_name_list and para_value_list must have same dimension!')
        sys.exit()
    # generate all parameter combinations
    para_com_list = list(itertools.product(*para_value_list))
    
    # generate DataFrame to store all sets of parameters
    para_pd0 = pd.DataFrame(para_com_list, columns=para_name_list)
    
    cst_para_pd(_cst_dir=r"C:\CST_Projects\Twist_Horn_2020",
                _cst_project_name='Ridged_WG_C01D01',
                _snp_rawfile_dir='Export',
                _snp_rawfile_name='S-Parameters_S1,1',
                _snp_file_format='txt',
                _h5_enable=False,
                _rad_enable=False,
                _para_pd=para_pd0)
    
    # cst_para_study(cst_dir=r"C:\CST_Projects\Twist_Horn_2020",
    #                 cst_project_name='Ridged_WG_C01D01',
    #                 snp_file_rawpath='Export',
    #                 snp_file_rawname='S-Parameters_S2,1',
    #                 snp_file_format='txt',
    #                 h5_enable=False,
    #                 rad_enable=False,
    #                 para_name_list=['Launcher_RidgeW', 'Launcher_RidgeGap'],
    #                 para_value_list=[np.around(np.linspace(3.5, 4.5, 4, endpoint=True), decimals=2),
    #                                   np.around(np.linspace(0.5, 1, 1, endpoint=True), decimals=2)])

    '''
    h5 file and rad file handling is not ready
    '''
