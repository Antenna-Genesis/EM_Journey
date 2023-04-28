'''
Created on 2 Jan 2019

@author: carlos.vancoevorden
'''


'''
Created on 26 Oct 2018

@author: carlos.vancoevorden
'''
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import skrf as rf
from os import walk
import pandas as pd
import matplotlib

import matplotlib.cm as cm



class create_Polar(object):
    
    '''
    This buddy will read, extract data and plot polars
    '''
    
    
    def create_polarAx(self,name,fig,lims):
    
        fig.patch.set_facecolor('white')
        plt.gca().set_aspect('equal')

        font2 = {'family' : 'arial',
                'weight' : 'normal',
                'size'   : 70}
         
        plt.rc('font', **font2)
        # po = plt.tricontourf(triang, summed_Gain, cmap='jet', vmin=-30, vmax=10)
        
        dynamic_range = lims[1]-lims[0]
        circle_delta = lims[2]
        
        # i first normalize the fields to 5 db up the maximum
        
        #FF = 10*np.log10(Fields)
        
        
        
      
        self.maxGain = 0
        # print('outer ring is ' + str(self.maxGain))
       
        
        plt.axis('off')
        
        
        kk = 0
        
        # outer circle
        ##########################################################
        circle2 = plt.Circle((0.0, 0), dynamic_range + kk*self.maxGain, color='black',lw = 8,ls='-', fill = False)
        plt.gca().add_artist(circle2)
        ##########################################################
        
        #inner circles
        ##########################################################
        number_of_circles = int(dynamic_range/circle_delta)
        for n in range(int(number_of_circles)):
            if np.mod(n,2) == 0:
                circle2 = plt.Circle((0.0, 0), dynamic_range - (n+1)*circle_delta, color='black',lw = 4,ls='--', fill = False)
            else:
                circle2 = plt.Circle((0.0, 0), dynamic_range - (n+1)*circle_delta, color='grey',lw = 4,ls='--', fill = False)
            plt.gca().add_artist(circle2)
            
            if np.mod(n,2) == 0:
                
                t = plt.text((dynamic_range - (n+1)*circle_delta)*np.cos(3*np.pi/4), (dynamic_range - (n+1)*circle_delta)*np.sin(3*np.pi/4), str(int((lims[1]-circle_delta*(n+1)))), \
                 fontsize = 60, horizontalalignment='center', rotation = (0))
        
                t.set_bbox(dict(facecolor='white', alpha=0.))
        #Lines circles
        ##########################################################
        number_of_lines = 12
        for n in range(number_of_lines):

            plt.plot([0, (dynamic_range + kk*self.maxGain)*np.cos(2*np.pi*n/number_of_lines)], \
                     [0, (dynamic_range + kk*self.maxGain)*np.sin(2*np.pi*n/number_of_lines)], 'k--', lw=4)
        ##########################################################
        

        rad_outer_text =  (dynamic_range + kk*self.maxGain)*1.1   
        if 'theta' in name:
            
            for n in range(number_of_lines-1):
        ##########################################################
                t = plt.text(rad_outer_text*np.cos(2*np.pi*(n+1)/number_of_lines), \
                         rad_outer_text*np.sin(2*np.pi*(n+1)/number_of_lines)-0, \
                         str(int(n+1)*30), \
                         fontsize=60, horizontalalignment='center',verticalalignment='center', \
                         rotation = (360*(n+1)/number_of_lines)-np.sign(np.sin(int(n+1)*np.pi/6))*90)
                t.set_bbox(dict(facecolor='white', alpha=0.))
                
            t = plt.text(rad_outer_text*np.cos(0), \
                         rad_outer_text*np.sin(0)-0, \
                         str(0), \
                         fontsize=60, horizontalalignment='center',verticalalignment='center', rotation = (0*(n+1)/number_of_lines))
            
            t.set_bbox(dict(facecolor='white', alpha=0.))
            
#             t = plt.text((dynamic_range + kk*self.maxGain)*1.3*np.cos(np.pi/2 + 0), \
#             (dynamic_range + kk*self.maxGain)*1.3*np.sin(-np.pi/2 +0), \
#             'phi (deg)', \
#             fontsize=40, horizontalalignment='center', rotation = (0))    
#             t.set_bbox(dict(facecolor='white', alpha=0.))
        else:    
            for n in range(number_of_lines-1):
        ##########################################################
                t = plt.text(rad_outer_text*np.cos(np.pi/2 + 2*np.pi*(n+1)/number_of_lines), \
                    rad_outer_text*np.sin(np.pi/2 + 2*np.pi*(n+1)/number_of_lines), \
                    str(int(np.sign(np.sin(int(n+1)*np.pi/6))*(np.abs(int(np.log10(360*(n+1)/number_of_lines)/np.log10(180))*180-np.mod(360*(n+1)/number_of_lines,180))))), \
                    fontsize=60, horizontalalignment='center',verticalalignment='center', rotation = (360*(n+1)/number_of_lines))
                
                t.set_bbox(dict(facecolor='white', alpha=0.))
            
            t = plt.text(rad_outer_text*np.cos(np.pi/2), \
                         rad_outer_text*np.sin(np.pi/2), \
                         str(0), \
                         fontsize=60, horizontalalignment='center',verticalalignment='center', rotation = (0*(n+1)/number_of_lines))
            t.set_bbox(dict(facecolor='white', alpha=0.))
            
#             t = plt.text((dynamic_range + kk*self.maxGain)*1.3*np.cos(np.pi/2 + 0), \
#             (dynamic_range + kk*self.maxGain)*1.3*np.sin(-np.pi/2 +0), \
#             'theta (deg)', \
#             fontsize=40, horizontalalignment='center', rotation = (0))       
#             
#             t.set_bbox(dict(facecolor='white', alpha=0.))
            
            

        
        #import matplotlib.image as image
        #import matplotlib.cbook as cbook
        
        # datafile = cbook.get_sample_data('C:\Measurements/logo.png', asfileobj=False)
        # im = image.imread(datafile)
        # fig.figimage(im, 1600, 0, zorder=3)



    def __init__(self,filename,options,exp):
        '''
        Constructor
        '''
        plt.close('all_height')
        fig,ax = plt.subplots()
        
        fig.set_size_inches(36., 20.25)    
        plt.tick_params(axis='both', which='major', labelsize=80)  
        
        
        self.create_polarAx(options.labelang,fig,[float(options.lims[0]),float(options.lims[1]),float(options.lims[2])])
        
        Ns = len(options.data)
        
        ax.set_prop_cycle('color',plt.cm.jet(np.linspace(0,1,Ns)))
        
        for n in range(Ns):
            lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  + \
                  '  ' + exp.samples[int(options.data[n].split(',')[0])-1].sampleName[0]  + \
                  '  ' + options.labelang + '=' + options.data[n].split(',')[2] + ' '+ \
                  options.data[n].split(',')[5] + 'MHz'
            
            if options.normalize == 'yes':
                options.data2Plot[n][:,1] -= options.data2Plot[n][:,1].max()
                
            
            options.data2Plot[n][options.data2Plot[n][:,1]<float(options.lims[0]),1] = float(options.lims[0])
            
            if options.labelang == 'phi':
                x = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.cos(options.data2Plot[n][:,0]+np.pi/2)
                y = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.sin(options.data2Plot[n][:,0]+np.pi/2)
            else:
                
                x = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.cos(options.data2Plot[n][:,0])
                y = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.sin(options.data2Plot[n][:,0])
            
            
            if options.data[n].split(',')[3] != 'jet':
                
                plt.plot(x,y,color = options.data[n].split(',')[3] , \
                     lw = 7, ls = options.data[n].split(',')[4], label = lab)
            else:
                plt.plot(x,y,lw = 7, ls = options.data[n].split(',')[4], label = lab)
            
            
        # uncomment below to add labels
        # plt.legend(bbox_to_anchor=( 1, 1), loc = 0, borderaxespad=0., ncol = 1,prop={'size':40})
        
        plt.savefig(filename, pad_inches = 0, transparent=True)
        plt.close()
        
class create_Polar2D(object):
    
    '''
    This buddy will read, extract data and plot polars
    '''
    
    
    def create_polarAx(self,name,fig,lims):
    
        fig.patch.set_facecolor('white')
        plt.gca().set_aspect('equal')

        font2 = {'family' : 'arial',
                'weight' : 'normal',
                'size'   : 70}
         
        plt.rc('font', **font2)
        # po = plt.tricontourf(triang, summed_Gain, cmap='jet', vmin=-30, vmax=10)
        
        dynamic_range = lims[1]-lims[0]
        circle_delta = lims[2]
        
        # i first normalize the fields to 5 db up the maximum
        
        #FF = 10*np.log10(Fields)
        
        
        
      
        self.maxGain = 0
        # print('outer ring is ' + str(self.maxGain))
       
        
        plt.axis('off')
        
        
        kk = 0
        
        # outer circle
        ##########################################################
        circle2 = plt.Circle((0.0, 0), dynamic_range + kk*self.maxGain, color='black',lw = 8,ls='-', fill = False)
        plt.gca().add_artist(circle2)
        ##########################################################
        
        #inner circles
        ##########################################################
        number_of_circles = int(dynamic_range/circle_delta)
        for n in range(int(number_of_circles)):
            if np.mod(n,2) == 0:
                circle2 = plt.Circle((0.0, 0), dynamic_range - (n+1)*circle_delta, color='black',lw = 4,ls='--', fill = False)
            else:
                circle2 = plt.Circle((0.0, 0), dynamic_range - (n+1)*circle_delta, color='grey',lw = 4,ls='--', fill = False)
            plt.gca().add_artist(circle2)
            
            if np.mod(n,2) == 0:
                
                t = plt.text((dynamic_range - (n+1)*circle_delta)*np.cos(3*np.pi/4), (dynamic_range - (n+1)*circle_delta)*np.sin(3*np.pi/4), str(int((lims[1]-circle_delta*(n+1)))), \
                 fontsize = 60, horizontalalignment='center', rotation = (0))
        
                t.set_bbox(dict(facecolor='white', alpha=0.))
        #Lines circles
        ##########################################################
        number_of_lines = 12
        for n in range(number_of_lines):

            plt.plot([0, (dynamic_range + kk*self.maxGain)*np.cos(2*np.pi*n/number_of_lines)], \
                     [0, (dynamic_range + kk*self.maxGain)*np.sin(2*np.pi*n/number_of_lines)], 'k--', lw=4)
        ##########################################################
        

        rad_outer_text =  (dynamic_range + kk*self.maxGain)*1.1   
      
            
        for n in range(number_of_lines-1):
    ##########################################################
            t = plt.text(rad_outer_text*np.cos(2*np.pi*(n+1)/number_of_lines), \
                     rad_outer_text*np.sin(2*np.pi*(n+1)/number_of_lines)-0, \
                     str(int(n+1)*30), \
                     fontsize=60, horizontalalignment='center',verticalalignment='center', \
                     rotation = (360*(n+1)/number_of_lines)-np.sign(np.sin(int(n+1)*np.pi/6))*90)
            t.set_bbox(dict(facecolor='white', alpha=0.))
            
        t = plt.text(rad_outer_text*np.cos(0), \
                     rad_outer_text*np.sin(0)-0, \
                     str(0), \
                     fontsize=60, horizontalalignment='center',verticalalignment='center', rotation = (0*(n+1)/number_of_lines))
        
        t.set_bbox(dict(facecolor='white', alpha=0.))
            
#             t = plt.text((dynamic_range + kk*self.maxGain)*1.3*np.cos(np.pi/2 + 0), \
#             (dynamic_range + kk*self.maxGain)*1.3*np.sin(-np.pi/2 +0), \
#             'phi (deg)', \
#             fontsize=40, horizontalalignment='center', rotation = (0))    
#             t.set_bbox(dict(facecolor='white', alpha=0.))
       



    def __init__(self,filename,options,exp):
        '''
        Constructor
        '''
        plt.close('all_height')
        fig,ax = plt.subplots()
        
        fig.set_size_inches(36., 20.25)    
        plt.tick_params(axis='both', which='major', labelsize=80)  
        
        
        self.create_polarAx(options.labelang,fig,[float(options.lims[0]),float(options.lims[1]),float(options.lims[2])])
        
        Ns = len(options.data)
        
        ax.set_prop_cycle('color',plt.cm.jet(np.linspace(0,1,Ns)))
        
        for n in range(Ns):
            lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  + \
                  '  ' + exp.samples[int(options.data[n].split(',')[0])-1].sampleName[0]  + \
                  '  ' + options.labelang + '=' + options.data[n].split(',')[2] + ' '+ \
                  options.data[n].split(',')[5] + 'MHz'
            
            if options.normalize == 'yes':
                options.data2Plot[n][:,1] -= options.data2Plot[n][:,1].max()
                
            
            options.data2Plot[n][options.data2Plot[n][:,1]<float(options.lims[0]),1] = float(options.lims[0])
            
            if options.labelang == 'phi':
                x = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.cos(options.data2Plot[n][:,0]+np.pi/2)
                y = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.sin(options.data2Plot[n][:,0]+np.pi/2)
            else:
                
                x = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.cos(options.data2Plot[n][:,0])
                y = (options.data2Plot[n][:,1]-float(options.lims[0])) * np.sin(options.data2Plot[n][:,0])
            
            
            if options.data[n].split(',')[3] != 'jet':
                
                plt.plot(x,y,color = options.data[n].split(',')[3] , \
                     lw = 7, ls = options.data[n].split(',')[4], label = lab)
            else:
                plt.plot(x,y,lw = 7, ls = options.data[n].split(',')[4], label = lab)
            
            
        # uncomment below to add labels
        # plt.legend(bbox_to_anchor=( 1, 1), loc = 0, borderaxespad=0., ncol = 1,prop={'size':40})
        
        plt.savefig(filename, pad_inches = 0, transparent=True)

class create_Cartesians(object):
    '''
    classdocs
    '''

    
    def __init__(self,filename,options,exp):
        '''
        Constructor
        '''
        fig = plt.figure()
        
        ax = fig.add_subplot(1, 1, 1)
        
        
        Ns = len(options.data)
        self.ax = ax
        self.fig = fig
        bands = [[float(band.split(',')[0]),float(band.split(',')[1]) ] for band in options.bands]
        xlim = [float(x) for x in options.limx]
        ylim = [float(x) for x in options.limy]
        reqs = [[float(band.split(',')[2]),float(band.split(',')[3]) ] for band in options.bands]
 
        ax.set_prop_cycle('color',plt.cm.jet(np.linspace(0,1,Ns)))
        
        
        for n in range(Ns):
            
             
#             if int(options.data[n].split(',')[1].split('-')[0]) == int(options.data[n].split(',')[1].split('-')[1]):
#                 lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  
#             else:
#                 lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  + \
#                       '-' + \
#                       exp.labels[int(options.data[n].split(',')[1].split('-')[1])-1]
                  
#                   
            if int(options.data[n].split(',')[1].split('-')[0]) == int(options.data[n].split(',')[1].split('-')[1]):
                lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  + \
                   '  ' + exp.samples[int(options.data[n].split(',')[0])-1].sampleName[0]
            else:
                lab = exp.labels[int(options.data[n].split(',')[1].split('-')[0])-1]  + \
                      '-' + \
                      exp.labels[int(options.data[n].split(',')[1].split('-')[1])-1]  + \
                      '  ' + exp.samples[int(options.data[n].split(',')[0])-1].sampleName[0] 
                  
            
            
#             if int(options.data[n].split(',')[1].split('-')[0])==1 and options.magnitude == 'VSWR':
#                 
#                 shift = 0.0
#                 corr = 0.0
#                 print('warning doing tricks:',shift,corr)
#             elif int(options.data[n].split(',')[1].split('-')[0])==1 and options.magnitude == 'efficiency':
#                 print('warning doing tricks')
#                 shift = 0.0
#                 corr = 0.0    
#                 print('warning doing tricks:',shift,corr)
#             else:
#                 shift = 0.00
#                 corr = 0   
#                 print('warning doing tricks:',shift,corr)      
            shift = 0.0
            corr = 0  
            intervalo = (options.data2Plot[n][:,0]>=xlim[0]-shift) & (options.data2Plot[n][:,0]<=xlim[1]-shift)
            

            if options.data[n].split(',')[2] != 'jet':
            
                plt.plot(options.data2Plot[n][intervalo,0] +shift ,options.data2Plot[n][intervalo,1]+corr,color = options.data[n].split(',')[2] , \
                     lw = 7, ls = options.data[n].split(',')[3], label = lab)
            else:
                plt.plot(options.data2Plot[n][intervalo,0] +shift ,options.data2Plot[n][intervalo,1]+corr, \
                     lw = 7, ls = options.data[n].split(',')[3], label = lab)
            
        
        # # 
        # 
        # 

                  
        font = {'family' : 'arial',
                'weight' : 'normal',
                'size'   : 80}
         
        #plt.rc('font', **font)
        
            
        plt.sca(ax)                          
       
        fig.canvas.draw()
        
        plt.grid(True,lw=4 ,ls ='--')
        plt.grid(b=True, which='minor', color='r', linestyle='--')
        ax.set_axisbelow(True)
        plt.setp(ax.spines.values(), linewidth=8)
        plt.xlabel(options.labelx, fontdict=font)
        plt.ylabel(options.labely, fontdict=font)
                 
        plt.xlim([xlim[0],xlim[1]])
        plt.ylim([ylim[0],ylim[1]])
        plt.xticks(np.arange(xlim[0],xlim[1]+xlim[2],xlim[2]))
        
        plt.yticks(np.arange(ylim[0]+ylim[2], ylim[1]+ylim[2] ,ylim[2]))
        
        
        
        fig.set_size_inches(36., 20.25)    
        plt.tick_params(axis='both', which='major', labelsize=80)  

        if options.magnitude == 'VSWR':
            
            plt.yticks(np.arange(ylim[0]+ylim[2], ylim[1] +ylim[2] ,ylim[2]))
            
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f')) 
             
        elif options.magnitude == 'Isolation':
            plt.yticks(np.arange(ylim[0], ylim[1] ,ylim[2]))
            #from matplotlib.ticker import StrMethodFormatter
            ax.invert_yaxis()
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f')) # No decimal places
            
                
        elif options.magnitude == 'ECC_circuital':
            plt.yticks(np.arange(ylim[0]+ylim[2], ylim[1] + ylim[2] ,ylim[2]))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f')) # No decimal places
        
        
        
           
        plt.legend(bbox_to_anchor=( 1, 1), loc = 1, borderaxespad=0., ncol = 1,prop={'size':40})
        from matplotlib.patches import Rectangle
                  
        for k,ba in enumerate(bands):
            someX, someY = ba[0], ylim[1]
            plt.gca().add_patch(Rectangle((someX , someY), ba[1]-ba[0], ylim[0]-ylim[1],\
                facecolor="lightsteelblue",alpha = 0.4,linewidth = 0))
                                                   
            plt.gca().add_line(plt.Line2D([bands[k][0],bands[k][1]],[reqs[k][1],reqs[k][1]] \
                ,linewidth = 10, color = 'red', ls ='--',zorder = 100)) 
            
            plt.gca().add_line(plt.Line2D([bands[k][0],bands[k][1]],[reqs[k][0],reqs[k][0]] \
                ,linewidth = 10, color = 'green', ls ='--',zorder = 100))        
        #plt.savefig(Graph_folder + grap_filename, bbox_inches='tight')
        
        import matplotlib.image as image
        import matplotlib.cbook as cbook
                
        datafile = cbook.get_sample_data('C:\Dropbox\Design_Works\Github\Pantools\PaPa\logo.png', asfileobj=False)
        im = image.imread(datafile)
        fig.figimage(im, 2900, 0, zorder=3)
        
        
        plt.savefig(filename, pad_inches = 0, transparent=True)
        plt.close()
        
class read_plot_file(object):
    
    '''
        Constructor
    '''
    def __init__(self,filename):
        
        with open(filename) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        

        f.close()
        content = [x for x in [x.rstrip() for x in content] if x] 
        
        self.samples = content.count('Begin Sample')
        
        
        
        self.Nplots = content.count('NewPlot')
        self.Nplots_Cartesians = content.count('cartesian')
        self.Nplots_Polars = content.count('polar')
        self.Nexports2D = content.count('Export2D')
        self.Nexports1D = content.count('Export1D')
        self.Nexports = self.Nexports2D + self.Nexports1D
        
        self.options = ['']*(self.Nplots+self.Nexports)
        
      
        # first the plots
        
        ind_ini = [i for i, x in enumerate(content) if x == "NewPlot"]
        ind_fin = [i for i, x in enumerate(content) if x == "EndPlot"]
               

        for n in range(self.Nplots):
            
            line_ini = ind_ini[n]
            line_end = ind_fin[n]
            
           
            subcontent = content[line_ini:line_end]
            
            print(subcontent)
            
            if subcontent[1] == 'cartesian':
                Ndata = len([x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x])
                self.options[n] = cartesian_object(subcontent[1],Ndata)
                self.options[n].magnitude = subcontent[2]
                
                self.options[n].limx = [x for i, x in enumerate(subcontent) if 'limx' in x][0].split('=')[1].replace(" ", "").split(',')
                self.options[n].limy = [x for i, x in enumerate(subcontent) if 'limy' in x][0].split('=')[1].replace(" ", "").split(',')
                
                self.options[n].labelx = [x for i, x in enumerate(subcontent) if 'labelx' in x][0].split('=')[1].strip()
                self.options[n].labely = [x for i, x in enumerate(subcontent) if 'labely' in x][0].split('=')[1].strip()
                
                self.options[n].bands = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'bands' in x]
                
                self.options[n].data = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
                
            elif subcontent[1] == 'polar':
                Ndata = len([x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x])
                self.options[n] = polar_object(subcontent[1],Ndata)
                self.options[n].magnitude = subcontent[2]
                
                self.options[n].data = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                self.options[n].normalize = [x for i, x in enumerate(subcontent) if 'normalize' in x][0].split('=')[1].strip()
                self.options[n].labelang  = [x for i, x in enumerate(subcontent) if 'labelang' in x][0].split('=')[1].strip()
        
                self.options[n].lims = [x for i, x in enumerate(subcontent) if 'limsRad' in x][0].split('=')[1].replace(" ", "").split(',')
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
        
        
            elif subcontent[1] == 'cartesian2D':
                Ndata = 1
                self.options[n] = cartesian2D_object(subcontent[1],Ndata)
                self.options[n].magnitude = subcontent[2]
                
                
                self.options[n].limz = [x for i, x in enumerate(subcontent) if 'limz' in x][0].split('=')[1].replace(" ", "").split(',')
                
                self.options[n].labelx = [x for i, x in enumerate(subcontent) if 'labelx' in x][0].split('=')[1].strip()
                self.options[n].labely = [x for i, x in enumerate(subcontent) if 'labely' in x][0].split('=')[1].strip()
                
                                
                self.options[n].data = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
                
            elif subcontent[1] == 'polar2D':
                Ndata = 1
                self.options[n] = Polar2D_object(subcontent[1])
                self.options[n].magnitude = subcontent[2]
                
                
                self.options[n].limz = [x for i, x in enumerate(subcontent) if 'limz' in x][0].split('=')[1].replace(" ", "").split(',')
                
                self.options[n].labelx = [x for i, x in enumerate(subcontent) if 'labelx' in x][0].split('=')[1].strip()
                self.options[n].labely = [x for i, x in enumerate(subcontent) if 'labely' in x][0].split('=')[1].strip()
                
                                
                self.options[n].data = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
        
            elif subcontent[1] == 'polar3D':
                Ndata = 1
                self.options[n] = cartesian3D_object(subcontent[1],Ndata)
                self.options[n].magnitude = subcontent[2]
                
                
                self.options[n].limz = [x for i, x in enumerate(subcontent) if 'limz' in x][0].split('=')[1].replace(" ", "").split(',')
                
                self.options[n].camera = [x for i, x in enumerate(subcontent) if 'camera' in x][0].split('=')[1].replace(" ", "").split(',')
                self.options[n].light = [x for i, x in enumerate(subcontent) if 'light' in x][0].split('=')[1].replace(" ", "").split(',')
                
                           
                self.options[n].data = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
                
                
        # Then the exports the plots
        
        ind_ini = [i for i, x in enumerate(content) if x == "NewExport"]
        ind_fin = [i for i, x in enumerate(content) if x == "EndExport"]
               

        for n in range(self.Nplots,self.Nplots+self.Nexports):
            
            line_ini = ind_ini[n - self.Nplots]
            line_end = ind_fin[n - self.Nplots]
            
           
            subcontent = content[line_ini:line_end]
            
            print(subcontent)
            
            if subcontent[1] == 'Export2D':
                
                self.options[n] = Export2D_object(subcontent[1])
                self.options[n].magnitude = subcontent[2]
                
                self.options[n].data= [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'data' in x]
                
                
                self.options[n].prefix = [x for i, x in enumerate(subcontent) if 'prefix' in x][0].split('=')[1].strip()
                self.options[n].sufix = [x for i, x in enumerate(subcontent) if 'sufix' in x][0].split('=')[1].strip()
            
class cartesian_object(object):
    
    def __init__(self,tipo,Ndata):
        
        self.type = tipo
        self.magnitude = []
        
        self.labelx = []
        self.labely = []
        
        self.limx = []
        self.limy = []
        
        self.bands = []
        self.reqs = []
        self.data  = []
        self.data2Plot  = ['']*Ndata
        self.prefix = []
        self.sufix = []
        
        
class cartesian2D_object(object):
    
    def __init__(self,tipo,Ndata):
        
        self.type = tipo
        self.magnitude = []
        
        self.labelx = []
        self.labely = []
        
        self.limz = []
        self.data  = []
        self.data2Plot  = ['']*Ndata
        self.prefix = []
        self.sufix = []
        
        
class Polar2D_object(object):
    
    def __init__(self,tipo):
        
        self.type = tipo
        self.magnitude = []
        
        self.labelx = []
        self.labely = []
        
        self.limx = []
        self.limy = []
        self.limz = []
        self.data  = []
        self.data2Plot  = ['']
        self.prefix = []
        self.sufix = []        
        
class cartesian3D_object(object):
    
    def __init__(self,tipo,Ndata):
        
        self.type = tipo
        self.magnitude = []
        
        self.light = []
        self.camera = []
        

        self.limz = []
        self.data  = []
        self.data2Plot  = ['']*Ndata
        self.prefix = []
        self.sufix = []
                
        
class polar_object(object):
    
    def __init__(self,tipo,Ndata):
        
        self.type = tipo
        
        self.magnitude = []
        
        self.normalized = []
        self.labelang = []
        
        self.lims = []
        
        self.data  = []
        self.data2Plot  = []
        self.reqs = []
        
        self.prefix = []
        self.sufix = []
        
        self.data2Plot  = ['']*Ndata
class Export2D_object(object):
    
    def __init__(self,tipo):
        
        self.type = tipo
        self.magnitude = []
        self.freq = []
        self.prefix = []
        self.sufix = []
        self.data2Plot  = ['']
        
class get_data_to_plot(object):
    
    
    def  __init__(self,opts,exp,total_df):
    
        # i assume al antennas have same l
        
        
 
        if opts.magnitude == 'VSWR':
            # i need to find the VSWR data and store in opts
            
            #first i will create an numpy array to store all_height the data.
            
            # i will get the first file to get the frequencies
                  
            
            nd = len(opts.data)
            
            
            for n in range(nd):
                
                sample_index = int(opts.data[n].split(',')[0])-1
                
                thepath = exp.samples[sample_index].sparsFolderVSWR[0]
                files_infolder = next(walk(thepath))[2] 
                
                
                t1 = '_' + opts.data[n].split(',')[1].split('-')[0] + '_'
                t2 = '_' + opts.data[n].split(',')[1].split('-')[0] + '.' 
        
                files_with_port = [s for s in files_infolder if (t1 in s) or (t2 in s)]
            
                M = rf.Network(thepath+'/' + files_with_port[0])
                
                if opts.data[n].split(',')[1].split('-')[0] == files_with_port[0].split('_')[1]:
                
                    prt = 0
                else:
                    
                    prt = 1
                if 'dB' in opts.labely:
                    VSWR = M.s_db[:,prt,prt]
                else:
                    VSWR = (1 + M.s_mag[:,prt,prt])/(1-M.s_mag[:,prt,prt])
                
                nf = M.frequency.npoints
                
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = M.f/1e9
                
                opts.data2Plot[n][:,1] =[x for x in VSWR]
                
                
            
            
            
        elif opts.magnitude == 'Isolation':
            # i need to find the VSWR data and store in opts
            
            #first i will create an numpy array to store all_height the data.
            
            
            
            # i will get the first file to get the frequencies

            nd = len(opts.data)
         
            for n in range(nd):
                
                sample_index = int(opts.data[n].split(',')[0])-1
                
                thepath = exp.samples[sample_index].folderSpars[0]
                files_infolder = next(walk(thepath))[2] 
                
                
              
                
                
                
                fileIso = 'P_' + opts.data[n].split(',')[1].split('-')[0] + \
                 '_' +opts.data[n].split(',')[1].split('-')[1] + '.s2p'
    
                M = rf.Network(thepath +'\\' + fileIso)
                
                nf = M.frequency.npoints
                                
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = M.f/1e9
                
                opts.data2Plot[n][:,1] =[-x for x in M.s_db[:,0,1] ]
            
            
        elif opts.magnitude == 'ECC_circuital':
            # i need to find the VSWR data and store in opts
            
            #first i will create an numpy array to store all_height the data.
            
            
            
            # i will get the first file to get the frequencies

            nd = len(opts.data)
         
            for n in range(nd):
                
                sample_index = int(opts.data[n].split(',')[0])-1
                
                thepath = exp.samples[sample_index].folderSpars[0]
                files_infolder = next(walk(thepath))[2] 
                
                
              
                
                
                
                fileIso = 'P_' + opts.data[n].split(',')[1].split('-')[0] + \
                 '_' +opts.data[n].split(',')[1].split('-')[1] + '.s2p'
    
                M = rf.Network(thepath +'/' + fileIso)
                
                nf = M.frequency.npoints
                                
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = M.f/1e9
                
                
                ECC = (np.abs(M.s[:,0,1]*np.conjugate(M.s[:,0,0])+M.s[:,1,1]*np.conjugate(M.s[:,1,0]))**2)/ \
                (  (1 - np.abs(M.s[:,0,0])**2  - np.abs(M.s[:,1,0])**2 ) * (1 - np.abs(M.s[:,1,1])**2   - np.abs(M.s[:,0,1])**2)     )
          
                  
               
                
                opts.data2Plot[n][:,1] =[x for x in 10*np.log10(ECC)] 
            
        elif opts.magnitude == 'Efficiency':
            
            aux_df = total_df[2]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            nd = len(opts.data)
            
      
            for n in range(nd):
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                
                antenna_label = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+1]

                if '%' in opts.labely:
                    opts.data2Plot[n][:,1] =[x for x in aux_df[columna][aux_df.Antenna == antenna_label].values] 
                else:
                    opts.data2Plot[n][:,1] =[10*np.log10(x/100) for x in aux_df[columna][aux_df.Antenna == antenna_label].values]
        
        elif opts.magnitude == 'SectorAvGain':
            
            aux_df = total_df[4]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            nd = len(opts.data)
            
      
            for n in range(nd):
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                
                antenna_label = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+1]

                
                opts.data2Plot[n][:,1] =[x for x in aux_df[columna][aux_df.Antenna == antenna_label].values] 
          
            
        elif opts.magnitude == 'Peakgain':
            
            aux_df = total_df[1]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            
            nd = len(opts.data)
            

            
            for n in range(nd):
                
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                
                antenna_label = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+1]
                               
                opts.data2Plot[n][:,1] =[x for x in aux_df[columna][aux_df.Antenna == antenna_label].values] 
        
        
        elif opts.magnitude == 'Coverage':
            
            aux_df = total_df[3]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            
            nd = len(opts.data)
            

            
            for n in range(nd):
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                antenna_label = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+1]
                
                opts.data2Plot[n][:,1] =[x for x in aux_df[columna][aux_df.Antenna == antenna_label].values]
                
                
                
                
        elif opts.magnitude == 'ECCFields':
            
            aux_df = total_df[5]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            
            nd = len(opts.data)
            

            
            for n in range(nd):
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                antenna_label1 = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                antenna_label2 = exp.labels[int(opts.data[n].split(',')[1].split('-')[1])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+2]
                
                if 'dB' in opts.labely:
                    opts.data2Plot[n][:,1] =[10*np.log10(x) for x in aux_df[columna][(aux_df['Antenna 1'] == antenna_label1)&(aux_df['Antenna 2'] == antenna_label2)].values] 
                else:
                    opts.data2Plot[n][:,1] =[x for x in aux_df[columna][(aux_df['Antenna 1'] == antenna_label1)&(aux_df['Antenna 2'] == antenna_label2)].values] 
                
            
        elif opts.magnitude == 'Ripple':
            
            aux_df = total_df[0]
            
            aux_df=aux_df.dropna()
            
            nf = aux_df.Freq.drop_duplicates().values.shape[0]
            
            nd = len(opts.data)

            
            for n in range(nd):
                # aux_df.AnglePlot[n] = np.zeros([nf,2])
                opts.data2Plot[n] = np.zeros([nf,2])
                opts.data2Plot[n][:,0] = aux_df.Freq.drop_duplicates().values
                
                antenna_label = exp.labels[int(opts.data[n].split(',')[1].split('-')[0])-1]
                columna = aux_df.columns[int(opts.data[n].split(',')[0])+3]
                kk = aux_df[columna][(aux_df.Antenna == antenna_label)& \
                                     (aux_df.Angle == int(opts.data[n].split(',')[-1].split('-')[1]))& \
                                     (aux_df.Cut == opts.data[n].split(',')[-1].split('-')[0])].values
                opts.data2Plot[n][:,1] =[x for x in kk]
        
        
        
        elif opts.type == 'polar':
            
            nd = len(opts.data)

            
            for n in range(nd):
                
                antenna =  exp.samples[int(opts.data[n].split(',')[0])-1].antennas[int(opts.data[n].split(',')[1])-1]
                
                component = opts.magnitude
                print('you are plotting ' +  component)
                antenna.Theta,antenna.Phi,antenna.active_field = antenna.get_fields(float(opts.data[n].split(',')[-1])*1e6, \
                            component, exp.samples[int(opts.data[n].split(',')[0])-1].sphere_sampling)
                
 
                slc =  antenna.get_slice((opts.labelang,float(opts.data[n].split(',')[2])),exp.samples[int(opts.data[n].split(',')[0])-1].decimated_sphere_sampling)
                nang = len(slc.data)
                
                opts.data2Plot[n] = np.zeros([nang,2])
                
                opts.data2Plot[n][:,1] = slc.data
                opts.data2Plot[n][:,0] = slc.angledata*np.pi/180
                
#                 if opts.labelang== 'theta':
#                     
#                     opts.data2Plot[n][:,0] = np.linspace(-np.pi, np.pi, nang)
#                 else: 
#                 
#                     opts.data2Plot[n][:,0] = np.linspace(0, 2*np.pi, nang)
#                     
                    
                    
        elif opts.type == 'cartesian2D' or opts.type == 'polar3D' or  opts.type == 'Export2D':
            
                    
            antenna =  exp.samples[int(opts.data[0].split(',')[0])-1].antennas[int(opts.data[0].split(',')[1])-1]
                
            component = opts.magnitude
            
            if  any([component in comp for comp in exp.samples[int(opts.data[0].split(',')[0])-1].components_available]):
                
                antenna.Theta,antenna.Phi,antenna.active_field = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          component,exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                opts.data2Plot[0] = antenna.active_field # np.vstack((antenna.active_field,antenna.active_field[0]))
            
            elif component  == 'Vertical' or component == 'Horizontal':
                # E(Phi). Real part    E(Phi). Imaginary part    E(Theta). Real part    E(Theta). Imaginary part
                antenna.Theta,antenna.Phi,EThetaReal = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          'E(Theta). Real part', \
                                                          exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                antenna.Theta,antenna.Phi,EThetaImag = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          'E(Theta). Imaginary part', \
                                                          exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                antenna.Theta,antenna.Phi,EPhiReal = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          'E(Phi). Real part', \
                                                          exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                antenna.Theta,antenna.Phi,EPhiImag = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          'E(Phi). Imaginary part', \
                                                          exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                ETheta = EThetaReal + 1j*EThetaImag
                EPhi = EPhiReal + 1j*EPhiImag
    
                
                theta = np.linspace(-np.pi,np.pi,ETheta.shape[1])
                phi = np.linspace(0,np.pi,ETheta.shape[0])
                
                Th,Ph = np.meshgrid(theta,phi)
                
                # with this I calculate the electric 
                EVertical = np.multiply(ETheta,np.sin(np.abs(Th)))
                # EHorizontal es la suma vectorial de 
                # np.multiply(ETheta,np.cos(np.abs(Th))) en la componente rho y 
                # EPhi en la componente phi
                
                #now i calculate radiation intensities
                UVertical =1/(2*120*np.pi)*np.power(np.abs(EVertical),2)
                UHorizontal =1/(2*120*np.pi)*(np.power(np.abs(np.multiply(ETheta,np.cos(np.abs(Th)))),2) + \
                                            np.power(np.abs(EPhi),2))
                                            
                #now i need input power
                # i read Gain to calculate efficiency
                antenna.Theta,antenna.Phi,GaindB = antenna.get_fields(float(opts.data[0].split(',')[-1])*1e6, \
                                                          'Gain . dB', \
                                                          exp.samples[int(opts.data[0].split(',')[0])-1].sphere_sampling)
                
                GainLin = np.power(10,GaindB/10)
                
                eff = self.calculate_integral(GainLin, Th, Ph)/(4*np.pi)
                
                Utotal = 1/(240*np.pi)*(np.power(np.abs(ETheta),2) + np.power(np.abs(EPhi),2))
                Pin = self.calculate_integral(Utotal, Th, Ph)/eff
                print(eff*100,Pin)
                GV = 4*np.pi*UVertical/Pin
                GH = 4*np.pi*UHorizontal/Pin

                
            
                if component  == 'Vertical':
                    opts.data2Plot[0] = 10*np.log10(GV+10e-20)
                else:
                    opts.data2Plot[0] = 10*np.log10(GH+10e-20)


            else:
                print('Do not be malakas and plot a magnitude available in Satimo Gain file or vertical or horizontal')


    def calculate_integral(self,Field,theta,phi): 
        '''
        This does integrals :)
        '''
        delta_th = np.abs(theta[0][0]-theta[0][1])*np.ones(theta.shape)
        delta_ph = np.abs(phi[0][0]-phi[1][0])*np.ones(phi.shape)
         
        solid_angle =np.multiply(np.sign(np.sin(theta)),
                                np.multiply(np.sin(theta),
                                np.multiply(delta_th,delta_ph)))
         
 
         
        Integral = np.sum(np.multiply(Field,solid_angle))  

                
        return Integral
        
        

class create_Cartesian2D(object):
    
        def __init__(self,filename,options,exp):
            
            fig, ax = plt.subplots()
    
            fig.patch.set_facecolor('white')
            plt.gca().set_aspect('equal')
            
            
            
            font2 = {'family' : 'arial',
                    'weight' : 'normal',
                    'size'   : 16}
             
            plt.rc('font', **font2)
            
            
            
            min_value = float(options.limz[0])
            max_value = float(options.limz[1])
            
            color_dimension = options.data2Plot # change to desired fourth dimension
            minn, maxx = min_value, max_value
            norm = matplotlib.colors.Normalize(minn, maxx)
            # 
            matplotlib.colors.LightSource(55,45)
            m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
            m.set_array([])
            #     
            Ntheta = options.data2Plot[0].shape[1]
            Nphi = options.data2Plot[0].shape[0]
                                              
            mod_data1 = options.data2Plot[0][:,int((Ntheta-1)/2)::]
            mod_data2 = options.data2Plot[0][:,0:int((Ntheta-1)/2)+1]
            
            data2plot = np.vstack((mod_data1,np.fliplr(mod_data2)))
            data2plot = np.transpose(data2plot)
            #data2plot = np.flipud(np.fliplr(data2plot))
            
            theta = np.linspace(0,180,data2plot.shape[0])
            phi = np.linspace(0,360,data2plot.shape[1])
            
            Ph,Th = np.meshgrid(phi,theta)
            plt.contourf(Ph,Th,data2plot,int(options.limz[2]),vmin=min_value, vmax=max_value,cmap=cm.jet)
              
            cb = plt.colorbar(m,fraction=0.02, pad=0.04)
            cb.set_clim(min_value, max_value)
            #         
            cb.set_label(label= 'Gain [dBi]',size = 20)
            cb.ax.tick_params(labelsize = 20)
            
            plt.xticks(ticks= np.linspace(0,360,13), labels=None)
            plt.yticks(ticks= np.linspace(0,180,7), labels=None)
            
            plt.grid(b=None, which='major', axis='both',linestyle = '--',linewidth = 1)
            
            plt.xlabel('Phi [deg]', font2)
            plt.ylabel('Theta [deg]', font2)
            
            ax.xaxis.grid(True, zorder=1)
            ax.yaxis.grid(True, zorder=1)
                    
            fig.set_size_inches(18*0.8, 10.125*0.8)   
            
            plt.savefig(filename, pad_inches = 0, transparent=True)
    
            
            plt.clf()
            plt.close(fig)
        

class export_2D(object):
    
    def __init__(self,name,F):
    

        Ntheta = F.shape[1]
        Nphi = F.shape[0]
                                          
        mod_data1 = F[:,int((Ntheta-1)/2)::]
        mod_data2 = F[:,0:int((Ntheta-1)/2)+1]
        
        data2plot = np.vstack((mod_data1,np.fliplr(mod_data2)))
        data2plot = np.transpose(data2plot)

        data2plot = np.hstack((data2plot,[[v] for v in data2plot[:,0]]))
        
        theta = np.linspace(0,180,data2plot.shape[0])
        phi = np.linspace(0,360,data2plot.shape[1])



        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(name + '.xlsx', engine='xlsxwriter')

        row_labels = ['phi = ' + str(ang) for ang in phi]
        col_labels = ['theta = ' + str(ang) for ang in theta]
        
        df = pd.DataFrame(data = data2plot ,columns = row_labels,index = col_labels)
        
        
        df.to_excel(writer, sheet_name='Gain_3D',index = True)
        
        writer.save()

class create_Polar_3D(object):

    
    def __init__(self,filename,options,exp):
           
        from mpl_toolkits.mplot3d import Axes3D
    

        from matplotlib import cm
        from matplotlib.patches import FancyArrowPatch
        from mpl_toolkits.mplot3d import proj3d
        
        class Arrow3D(FancyArrowPatch):
            def __init__(self, xs, ys, zs, *args, **kwargs):
                FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
                self._verts3d = xs, ys, zs
        
            def draw(self, renderer):
                xs3d, ys3d, zs3d = self._verts3d
                xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
                self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
                FancyArrowPatch.draw(self, renderer)
        
        def Rx(phi):
            return np.array([[1, 0, 0],
                             [0, np.cos(phi), -np.sin(phi)],
                             [0, np.sin(phi), np.cos(phi)]])
        
        def Ry(theta):
            return np.array([[np.cos(theta), 0, np.sin(theta)],
                             [0, 1, 0],
                             [-np.sin(theta), 0, np.cos(theta)]])
        
        def Rz(psi):
            return np.array([[np.cos(psi), -np.sin(psi), 0],
                             [np.sin(psi), np.cos(psi), 0],
                             [0, 0, 1]])
        
        # define origin
        o = np.array([0,0,0])
        
        # define ox0y0z0 axes
        x0 = np.array([1.5,0,0])
        y0 = np.array([0,1.5,0])
        z0 = np.array([0,0,1.5])
        
        
        
        # produce figure
        #fig = plt.figure()
        #ax = fig.add_subplot(111, projection='3d')
        
        FS = 30
        
        
        fig = plt.figure(figsize=plt.figaspect(0.5)*1.5) #Adjusts the aspect ratio and enlarges the figure (text does not enlarge)
        ax = fig.gca(projection='3d')     
        # plot ox0y0z0 axes
        a = Arrow3D([o[0], x0[0]], [o[1], x0[1]], [o[2], x0[2]], mutation_scale=20, arrowstyle='-|>', color='k')
        ax.add_artist(a)
        a = Arrow3D([o[0], y0[0]], [o[1], y0[1]], [o[2], y0[2]], mutation_scale=20, arrowstyle='-|>', color='k')
        ax.add_artist(a)
        a = Arrow3D([o[0], z0[0]], [o[1], z0[1]], [o[2], z0[2]], mutation_scale=20, arrowstyle='-|>', color='k')
        ax.add_artist(a)
        
        
        
        
        text_options = {'horizontalalignment': 'center',
                        'verticalalignment': 'center',
                        'fontsize': FS,'zorder': 100}
        
        # add label for origin
        #ax.text(0.0,0.0,-0.05,r'$o$', **text_options)
        
        # add labels for x axes
        t = ax.text(1.1*x0[0],1.1*x0[1],1.1*x0[2],r'$x$', **text_options)
        t.set_bbox(dict(alpha=0.0))
        # add lables for y axes
        t = ax.text(1.1*y0[0],1.1*y0[1],1.1*y0[2],r'$y$', **text_options)
        t.set_bbox(dict(alpha=0.0))
        # add lables for z axes
        t = ax.text(1.1*z0[0],1.1*z0[1],1.1*z0[2],r'$z$', **text_options)
        t.set_bbox(dict(alpha=0.0))
        
        
        # show figure
        ax.view_init(elev=float(options.camera[0]), azim=float(options.camera[1]))
        ax.set_axis_off()
        
        min_value = float(options.limz[0])
        max_value = float(options.limz[1])
            
      
        
        #options.data2Plot[np.where(np.array(options.data2Plot[0]) < min_value)]  = min_value
        
        Ntheta = options.data2Plot[0].shape[1]
        Nphi = options.data2Plot[0].shape[0]
                                          
        mod_data1 = options.data2Plot[0][:,int((Ntheta-1)/2)::]
        mod_data2 = options.data2Plot[0][:,0:int((Ntheta-1)/2)+1]
        
        data2plot = np.vstack((mod_data1,np.fliplr(mod_data2)))
        data2plot = np.transpose(data2plot)

        data2plot = np.hstack((data2plot,[[v] for v in data2plot[:,0]]))
        
        theta = np.linspace(0,np.pi,data2plot.shape[0])
        phi = np.linspace(0,2*np.pi,data2plot.shape[1])
        
        Ph,Th = np.meshgrid(phi,theta)
        
        R = np.array(data2plot)
        
        
        
        aa = R.max()/(max_value*(R.max() - min_value))
        bb = -((R.max()*min_value)/(max_value*(R.max() - min_value)))

        R = aa*R+bb
        
        
        X = R * np.sin(Th) * np.cos(Ph)
        Y = R * np.sin(Th) * np.sin(Ph)
        Z = R * np.cos(Th)
        
        
        
        
        
        
        # fourth dimention - colormap
        # create colormap according to x-value (can use any 50x50 array)
        color_dimension = data2plot # change to desired fourth dimension
        minn, maxx = min_value, max_value
        norm = matplotlib.colors.Normalize(minn, maxx)
        
        matplotlib.colors.LightSource(float(options.light[0]),float(options.light[1]))
        m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
        m.set_array([])
        fcolors = m.to_rgba(color_dimension)
        
        ax.plot_surface(X, Y, Z, rstride=1,  cstride=1, vmin=minn, 
                              vmax=maxx,
                              facecolors=fcolors,linewidth = 0,alpha = 0.8, shade = False, antialiased=False,zorder  = 1000)
        
        #p = ax.plot_surface(
        #    X, Y, Z, rstride=1,  cstride=1,
        #    linewidth=0,facecolors=cm.jet(R/R.max()) ,antialiased=False, alpha=1,zorder = 10)
        # Add a color bar which maps values to colors.
        
        
        # m = plt.cm.ScalarMappable(norm = norm, cmap='jet')
        m.set_array(color_dimension)
    
    
        
        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        
        cb = plt.colorbar(m, fraction=0.03, pad=0.00,aspect = 10,shrink = 8)
    
        
        cb.set_label(label= 'Gain [dBi]',size = 24)
        cb.ax.tick_params(labelsize = 16)
        ax.set_aspect('auto')
   
        fig.set_size_inches(18, 10.125) 

                                                
        
        plt.savefig(filename, pad_inches = 0, transparent=True)
#         self.writetofile(exp.folderplot[0] + '\\'  + filename, data2plot, \
#                          np.linspace(0,180,data2plot.shape[0]), \
#                          np.linspace(0,360,data2plot.shape[1]))
        
        plt.clf()
        plt.close(fig)
    
        
class create_Polar_3D_mayavi(object):

    
    def __init__(self,filename,options,exp):
           
        
        
        min_value = float(options.limz[0])
        max_value = float(options.limz[1])
            
        Dynamic_Range = max_value-min_value
        
        #options.data2Plot[np.where(np.array(options.data2Plot[0]) < min_value)]  = min_value
        
        Ntheta = options.data2Plot[0].shape[1]
        Nphi = options.data2Plot[0].shape[0]
                                          
        mod_data1 = options.data2Plot[0][:,int((Ntheta-1)/2)::]
        mod_data2 = options.data2Plot[0][:,0:int((Ntheta-1)/2)+1]
        
        data2plot = np.vstack((mod_data1,np.fliplr(mod_data2)))
        data2plot = np.transpose(data2plot)

        data2plot = np.hstack((data2plot,[[v] for v in data2plot[:,0]]))
        
        theta = np.linspace(0,np.pi,data2plot.shape[0])
        phi = np.linspace(0,2*np.pi,data2plot.shape[1])
        
        Ph,Th = np.meshgrid(phi,theta)
        
        R = np.array(data2plot)
        
        R[R<min_value] = min_value
        
        R[R>max_value] = max_value
        
        aa = 1 #R.max()/(max_value*(R.max() - min_value))
        bb = -min_value # -((R.max()*min_value)/(max_value*(R.max() - min_value)))

        R = aa*R+bb
        
        
        X = R * np.sin(Th) * np.cos(Ph)
        Y = R * np.sin(Th) * np.sin(Ph)
        Z = R * np.cos(Th)
        
        
        from mayavi import mlab


        black = (0,0,0)
        red = (1,0,0)
        green = (0,1,0)
        blue = (0,0,1)
        white = (1,1,1)
        
        mlab.figure(bgcolor=white)
        mlab.plot3d([0, 1.3*Dynamic_Range], [0, 0], [0, 0], color=red, tube_radius=0.5*Dynamic_Range/45)
        mlab.plot3d([0, 0], [0, 1.3*Dynamic_Range], [0, 0], color=green, tube_radius=0.5*Dynamic_Range/45)
        mlab.plot3d([0, 0], [0, 0], [0, 1.3*Dynamic_Range], color=blue, tube_radius=0.5*Dynamic_Range/45)
        mlab.text3d(1.25*Dynamic_Range, +5*Dynamic_Range/45, +5*Dynamic_Range/45, 'X', color=black, scale=5.*Dynamic_Range/45)
        mlab.text3d(5*Dynamic_Range/45, 1.25*Dynamic_Range, +5*Dynamic_Range/45, 'Y', color=black, scale=5.*Dynamic_Range/45)
        mlab.text3d(5*Dynamic_Range/45, 5*Dynamic_Range/45, 1.25*Dynamic_Range, 'Z', color=black, scale=5.*Dynamic_Range/45)
        
        O1 = mlab.mesh(X, Y, Z, scalars = data2plot,vmax = max_value,vmin = min_value,opacity = 1)
        
        mlab.mesh(X, Y, Z, representation = 'wireframe',color = black)        
        
        cb = mlab.scalarbar(object  =O1, orientation= 'vertical', nb_labels=10,label_fmt = '%.0f' )
        
#         cb.title_text_property.color = (0,0,0)
        cb.label_text_property.color = (0,0,0)
       
        cb.scalar_bar.unconstrained_font_size = True
        cb.label_text_property.font_size=32
#         module_manager1 = engine.scenes[0].children[2].children[1]
#         module_manager1.scalar_lut_manager.scalar_bar_representation.moving = 1
#
#         module_manager1.scalar_lut_manager.scalar_bar_representation.position = array([0.5, 0.5])
#         module_manager1.scalar_lut_manager.scalar_bar_representation.position2 = array([0.25, 0.9 ])

#         cb.title_text_property.orientation = -90
       
#         cb.title_text_property.font_size=52

        cb.scalar_bar_representation.moving = 1
        cb.scalar_bar_representation.maximum_size = [100000, 100000]
        cb.scalar_bar_representation.minimum_size = [1, 1]
        cb.scalar_bar_representation.position = [0.2, 0.1]
        cb.scalar_bar_representation.position2 = [0.3, 0.8 ]
        """An example of a cone, ie a non-regular mesh defined by its
            triangles.
        """
        
        n = 8
        t = np.linspace(-np.pi, np.pi, n)
        z = np.exp(1j * t)
        x = z.real.copy() 
        y = z.imag.copy()
        z = np.zeros_like(x)
        
        triangles = [(0, i, i + 1) for i in range(1, n)]
        x = np.r_[0, 2*Dynamic_Range/45*x] 
        y = np.r_[0, 2*Dynamic_Range/45*y] 
        z = np.r_[5*Dynamic_Range/45, 2*Dynamic_Range/45*z] + 1.3*Dynamic_Range
        
        mlab.triangular_mesh(z, y, x, triangles, scale_factor = 10, color = red) 
        mlab.triangular_mesh(x, z, y, triangles, scale_factor = 10, color = green) 
        mlab.triangular_mesh(x, y, z, triangles, scale_factor = 10, color = blue) 
#          \
        
        mlab.view(elevation=float(options.camera[0]),azimuth  = float(options.camera[1]))
        
        mlab.savefig(filename + ".jpg",size = (180, 101.25))        