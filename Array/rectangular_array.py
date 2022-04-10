# -*- coding: utf-8 -*-
"""
definition of virtual array reflection coefficient (VARC)

Antenna array size is M×N (M can equal to N). The S-parameter matrix element is S_mn
The normalized exciting coefficient for antenna element n is C_n e^(jφ_n ).
For antenna element m, the active reflection coefficient is
〖ARC〗_m=∑_(n=1)^(M×N)▒〖S_mn×C_n e^(jφ_n ) 〗 .
The virtual array reflection coefficient of the array is
VARC=∑_(m=1)^(M×N)▒〖C_m e^(jφ_m )×〖ARC〗_m 〗=∑_(m=1)^(M×N)▒〖C_m e^(jφ_m )×∑_(n=1)^(M×N)▒〖S_mn×C_n e^(jφ_n ) 〗〗

Created on Mon Dec  3 17:41:44 2018

@author: kai.lu
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants as sc
import pandas as pd
import sys
import os
import time

start_time = time.time()
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(f'This program started at: {time_string}')
current_dir = os.getcwd()  # get current dir


rad_dir_layers = [current_dir, 'Data', 'Rad']
rad_dir = os.path.join(*rad_dir_layers)
snp_dir_layers = [current_dir, 'Data', 'Snp']
snp_dir = os.path.join(*snp_dir_layers)
os.chdir("..")  # go up one dir layer
up_dir = os.getcwd()
from Tools.plot_all import taplot_cart1d, taplot_cart1d_frame, taplot_cart1d_lines
from Tools.converter import pw_linear2db, pw_db2linear, s11db2efflinear
from Tools.cst import TBPPTable1d
from Tools import pattern_all as pattern
from Tools.plot_all import plot_cartersian_1d, plot_polar2d, plot_polar1d, pattern_1d, polar_plot_3db_bw, \
    find_max_sidelobe

result_dir = current_dir
result_processed_folder = os.path.join(result_dir, 'Post-processed')
figure_folder = os.path.join(result_processed_folder, 'Figures')
if not os.path.exists(figure_folder):
    os.makedirs(figure_folder)
######################################################################
start_time = time.time()
opr_freq = 27  # in GHz
doa_theta = 30  # in deg
doa_phi = 90  # in deg
opr_wavelength = sc.speed_of_light / 1e6 / opr_freq  # in mm

array_grid_spacingx = opr_wavelength / 2  # in mm
array_grid_spacingy = array_grid_spacingx
array_row_num = 8
array_col_num = 8
port_num = array_row_num * array_col_num

######################################################################
opr_wavelength = 3e8 / 1e6 / opr_freq  # in mm
ang_wave_number = 2 * np.pi / opr_wavelength  # in rad/mm

doa_theta_rad = doa_theta * np.pi / 180  # in deg
doa_phi_rad = doa_phi * np.pi / 180  # in deg
doa_direction_cart = [np.sin(doa_theta_rad) * np.cos(doa_phi_rad), np.sin(doa_theta_rad) * np.sin(doa_phi_rad)]
######################################################################

uniform_mag = 'y'  # or 'n'
if uniform_mag.lower() == 'y':
    norm_array_feeding_coefs_mag = 1 / np.sqrt(port_num) * np.ones((1, port_num))
elif uniform_mag.lower() == 'n':
    norm_array_feeding_coefs_mag = input('Are you serious? Define the array yourself now!')
    norm_array_feeding_coefs_mag /= np.linalg.norm(norm_array_feeding_coefs_mag)

norm_array_feeding_coefs_phase = np.zeros((1, port_num))  # in deg
for port_indx in range(port_num):
    row_indx = port_indx // array_col_num
    col_indx = port_indx % array_col_num
    x_location = array_grid_spacingx * col_indx
    y_location = array_grid_spacingy * row_indx
    norm_array_feeding_coefs_phase[0, port_indx] = -ang_wave_number * np.dot([x_location, y_location],
                                                                             doa_direction_cart)
print(norm_array_feeding_coefs_phase * 180 / np.pi)
norm_array_feeding_coefs = norm_array_feeding_coefs_mag * np.exp(1j * norm_array_feeding_coefs_phase)
######################################################################
# sys.exit()
######################################################################
# star to deal with the pattern
#    input region for pattern post-processing
result_root_folder = r'D:\OneDrive - City University of Hong Kong\Documents\VARC\Farfield'
# C:\Users\kai.lu\Documents\temp\VARC\TAP-1\Array_64_TD_PP\Export\Farfield

freq_interest = opr_freq

fig_dir = f'/Pattern_Figs/{freq_interest}GHz'
data_dir = f'/Pattern_Data/{freq_interest}GHz'
rtick_list = list(range(-15, 26, 5))
polar2d_range = [-15, 26]
thetaticks = np.arange(0, 360, 30)
######################################################################
# post process and plot
figure_folder = result_root_folder + fig_dir
if not os.path.exists(figure_folder):
    os.makedirs(figure_folder)
data_folder = result_root_folder + data_dir
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
pattern_num = port_num
file_name_list = []
for name_indx in range(pattern_num):
    file_name_list.append('farfield (f={}) [{}].TXT'.format(freq_interest, name_indx + 1))
# norm_mag_array = mag_array / np.linalg.norm(mag_array)
norm_complex_array = norm_array_feeding_coefs
##############################
first_pattern_path = result_root_folder + '/' + file_name_list[0]
# \\ for Win only, / for both Win and Mac
pattern1 = pattern.CST_txt_pattern(first_pattern_path)
phi_rad = pattern1.phi_rad_kai
phi_deg = pattern1.phi_deg_kai
theta_rad = pattern1.theta_rad_kai
theta_deg = pattern1.theta_deg_kai
pattern_component_num = pattern1.pattern_component_num
phi_num = len(phi_rad)
theta_num = len(theta_rad)
############################################
# import the pattern data
# patterns_ready = input('Are you going to use the previous imported patterns?')
patterns_ready = 'n'
if 'y' in patterns_ready.lower():
    pass
elif 'n' in patterns_ready.lower():
    # prepare a empty matrix to store patterns
    Gain_total_matrix = np.zeros((pattern_num, theta_num, phi_num, pattern_component_num), dtype=np.complex_)
    for port_indx, port_name in enumerate(file_name_list):
        print('Reading pattern from Port {}'.format(port_indx + 1))
        # Gain_single_port = np.zeros((freq_num, phi_num, theta_num, pattern_component_num), dtype=np.complex_)
        pattern_full_path = result_root_folder + '/' + port_name
        pattern_temp = pattern.CST_txt_pattern(pattern_full_path)
        Gain_total_matrix[port_indx, :, :, :] = pattern_temp.cst_pattern
else:
    print("It is not a proper answer!")
    sys.exit()
#############################################
ax = plt.subplot(111, polar=True)
ax.set_theta_direction(1)
ax.set_theta_zero_location("E")  # or ax.set_theta_offset(pi)
ax.set_rlabel_position(180)

gain_temp = np.zeros((theta_num, phi_num, pattern_component_num), dtype=np.complex_)
Gain_ave = np.zeros((theta_num, phi_num, pattern_component_num), dtype=np.complex_)
for port_indx in range(pattern_num):
    gain_temp = Gain_total_matrix[port_indx, :, :, :]
    #    if port_indx < pattern_num:
    print('Adding pattern from Port {}'.format(port_indx + 1))
    Gain_ave[:, :, 1] += norm_complex_array[0, port_indx] * gain_temp[:, :, 1]  # E_theta
    Gain_ave[:, :, 2] += norm_complex_array[0, port_indx] * gain_temp[:, :, 2]  # E_phi
# calculate total gain by adding G-phi and G-theta
Gain_ave[:, :, 0] = np.sqrt(np.abs(Gain_ave[:, :, 1]) ** 2 + np.abs(Gain_ave[:, :, 2]) ** 2)
Gain_2dpolar = np.real(20 * np.log10(Gain_ave[:, :, 0]))
Gain_2dpolar[np.where(Gain_2dpolar < polar2d_range[0])] = polar2d_range[0]
Gain_2dpolar[np.where(Gain_2dpolar > polar2d_range[1])] = polar2d_range[1]
########################
Gain_2dpolar_max = float(format(Gain_2dpolar.max(), '.2f'))
gain_contour = [Gain_2dpolar_max - 10, Gain_2dpolar_max - 3, Gain_2dpolar_max - 1e-6]
########################
plot_title = f'Polar_Plot2D_doa_phi={doa_phi}deg_theta={doa_theta}deg'  # doa_theta = 15+45 # in deg doa_phi = 0 # in deg
plot_polar2d(phi_rad, theta_deg, Gain_2dpolar, polar2d_range, gain_contour, plot_title, figure_folder)
print('Finished 2D polar plot!')
########################
all_peaks = []
constant_plane = 'phi'
# need to change the phi plane, as numbering order of James' model is different from Kai's definition
plane_ang_deg = 360 - doa_phi
pattern_theta_const = pattern_1d(theta_deg, phi_deg, Gain_2dpolar, constant_plane, plane_ang_deg)
peaks = list(find_max_sidelobe(phi_deg, pattern_theta_const.reshape(phi_num, )))
all_peaks.append(peaks)
########################
peak_file_name = f'Peak_SLL_doa_phi={doa_phi}deg_theta={doa_theta}deg.txt'
# clean the data txt file
open(data_folder + '/' + peak_file_name, 'w').close()
with open(data_folder + '/' + peak_file_name, 'a') as f:
    f.write(f'Peaks_Lobes_doa_phi={doa_phi}deg_doa_theta={doa_theta}deg' + " \n")
    f.write('Peak(dB) ' + 'SLL(dB) ' + 'Peak_loc(deg) ' + 'SLL_loc(deg)' + " \n")
    for item in peaks:
        if item == peaks[-1]:
            f.write("%s\n" % item)
        else:
            f.write("%s     " % item)
###########
fig = polar_plot_3db_bw(phi_deg, pattern_theta_const.reshape(phi_num, ), rtick_list)  # alway phi_deg is used
plot_title = 'Frequency = {}GHz, {} = {}deg plane'.format(str(freq_interest), constant_plane, str(doa_phi))
fig.set_title(plot_title)
plt.tight_layout()
# plt.show()
plot_name = f'Polar_Plot1D_doa_phi={doa_phi}deg_doa_theta={doa_theta}deg'
plt.savefig(os.path.join(figure_folder, plot_name))
plt.close()

elapsed_time = time.time() - start_time
print('Overall time for this post-processing is: {}s'.format(elapsed_time))
print('Finished all_height!')
