import time
import os
import shutil
import numpy as np
import pandas as pd
def findWid(data):
    wid_list=[]
    eff_list=[]
    t = (np.argmax(data, axis=0))
    Maxgain=(data[t[1]][1])
    Wid=0
    limit=Maxgain-3
    for i in range(len(data)):
        if data[i][1]>=limit:
            eff_list.append(data[i][0])
        elif  len(eff_list):
            wid_list.append(max(eff_list)-min(eff_list))
            if (data[t[1]][0])<=max(eff_list) and (data[t[1]][0])>=min(eff_list) and ((min(eff_list))!=data[0][0])and ((max(eff_list))!=data[len(data)-1][0]):
                Wid=max(eff_list)-min(eff_list)
            if (data[t[1]][0])<=max(eff_list) and (data[t[1]][0])>=min(eff_list) and ((min(eff_list))==data[0][0]):
                for k in range(len(data)):
                    print('caution')
                    print(len(data)-1-k)
                    if data[len(data)-1-k][1]<limit and k!=0:
                        Wid=max(eff_list)-min(eff_list)+data[len(data)-1][0]-data[len(data)-k][0]
                        break
                    if data[len(data)-1-k][1]<limit and k==0:
                        Wid=max(eff_list)-min(eff_list)
                        break
            if (data[t[1]][0])<=max(eff_list) and (data[t[1]][0])>=min(eff_list) and ((max(eff_list))==data[len(data)-1][0]):
                for k in range(len(data)):
                    if data[k][1]<limit and k!=0:
                        Wid=max(eff_list)-min(eff_list)+data[k-1][0]
                        break
                    if data[k][1]<limit and k==0:
                        Wid=max(eff_list)-min(eff_list)
                        break


            eff_list=[]


    return [Maxgain,Wid]



