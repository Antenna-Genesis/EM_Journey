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
    export_result_file_name='Parameter.csv'
    export_result_file_path1=export_result_dir+'\\'+'s11_'+export_result_file_name
    export_result_file_path2=export_result_dir+'\\'+'s21_'+export_result_file_name
    export_image_file_path='F:\\ydl\\PSO_TEST\\image_test'
    h = HFSS()
    h.init()
    h.solve('Setup1')
    Result_items1=["dB(S11)"]
    h.createSpreport('Sparameter1','Setup1',Result_items1)
    print('s11create+1')
    h.exportTofile('Sparameter1', export_result_dir,'s11_'+export_result_file_name )
    print('s11export+1')
    
    Result_items2=["dB(S21)"]
    h.createSpreport('Sparameter2','Setup1',Result_items2)
    print('s21create+1')
    h.exportTofile('Sparameter2', export_result_dir,'s21_'+export_result_file_name )
    print('s21export+1')
    
    h.combine('Sparameter2','Sparameter1',Result_items2)
    h.turnblue('Sparameter1',"dB(S21)")
   
    
    
    with open(export_result_file_path1) as f:
        text=f.readlines()
    data1=[]
    for line in text[1:]:
        f1, S11=line.strip().split(',')
        data1.append((f1, S11))
    data1=np.array(data1,dtype=float)#导出频率、s参数
    
    mask1=np.copy(data1)
    p3_1=mask1[np.where(mask1[:,1]==np.min(mask1[:,1])),0]
    
    mask1[np.where((mask1[:,0]<3.3)),1]=np.nan
    mask1[np.where((mask1[:,0]>3.7)),1]=np.nan#带宽为3.3-3.7
    p1=np.copy(mask1)
    p1[np.where(~np.isnan(p1[:,1])),1]=-10
    v1=mask1-p1      #与-10dB做差
    
    with open(export_result_file_path2) as f:
            text=f.readlines()
    data2=[]
    for line in text[1:]:
        f2, s21=line.strip().split(',')
        data2.append((f2, s21))
    data2=np.array(data2,dtype=float)
    
    mask2=np.copy(data2)
    p3_2=mask2[np.where(mask2[:,1]==np.min(mask2[:,1])),0]
    
    mask2[np.where((mask2[:,0]<3.2)),1]=np.nan
    mask2[np.where((mask2[:,0]>3.8)),1]=np.nan
    p2=np.copy(mask2)
    p2[np.where(~np.isnan(p2[:,1])),1]=-20
    v2=mask2-p2     
    
 
    
    value1=np.delete(v1,np.where(np.isnan(v1))[0],axis=0)
    value1=value1[:,1]
    value1[value1>0]=0
    finalval1=np.sum(value1<0)#v1值为s11曲线带宽的评估值
    
    value2=np.delete(v2,np.where(np.isnan(v2))[0],axis=0)
    value2=value2[:,1]
    value2[value2>0]=0
    finalval2=np.sum(value2<0)#v2值为s21曲线带宽的评估值
    
    finalval3=abs(p3_1[0,0]-freq)+abs(p3_2[0,0]-freq)
    #v3值为S11、S21中心频率差值
    print('finalval1',finalval1,'  finalval2',finalval2,'  finalval3',finalval3)
    
    r1=2;r2=1;r3=20;
    cost_function_value=-finalval1*r1-finalval2*r2+finalval3*r3
    #加权得到总评估值(由于总评估值与指标优劣之间基本为单调关系，最优值没有设置为0，评估值越小指标基本越好)
    #增加中心频率差值这一项主要是为了优化两条曲线的图像，使其最小值重合，否则经常出现两条曲线谷值均不在带内，一条单调增一条单调减的情况
    h.exportimage('Sparameter1',export_image_file_path,'cost='+str(cost_function_value))
    
    h.deleteAllreports()
    return cost_function_value
