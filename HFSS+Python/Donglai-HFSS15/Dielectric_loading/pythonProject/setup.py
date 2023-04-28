# -*- coding: utf-8 -*-
import time
import os
import shutil
from HFSS import HFSS
start_time = time.time()
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
time_string_file_name = time.strftime("%m_%d_%Y__%H_%M_%S", named_tuple)
print(f'This program started at: {time_string}')

hfss_file_dir = r"F:\ydl\PSO_TEST\dir_file\Temp"#name1
if not os.path.exists(hfss_file_dir):
    os.makedirs(hfss_file_dir)
hfss_file_name = f'PSO_TEST {time_string_file_name}'#name2
hfss_result_file_path = hfss_file_dir +'\\'+hfss_file_name+'.hfssresults'



export_result_dir = r"F:\ydl\PSO_TEST\dir_file\Result"#name3
if not os.path.exists(export_result_dir):
    os.makedirs(export_result_dir)
export_result_file_name = 'S Parameter.csv'#name4
export_result_file_path = export_result_dir+'\\'+export_result_file_name

hfss_Optimization_record_dir = r"F:\ydl\PSO_TEST\dir_file\Record"#name5
if not os.path.exists(hfss_Optimization_record_dir):
    os.makedirs(hfss_Optimization_record_dir)
hfss_Optimization_record_file_name = f'Record for simulations {time_string_file_name}.txt'

h = HFSS()
h.init()

#%% Set setup PSO and start optimization

# Set setup PSO and start optimization
from PSO import PSO

optimization_target='''***************************************************************\n
the target : Design a DRA operating HEM mode at 3.5 GHz based on PSO\n
***************************************************************\n'''

Optimization_variables='rad1','posz','d_die'

pso = PSO(Optimization_variables=Optimization_variables, n_dim=3, pop=10, max_iter=10,
          lb=[1,1,5], ub=[3,6,10], w=0.8, c1=0.5, c2=0.5,
          optimization_target=optimization_target, export_result_dir=export_result_dir,export_result_file_name=export_result_file_name,
          hfss_Optimization_record_dir=hfss_Optimization_record_dir, hfss_Optimization_record_file_name=hfss_Optimization_record_file_name)
pso.run()




# Optimization over and close the software
# h.closeProject()
elapsed_time = time.time() - start_time
print(f'Overall time for this script is: {elapsed_time:.3f}s')
print('Finished all!')

# #print("Files are: %s" %os.listdir(hfss_file_dir))
# #os.removedirs(Hfss_file_path)

# ##Clean temp folder
#shutil.rmtree(hfss_file_dir)
# #os.mkdir(hfss_file_dir)

# ##Clean hfss file result folder
shutil.rmtree(hfss_result_file_path)
# #os.mkdir(hfss_result_file_path)
