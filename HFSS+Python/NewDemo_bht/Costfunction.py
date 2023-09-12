# -*- coding: utf-8 -*-
"""
@author: YANG Chen
modify: bht
"""
from HFSS import HFSS
import numpy as np
import math as mt

def costfunction(X):
    Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
    export_result_dir = r"D:\Cylinder_DRA_study\Result"
    export_result_file_name = 's11.csv'
    export_result_file_path = export_result_dir + '\\' + export_result_file_name

    freq = 3.5
    h = HFSS()
    h.openProject("D:\Cylinder_DRA_study\Temp", "Cylinder_DRA") #打开HFSS
    h.init()

    for k in range(0, len(Optimization_variables)):
        variable = h.getVariablevalue(Optimization_variables[k])
        variable_value, variable_unit = h.convertVariabletovalueandunit(variable)
        h.changeVariablevalue(Optimization_variables[k], X[k], variable_unit)

    h.solve('Setup1')
    Result_items=["dB(S11)"]

    h.createSpreport('Sparameter','Setup1',Result_items)
    print('create+1')
    h.exportTofile('Sparameter', export_result_dir, export_result_file_name)
    print('export+1')

    with open(export_result_file_path) as f:
        text=f.readlines()
    data=[]

    for line in text[1:]:
        f, S11=line.strip().split(',')
        data.append((f, S11))
    data=np.array(data,dtype=float)
    mask=data[np.where((freq==data[:,0])),1]
    cost_function_value = (mask+35)**2
    #yangcheng 代码语法的简单写法，至于意义是什么，你去问他罢:(

    print(cost_function_value[0,0])
    h.deleteAllreports()
    h.closeProject() #关闭HFSS
    return cost_function_value[0,0]

if __name__ == '__main__':
    costfunction( [10,20,10] )