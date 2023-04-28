import time
import os
import shutil
from datetime import datetime
import numpy as np
import pandas as pd
import sys
# from Simu import sim
from Simuface import sim
import random
from OtherFun import pro_xoz
from OtherFun import FindSPeak
from findwidth import findWid
ser_path="D://baisq//2022_12_06"
DataSetSize=1000
DRmat_num=8
height=[]
eff_count=4000
# for i in range(50):
#     for m in range(DRmat_num):
#         height.append([])
#         for n in range(DRmat_num):
#             height[m].append(str(1 + (30 - 0.1) * random.random()) + 'mm')
# for i in range(1):
#     for m in range(DRmat_num):
#         height.append([])
#         for n in range(DRmat_num):
#             height[m].append('30mm')
for i in range(4000,8000):
    for k1 in range(4):
        height.append([])
        for k2 in range(4):
            height[k1].append([])
    for m in range(2):
       height.append([])
       for n in range(2):
            height[m][n]=str(2 + (32 - 2) * random.random()) + 'mm'
    for p in range(2,4):
        for q in range(2):
            height[p][q]=height[3-p][q]
    for x in range(4):
        for y in range(2,4):
            height[x][y]=height[x][3-y]
    sim(height, 5, 0, eff_count)
    ex_h=pd.DataFrame(height)
    data = pd.read_csv(ser_path+"//result//sim" + str(eff_count) + "//S Parameter" + str(eff_count) + ".csv",
                       header=None)
    data = np.array(data)
    data = np.delete(data, 0, axis=0)
    data = data.astype(np.float)
    r = np.amax(data, axis=0)
    t = (np.argmax(data, axis=0))
    if data[t[1]][1]<10:
        ex_h.to_csv(ser_path+"//result//sim"+str(eff_count)+"//height"+str(eff_count)+".csv")
        SPeak=FindSPeak(data)
        peaknum=[]
        Smin=[]
        fsolve=[]
        rad_pic1=[]
        rad_pic2=[]
        print(SPeak[0])
        print(SPeak[1])
        for m1 in range(len(SPeak[1][0])):
            if SPeak[1][0][m1]<-10:
                peaknum.append(m1)
        for m2 in range(len(peaknum)):
            print(SPeak[0][0][peaknum[m2]])
            sim(height, SPeak[0][0][peaknum[m2]], 1, eff_count,"rad_pat1_"+str(SPeak[0][0][peaknum[m2]])+".csv","rad_pat2_"+str(SPeak[0][0][peaknum[m2]])+".csv")
            data = pd.read_csv(ser_path+"//result//sim" + str(eff_count) + "//rad_pat1_"+str(SPeak[0][0][peaknum[m2]])+".csv",header=None)
            data = np.array(data)
            data = np.delete(data, 0, axis=0)
            data = data.astype(np.float)
            maxgain=[]
            r = np.amax(data, axis=0)
            t = (np.argmax(data, axis=0))
            # print(data[t[1]][1])
            rad1=findWid(data)
            data = pd.read_csv(
                ser_path+"//result//sim" + str(eff_count) + "//rad_pat2_" + str(SPeak[0][0][peaknum[m2]]) + ".csv",header=None)
            data = np.array(data)
            data = np.delete(data, 0, axis=0)
            data = data.astype(np.float)
            print(data)
            r = np.amax(data, axis=0)
            t = (np.argmax(data, axis=0))
            # print(data[t[1]][1])
            rad2=findWid(data)
            fsolve.append(SPeak[0][0][peaknum[m2]])
            Smin.append(SPeak[1][0][peaknum[m2]])
            rad_pic1.append(rad1)
            rad_pic2.append(rad2)
        para_list=[len(peaknum)]+fsolve+Smin+rad_pic1+rad_pic2
        print (para_list)
        ex_para=pd.DataFrame(para_list)
        ex_para.to_csv(ser_path+"//result//sim"+str(eff_count)+"//para"+str(eff_count)+".csv")
        height=[]
        eff_count = eff_count + 1
    else:
        height=[]
        os.remove(ser_path+"//result//sim" + str(eff_count) + "//S Parameter" + str(eff_count) + ".csv")
        continue

