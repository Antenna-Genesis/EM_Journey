import pandas as pd
import numpy as np
import skrf as rf


from os import walk




class project(object):
    
    def data_frame_gain_ripple(self):
        '''
        I will create a dataframe with 
        '''
    
        
        index = np.arange(0,(self.Nsamples*len(self.freqlist)*len(self.phicuts)+len(self.thetacuts)*len(self.labels)))
        

        col_labels = ['Antenna','Cut','Angle','Freq'] + ['Gain_Ripple' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(index=index, columns = col_labels)
       
        
        return df
    
    
    def data_frame_stats(self):
        '''
        I will create a dataframe with 
        '''
        
    

        col_labels = ['Pair','Band','eff_max','eff_min','prg_max','prg_min']
        
        df = pd.DataFrame(columns = col_labels)
       
        
        return df
    
    
    def data_frame_gain_peak(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        index = np.arange(0,(self.Nsamples*len(self.freqlist)))
        

        col_labels = ['Antenna','Freq'] + ['Gain_Peak' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(index=index, columns = col_labels)
       
        
        return df
    
    
    def data_frame_efficiency(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        index = np.arange(0,(self.Nsamples*len(self.freqlist)))
        

        col_labels = ['Antenna','Freq'] + ['Efficiency' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(index=index, columns = col_labels)
       
        
        return df

    def data_frame_sector_av_gain(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        index = np.arange(0,(self.Nsamples*len(self.freqlist)))
        

        col_labels = ['Antenna','Freq'] + ['Sector_av_gain' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(index=index, columns = col_labels)
       
        
        return df

    def data_frame_coverage(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        index = np.arange(0,(self.Nsamples*len(self.freqlist)))
        

        col_labels = ['Antenna','Freq'] + ['Coverage' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(index=index, columns = col_labels)
       
        
        return df
 
    def data_frame_VSWR(self):
        '''
        I will create a dataframe with 
        '''
   
        col_labels = ['Antenna','Band'] 
        
        for n in range(self.Nsamples):
            col_labels = col_labels +  list(['VSWR_min' + str(n+1)] + ['VSWR_max' + str(n+1)])
        
        
        df = pd.DataFrame(columns = col_labels)
       
        
        return df
    
    
    def data_frame_eff_minmax(self):
        '''
        I will create a dataframe with 
        '''
   
        col_labels = ['Antenna','Band'] 
        
        for n in range(self.Nsamples):
            col_labels = col_labels +  list(['Efficiency_min' + str(n+1)] + ['Efficiency_max' + str(n+1)])
        
        
        df = pd.DataFrame(columns = col_labels)
        
        return df
        
    def data_frame_prg_minmax(self):
        '''
        I will create a dataframe with 
        '''
   
        col_labels = ['Antenna','Band'] 
        
        for n in range(self.Nsamples):
            col_labels = col_labels +  list(['Peakgain_min' + str(n+1)] + ['Peakgain_max' + str(n+1)])
        
        
        df = pd.DataFrame(columns = col_labels)
       
        
        return df
  
    def data_isolation(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        
        

        col_labels = ['Antenna 1','Antenna 2','Band'] 
        
    
        
        for n in range(self.Nsamples):
            col_labels = col_labels +  list(['Isolation' + str(n+1)] + ['Fulfilled' + str(n+1)] + ['Average' + str(n+1)] )
            
        df = pd.DataFrame(columns = col_labels)
       
        
        return df

    def data_ECC(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        
        

        col_labels = ['Antenna 1','Antenna 2','Band'] + ['ECC' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(columns = col_labels)
       
        
        return df
    
    def data_ECC_Fields(self):
        '''
        I will create a dataframe with 
        '''
        from builtins import str
        
        
        

        col_labels = ['Antenna 1','Antenna 2','Freq'] + ['ECC' + str(n+1) for n in range(self.Nsamples)]
        
        
        df = pd.DataFrame(columns = col_labels)
       
        
        return df
    
    def __init__(self,filename):
        
        with open(filename) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        

        f.close()
        content = [x for x in [x.rstrip() for x in content] if x] 
        
        self.Nsamples = content.count('Begin Sample')    
        
        self.samples = ['']*self.Nsamples
        
        
        
        
        
        ind_ini = [i for i, x in enumerate(content) if x == "Begin General"]
        ind_fin = [i for i, x in enumerate(content) if x == "End General"]
        
        subcontent = content[ind_ini[0]:ind_fin[0]]
        
        self.folderplot = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'folderplot' in x]
        
        aux = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'banda' in x]
        
        self.bands = [list(map(float, l[1:-1].split(','))) for l in aux]
        
        
        
        
        
        
        aux = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'ECC' in x]
        self.ECC = [[list(map(int,l[1:-1].split('-')[0][1:-1].split(','))),list(map(int,l[1:-1].split('-')[1][1:-1].split(',')))] for l in aux]
        
        
        aux = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'aggregated' in x]
        self.aggregated = [list(map(int, l[1:-1].split(','))) for l in aux]
        
        self.sphere_angles = []
        self.labels = [x for i, x in enumerate(subcontent) if 'labels' in x][0].split('=')[1].replace(" ", "")[1:-1].split(',')
        
        aux = [x for i, x in enumerate(subcontent) if 'thetacuts' in x][0].split('=')[1].replace(" ", "")[1:-1].split(',')
        self.thetacuts = list(map(float,aux))
        
        aux = [x for i, x in enumerate(subcontent) if 'phicuts' in x][0].split('=')[1].replace(" ", "")[1:-1].split(',')
        self.phicuts = list(map(float,aux))
        
        aux = [x for i, x in enumerate(subcontent) if 'freqsindex' in x][0].split('=')[1].replace(" ", "")[1:-1].split(',')
        self.freqstart = int(aux[0])
        self.freqend = int(aux[1])
        self.freqdelta = int(aux[2])
        
        self.freqlist = np.arange(self.freqstart-1,self.freqend,self.freqdelta)
        
        self.bandname = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'bandname' in x]
        self.coverage = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'coverage' in x][0][1:-1].split(',')

        self.FieldAnalisys = [x for i, x in enumerate(subcontent) if 'FieldAnalisys' in x][0].split('=')[1].replace(" ", "")
        self.CircuitalAnalysis = [x for i, x in enumerate(subcontent) if 'CircuitalAnalysis' in x][0].split('=')[1].replace(" ", "")

        
        
        
        for n in range(self.Nsamples):
            self.samples[n] = antenna_system(filename,self,n)
        

class antenna_system(object):
    '''
    classdocs
    '''
    
    
    def __init__(self,filename,project,n):
        '''
        Constructor
        each system will use their own input file
        '''

        with open(filename) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        

        f.close()
        content = [x for x in [x.rstrip() for x in content] if x] 
        ind_ini = [i for i, x in enumerate(content) if x == "Begin Sample"]
        ind_fin = [i for i, x in enumerate(content) if x == "End Sample"]
        
        subcontent = content[ind_ini[n]:ind_fin[n]]
        
        self.folders = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'folderField' in x]
        self.folderSpars = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'folderS-pars' in x]
        
        self.sparsFolderVSWR = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'sparsFolderVSWR' in x]
        
        
        
        self.sampleName = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'SampleName' in x]
        
        self.decimate = list(map(int,[x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'decimate' in x][0][1:-1].split(',')))

        self.freqscorrection = list(map(float,[x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'freqscorrection' in x][0][1:-1].split(',')))
         
        aux = [x.split('=')[1].strip() for i, x in enumerate(subcontent) if 'correctioneff' in x]
        
        self.correctioneff = [list(map(float,l[1:-1].split(','))) for l in aux]
        
        self.N_antennas = len(self.folders) 
        self.antennas = ['']*(self.N_antennas+len(project.aggregated))
            # initializing antennas
        for ind, folders in enumerate(self.folders):            
            self.antennas[ind] = antenna(folders +'\\'+ folders.split('\\')[-1] + '_Gain'  + '.txt',self,project,ind)
            
        
        for ind in range(len(project.aggregated)):
            dataframe  = self.aggregate_fields(self.antennas,project.aggregated[ind])
            self.antennas[ind+self.N_antennas] = antenna(dataframe,self,project,ind)
                  
        df = self.antennas[0].FullData
        self.components_available = df.columns[3::]
        self.frequencies = df['Frequency'].unique()
        self.number_of_freqs  = len(self.frequencies)
            
        aux_df = df.loc[df['Frequency'] == self.frequencies[1]]
        
        theta = [float("{0:.2f}".format((th)*180/np.pi)) for th in aux_df['Theta'].values]
        phi = [float("{0:.2f}".format((ph)*180/np.pi)) for ph in aux_df['Phi'].values]
    
            
            
        theta_N = int(360/(theta[1]-theta[0]) + 1)
        phi_N = int(aux_df.shape[0]/theta_N)
        
        self.theta_N = theta_N
        self.phi_N = phi_N
        self.sphere_sampling = [phi_N,theta_N]
            
        self.theta = np.reshape(theta,[phi_N,theta_N])[::int(self.decimate[0]),::int(self.decimate[1])]
        self.slice_theta = self.theta[0,:]
            
        self.phi = np.reshape(phi,[phi_N,theta_N])[::int(self.decimate[0]),::int(self.decimate[1])]
        self.slice_phi = np.linspace(0,360,2*phi_N/int(self.decimate[0])+1)
    
        self.decimated_sphere_sampling = self.theta.shape
            
        self.Ncuts = len(project.thetacuts)+len(project.phicuts)
        
        

        
        
        self.files = next(walk(self.folderSpars[0]))[2]
        
        self.filesvswr = next(walk(self.sparsFolderVSWR[0]))[2]
           
        self.iso_indexes = [(int(files.split('.')[0].split('_')[1]),int(files.split('.')[0].split('_')[2])) for files in self.files]
           
        self.VSWR_indexes = [(int(files.split('.')[0].split('_')[1]),int(files.split('.')[0].split('_')[2])) for files in self.filesvswr]
            
        self.availbable_VSWR = list(set([item for sublist in self.VSWR_indexes for item in sublist]))
            
        dummy_S = rf.Network(self.folderSpars[0] + '\\' + self.files[0])
            
        self.Spars_frequencies = dummy_S.f/1e9
            
            
    
        self.freq = dummy_S.f/1e9
            
        self.Spars_index_in_band = ['']*len(project.bands)
            
        for n in range(len(project.bands)):
            self.Spars_index_in_band[n] = np.where(np.logical_and(self.Spars_frequencies>=project.bands[n][0], self.Spars_frequencies<=project.bands[n][1]))[0]      
    
    
        self.field_index_in_band = ['']*len(project.bands)
            
        for n in range(len(project.bands)):
                self.field_index_in_band[n] = np.where(np.logical_and(self.frequencies>=project.bands[n][0], self.frequencies<=project.bands[n][1]))[0]      


    def Iso_in_band(self,index,folder,inbanders):
        
        M = rf.Network(folder[0] + '//' + 'P_' + str(index[0]) +'_' + str(index[1]) +'.s2p')
        attenuation = 0
        Iso = M.s_db[inbanders,0,1] - attenuation  
        
        # print('P_' + str(index[0]) +'_' + str(index[1]) +'.s2p',-Iso.max())
        return -Iso
    

    
    
    def IsoFullfilled_in_band(self,index,folder,inbanders):
        
        M = rf.Network(folder[0] + '//'+ 'P_' + str(index[0]) +'_' + str(index[1]) +'.s2p')
        attenuation = 0
        Iso = M.s_db[inbanders,0,1] - attenuation  
        req = -20
        
        if (index[0] in [1,2,3,4])&(index[1] in [5,6,7,8]):
            req = -45
        elif (index[1] in [1,2,3,4])&(index[0] in [5,6,7,8]):
            req = -45
            
        freqs_in_band = M.f[inbanders]
        Isomask = np.zeros(freqs_in_band.shape)
        Isomask[Iso<=req] =1
        
        total_span = freqs_in_band[-1]-freqs_in_band[0]
        delta_freq = np.ones(freqs_in_band.shape)*(total_span/(freqs_in_band.shape[0]))
        
        
        # print(index,req,100*np.sum(np.multiply(Isomask,delta_freq))/total_span)
        
        return 100*np.sum(np.multiply(Isomask,delta_freq))/total_span
    
    
    def ECC_in_band(self,index,folder,inbanders):
        
        M = rf.Network(folder[0] +'//' + 'P_' + str(index[0]) +'_' + str(index[1]) +'.s2p')
        
        ECC = (np.abs(M.s[:,0,1]*np.conjugate(M.s[:,0,0])+M.s[:,1,1]*np.conjugate(M.s[:,1,0]))**2)/ \
         (  (1 - np.abs(M.s[:,0,0])**2  - np.abs(M.s[:,1,0])**2 ) * (1 - np.abs(M.s[:,1,1])**2   - np.abs(M.s[:,0,1])**2)     )
          
        return 10*np.log10(abs(ECC[inbanders])).max()
       
    
    def get_VSWR_index(self,port):
                
        t1 = '_' + str(port) + '_'
        
        
        t2 = '_' + str(port) + '.' 
        
       
        
        files_with_port = [s for s in self.filesvswr if (t1 in s) or (t2 in s)]
        
        return [[meas,meas.split('.')[0].split('_').index(str(port))-1] for meas in files_with_port]


    def ECC_fields(self,Field1_the,Field1_phi,Field2_the,Field2_phi,theta,phi):
        
        
        
        F1F2 = np.multiply(np.conjugate(Field1_the),Field2_the) +np.multiply(np.conjugate(Field1_phi),Field2_phi)
        
        F1F1 = np.multiply(np.conjugate(Field1_the),Field1_the) +np.multiply(np.conjugate(Field1_phi),Field1_phi)
        
        
        F2F2 = np.multiply(np.conjugate(Field2_the),Field2_the) +np.multiply(np.conjugate(Field2_phi),Field2_phi)
        
        I12 = self.calculate_integral(F1F2, theta, phi) 
        
        I11 = np.real(self.calculate_integral(F1F1, theta, phi)) 
        
        I22 = np.real(self.calculate_integral(F2F2, theta, phi)) 
        
        ECC = float(np.power(np.abs(I12),2)/(I11*I22))
        
        return ECC
    
    def calculate_integral(self,Field,theta,phi): 
        
 
        

        delta_th = np.abs(theta[0][0]-theta[0][1])*np.ones(theta.shape)*np.pi/180
        delta_ph = np.abs(phi[0][0]-phi[1][0])*np.ones(phi.shape)*np.pi/180
        
        solid_angle =np.multiply(np.sign(np.sin(theta*np.pi/180)),
                                np.multiply(np.sin(theta*np.pi/180),
                                np.multiply(delta_th,delta_ph)))
        

        
        Integral = np.sum(np.multiply(Field,solid_angle))  
        
                
        return Integral
    def aggregate_fields(self,antennas,indexes):
        df_aux = pd.DataFrame(index=antennas[0].FullData.index, columns=antennas[0].FullData.columns)
        
        
        df_aux[df_aux.columns[0]] =  antennas[0].FullData[df_aux.columns[0]].values
        df_aux[df_aux.columns[1]] =  antennas[0].FullData[df_aux.columns[1]].values
        df_aux[df_aux.columns[2]] =  antennas[0].FullData[df_aux.columns[2]].values
        
        
        for col in antennas[0].FullData.columns[3:]:
            aux = np.zeros([antennas[0].FullData.shape[0]])
            for ant in indexes:
                if col ==  'Gain . dB':
                    aux += np.power(10,antennas[ant-1].FullData[col].values/10)
                else:
                    aux += antennas[ant-1].FullData[col].values
                    # in the future, with this, we can generate array patterns
            if col ==  'Gain . dB':
                    df_aux[col] = 10*np.log10(aux/len(indexes)) 
            else:
                    df_aux[col] = aux        
                    
        return df_aux    
class antenna(object):
    '''
    classdocs
    '''
    
    
    def coverage(self,theta,phi,cov): 
        
        
        # i use a mask where the value is zero if the ripple is larger than the limit 
        
        
        
        Field = self.active_field
        
        mask = np.ones(Field.shape)
        
        areaMask = np.zeros(Field.shape)
        
        # this mask only takes the directions of interest
        
        if cov[0] == 'hemisphere':
            M = (theta > -90 ) & (theta <= 90)
        else:
            M = np.full((Field.shape[0],Field.shape[1]), True, dtype=bool)
   
        #Here I have ones in directions of interest
        areaMask[M] = 1
        
        # I calculate the area of the sector of interest
        
        Area_aux =  self.calculate_integral(areaMask, theta, phi)
        
     
        # now I calculate average gain in the sector of interest     
        
        # I first convert the Field in linear and multiply it by the angle mask
        Field_aux  = np.multiply(np.power(10,Field/10),areaMask)
       
        # now i calculate the average Gain in that sector
        
        avField_in_sector = 10*np.log10(self.calculate_integral(Field_aux, theta, phi)/Area_aux)
        
        
        # mask all_height one. I make zeroes where the ripple is larger than the max ripple
        mask[np.abs(Field-avField_in_sector)>float(cov[1])] = 0
        
        # I also make zeros in the regions that are not of interest
        mask[~M] = 0
        
    
        # now i calculate the area
               
        return 100*self.calculate_integral(mask, theta, phi)/(Area_aux)
        
        
         
    
    def efficiency(self,theta,phi):
        
        
        Field = np.power(10,self.active_field/10)
        
                
        return 100*self.calculate_integral(Field, theta, phi)/(4*np.pi)
    
    def av_sector_gain(self,theta,phi,mask):
          
          
           
        
        Field = np.power(10,self.active_field/10)
        
        integral_gain = self.calculate_integral(mask, theta, phi)
        
        Field = np.multiply(Field,mask)
        
       
        
        return 10*np.log10(self.calculate_integral(Field, theta, phi)/(integral_gain))
    
    def calculate_integral(self,Field,theta,phi): 
        
 
        

        delta_th = np.abs(theta[0][0]-theta[0][1])*np.ones(theta.shape)*np.pi/180
        delta_ph = np.abs(phi[0][0]-phi[1][0])*np.ones(phi.shape)*np.pi/180
        
        solid_angle =np.multiply(np.sign(np.sin(theta*np.pi/180)),
                                np.multiply(np.sin(theta*np.pi/180),
                                np.multiply(delta_th,delta_ph)))
        

        
        Integral = np.sum(np.multiply(Field,solid_angle))  
        
                
        return Integral
    
    def get_slice(self,angle,sampling):
        '''
        we get a 1D array
        angle is a tupple ('phi'/'theta', angle in degrees)
        sampling gets the number of points we have ntheta, nphi
        '''

        if angle[0] == 'theta':
#             delta_ang = 360/(sampling[1]-1)
            index_theta1 = np.where(self.Theta[0,:]==angle[1])[0][0]
            index_theta2 = np.where(self.Theta[0,:]==-angle[1])[0][0]
            dummy = slices_maker(angle)
            
            if hasattr(self, 'active_field')== False:
                print('Please do no be malakas and get the 3D fields for this frequency')
            else:
                # in theta cut we need to go from 180 to 360
                aux = self.active_field[:,index_theta2]
                aux2 = self.active_field[:,index_theta1]
                dummy.data = np.hstack((np.hstack((aux,aux2)),aux[0]))
                dummy.Gain_Peak = dummy.data.max()
                dummy.Gain_Ripple = dummy.data.max()-dummy.data.min()
                dummy.angle =angle
                aux = self.Phi[:,index_theta2]+180
                aux2 = self.Phi[:,index_theta1]                
                dummy.angledata = np.hstack((np.hstack((aux,aux2)),aux[0]))
            
        elif angle[0] == 'phi' :  
#             if angle[1]==90:
#                 print(angle)
#             delta_ang = 180/(sampling[0])
            index_phi = np.where(self.Phi[:,0]==angle[1])[0][0]
            dummy = slices_maker(angle)
            
            if hasattr(self, 'active_field')== False:
                print('Please do no be malakas and get the 3D fields for this frequency')
            else:
    
                dummy.data = self.active_field[index_phi,:]
                dummy.Gain_Peak = dummy.data.max()
                dummy.Gain_Ripple = dummy.data.max()-dummy.data.min()
                dummy.angledata = self.Theta[index_phi,:]
        return dummy
    def get_fields(self,freq,component,shaper):
        '''
        freq is the frequency we want to extract data 
        component is the component name
        shaper = [phi_N,theta_N]
        
        '''
        
        
        # from scipy.interpolate import interp1d
  
        aux_df = self.FullData.loc[self.FullData['Frequency'] == freq]
        
        # here I apply the correction before returning back the field at freq 
        # corrections should only be applied to Gain, not to Electric fields....
        
            
        Fields = np.reshape([float("{0:.2f}".format(fc)) for fc in aux_df[component].values],shaper)[::self.decimate[0],::self.decimate[1]]
        Theta = np.reshape([float("{0:.2f}".format(fc*180/np.pi)) for fc in aux_df['Theta'].values],shaper)[::self.decimate[0],::self.decimate[1]]
        Phi = np.reshape([float("{0:.2f}".format(fc*180/np.pi)) for fc in aux_df['Phi'].values],shaper)[::self.decimate[0],::self.decimate[1]]
    
        return Theta,Phi,Fields
    
    
    
    def get_complex_fields(self,freq,shaper):
        '''
        freq is the frequency we want to extract data 
        component is the component name
        shaper = [phi_N,theta_N]
        
        '''
        
        
        # from scipy.interpolate import interp1d
  
        aux_df = self.FullData.loc[self.FullData['Frequency'] == freq]
        
        # here I apply the correction before returning back the field at freq 
        # corrections should only be applied to Gain, not to Electric fields....
        EPHI = np.reshape([float("{0:.2f}".format(fc)) for fc in aux_df['E(Phi). Real part'].values],shaper)[::self.decimate[0],::self.decimate[1]] + \
                 1j*np.reshape([float("{0:.2f}".format(fc)) for fc in aux_df['E(Phi). Imaginary part'].values],shaper)[::self.decimate[0],::self.decimate[1]] 
        ETHE = np.reshape([float("{0:.2f}".format(fc)) for fc in aux_df['E(Theta). Real part'].values],shaper)[::self.decimate[0],::self.decimate[1]] + \
                 1j*np.reshape([float("{0:.2f}".format(fc)) for fc in aux_df['E(Theta). Imaginary part'].values],shaper)[::self.decimate[0],::self.decimate[1]]                  
        

            
    
        return ETHE,EPHI
        
    
     
    def VSWR_in_band(self,file,folder,inbanders):
        
        
        M = rf.Network(folder[0] +'//' +file[0])
        attenuation = 0
        VSWR = (1+M.s_mag[inbanders,file[1],file[1]]*np.power(10,-attenuation/10))/ \
            (1-M.s_mag[inbanders,file[1],file[1]]*np.power(10,-attenuation/10)) 
        return VSWR.min(),VSWR.max()
        
    
    def get_corrections(self):    
        
        from scipy.interpolate import interp1d
        
        corr_interp = interp1d(self.corrections[0], self.corrections[1], kind='linear')
        
        freqs = self.FullData['Frequency'].values
        
        self.FullData['Gain . dB'] = self.FullData['Gain . dB'].values + corr_interp(freqs/1e9) 
        

    def transform_Fields(self,active_field,theta,phi):
        '''
        some tricks to RP
        '''
        print('kk')
        
    def __init__(self,data_container,system,project,ind):
        '''
        Antenna is a single frequency object
        we will need to loop over frequencies in the main folder
        '''

        self.corrections = [system.freqscorrection,system.correctioneff[ind]]
        self.slices = [''] * (len(project.thetacuts)+len(project.phicuts))
        self.Nant = len(project.labels)
        self.decimate = system.decimate
        
        if isinstance(data_container, str):
            self.FullData = reader_GainFile(data_container).df
            self.get_corrections()
        else:
            self.FullData = data_container
                
        
       
        n = 0
        for cut in project.thetacuts: # here i loop in theta cuts
            self.slices[n] = slices_maker(('theta',cut))
            n += 1
            
        for cut in project.phicuts: # here i loop in theta cuts
            self.slices[n] = slices_maker(('phi',cut))
            n += 1
            
class slices_maker(object):
        
    def __init__(self,angle):
        self.angle = []
        self.angle = angle
        self.Gain_Ripple = []
        self.Gain_Peak = []
        self.data = []
        self.angledata = []
        
class reader_GainFile(object):
    '''
    classdocs
    '''

    def __init__(self, satimofile):
        '''
        Constructor
        '''

        df = pd.read_csv(satimofile, skiprows=[0], sep='\t',  lineterminator='\n', encoding='utf-8')
        # use this to remove the '/r'
        df = df.rename(columns = {df.columns[-1] : df.columns[-1][:-1]})
        
        self.df = df       
        

class Read_input(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        from builtins import int

        with open(filename) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        

        f.close()
        content = [x for x in [x.rstrip() for x in content] if x] 
        
        
        print('_______________________________________')
        
        print('Reading ' + filename.split('/')[-1] + ' as input options file')
        
        print('_______________________________________')
        
        self.folders = []
        self.bands = []
        self.freqlist = []
        self.freqsindex = []
        self.graphFolder = []
        self.sparsFolder = []
        self.sparsFolderVSWR=[]
        self.sphere_angles = []
        self.labels = []
        self.correctioneff = []
        self.freqscorrection = []
        self.thetacuts = []
        self.phicuts = []
        self.freqstart = []
        self.freqend = []
        self.freqdelta = []
        self.group = []
        self.bandname = []
        self.coverage = []

        self.FieldAnalisys = []
        self.CircuitalAnalysis = []

        self.decimate = []
        
        for n in range(len(content)):
            
            #    print( content[n])
            item = content[n].split('=')[0].split('_')
            value = content[n].split('=')[1][1:]
            print(item ,value)
            if item[0].strip() == 'folder':
                self.folders.append(value + '\\')
            
            if item[0].strip() == 'group':
                    self.group.append([int(i) for i in value[1:-1].split(',')]) 
            
            if item[0].strip() == 'labels':
                    self.labels = [t for t in value[1:-1].split(',')]   
                    

            if item[0].strip() == 'sparsFolder':
                self.sparsFolder.append(value + '/')
                
            if item[0].strip() == 'sparsFolderVSWR':
                self.sparsFolderVSWR.append(value + '/')
                
            if item[0].strip() == 'bandname':
                self.bandname.append(value)
                
            if item[0].strip() == 'FieldAnalisys':
                self.FieldAnalisys = value
            
            if item[0].strip() == 'CircuitalAnalysis':
                self.CircuitalAnalysis = value
                
                
        
            
            
            if item[0].strip() == 'graphFolder':
                self.graphFolder.append(value + '/')
                    
                
            if item[0].strip() == 'band':
                
                self.bands.append([float(value[1:-1].split(',')[0]),float(value[1:-1].split(',')[1])]) 
                
            
            if item[0].strip() == 'freqlist':
                if not not value[1:-1]:
                    self.freqlist = [int(i) for i in value[1:-1].split(',')]
                    
                    
            if item[0].strip() == 'freqsindex':
                if not not value[1:-1]:
                    self.freqsindex = [int(i) for i in value[1:-1].split(',')]
                    
            
            if item[0].strip() == 'thetacuts':
                
                if not not value[1:-1]:
                    self.thetacuts = [float(i) for i in value[1:-1].split(',')]   
            
            if item[0].strip() == 'phicuts':
                    if not not value[1:-1]:
                        self.phicuts = [float(i) for i in value[1:-1].split(',')]   
                
            if item[0].strip() == 'sphereangles':
                self.sphere_angles.append([float(value[1:-1].split(',')[0]),float(value[1:-1].split(',')[1])]) 
                
            
                             
            if item[0].strip() == 'correctioneff':
                self.correctioneff.append([float(i) for i in value[1:-1].split(',')])
                
            if item[0].strip() == 'freqscorrection':
                self.freqscorrection.append([float(i) for i in value[1:-1].split(',')])
           
                
            if item[0].strip() == 'decimate':
                self.decimate = [int(i) for i in value[1:-1].split(',')]
                
            if item[0].strip() == 'coverage':
                self.coverage = (value.split(',')[0][2:-1],float(value.split(',')[1][0:-1]))      
                        
        self.Nports = len(self.folders)
        
        if not self.freqlist:
            self.freqlist = list(range(self.freqsindex[0]-1,self.freqsindex[1],self.freqsindex[2])) 
        