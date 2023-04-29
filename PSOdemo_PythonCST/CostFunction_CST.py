import time
import sys
import os
import numpy as np
from CST_Library import cst_interface
import numpy as np
import math as mt
from math import log, exp
from openbox import sp
import csv
import wintest

def read_s11_from_exportreport(file=r'D:\DRAtest\s11.txt'):
    #从打出的txt中提取数据
    with open(file, encoding='utf-8') as file:
        content = file.read()
    sp=content.split()
    uu=0
    for spi in sp:
        if spi[len(spi)-1]<'9' and spi[len(spi)-1]>'0' and spi[0]!='S':
            break
        uu=uu+1
    sp=sp[uu:]

    f=[]
    s11=[]
    for i in range(len(sp)):
        if i%2==0:
            f.append(float(sp[i]))
        else:
            s11.append(float(sp[i]))
    return f,s11

def CostfuncForDRA(Op2, testx):
    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')

    current_dir = os.path.dirname(os.path.realpath(__file__))
    cstpos = current_dir + r'\DRAtest.cst'
    while True:
        cst_temp = cst_interface.cst()
        cst_temp.open_mws(cstpos)#打开cst文件
        time.sleep(5)
        if wintest.is_CST_open("DRAtest"): #直到打开成功
            break

    for i in range(len(Op2)):
       # print(Op2[i], testx[i])
        cst_temp.store_para(Op2[i], testx[i])
    cst_temp.update_para() #更新参数变量

    cst_temp.run_cst() #运行

    s11pos = current_dir + r'\DRAtest\s11.txt'
    cst_temp.export_ascii_1d("1D Results\S-Parameters\S1,1", s11pos)
    cst_temp.delete_result()
   # cst_temp.save_cst()
    cst_temp.quit_cst()
    wintest.close_cst_window("DRAtest")

    freq=3.5
    f,s11=read_s11_from_exportreport(s11pos)
    tab = np.array([f, s11])
    data=tab.T #读出数据
    mask = np.copy(data)
    mask[:, 1:2] = np.nan
    mask[np.where((freq == mask[:, 0])), 1] = -35

    difference_value = data - mask
    difference_value = np.delete(difference_value, np.where(np.isnan(difference_value))[0], axis=0)
    difference_value[difference_value < 0] = 0
    difference_value = difference_value[:, 1]
    cost_function_value = np.sum(difference_value ** 2)

    print(cost_function_value)

    elapsed_time = time.time() - start_time
    print(f'Overall time for script is: {elapsed_time:.3f}s')
    print('Finished all!')
    #关闭HFSS
    return cost_function_value

if __name__ == "__main__":
    Op2=['DR_r', 'DR_h', 'mono_h']
    print(CostfuncForDRA(Op2, [12,22,10]))
    time.sleep(5)
    print(CostfuncForDRA(Op2, [8, 20, 12]))

