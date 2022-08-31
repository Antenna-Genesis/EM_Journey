# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 13:19:51 2021

@author: YANG Chen
"""
from HFSS import HFSS
import numpy as np
from Resultpostprocess import readFldfield
import math as mt

def costfunction(export_result_dir, export_result_file_name, export_result_file_path,
                 freq = 3.5):
    h = HFSS()
    h.init()
    h.solve('Setup1')
    Result_items=["dB(S11)"]
    h.createSpreport('Sparameter','Setup1',Result_items)
    print('create+1')
    h.exportTofile('Sparameter', export_result_dir, export_result_file_name)
    print('export+1')

    h.deleteAllreports()
    with open(export_result_file_path) as f:
        text=f.readlines()
    data=[]

    for line in text[1:]:
        f, S11=line.strip().split(',')
        data.append((f, S11))
    data=np.array(data,dtype=float)
    mask=np.copy(data)
    mask[:,1:2]=np.nan
    mask[np.where((freq==mask[:,0])),1]=-35
      #**************************************************
    #       the target : operating frequency is freq
    #**************************************************
    difference_value=data-mask
    difference_value=np.delete(difference_value,np.where(np.isnan(difference_value))[0],axis=0)
    difference_value[difference_value<0]=0
    difference_value=difference_value[:,1]
    cost_function_value=np.sum(difference_value**2)
    return cost_function_value
