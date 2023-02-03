import time
import os
import shutil
import numpy as np
import pandas as pd
import scipy.signal as sg
def pro_xoz(data):
    re_list=[]
    la_list=[]
    deg_list=[]
    data=np.array(data)
    for i in range(len(data[0])):
        if (i+1)%2==0:
            la_list.append(i)
            deg_list.append(data[1][i])
            # print(data[1][i])
        elif i!=0:
            # print(2)
            re_list.append(data[1][i])
            # print(data[1][i])
        else:
            continue
    # print(deg_list)
    # print(re_list)
    re_list=np.array(list(zip(deg_list,re_list)))
    re_list=re_list.astype(np.float)
    return re_list

def FindSPeak(data):
    peak_val=[]
    data_val=[]
    S_val=[]
    peak=[]
    for m in range(len(data)):
        data_val.append(data[m][1])
        peak.append(data[m][0])
    data_val=np.array(data_val)
    peak=np.array(peak)
    peak_index=sg.argrelmin(data_val)
    for i in range(len(peak_index)):
        peak_val.append(data_val[peak_index[i]])
        # print(peak_val)
        # print(peak)
        # print(peak_index[i])
        S_val.append(peak[peak_index[i]])
    return [S_val,peak_val]





