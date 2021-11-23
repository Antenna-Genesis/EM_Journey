"""
Created on Tue Nov 29 16:29:57 2018
To plot figures for TAP papers
@author: kai.lu

make sure the pattern data stored in the following format
column 1 and 6 are simulation angle and measurement angle respectively ('-180 to 180');
column 2,3,4,5, simulation pattern (order of HFSS output), and 7,8,9,10, measurement pattern
column 2 Gain_LHCP or Gain_Phi in Phi=0 plane, simulation
column 3 Gain_LHCP or Gain_Phi in Phi=90 plane, simulation
column 4 Gain_RHCP or Gain_Theta in Phi=0 plane, simulation
column 5 Gain_RHCP or Gain_Theta in Phi=90 plane, simulation
column 7 Gain_LHCP or Gain_Phi in Phi=0 plane, measurement
column 8 Gain_LHCP or Gain_Phi in Phi=90 plane, measurement
column 9 Gain_RHCP or Gain_Theta in Phi=0 plane, measurement
column 10 Gain_RHCP or Gain_Theta in Phi=90 plane, measurement
AR can be calculated from RHCP and LHCP components:
https://www.etsi.org/deliver/etsi_tr/102000_102099/10203102/01.01.01_60/tr_10203102v010101p.pdf

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os
import time
import warnings
# os.chdir("..")  # go up one dir layer
# up_dir = os.getcwd()
from Tools.calculation.find_bw import find_beamwidth as fb
# from Tools.plot_all import taplot_cart1d, taplot_cart1d_frame, taplot_cart1d_lines, linestyle_generator
# from Tools.converter import pw_linear2db, pw_db2linear, s11db2vswr
# from Tools.cst import TBPPTable1d


def db2linear(db_array):
    linear_array = 10 ** (db_array / 20)
    return linear_array


def linear2db(linear_array):
    db_array = 20 * np.log10(linear_array)
    return db_array


def ar_db(cp_db1, cp_db2):
    cp_linear1 = db2linear(cp_db1)
    cp_linear2 = db2linear(cp_db2)
    ar_linear = abs((cp_linear1 + cp_linear2) / (cp_linear1 - cp_linear2))
    _ar_db = linear2db(ar_linear)
    return _ar_db


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 6

start_time = time.time()
named_tuple = time.localtime()  # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
print(f'This program started at: {time_string}')
script_dir = os.path.dirname(os.path.realpath(__file__))
# get the dir of the py file

rad_dir = input('What is the directory of the Radiation Excel file?:')

# rad_dir_layers = [result_dir, 'Data', 'Rad']
# rad_dir = os.path.join(*rad_dir_layers)

result_processed_folder = os.path.join(rad_dir, 'Post-processed')
figure_folder = os.path.join(result_processed_folder, 'Figures')
if not os.path.exists(figure_folder):
    os.makedirs(figure_folder)
data_folder = result_processed_folder + '/Data'  # show different ways of making a file path
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

###############################################################################
#  go to the bottom to check pattern format
#  file name format should be as: '26GHz'
lp_or_cp = 'cp'
freq = input('What is the frequency in GHz?:')
freq_name = str(freq) + "GHz"
file_name = freq_name  # '26GHz'
file_type = '.xlsx'
fig_type = '.png'
file_dir = f'{rad_dir}/{file_name}{file_type}'
patterns = pd.read_excel(file_dir, header=None)  # import pattern as a df object
# angle in radian is needed for polar plots
patterns[10] = patterns[0] * np.pi / 180
patterns[11] = patterns[5] * np.pi / 180
plot_title_list = ['XOZ Plane', 'YOZ Plane']  # r'$\phi=0^\circ$', r'$\phi=90^\circ$'
figure_name = 'Patterns'
r_resolution = 10
theta_resolution = 30
rtick_list = list(range(-40, 1, r_resolution))
thetaticks = np.arange(0, 181, theta_resolution)
left_thetaticks = np.delete(thetaticks, [0, len(thetaticks) - 1])
left_thetaticks = np.flip(left_thetaticks)
thetaticks = np.append(thetaticks, left_thetaticks)
deg_symbol = u"\u00b0"  # u'\N{DEGREE SIGN}'
theta_labels = [str(i) + deg_symbol for i in thetaticks]

store_parameters = 'yes'

# set legend labels
if lp_or_cp.lower() == 'cp':
    legend_labels = ["Simulated Gain_LHCP", "Simulated Gain_RHCP", "Measured Gain_LHCP", "Measured Gain_RHCP"]
elif lp_or_cp.lower() == 'lp':
    legend_labels = ["Simulated Gain_Phi", "Simulated Gain_Theta", "Measured Gain_Phi", "Measured Gain_Theta"]
else:
    warnings.warn('Only lp or cp is allowed for lp_or_cp!')
    sys.exit()
# find peak gains, normalize the patterns and calculate 3dB beamwidths
# pick up the larger one among the two different cutting planes
simu_peak_gain1 = max(patterns[1].max(), patterns[2].max())
simu_peak_gain2 = max(patterns[3].max(), patterns[4].max())

simu_pattern_angdeg = np.asarray(patterns[0].dropna())
meas_pattern_angdeg = np.asarray(patterns[5].dropna())
# normalize the patterns
if simu_peak_gain1 >= simu_peak_gain2:
    # the peak gain of co-pol is simu_peak_gain1
    simu_peak_gain = simu_peak_gain1
    patterns.iloc[:, 1:5] -= simu_peak_gain  # normalization

    meas_peak_gain = max(patterns[6].max(), patterns[7].max())
    patterns.iloc[:, 6:10] -= meas_peak_gain  # normalization
    # 3dB beamwidth in the co-pol patterns
    simu_beam3dB_phi0 = fb(simu_pattern_angdeg, np.asarray(patterns[1].dropna()), 3)
    simu_beam3dB_phi90 = fb(simu_pattern_angdeg, np.asarray(patterns[2].dropna()), 3)
    meas_beam3dB_phi0 = fb(meas_pattern_angdeg, np.asarray(patterns[6].dropna()), 3)
    meas_beam3dB_phi90 = fb(meas_pattern_angdeg, np.asarray(patterns[7].dropna()), 3)

else:
    # the peak gain of co-pol is simu_peak_gain2
    simu_peak_gain = simu_peak_gain2
    patterns.iloc[:, 1:5] -= simu_peak_gain  # normalization

    meas_peak_gain = max(patterns[8].max(), patterns[9].max())
    patterns.iloc[:, 6:10] -= meas_peak_gain  # normalization
    # 3dB beamwidth in the co-pol patterns
    simu_beam3dB_phi0 = fb(simu_pattern_angdeg, np.asarray(patterns[3].dropna()), 3)  # 3dB beamwidth
    simu_beam3dB_phi90 = fb(simu_pattern_angdeg, np.asarray(patterns[4].dropna()), 3)  # 3dB beamwidth
    meas_beam3dB_phi0 = fb(meas_pattern_angdeg, np.asarray(patterns[8].dropna()), 3)  # 3dB beamwidth
    meas_beam3dB_phi90 = fb(meas_pattern_angdeg, np.asarray(patterns[9].dropna()), 3)  # 3dB beamwidth

# extract AR patterns
simu_ar_phi0 = ar_db(np.asarray(patterns[1].dropna()), np.asarray(patterns[3].dropna()))
simu_ar_phi90 = ar_db(np.asarray(patterns[2].dropna()), np.asarray(patterns[4].dropna()))
meas_ar_phi0 = ar_db(np.asarray(patterns[6].dropna()), np.asarray(patterns[8].dropna()))
meas_ar_phi90 = ar_db(np.asarray(patterns[7].dropna()), np.asarray(patterns[9].dropna()))

# normalize and revert the AR pattern, so that fb function can be used
simu_ar_phi0 = -(simu_ar_phi0 - simu_ar_phi0.min())
simu_ar_phi90 = -(simu_ar_phi90 - simu_ar_phi90.min())
meas_ar_phi0 = -(meas_ar_phi0 - meas_ar_phi0.min())
meas_ar_phi90 = -(meas_ar_phi90 - meas_ar_phi90.min())

fig, ax = plt.subplots()
ax.plot(simu_pattern_angdeg, simu_ar_phi0, label="simu_ar_phi0")
ax.plot(simu_pattern_angdeg, simu_ar_phi90, label="simu_ar_phi90")
ax.plot(meas_pattern_angdeg, meas_ar_phi0, label="meas_ar_phi0")
ax.plot(meas_pattern_angdeg, meas_ar_phi90, label="meas_ar_phi90")
ax.set_ylim(-6, 0)
ax.set_xlim(-60, 60)
plt.legend()
plt.show()
plt.close()
# 3dB beamwidth in the AR patterns
simu_arbeam3dB_phi0 = fb(simu_pattern_angdeg, simu_ar_phi0, 3)
simu_arbeam3dB_phi90 = fb(simu_pattern_angdeg, simu_ar_phi90, 3)
meas_arbeam3dB_phi0 = fb(meas_pattern_angdeg, meas_ar_phi0, 3)
meas_arbeam3dB_phi90 = fb(meas_pattern_angdeg, meas_ar_phi90, 3)

if 'y' in store_parameters:
    pattern_file_name = freq_name + '_Peak_Gains_and_HPBWs.txt'
    open(data_folder + '/' + pattern_file_name, 'w').close()  # clean the data txt file
    with open(data_folder + '/' + pattern_file_name, 'a') as f:
        f.write(f'Max simulated gain is {simu_peak_gain}dB;' + " \n\n")
        f.write(f'Max measured gain is {meas_peak_gain}dB;' + " \n\n")
        f.write(f'Simulation, 3dB beamwidth in phi=0deg plane: {simu_beam3dB_phi0[0]};' + " \n\n")
        f.write(f'Simulation, 3dB AR beamwidth in phi=0deg plane: {simu_arbeam3dB_phi0[0]};' + " \n\n")
        f.write(f'Simulation, 3dB beamwidth in phi=90deg plane: {simu_beam3dB_phi90[0]};' + " \n\n")
        f.write(f'Simulation, 3dB AR beamwidth in phi=90deg plane: {simu_arbeam3dB_phi90[0]};' + " \n\n")
        f.write(f'Simulation, beam area: {simu_beam3dB_phi0[0] * simu_beam3dB_phi90[0]};' + " \n\n")
        f.write(f'Measurement, 3dB beamwidth in phi=0deg plane: {meas_beam3dB_phi0[0]};' + " \n\n")
        f.write(f'Measurement, 3dB AR beamwidth in phi=0deg plane: {meas_arbeam3dB_phi0[0]};' + " \n\n")
        f.write(f'Measurement, 3dB beamwidth in phi=90deg plane: {meas_beam3dB_phi90[0]};' + " \n\n")
        f.write(f'Measurement, 3dB AR beamwidth in phi=90deg plane: {meas_arbeam3dB_phi90[0]};' + " \n\n")
        f.write(f'Measurement, beam area: {meas_beam3dB_phi0[0] * meas_beam3dB_phi90[0]}.')


elif 'n' in store_parameters:
    print('The pattern parameters are not stored.')
    print(f'Max simulated gain is {simu_peak_gain}dB, Max measured gain is {meas_peak_gain}dB;')
    print(f'Simulation, 3dB beamwidth in phi=0deg plane: {simu_beam3dB_phi0[0]};')
    print(f'Simulation, 3dB beamwidth in phi=90deg plane: {simu_beam3dB_phi90[0]};')
    print(f'Simulation, beam area: {simu_beam3dB_phi0[0] * simu_beam3dB_phi90[0]};')
    print(f'Measurement, 3dB beamwidth in phi=0deg plane: {meas_beam3dB_phi0[0]};')
    print(f'Measurement, 3dB beamwidth in phi=90deg plane: {meas_beam3dB_phi90[0]};')
    print(f'Measurement, beam area: {meas_beam3dB_phi0[0] * meas_beam3dB_phi90[0]}.')
else:
    warnings.warn('store_parameters must be yes, y, no or n!')
    sys.exit()

# plot the patterns
fig, axes = plt.subplots(1, 2, figsize=(4.32, 3.24), subplot_kw=dict(polar=True))
xy_names = ['x', 'y']
for plot_indx, ax in enumerate(axes):
    plot_title = plot_title_list[plot_indx]
    # plot phi = 0 deg first, then phi=90deg
    theta_direction = -1
    theta_zero_location = 'N'
    ax.set_theta_direction(theta_direction)
    ax.set_theta_zero_location(theta_zero_location)  # or ax.set_theta_offset(pi)

    ax.plot(patterns[10], patterns[1 + plot_indx], 'og', ls='dashed', markersize=5, markevery=20)
    ax.plot(patterns[10], patterns[3 + plot_indx], color='k', ls='dashed')
    ax.plot(patterns[11], patterns[6 + plot_indx], 'ob', ls='solid', markersize=5, markevery=20)
    ax.plot(patterns[11], patterns[8 + plot_indx], color='r', ls='solid')
    # markersize=5, markevery=marker_every

    ax.set_rmax(rtick_list[-1])
    ax.grid(True)
    ax.set_rticks(rtick_list)
    ax.set_ylim(rtick_list[0], rtick_list[-1])
    ax.set_rlabel_position(270)
    ax.set_thetagrids(angles=np.arange(0, 360, theta_resolution), labels=theta_labels)

    ax.tick_params(axis='x', pad=0)  # push tick labels closer to polar circle
    ax.set_title(plot_title, fontsize=8, fontfamily="Times New Roman", y=1.1)  # , va='bottom'
    ax.text(-0.16, 7.5, r'$\theta$ =', {'color': 'k', 'fontsize': 8, 'ha': 'center', 'va': 'center'})
    xyname = xy_names[plot_indx]
    ax.text(0.2 + 0.6, 10, f'(+{xyname})', {'color': 'k', 'fontsize': 8, 'ha': 'center', 'va': 'center'})
    ax.text(-0.8, 10, f'(-{xyname})', {'color': 'k', 'fontsize': 8, 'ha': 'center', 'va': 'center'})
fig.text(0.5, 0.78, r'Normalized Patterns (dB)', {'color': 'k', 'fontsize': 8, 'ha': 'center', 'va': 'center'})
# file_name
fig.text(0.5, 0.72, freq_name, {'color': 'k', 'fontsize': 8, 'ha': 'center', 'va': 'center'})
fig.legend(legend_labels, fontsize=8, loc='lower center',
           bbox_to_anchor=(0.5, 0.02), fancybox=True, shadow=False, ncol=2)
fig.subplots_adjust(wspace=-0.7)  # push two polar plots closer
plt.tight_layout()  # necessary to keep tight
plot_name = freq_name + ', ' + figure_name + fig_type
plt.savefig(os.path.join(figure_folder, plot_name), bbox_inches='tight', dpi=200)  # figsize=(4.32, 3.24),
plt.close()

###############################################################################
elapsed_time = time.time() - start_time
print('Overall time for this post-processing is: {}s'.format(elapsed_time))
print('Finished all!')
