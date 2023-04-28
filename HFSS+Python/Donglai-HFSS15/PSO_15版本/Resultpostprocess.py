# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:11:17 2020

@author: cyang58
"""
import re
import numpy as np
import matplotlib.pyplot as plt
    
def BW(array, target):
    if array[int((len(array)-1)/2)]<-10:      
      L, R=int((len(array)-1)/2-1),int((len(array)-1)/2+1)
      while array[L] < target and L > -1:
        L-=1
      while (array[R] < target and R < (len(array)-1)):
        R+=1 
      return (R-L-2)/len(array)
    else:
      return 0
      
  
def convertVariabletovalueandunit(Var_name):
    val=float(re.findall(r"\-?\d+\.?\d*",Var_name)[0])
    unit=''.join(re.findall(r'[A-Za-z]', Var_name))
    return val,unit

def readRectradiationpattern(result_path, Filename):
    Fld_path=result_path+'\\'+Filename
    with open(Fld_path) as f:
        text=f.readlines()   
    return text   


def readFldfield(result_path, Filename):
    Fld_path=result_path+'\\'+Filename+".fld"
    with open(Fld_path) as f:
        text=f.readlines()
    value=float(''.join(text[1:]))    
    return value

def plot1DRectradiationpattern(text):
    data=[]
    for line in text[2:]:
        Deg,Gainphi,Gaintheta=line.split(',')
        data.append((Deg,Gainphi,Gaintheta))
    data=np.array(data,dtype=float)
    Deg,Gainphi,Gaintheta=zip(*data)
    plt.plot(Deg, Gainphi)
    plt.plot(Deg, Gaintheta)
    plt.grid()
    plt.show()
    
    
def plot3Dfieldpattern(result_path, Filename):
    Fld_path=result_path+'\\'+Filename+".fld"
    with open(Fld_path) as f:
        text=f.readlines()
#    # decide the unit from the first line
#    unit_mapping={'mm':1e-3,'cm':1e-2,'dm':1e-1}
#    for key in unit_mapping:
#        if key in text[0]:
#            unit=unit_mapping[key]
    # read the data    
    data=[]
    for line in text[2:]:
        x,y,z,Null,value=line.split(" ")
        data.append((x,y,z,value))
    data=np.array(data,dtype=float)
    
    data_grid=np.array(re.findall(r"\-?\d+\.?\d*",text[0]),dtype=float).reshape(3,3)
    Grid=(data_grid[1]-data_grid[0])/data_grid[2]
    
    print('MAX:{}'.format(max(10*np.log10(data[:,3]))))
    print('MIN:{}'.format(min(10*np.log10(data[:,3]))))
    x=data[:,0].reshape((int(Grid[0])+1,int(Grid[1])+1))
    y=data[:,1].reshape((int(Grid[0])+1,int(Grid[1])+1))
    value=10*np.log10(data[:,3]).reshape((int(Grid[0])+1,int(Grid[1])+1))
    # plot the result
    import matplotlib.pyplot as plt
    import matplotlib.animation as anima
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    figure = plt.figure()
    axes = Axes3D(figure)
    axes.plot_surface(x, y, value,cmap='rainbow')
    axes.set_zlim(min(10*np.log10(data[:,3])),max(10*np.log10(data[:,3])))
    plt.contourf(x, y, value, 10, zdir='z',offset=max(10*np.log10(data[:,3])),cmap='rainbow')
    plt.show()
    def rotate(angle):
       axes.view_init(azim=angle)
    rot_animation = anima.FuncAnimation(figure, rotate, frames=np.arange(0,363,3),interval=80)
    rot_animation.save(result_path+'/E_field_rotation.gif', dpi=220, writer='imagemagick')
#    rot_animation.save(result_path+'/E_field_rotation.gif', dpi=80, writer='pillow')
   
       
     
    
    