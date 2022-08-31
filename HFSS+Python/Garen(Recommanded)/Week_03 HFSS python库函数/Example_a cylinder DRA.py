# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:59:24 2021

@author: cyang58
"""

import time
import os
import shutil 
from HFSS import HFSS
start_time = time.time()
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(f'This program started at: {time_string}')

hfss_file_dir = r"D:\Cylinder_DRA_study\Temp"
if not os.path.exists(hfss_file_dir):
    os.makedirs(hfss_file_dir)
hfss_file_name = 'Cylinder_DRA'
hfss_result_file_path = hfss_file_dir +'\\'+hfss_file_name+'.aedtresults'

export_result_dir = r"D:\Cylinder_DRA_study\Result"
if not os.path.exists(export_result_dir):
    os.makedirs(export_result_dir)
export_result_file_name = 'S Parameter.csv'
export_result_file_path = export_result_dir+'\\'+export_result_file_name

hfss_Optimization_record_dir = r"D:\Cylinder_DRA_study\Record"
if not os.path.exists(hfss_Optimization_record_dir):
    os.makedirs(hfss_Optimization_record_dir)
hfss_Optimization_record_file_name = 'Record for simulations.txt'

h = HFSS()

# Launch ANSYS Electronics Desktop
h.launch()
print('Successfully open ANSYS Electronics Desktop')

# Set all variables
h.setVariable('DR_radius', 10, 'mm')
h.setVariable('DR_height', 20, 'mm')
h.setVariable('Monopole_position', 10, 'mm')
h.setVariable('Ground_radius', 40, 'mm')
h.setVariable('Ground_height', 2, 'mm')
h.setVariable('Monopole_radius', 0.635, 'mm')
h.setVariable('Monopole_height', 8, 'mm')
h.setVariable('Feed_height', 9, 'mm')
print('Successfully Set all variables')

# Set model
h.addMaterial('DK10', 10, 0.0032)
h.createCylinder('0mm','0mm','0mm','Ground_radius','-Ground_height','Z','Ground','copper','F')
h.createPolyprism('0mm','0mm', '0mm','DR_radius','DR_height','Z',0,'DR', 'DK10','')
h.createCylinder('Monopole_position','0mm','0mm','Monopole_radius','Monopole_height','Z','Monopole','copper','F')
h.subtractt('DR','Monopole')
h.createCylinder('Monopole_position','0mm','0mm','2.03mm','-Ground_height','Z','Ground_hole','vacuum','')
h.createCylinder('Monopole_position','0mm','0mm','2.03mm','-Feed_height','Z','Feed_substrate','teflon_based','')
h.createCylinder('Monopole_position','0mm','-Ground_height','2.8mm','-Feed_height+Ground_height','Z','Feed_outer','copper','F')
h.createCylinder('Monopole_position','0mm','0mm','Monopole_radius','-Feed_height','Z','Feed_inner','copper','F')
h.createCylinder('Monopole_position','0mm','-Feed_height','3mm','-2mm','Z','Port','pec','F')
face_id = h.getFacebyposition('Port','Monopole_position','0mm','-Feed_height') 
Monopole_po=h.getVariablevalue('Monopole_position')
Feed_he=h.getVariablevalue('Feed_height')
h.assignWaveport(face_id,Monopole_po,'0mm','-'+Feed_he,Monopole_po,'3mm','-'+Feed_he)
h.subtractf('Ground','Ground_hole')
h.subtractt('Feed_outer','Feed_substrate')
h.subtractt('Feed_substrate','Feed_inner')
# Set Exciation and radiation boundary
h.createRegion('30mm')
h.assignRadiationRegion()
print('Successfully set Model, exciation and radiation boundary')

# Set setup and analysis and solve
h.insertSetup('Setup1', '3.5GHz')
h.insertFrequencysweep('Setup1', '1GHz', '6GHz', '50MHz', 'Fast')
h.saveProject(hfss_file_dir, hfss_file_name)
h.fitAll()
hfss_run_start_time = time.time()
h.solve('Setup1')
hfss_run_elapsed_time = time.time() - hfss_run_start_time
print(f'Overall running time of this project is {hfss_run_elapsed_time:.3f}s')

Result_items=["dB(S11)"]
h.createSpreport('Sparameter','Setup1',Result_items)
h.exportTofile('Sparameter', export_result_dir, export_result_file_name)
print('Successfully Slove and export the result')
h.deleteAllreports()

#h.closeProject()
elapsed_time = time.time() - start_time
print(f'Overall time for this script is: {elapsed_time:.3f}s')
print('Finished all!')

#print("Files are: %s" %os.listdir(hfss_file_dir))
#os.removedirs(Hfss_file_path)

##Clean temp folder
#shutil.rmtree(hfss_file_dir)  
#os.mkdir(hfss_file_dir)

##Clean hfss file result folder
#shutil.rmtree(hfss_result_file_path)  
#os.mkdir(hfss_result_file_path)