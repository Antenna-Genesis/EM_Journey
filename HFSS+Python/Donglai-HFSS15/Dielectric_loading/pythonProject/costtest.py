# -*- coding: utf-8 -*-
from HFSS import HFSS
import time
import numpy as np


named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
time_string_file_name = time.strftime("%m_%d_%Y__%H_%M_%S", named_tuple)
export_result_dir='F:\\ydl\\PSO_TEST\\temp_test'
export_result_file_name='Parameter.csv'
export_result_file_path1=export_result_dir+'\\'+'s11_'+export_result_file_name
export_result_file_path2=export_result_dir+'\\'+'s21_'+export_result_file_name

freq=3.5


# h = HFSS()
# h.init()
# h.solve('Setup1')
# Result_items1=["dB(S11)"]
# h.createSpreport('Sparameter1','Setup1',Result_items1)
# print('s11create+1')
# h.exportTofile('Sparameter1', export_result_dir,'s11_'+export_result_file_name )
# print('s11export+1')

# Result_items2=["dB(S21)"]
# h.createSpreport('Sparameter2','Setup1',Result_items2)
# print('s21create+1')
# h.exportTofile('Sparameter2', export_result_dir,'s21_'+export_result_file_name )
# print('s21export+1')

# h.deleteAllreports()


with open(export_result_file_path1) as f:
        text=f.readlines()
data1=[]
for line in text[1:]:
    f1, S11=line.strip().split(',')
    data1.append((f1, S11))
data1=np.array(data1,dtype=float)

mask1=np.copy(data1)
p3_1=mask1[np.where(mask1[:,1]==np.min(mask1[:,1])),0]

mask1[np.where((mask1[:,0]<3.3)),1]=np.nan
mask1[np.where((mask1[:,0]>3.7)),1]=np.nan
p1=np.copy(mask1)
p1[np.where(~np.isnan(p1[:,1])),1]=-10
v1=mask1-p1

with open(export_result_file_path2) as f:
        text=f.readlines()
data2=[]
for line in text[1:]:
    f2, s21=line.strip().split(',')
    data2.append((f2, s21))
data2=np.array(data2,dtype=float)

mask2=np.copy(data2)
p3_2=mask2[np.where(mask2[:,1]==np.min(mask2[:,1])),0]

mask2[np.where((mask2[:,0]<3.3)),1]=np.nan
mask2[np.where((mask2[:,0]>3.7)),1]=np.nan
p2=np.copy(mask2)
p2[np.where(~np.isnan(p2[:,1])),1]=-20
v2=mask2-p2

value1=np.delete(v1,np.where(np.isnan(v1))[0],axis=0)
value1=value1[:,1]
finalval=np.sum(value1)

value1=np.delete(v1,np.where(np.isnan(v1))[0],axis=0)
value1=value1[:,1]
value1[value1>0]=0
finalval1=np.sum(value1)

value2=np.delete(v2,np.where(np.isnan(v2))[0],axis=0)
value2=value2[:,1]
value2[value2>0]=0
finalval2=np.sum(value2)

finalval3=abs(p3_1[0,0]-freq)+abs(p3_2[0,0]-freq)
print(p2)



