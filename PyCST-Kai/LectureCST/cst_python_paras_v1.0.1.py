# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:49:57 2020
@author: kai.lu
"""
import warnings
import sys
import os
import numpy as np
import itertools
import pandas as pd
from skrf import Network
import shutil
import time
start_time = time.time()
######################################################################
# define location to store the CST file
cst_WorkDir = r"C:\CST_Projects\Temp"
cst_ProjectName = 'coaxial_antenna'
cst_file = os.path.join(cst_WorkDir, cst_ProjectName+'.cst')  # close this cst file before you start
# folder to store exported files
export_dir = os.path.join(cst_WorkDir, cst_ProjectName+'_Exported')

# command to run CST from command window
cst_Command = '"C:\Program Files (x86)\CST STUDIO SUITE 2019\CST DESIGN ENVIRONMENT.exe"'
# define vbs script for parameter control
cst_VbaScript = os.path.join(cst_WorkDir, cst_ProjectName+"_vba_script.bas")

# folder containing exported radiation files directly from CST
RadPath_raw = os.path.join(cst_WorkDir, cst_ProjectName, "Export", 'Farfield')

# file name: farfield_(f=fctr)_[1]
rad_filename_raw = 'farfield_(f=fctr)_[1].txt'
rad_filename_rawpath = os.path.join(RadPath_raw, rad_filename_raw)

# folder containing exported touchstone files directly from CST
snpPath_raw = os.path.join(*[cst_WorkDir, cst_ProjectName, 'Result', 'TOUCHSTONE files'])

# file name: MWS-run-0001
snp_filename_raw = 'MWS-run-0001.s1p'
snp_filename_rawpath = os.path.join(snpPath_raw, snp_filename_raw)

# snp folder to contain all snp files with RunID as names
snp_dir = os.path.join(export_dir, "Snp")
if not os.path.exists(snp_dir):
    os.makedirs(snp_dir)

# rad folder to contain all rad files with RunID as names
rad_dir = os.path.join(export_dir, "Rad")
if not os.path.exists(rad_dir):
    os.makedirs(rad_dir)

# define parameter ranges and sampling points
para_name_list = ['Probe_L', 'Coax_L']
para_value_list = [np.around(np.linspace(20, 30, 2, endpoint=True), decimals=2),
                   np.around(np.linspace(20, 30, 2, endpoint=True), decimals=2)]
if len(para_name_list) != len(para_value_list):
    warnings.warn('para_name_list and para_value_list must have same dimension!')
    sys.exit()
# generate all parameter combinations
para_com_list = list(itertools.product(*para_value_list))

# generate DataFrame to store all sets of parameters
para_pd = pd.DataFrame(para_com_list, columns=para_name_list)

# convert to new dictionary format for iteration
# this line can be omitted if you use DataFrame directly
para_dict_all = para_pd.to_dict('index')
# format of para_dict_all, {0:{'Probe_L': 20, 'Coax_L': 25}, 1:{...},...}

# define frequency unit for snp file processing
freq_unit = 'GHz'

# define port number for snp file processing
ant_indx_port2, ant_indx_port1 = 0, 0
# loop
for key, para_dict in para_dict_all.items():
    run_id = key + 1
    print(f'RunID: {run_id} -> {para_dict}')

    # empty results of snp and rad
    shutil.rmtree(snpPath_raw, ignore_errors=True)
    shutil.rmtree(RadPath_raw, ignore_errors=True)

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

    # load snp file
    snp_file_dir = os.path.join(snpPath_raw, snp_filename_raw)
    ntwk_full_band = Network(snp_file_dir)
    # change frequency unit
    ntwk_full_band.frequency.unit = freq_unit
    # rescale frequency according to pre-defined unit
    freq_full_band = ntwk_full_band.frequency.f_scaled
    snp_full_band = ntwk_full_band.s_db[:, ant_indx_port2, ant_indx_port1]
    # make sure all s11(dB) smaller than 0
    snp_full_band[snp_full_band > 0] = -10e-10

    snp_complex_full_band = ntwk_full_band.s[:, ant_indx_port2, ant_indx_port1]
    snp_complex_full_band[np.abs(snp_complex_full_band) > 1] = 1 - 10e-10

    snp_filename_new_path = os.path.join(snp_dir, f'RunID={str(run_id)}.s1p')
    shutil.copy(snp_filename_rawpath, snp_filename_new_path)

    rad_filename_new_path = os.path.join(rad_dir, f'RunID={str(run_id)}.txt')
    shutil.copy(rad_filename_rawpath, rad_filename_new_path)

    # pause 1 second to release mws
    time.sleep(1)

    # count simulation times
    print(f"Finished no. {run_id} of all simulations")

######################################################################
elapsed_time = time.time() - start_time
print('Overall time for this post-processing is: {}s'.format(elapsed_time))
print('Finished all!')
