class SatimoPattern(object):
    """
    deal with radiation pattern from Satimo
    """
    col_header_list_default = ['Frequency',
                               'Phi',
                               'Theta',
                               'E(Phi). Real part',
                               'E(Phi). Imaginary part',
                               'E(Theta). Real part',
                               'E(Theta). Imaginary part',
                               'Gain . dB']
    pattern_component_num_default = 3

    def __init__(self, filename, col_header_list=col_header_list_default,
                 pattern_component_num=pattern_component_num_default):
#        import numpy as np
#        import warnings
        self.filename = filename
        self.col_header_list = col_header_list
        self.pattern_component_num = pattern_component_num
        self.read_txt(filename)

    def read_txt(self, filename):
        # global first_line
        import warnings
        import numpy as np
        import sys
        with open(filename, 'r') as raw_pattern_file:
            satimo_lines = raw_pattern_file.readlines()
            #  "with" ensures the file is always cleaned up promptly and correctly
            print('Importing lines from Satimo pattern file...')
        axis_num = int(satimo_lines[0])
        col_header = satimo_lines[1]

        if self.col_header_list[-1] not in col_header:
            warnings.warn('You need at lest to export the overall Gain: "{}"'.format(self.col_header_list[-1]))
            sys.exit()
        else:
            if (self.col_header_list[-2] not in col_header) or (self.col_header_list[-3] not in col_header)\
                or (self.col_header_list[-4] not in col_header) or (self.col_header_list[-5] not in col_header):
                warnings.warn('The overall gain is available in the Satimo txt file, but not all_height of E_theta and E_phi are in. If you need the vector information, please re-export the radiation pattern according to the following format: {}'.format(self.col_header_list))
                self.E_theta_phi_in = 'n'
                self.pattern_component_num = 1
            else:
                self.E_theta_phi_in = 'y'
#        for header_name in self.col_header_list:
#            if header_name not in col_header:
#                warnings.warn('You need to re-export the radiation pattern according to the following format: {}'.format(self.col_header_list))
#                exit()
        if axis_num != 3:
            warnings.warn('The pattern is not 3-dimensional, re-export using the iterative mode!')
            sys.exit()

        line = satimo_lines[2]  # extract column numbers
        first_line = line.split()

        #            print('The first line in the current Satimo txt file is:')
        #            print(first_line)
        col_num = len(first_line)
        # print(col_num)
        satimo_data_line = satimo_lines[2:]
        satimo_data_lines_num = len(satimo_data_line)
        # print(satimo_data_lines_num)
        satimo_matrix = np.zeros((satimo_data_lines_num, col_num))
        #        print(np.shape(satimo_matrix))
        # exclude the headers
        for line_indx, line in enumerate(satimo_data_line):
            satimo_data = line.split()
            # print(satimo_data)
            satimo_matrix[line_indx, :] = satimo_data
        freq = np.unique(satimo_matrix[:, 0])
        freq_num = len(freq)
        phi = np.unique(satimo_matrix[:int(satimo_data_lines_num / freq_num), 1])
        phi_num = len(phi)
        theta = np.unique(satimo_matrix[:int(satimo_data_lines_num / freq_num / phi_num), 2])
        theta_num = len(theta)

        self.dataline_num = satimo_data_lines_num
        self.freq = freq.reshape(freq_num, 1)
#        self.theta_rad = np.linspace(-np.pi, np.pi, theta_num, endpoint=True).reshape(theta_num, 1)
#        self.phi_deg = np.linspace(0, 180 - 180 / phi_num, phi_num, endpoint=True).reshape(phi_num, 1)
        self.freq_num = freq_num
        self.phi_num = phi_num
        self.theta_num = theta_num
        if self.theta_num % 2 != 1 or self.phi_num % 2 != 0:
            warnings.warn('Theta number must be odd, Phi number must be even!')
            sys.exit()
        print('Theta ranges from -pi to pi, and Phi ranges from 0 to pi')
        self.theta_num_kai = int((self.theta_num + 1) / 2)
        self.phi_num_kai = int(self.phi_num * 2)
        self.theta_rad_kai = np.linspace(0, np.pi, self.theta_num_kai, endpoint=True)
        self.theta_deg_kai = np.linspace(0, 180, self.theta_num_kai, endpoint=True)
        self.phi_rad_kai = np.linspace(0, 2 * np.pi - np.pi / self.phi_num_kai, self.phi_num_kai, endpoint=True)
        self.phi_deg_kai = np.linspace(0, 360 - 360 / self.phi_num_kai, self.phi_num_kai, endpoint=True)
        self.all_data = satimo_matrix

    def pattern_groupby_freq(self):
        import numpy as np

        satimo_matrix = self.all_data
        satimo_pattern = np.zeros((self.freq_num, self.theta_num, self.phi_num,
                                   self.pattern_component_num), dtype=np.complex_)
        
        pattern_size = self.phi_num * self.theta_num
        for row_indx in list(range(self.dataline_num)):
            freq_indx = int(row_indx // pattern_size)
            # // get divisor only integer value, / get divisor can be float value, % get remainder
            phi_indx = int((row_indx - freq_indx * pattern_size) // self.theta_num)
            theta_indx = int((row_indx - freq_indx * pattern_size) % self.theta_num)
            if self.E_theta_phi_in == 'y':
                satimo_pattern[freq_indx, theta_indx, phi_indx, 0] = satimo_matrix[row_indx, 7]  # col 7 for gain_dB
                satimo_pattern[freq_indx, theta_indx, phi_indx, 1] = satimo_matrix[row_indx, 3] + 1j * satimo_matrix[
                    row_indx, 4]  # col 3 and 4 for E_phi
                satimo_pattern[freq_indx, theta_indx, phi_indx, 2] = satimo_matrix[row_indx, 5] + 1j * satimo_matrix[
                    row_indx, 6]  # col 5 and 6 for E_theta
            elif self.E_theta_phi_in == 'n':
                satimo_pattern[freq_indx, theta_indx, phi_indx, 0] = satimo_matrix[row_indx, 3]  # col 3 for gain_dB now
        self.satimo_pattern = satimo_pattern
        
        
    def pattern_lp2cp(self):
        import numpy as np
        lp_satimo_pattern = self.satimo_pattern
        satimo_cp_pattern = np.zeros((self.freq_num, self.theta_num, self.phi_num,
                                   self.pattern_component_num), dtype=np.complex_)
        satimo_cp_pattern[:, :, :, 0] = lp_satimo_pattern[:, :, :, 0]
        satimo_cp_pattern[:, :, :, 1] = (lp_satimo_pattern[:, :, :, 2] - 1j * lp_satimo_pattern[:, :, :, 1])/np.sqrt(2)  # for E_lhcp
        satimo_cp_pattern[:, :, :, 2] = (lp_satimo_pattern[:, :, :, 2] + 1j * lp_satimo_pattern[:, :, :, 1])/np.sqrt(2)  # for E_rhcp
        self.satimo_pattern = satimo_cp_pattern
        print('Now you are playing with CP patterns, LHCP first, RHCP second.')
        '''
                % Column 1 - Re(E_x)
                % Column 2 - Im(E_x)
                % Column 3 - Re(E_y)
                % Column 4 - Im(E_y)

            ALHCP(n,m) = ((nf_data(1)+nf_data(4))+1i*(nf_data(2)-nf_data(3)))/sqrt(2);
            ARHCP(n,m) = ((nf_data(1)-nf_data(4))+1i*(nf_data(2)+nf_data(3)))/sqrt(2);
            % ALHCP and ARHCP should be transposed for further processing
            % calculate the CP near fields and store them
            % for LHCP to +z, E_L = (E_x-i*E_y)/sqrt(2); 
            % for RHCP to +z, E_R = (E_x+i*E_y)/sqrt(2);
        '''
        
    def peakgain(self):
        import numpy as np
        peakgain = np.zeros((self.freq_num, 2))
        peakgain[:, 0] = self.freq.reshape(self.freq_num)
        for freq_indx in range(self.freq_num):
            peakgain[freq_indx, 1] = np.real(self.satimo_pattern[freq_indx, :, :, 0]).max()
        return peakgain


    def pattern_format_kai(self):
        import numpy as np
        satimo_format_pattern = self.satimo_pattern
        self.kai_pattern = np.zeros((self.freq_num, self.theta_num_kai, self.phi_num_kai,
                                          self.pattern_component_num), dtype=np.complex_)
        self.kai_pattern[:, :, 0:self.phi_num, :] = satimo_format_pattern[:, self.theta_num_kai - 1:, :, :]
        pattern_temp = satimo_format_pattern[:, ::-1, :, :]
        # reverse the pattern on the theta dimension
        self.kai_pattern[:, :, self.phi_num:, :] = pattern_temp[:, self.theta_num_kai - 1:, :, :]
        print('Column for the same phi, row for the same theta')


    def single_freq_gain_total(self, freq_interest):
        import numpy as np
        freq_indx = int(np.where(self.freq == freq_interest)[0])
        gain_total_one_freq = np.real(self.kai_pattern[freq_indx, :, :, 0])
        return gain_total_one_freq
#    def single_freq_gain_total_desampling(self, freq_interest, desampling_rate):
#        single_freq_gain_total_predesample = single_freq_gain_total(self, freq_interest)
        

class CST_txt_pattern(object):
    """
    for single frequency only, the headers can be changed according to the output format
    """
    col_header_list_default = [
            'Theta [deg.]',  
            'Phi   [deg.]',  
            'Abs(Grlz)[      ]',   
            'Abs(Theta)[      ]',  
            'Phase(Theta)[deg.]',  
            'Abs(Phi  )[      ]', 
            'Phase(Phi  )[deg.]',  
            'Ax.Ratio[      ]']  
    # Abs(Grlz), Abs(Theta), Abs(Phi  ) are relatively gain values, not E values
    # for single frequency
    # make sure the distance is 1m
    # Theta [deg.]  Phi   [deg.]  Abs(Dir.)[      ]   Abs(Theta)[      ]  Phase(Theta)[deg.]  Abs(Phi  )[      ]  Phase(Phi  )[deg.]  Ax.Ratio[      ]  
                
    pattern_component_num_default = 3
    def __init__(self, filename, pattern_component_num=pattern_component_num_default,
                 col_header_list=col_header_list_default):

        self.filename = filename
        self.pattern_component_num = pattern_component_num
        self.col_header_list = col_header_list
        self.read_txt(filename)
        
    def read_txt(self, filename):
        import warnings
        import pandas as pd
        import numpy as np

        file_txt = open(filename, 'r')
        # use readline() to read the first line 
        first_line = file_txt.readline()

        # use the read line to read further.
        file_txt.close()
        for header_name in self.col_header_list:
            if header_name not in first_line:
                warnings.warn('You need to re-export the radiation pattern according to the following format: {}'.format(self.col_header_list))
                break
        cst_pattern_table = pd.read_table(filename, sep="\s+", skiprows=[1]) # extract total directivity
        
        cst_pattern_original_data = cst_pattern_table.to_numpy()
        # Method .as_matrix will be removed in a future version. Use .values instead.
        pattern_size = len(cst_pattern_original_data[:,0])
        
        if cst_pattern_original_data[0, 0] == 0 and cst_pattern_original_data[0, 1] == 0:
            
            line_indx = 0
            while cst_pattern_original_data[line_indx+1,1] == cst_pattern_original_data[line_indx,1]:
                line_indx += 1
                if line_indx > 1e9:
                    warnings.warn('Endless loop')
                    break
#            print('Sample points along theta angle is: {}'.format(line_indx+1))
            theta_step = cst_pattern_original_data[1,0] - cst_pattern_original_data[0,0]  
            phi_step = cst_pattern_original_data[line_indx+1,1] - cst_pattern_original_data[line_indx,1]
            self.theta_num_kai = int(180/theta_step + 1)  # from 0 to 180
            self.phi_num_kai = int(360/phi_step) # from 0 to one step from 360

            
            self.theta_deg_kai = np.linspace(0, 180, self.theta_num_kai, endpoint=True)
            self.phi_deg_kai = np.linspace(0, 360 - 360 / self.phi_num_kai, self.phi_num_kai, endpoint=True)
            self.theta_rad_kai = self.theta_deg_kai * np.pi / 180
            self.phi_rad_kai = self.phi_deg_kai * np.pi / 180
            
            
            self.cst_pattern = np.zeros((self.theta_num_kai, self.phi_num_kai,
                                       self.pattern_component_num), dtype=np.complex_)
            # theta aligned with the vertical direction, phi aligned with the horizontal direction
            for row_indx in range(pattern_size):
                # // get divisor only integer value, / get divisor can be float value, % get remainder
                phi_indx = int(row_indx // self.theta_num_kai)
                theta_indx = int(row_indx % self.theta_num_kai)
                self.cst_pattern[theta_indx, phi_indx, 0] = cst_pattern_original_data[row_indx, 2]  # col 2 for gain_dB
                self.cst_pattern[theta_indx, phi_indx, 1] = np.sqrt(cst_pattern_original_data[row_indx, 3]) * \
                np.exp(1j * cst_pattern_original_data[row_indx, 4] * np.pi/ 180)  # col 3 and 4 for E_theta
                self.cst_pattern[theta_indx, phi_indx, 2] = np.sqrt(cst_pattern_original_data[row_indx, 5]) * \
                np.exp(1j * cst_pattern_original_data[row_indx, 6] * np.pi/ 180)  # col 5 and 6 for E_phi
        else:
            warnings.warn('Both theta and phi must start from 0!')

class CST_ffs_pattern(object):
    """
    for single frequency only, the headers can be changed according to the output format
    Must export all_height fields as separated sources
    """
    col_header_list_default = ['Phi',  
                               'Theta',  
                               'Re(E_Theta)',   
                               'Im(E_Theta)',  
                               'Re(E_Phi)',  
                               'Im(E_Phi)']  
    # make sure the values are for the 1m distance            
    pattern_component_num_default = 3
    def __init__(self, filename, pattern_component_num=pattern_component_num_default,
                 col_header_list=col_header_list_default):

        self.filename = filename
        self.pattern_component_num = pattern_component_num
        self.col_header_list = col_header_list
        self.read_txt(filename) 
        
    def read_txt(self, filename):
        import warnings
        import numpy as np
############################
        with open(filename, 'r') as raw_pattern_file:
            cst_ffs_lines = raw_pattern_file.readlines()
            #  "with" ensures the file is always cleaned up promptly and correctly
            print('Importing lines from CST ffs pattern file...')
        if 'Frequencies' in cst_ffs_lines[8]:
            freq_num = int(cst_ffs_lines[9])
            freq = np.zeros((freq_num,1))
            # at the beginning, I want to process the exported file with multiple frequencies, but found it was easier not to do so
        else:
            warnings.warn('The location of // #Frequencies is wrong')
            exit()
        if 'Radiated/Accepted/Stimulated Power , Frequency' in cst_ffs_lines[20]:
#            read radiated power, accepted power and stimulated power
#            power_rad = float(cst_ffs_lines[21])
#            power_acpt = float(cst_ffs_lines[22])
            power_feed = float(cst_ffs_lines[23])
        else:
            warnings.warn('The location of Radiated/Accepted/Stimulated Power is wrong')
            exit()
        for freq_indx in range(freq_num):
            
            freq[freq_indx] = float(cst_ffs_lines[24 + freq_indx*5])
            # read frequency
            # 24 is the index for the first frequency
        freq_indx = 0
        if 'Total #phi samples, total #theta samples' in cst_ffs_lines[24 + freq_indx*5 + 3]:
            # read samples for phi and theta
            [self.phi_num, self.theta_num] = [int(item) for item in (cst_ffs_lines[24 + freq_indx*5 + 4].split())]
        
        ep0 = 8.854e-12 # F/m
        mu0 = 4 * np.pi * 1e-7 # H/m
        eta0 =  (mu0 / ep0) ** 0.5     
#        c0 = 1 / (mu0 * ep0) ** 0.5   
 
#        freq = float(cst_ffs_lines[24])
        
        # read the column content
        col_content = cst_ffs_lines[24 + freq_indx*5 + 6]
        for header_name in self.col_header_list:
            if header_name not in col_content:
                warnings.warn('You need to re-export the radiation pattern according to the following format: {}'.format(self.col_header_list))
                break
        # make sure the ffs format is according to this class
        data_start_indx = 24 + freq_indx*5 + 7
        line = cst_ffs_lines[data_start_indx]  
        # extract column numbers
        first_data_line = line.split()
        col_num = len(first_data_line)
        # get number of the data columns
        cst_ffs_data_line = cst_ffs_lines[data_start_indx:]
        pattern_size = len(cst_ffs_data_line)
        # get number of the data rows
        cst_ffs_matrix = np.zeros((pattern_size, col_num))
        for line_indx, line in enumerate(cst_ffs_data_line):
            cst_ffs_data = line.split()
            cst_ffs_matrix[line_indx, :] = cst_ffs_data
        self.phi_deg = cst_ffs_matrix[::self.theta_num, 0]
        self.theta_deg = cst_ffs_matrix[0:self.theta_num, 1]
        self.phi_rad = self.phi_deg * np.pi / 180
        self.theta_rad = self.theta_deg * np.pi / 180                     
############################
        if cst_ffs_matrix[0, 0] == 0 and cst_ffs_matrix[0, 1] == 0:

            self.cst_pattern = np.zeros((self.theta_num, self.phi_num,
                                       self.pattern_component_num), dtype=np.complex_)
            # theta aligned with the vertical direction, phi aligned with the horizontal direction
            for row_indx in range(pattern_size):
                # // get divisor only integer value, / get divisor can be float value, % get remainder
                phi_indx = int(row_indx // self.theta_num)
                theta_indx = int(row_indx % self.theta_num)
#                self.cst_pattern[theta_indx, phi_indx, 0] = cst_ffs_matrix[row_indx, 2]  # col 7 for gain_dB
                self.cst_pattern[theta_indx, phi_indx, 1] = cst_ffs_matrix[row_indx, 2] + \
                1j * cst_ffs_matrix[row_indx, 3]  # col 3 and 4 for E_theta
                self.cst_pattern[theta_indx, phi_indx, 2] = cst_ffs_matrix[row_indx, 4] + \
                1j * cst_ffs_matrix[row_indx, 5]  # col 5 and 6 for E_phi
                rad_density = 1/(2*eta0) * (np.abs(self.cst_pattern[theta_indx, phi_indx, 1])**2 \
                                 + np.abs(self.cst_pattern[theta_indx, phi_indx, 2])**2)
                self.cst_pattern[theta_indx, phi_indx, 0] = rad_density * 4 * np.pi / power_feed

        else:
            warnings.warn('Both theta and phi must start from 0!')

def gain_interpolate(gain_matrix_linear_nparray, theta_deg_nparray, phi_deg_nparray, theta, phi):
    """
    to calculate the gain interpolated at the direction of (theta, phi)
    the input and output can be either a scalar or a matrix (np.array)
    :param gain_matrix_linear_nparray:
    :param theta_deg_nparray:
    :param phi_deg_nparray:
    :param theta:
    :param phi:
    :return: the radiation strength (dB), in either the scalar or array form
    """
    import numpy as np
    gain_matrix_linear_nparray = np.real(gain_matrix_linear_nparray)
    if phi_deg_nparray[-1] != 360:
        #  to make sure the phi angle value between the last and first samples can be interpolated
        phi_deg_nparray = np.append(phi_deg_nparray, 360)
        # np.append is a function, not a property, "=" is necessary to change the left
        gain_matrix_linear_nparray = np.c_[gain_matrix_linear_nparray, gain_matrix_linear_nparray[:, 0]]

    #  resolution of the angles
    theta_deg_delta = theta_deg_nparray[1] - theta_deg_nparray[0]
    phi_deg_delta = phi_deg_nparray[1] - phi_deg_nparray[0]
    #  find the indexes for the neighbouring directions
    theta_indx_s = np.floor(theta / theta_deg_delta)
    theta_indx_s = theta_indx_s.astype(int)
    theta_indx_l = theta_indx_s + 1
    phi_indx_s = np.floor(phi / phi_deg_delta)
    phi_indx_s = phi_indx_s.astype(int)
    phi_indx_l = phi_indx_s + 1

    gain_thetas_phis = gain_matrix_linear_nparray[theta_indx_s, phi_indx_s]
    gain_thetas_phil = gain_matrix_linear_nparray[theta_indx_s, phi_indx_l]
    gain_thetal_phis = gain_matrix_linear_nparray[theta_indx_l, phi_indx_s]
    gain_thetal_phil = gain_matrix_linear_nparray[theta_indx_l, phi_indx_l]
    # interpolate along phi axis first, and then theta axis
    gain_thetas = gain_thetas_phis + (gain_thetas_phil - gain_thetas_phis) * \
        (phi - phi_deg_nparray[phi_indx_s]) / (phi_deg_nparray[phi_indx_l] - phi_deg_nparray[phi_indx_s])
    gain_thetal = gain_thetal_phis + (gain_thetal_phil - gain_thetal_phis) * \
        (phi - phi_deg_nparray[phi_indx_s]) / (phi_deg_nparray[phi_indx_l] - phi_deg_nparray[phi_indx_s])
    gain_interpolated = gain_thetas + (gain_thetal - gain_thetas) * (theta - theta_deg_nparray[theta_indx_s])\
        / (theta_deg_nparray[theta_indx_l] - theta_deg_nparray[theta_indx_s])
    return gain_interpolated
