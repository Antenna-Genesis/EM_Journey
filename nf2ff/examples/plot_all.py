# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:45:02 2018

@author: kai.lu
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import warnings
import matplotlib.cm as cm

def linestyle_generator(type_or_color, color_num):
    from itertools import cycle
    bgrcmyk = ['or', 'sb', 'dg', '*c', '^m', 'hy', 'Vk']
    sddd = ["-", "--", "-.", ":"]  # "solid", "dashed",, "dashdot" "dotted"
    style_list = []
    if type_or_color.lower() == 'type':
        cycle_list = cycle(sddd)
    elif type_or_color.lower() == 'color':
        cycle_list = cycle(bgrcmyk)
    else:
        warnings.warn('Only "type" or "color" is allowed here')  # raise?

    for i in range(color_num):
        style_list.append(next(cycle_list))
    return style_list

def patch_plot(freq_band, patch_mag, patch_names, patch_colors, fig_handle):
    """
    main function to plot patchs with lengends
    freq_highlight_band, patch_mag, highlight_patch_names, highlight_patch_colors should be lists for either single band or multibands
    e.g.
    [[1.92, 1.98], [1.71, 1.755]] 
    [[-30, 0], [-30, 0]] 
    [['Uplink'], ['Uplink']] 
    ['green', 'green']
    """
    patch_list = []  # create a list to store patch objects
    for band_indx in range(0, len(freq_band)):
        # add patch for each frequency band
        patch_freq_range = freq_band[band_indx]
        patch_mag_range = patch_mag[band_indx]
        patch_name = patch_names[band_indx]
        patch_color = patch_colors[band_indx]
        # extract patch information for each band
        patch = patch_add(patch_freq_range, patch_mag_range, patch_name, patch_color, fig_handle)
        patch_list.append(patch)
        # put all_height patch object into a list one by one
    patch_lengend(fig_handle, patch_names, patch_list) 

        
def patch_add(patch_freq_range, patch_mag_range, patch_name, patch_color, fig_handle):
    """
    add one patch to a figure
    """
    import matplotlib.patches as patches
    patch_freq_lower_limit = patch_freq_range[0]
    patch_mag_lower_limit = patch_mag_range[0]
    patch_freq_width = patch_freq_range[1] - patch_freq_range[0]
    patch_mag_height = patch_mag_range[1] - patch_mag_range[0]
    
    fig_handle.add_patch(patches.Rectangle((patch_freq_lower_limit, patch_mag_lower_limit),
                                           patch_freq_width, patch_mag_height, facecolor=patch_color, alpha=0.2))
    patch = patches.Patch(color=patch_color, label=patch_name, alpha=0.2)
    return patch
    

def patch_lengend(fig_handle, patch_names, patch_list):
    """
    add legends for the patches, must come together with patch_add
    """
    import matplotlib.pyplot as plt
    handles, labels = fig_handle.get_legend_handles_labels()
    # get existing handel and label from the figure
    handle_list, label_list = [], []
    for handle, label in zip(handles, labels):
        if label not in label_list:
            # add new handles and labels to lists
            handle_list.append(handle)
#            print(label)
            label_list.append(label)
    for patch_indx in range(len(patch_list)):
        if patch_names[patch_indx] not in label_list:
            # add patch handel and label lists
            handle_list.append(patch_list[patch_indx])
            label_list.append(patch_names[patch_indx])
#    print(label_list)
#    print(handle_list)
        
    plt.legend(handle_list, label_list)

def plot_cartersian_1d(figure_folder, ylabel, plot_title, label_grp, freq_list, patch_colors_grp,\
                       plot_data_grp, freq_band_grp, freq_limit_grp, y_mag_limits, patch_names_grp):
    '''
    plot 1D Cartesian figures with frequency as x-axis
    plot_data_grp and label_grp need to be in a list
    freq_limit_grp = [[2.300, 2.600], [5.000, 6.000]]
    patch_names_grp = [['2G_band'], ['5G_band']]
    patch_colors_grp = ['green', 'blue']
    freq_band_grp = [[[2.400, 2.480]], [[5.150, 5.875]]]
    y_mag_lower_limit = 0
    y_mag_upper_limit = 10
    '''
    for band_indx in range(len(freq_band_grp)):

        freq_lower_limit = freq_limit_grp[band_indx][0]
        freq_upper_limit = freq_limit_grp[band_indx][1]
        # define the patch information
        patch_names = patch_names_grp[band_indx]
        patch_colors = patch_colors_grp[band_indx]
        freq_band = freq_band_grp[band_indx]
        patch_mag = y_mag_limits
        y_mag_lower_limit = y_mag_limits[band_indx][0]
        y_mag_upper_limit = y_mag_limits[band_indx][1]
        band_name = patch_names_grp[band_indx][0]
        freq_sep_indx = [i for i, x in enumerate(freq_list) if freq_lower_limit <= x <= freq_upper_limit]
#        print(len(freq_sep_indx))
        # identify the necessary frequency range
#        print(freq_sep_indx)
        freq_start = freq_sep_indx[0]
        freq_end = freq_sep_indx[-1]
    
        fig1, ax = plt.subplots()  # must be define here for patch plotting
        for line_indx in range(len(label_grp)):
            plot_data = plot_data_grp[line_indx]
            plt.plot(freq_list[freq_start:freq_end + 1], plot_data[freq_start:freq_end + 1], label=label_grp[line_indx])
        
        plt.xlim(freq_lower_limit, freq_upper_limit)
        plt.ylim(y_mag_lower_limit, y_mag_upper_limit)
        plt.grid(axis='y', linestyle='--', color='0.75')
        plt.grid(axis='x', linestyle='--', color='0.75')
        plt.xlabel(r'Frequency (GHz)')
        plt.ylabel(ylabel)
        plt.title(plot_title)
        patch_plot(freq_band, patch_mag, patch_names, patch_colors, ax)
        plt.legend(loc='best')
#        plt.legend(ncol=4)
        plot_name =  '{}_{}.png'.format(band_name, plot_title)
        plt.tight_layout()
        plt.savefig(os.path.join(figure_folder, plot_name), dpi=300)
#        plt.show()
        plt.close()
def plot_polar2d(phi_rad, theta_deg, Gain_polar, polar2d_range, gain_contour, plot_title, figure_folder):
    # plot_polar2d(phi_rad, theta_deg, Gain_polar, polar2d_range, gain_contour, rtick_list, plot_title, figure_folder):
    '''
    plot 2D polar plots for a radiation pattern
    '''
    theta_direction = -1  # -1
    theta_zero_location = 'N' #  'N'
    ax = plt.subplot(111, polar=True)
    ax.set_theta_direction(theta_direction)
    ax.set_theta_zero_location(theta_zero_location)  # or ax.set_theta_offset(pi)
    thetaticks = np.arange(0, 360, 30)
    ax.set_rlabel_position(270) # 180
    ax.set_thetagrids(thetaticks)
    #################
    if abs(phi_rad[-1] - 2 * np.pi) <= 1e-3:
        pass
    else:
        phi_rad = np.append(phi_rad, 2*np.pi)
        Gain_polar = np.c_[Gain_polar, Gain_polar[:, 0]]
    # to make the 2D polar plot closed     
    ###############
    Gain_polar[np.where(Gain_polar < polar2d_range[0])] = polar2d_range[0]
    Gain_polar[np.where(Gain_polar > polar2d_range[1])] = polar2d_range[1]
    ctf = ax.contourf(phi_rad, theta_deg, Gain_polar, np.arange(polar2d_range[0], polar2d_range[1]), cmap=cm.jet)
    plt.colorbar(ctf)
    C = plt.contour(phi_rad, theta_deg, Gain_polar, gain_contour,
                    colors='black')  # , linewidth=0.3
    plt.clabel(C, inline=True, fontsize=8)
    
    plt.title(plot_title, va='bottom')
    plot_title = 'Polar_Plot2D_{}'.format(plot_title)
    plot_name = plot_title + '.png'
    plt.tight_layout()
    plt.savefig(os.path.join(figure_folder, plot_name), dpi=300)
    plt.close() 

def plot_polar1d(theta_deg, phi_deg, Gain_grp, constant_plane, plane_ang_deg, port_names, rtick_list, plot_title, figure_folder):
    # plot_polar1d(theta_deg, phi_deg, Gain_polar, constant_plane, plane_ang_deg, port_names,
    #              rtick_list, plot_title, pattern_figure_folder)
    import numpy as np
    # from plot import pattern_1d_polar as p1p
    if abs(phi_deg[-1] - 360) <= 1e-3:
        polar_ang_rad = phi_deg * np.pi /180
    else:
        polar_ang_rad = np.append(phi_deg * np.pi /180, 2*np.pi)
    theta_direction = -1
    theta_zero_location = 'N'
    ax = plt.subplot(111, polar=True)
    ax.set_theta_direction(theta_direction)
    ax.set_theta_zero_location(theta_zero_location)  # or ax.set_theta_offset(pi)
    thetaticks = np.arange(0, 360, 30)
    ax.set_rlabel_position(180)
    for port_indx, port_name in enumerate(port_names):
        Gain_single_port = Gain_grp[port_indx]
#        Gain_single_port = GdB_total_matrix[pair_indx][freq_indx][port_indx]
        pattern_1d = pattern_1d(theta_deg, phi_deg, Gain_single_port, constant_plane, plane_ang_deg)
        if abs(phi_deg[-1] - 360) <= 1e-3:
            pattern_1d = pattern_1d
        else:
            pattern_1d = np.append(pattern_1d, pattern_1d[0])
        ax.plot(polar_ang_rad, pattern_1d, label=port_name) # 
    ax.legend()
    ax.set_rmax(rtick_list[-1])
    ax.set_rticks(rtick_list)
    ax.theta_ticks = np.arange(0, 360, 30)
    ax.set_rlabel_position(45)
    ax.set_thetagrids(thetaticks)
#    ax.tick_params(thetaticks)
#    plot_title = '{}_Frequency={}GHz_{}={}deg_plane'.format(pair_name, str(freq), constant_plane, str(plane_ang_deg))
    ax.set_title(plot_title, y=1.1)
    plot_name = '{}.png'.format(plot_title)
    plt.tight_layout()
    plt.savefig(os.path.join(figure_folder, plot_name), dpi=300)
    plt.close()   
    
def pattern_1d(theta_deg_array, phi_deg_array, pattern_matrix, constant_plane, plane_ang_deg):
    """ to extract a cutting plane from a radiation pattern, pattern_matrix_db
        theta_array and phi_array are in deg, in array form,
        theta_array from 0 to 180, and phi_array from 0 to one step to 360 degree
        pattern_matrix can be in linear or in dB, column for the same phi, row for the same theta
        theta_deg_array, phi_deg_array, pattern_matrix have consistent size
        note the pattern arrangement is different from above
        constant_plane = 'theta' or 'phi'
        plane_ang_deg in degree, means the angle of the cutting plane
    """
    import warnings    
    import numpy as np
    import sys
    
    def find_nearest(array,value):
        idx = (np.abs(array-value)).argmin()
        return idx, array[idx]
    
    if constant_plane == 'theta':
        (closest_ang_indx, closest_ang) = find_nearest(theta_deg_array, plane_ang_deg)
        if abs(closest_ang - plane_ang_deg) > (theta_deg_array[1] - theta_deg_array[0]):
                warnings.warn('The input angle is out of scope!')
                sys.exit(1)
        else:
            ang_indx = closest_ang_indx
        pattern_1d_data = pattern_matrix[ang_indx,:]        
        
    elif constant_plane == 'phi':
        (closest_ang_indx, closest_ang) = find_nearest(phi_deg_array, plane_ang_deg)
        if abs(closest_ang - plane_ang_deg) > (phi_deg_array[1] - phi_deg_array[0]):
                warnings.warn('The input angle is out of scope!')
                sys.exit(1)
        else:
            ang_indx = closest_ang_indx
        if ang_indx < int(len(phi_deg_array)/2):
            pattern_1d_data = pattern_matrix[:, ang_indx]
            ang_opposite_indx = int(len(phi_deg_array)/2+1) + ang_indx
            pattern_1d_data_opposite = pattern_matrix[1:-1, ang_opposite_indx]
            pattern_1d_data = np.append(pattern_1d_data, pattern_1d_data_opposite[::-1])
        else:
            pattern_1d_data = pattern_matrix[:, ang_indx]
            ang_opposite_indx = -int(len(phi_deg_array)/2+1) + ang_indx
            pattern_1d_data_opposite = pattern_matrix[1:-1, ang_opposite_indx]
            pattern_1d_data = np.append(pattern_1d_data, pattern_1d_data_opposite[::-1])          
    else:
        warnings.warn('constant_plane can either by theta or phi!')
        sys.exit(1)
    return pattern_1d_data

def polar_plot_3db_bw(polar_ang_deg, polar_pattern, rtick_list):
    '''
    ax, figure handel
    polar_ang, 
    polar_pattern, data to be plotted
    constant_plane = 'theta' or 'phi'
    plane_ang_deg, angle of the constant plane
    constant_plane can be either theta or phi
    bw3db_highlight = 0 or 1
    '''
#    ax = plt.subplot(111, projection='polar')
#    ax.set_theta_direction(-1)
#    ax.set_theta_zero_location("N")  # or ax.set_theta_offset(pi)
#    the above lines must be defined outside, so that multiple lines can be plotted together
    import numpy as np
    import matplotlib.pyplot as plt
#    import warnings
#    import sys
    from Tools.calculation.find_bw import find_beamwidth as fb

    theta_direction = -1
    theta_zero_location = 'N'
    bw3db_highlight = 0
#    if constant_plane == 'theta':
#        theta_direction = 1
#        theta_zero_location = 'E'
#        bw3db_highlight = 0
#    elif constant_plane == 'phi':
#        theta_direction = -1
#        theta_zero_location = 'N'
#        bw3db_highlight = 0
#    else:
#        warnings.warn('constant_plane can be either theta or phi')
#        sys.exit(1)
    plt.figure()
    ax = plt.axes(projection='polar')
    #####################
    ax.set_theta_direction(theta_direction)
    ax.set_theta_zero_location(theta_zero_location)
    #####################
    
    polar_ang_size = len(polar_ang_deg)
    beam_3dB = fb(polar_ang_deg, polar_pattern, 3) # 3dB beamwidth
    bw_3dB = int(beam_3dB[0])
    bw_start = int(beam_3dB[1])
    bw_end = int(beam_3dB[2])
    polar_ang_rad = polar_ang_deg*np.pi/180
    if bw_start <= bw_end:
       if bw_start == 0 and abs(360 - (polar_ang_deg[1] - polar_ang_deg[0]) - polar_ang_deg[bw_end]) < 1e-3:
           # start from 0 degree and end at one less step to 360 degree
           mainbeam_range = polar_ang_rad[bw_start:bw_end + 1]
           mainbeam_range = np.append(mainbeam_range, [np.pi * 2])
           # close the range from 0 to 360 degree
           mainbeam_mag = [rtick_list[0]*np.ones(len(mainbeam_range)), rtick_list[-1]*np.ones(len(mainbeam_range))]
       else:
           mainbeam_range = polar_ang_rad[bw_start:bw_end + 1]
           mainbeam_mag = [rtick_list[0]*np.ones(len(mainbeam_range)), rtick_list[-1]*np.ones(len(mainbeam_range))]
    else:
       mainbeam_range_low = polar_ang_rad[bw_start] - 2 * np.pi
       # turn back one circle so that start smaller than end
       mainbeam_range_high = polar_ang_rad[bw_end + 1]
       main_beam_points = polar_ang_size - (bw_start - bw_end - 1)
       # count point one the opposite first
       mainbeam_range = np.linspace(mainbeam_range_low, mainbeam_range_high, num=main_beam_points, endpoint=True)
       mainbeam_mag = [rtick_list[0]*np.ones(len(mainbeam_range)), rtick_list[-1]*np.ones(len(mainbeam_range))]
       
#    if abs(polar_ang_deg[-1] - 360) <= 1e-3:
#        pass
#    else:
#        polar_ang_rad = np.append(polar_ang_rad, 2*np.pi)
#        polar_pattern = np.append(polar_pattern, polar_pattern[0])
    # make the plot line closed   
#    mainbeam_mag = mainbeam_mag*np.pi/180
    
    # temperary solution to close the pattern curve
    if abs(polar_ang_deg[-1] - 360) <= 1e-3:
        pass
    else:
        polar_ang_rad = np.append(polar_ang_rad, 2*np.pi)
        polar_pattern = np.append(polar_pattern, polar_pattern[0])
    
    ax.plot(polar_ang_rad, polar_pattern, label='Main_bw_3dB = ' + str(int(bw_3dB)) + ' degree')   
       
    ax.legend(loc=9, bbox_to_anchor=(0.5, -0.1))
    if bw3db_highlight:
        ax.fill_between(mainbeam_range, mainbeam_mag[0], mainbeam_mag[1],color='green', alpha=0.2)
    else:
        pass
    ax.set_rmax(rtick_list[-1])
    ax.set_rticks(rtick_list)
    thetaticks = np.arange(0, 360, 30)
    ax.set_rlabel_position(45)
    ax.set_thetagrids(thetaticks)#, frac=1.1)
    # plt.show()
    return ax

def find_max_sidelobe(polar_ang_deg, pattern_db1d):
    import numpy as np
    if polar_ang_deg[-1] == 360:
        polar_ang_deg = np.append(polar_ang_deg, polar_ang_deg[1])
        pattern_db1d = np.append(pattern_db1d, pattern_db1d[1])
    else:
        polar_ang_deg = np.append(polar_ang_deg,polar_ang_deg[0])
        polar_ang_deg = np.append(polar_ang_deg,polar_ang_deg[1])
        
        pattern_db1d = np.append(pattern_db1d, pattern_db1d[0])
        pattern_db1d = np.append(pattern_db1d, pattern_db1d[1])
        
    ext_deg = []
    ext_pattern_db1d = []
    for i in range(0,len(polar_ang_deg)-2):
        if pattern_db1d[i+1] > pattern_db1d[i] and pattern_db1d[i+1] > pattern_db1d[i+2]:
#            if gain_2[i+1] > gain_2[i+2]:
            ext_deg.append(polar_ang_deg[i+1])
            ext_pattern_db1d.append(pattern_db1d[i+1])

    print(ext_deg)
    print(ext_pattern_db1d)   
    
    pattern_db1d_1st_extmum = max(ext_pattern_db1d)
    index_1st_extmum = []
    for i in range(0,len(ext_pattern_db1d)):
        if ext_pattern_db1d[i] == pattern_db1d_1st_extmum:
            index_1st_extmum.append(i)
    
    # index_1st_extmum = ext_gain.index(gain_1st_extmum)
    deg_1st_extmum = [0 for i in range(len(index_1st_extmum))]
    for i in range(0,len(index_1st_extmum)):
        deg_1st_extmum[i] = ext_deg[index_1st_extmum[i]]
    
    print(pattern_db1d_1st_extmum)
    
    ext_deg.remove(deg_1st_extmum)
    ext_pattern_db1d.remove(pattern_db1d_1st_extmum)
    
    pattern_db1d_2nd_extmum = max(ext_pattern_db1d)  # relative value
    index_2nd_extmum = ext_pattern_db1d.index(pattern_db1d_2nd_extmum)
    deg_2nd_extmum = ext_deg[index_2nd_extmum]
    
    
    print(pattern_db1d_2nd_extmum)
    print(deg_2nd_extmum)
    #float("{0:.2f}".format(x)), x = format(3.1415926, '.0f')
    return float(format(pattern_db1d_1st_extmum, '.2f')), \
            float(format(pattern_db1d_2nd_extmum - pattern_db1d_1st_extmum, '.2f')), \
            float(format(deg_1st_extmum[0], '.0f')), \
            float(format(deg_2nd_extmum, '.0f'))
            
def taplot_cart1d(freq_list, plot_data_list, color_list, ln_type_list, xlabel, ylabel,
                  freq_limits, x_resolution, y_resolution,
                  highlight_band, qualifying_line,
                  y_mag_limits, legend_label_list,
                  figure_name, fig_type, figure_folder):
    #  plot multi curves in 1D Cartesian
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches as patches
    freq_lower_limit = freq_limits[0]
    freq_upper_limit = freq_limits[1]
    y_mag_lower_limit = y_mag_limits[0]
    y_mag_upper_limit = y_mag_limits[1]

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['figure.figsize'] = (4.32, 3.24)  # set default size of plots
    # plt.rcParams['image.interpolation'] = 'nearest'  # 设置 interpolation style
    # plt.rcParams['image.cmap'] = 'gray'
    plt.rcParams['savefig.dpi'] = 300  # 图片像素
    plt.rcParams['figure.dpi'] = 300  # 分辨率

    fig, ax = plt.subplots(figsize=(4.32, 3.24))

    for freq, plot_data, color, ln_type in zip(freq_list, plot_data_list, color_list, ln_type_list):
        freq_in_range = freq[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]
        # freq_in_range[np.where((6.056 <= freq) & (freq <= 12.16))]
        plot_data_in_range = plot_data[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]
        # plot_data_in_range = plot_data[np.where((x_lower_limit <= freq & freq <= x_upper_limit))]
        sample_point_num = len(freq_in_range)
        marker_every = int(np.ceil(sample_point_num / 20))  # 40 markers in total
        # print(marker_every)
        ax.plot(freq_in_range, plot_data_in_range, color[0]+ln_type+color[1], markersize=5, markevery=marker_every)  # color=color, ls=ln_type # fmt = '[marker][line][color]'

    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)

    ax.set_xlim(freq_lower_limit, freq_upper_limit)
    ax.set_ylim(y_mag_lower_limit, y_mag_upper_limit)
    ax.grid(axis='x', linewidth=1, linestyle='--', color='0.75')
    ax.grid(axis='y', linewidth=1, linestyle='--', color='0.75')
    # x_tick_num = int((x_upper_limit - x_lower_limit)/x_resolution)

    x_ticks = np.arange(freq_lower_limit, freq_upper_limit + x_resolution / 2, x_resolution)
    y_ticks = np.arange(y_mag_lower_limit, y_mag_upper_limit + y_resolution / 2, y_resolution)
    # print(x_ticks, y_ticks)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    ax.hlines(y=qualifying_line, xmin=highlight_band[0], xmax=highlight_band[1], linewidth=1, color='r')
    ax.add_patch(patches.Rectangle((highlight_band[0], y_mag_lower_limit),
                                   highlight_band[1] - highlight_band[0],
                                   y_mag_upper_limit - y_mag_lower_limit, facecolor='g', alpha=0.2))

    ax.legend(legend_label_list, fontsize=9)
    fig.tight_layout()
    # fig.set_size_inches(4.32, 3.24)
    plot_name = figure_name + fig_type
    fig.savefig(os.path.join(figure_folder, plot_name), bbox_inches='tight', dpi=300)  # dpi=500, , figsize=(4.32, 3.24)
    plt.close()

def taplot_cart1d_frame(fig, ax, xlabel, freq_limits, y_mag_limits, 
                        x_resolution, y_resolution, highlight_band, 
                        qualifying_line):    
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches as patches
    
    freq_lower_limit = freq_limits[0]
    freq_upper_limit = freq_limits[1]
    y_mag_lower_limit = y_mag_limits[0]
    y_mag_upper_limit = y_mag_limits[1]
    
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    
    ax.set_xlabel(xlabel, fontsize=9)
    ax.hlines(y=qualifying_line, xmin=highlight_band[0], xmax=highlight_band[1], linewidth=1, color='g')
    ax.add_patch(patches.Rectangle((highlight_band[0], y_mag_lower_limit),
                                   highlight_band[1] - highlight_band[0],
                                   y_mag_upper_limit - y_mag_lower_limit, facecolor='g', alpha=0.2))
    ax.set_xlim(freq_lower_limit, freq_upper_limit)
    ax.set_ylim(y_mag_lower_limit, y_mag_upper_limit)
    ax.grid(axis='x', linewidth=0.5, linestyle='--', color='0.75')
    ax.grid(axis='y', linewidth=0.5, linestyle='--', color='0.75')
    # x_tick_num = int((x_upper_limit - x_lower_limit)/x_resolution)

    x_ticks = np.arange(freq_lower_limit, freq_upper_limit + x_resolution / 2, x_resolution)
    y_ticks = np.arange(y_mag_lower_limit, y_mag_upper_limit + y_resolution / 2, y_resolution)
    # print(x_ticks, y_ticks)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    return fig, ax

def taplot_cart1d_lines(fig, ax, leftright, freq_list, plot_data_list, 
                        color_list, ln_type_list, ylabel, freq_limits, 
                        y_mag_limits, y_resolution, legend_label_list):
    #  plot multi curves in 1D Cartesian
    import numpy as np
    import sys
    import warnings
    
    freq_lower_limit = freq_limits[0]
    freq_upper_limit = freq_limits[1]
    y_mag_lower_limit = y_mag_limits[0]
    y_mag_upper_limit = y_mag_limits[1]
    
    if leftright.lower() == 'left':
        ax_plot = ax
        legendloc = 'lower left'
        ax_plot.set_ylabel(ylabel, fontsize=9)
    elif leftright.lower() == 'right':
        ax_plot = ax.twinx()  # ax, left axis by default
        legendloc = 'lower right'
        ax_plot.set_ylabel(ylabel, fontsize=9)
        ax_plot.set_ylim(y_mag_lower_limit, y_mag_upper_limit)
        ax_plot.grid(axis='y', linewidth=0.5, linestyle='--', color='0.75')
        y_ticks = np.arange(y_mag_lower_limit, y_mag_upper_limit + y_resolution / 2, y_resolution)
        ax_plot.set_yticks(y_ticks)
    else:
        warnings.warn("leftright must be either 'left' o 'right'!")
        sys.exit()
    
    for freq, plot_data, color, ln_type in zip(freq_list, plot_data_list, color_list, ln_type_list):
        freq_in_range = freq[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]
        # freq_in_range[np.where((6.056 <= freq) & (freq <= 12.16))]
        plot_data_in_range = plot_data[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]

        sample_point_num = len(freq_in_range)
        marker_every = int(np.ceil(sample_point_num / 20))  # 40 markers in total
        # print(marker_every)
        ax_plot.plot(freq_in_range, plot_data_in_range, color[0] + ln_type + color[1], markersize=5,
                markevery=marker_every)  # color=color, ls=ln_type # fmt = '[marker][line][color]'

        # ax_plot.plot(freq_in_range, plot_data_in_range, color=color, ls=ln_type)

    ax_plot.legend(legend_label_list, fontsize=9, loc=legendloc)

    fig.tight_layout()
    return fig, ax_plot


def taplot_polar1d(freq_list, plot_data_list, color_list, ln_type_list, xlabel, ylabel,
                  freq_limits, x_resolution, y_resolution,
                  highlight_band, qualifying_line,
                  y_mag_limits, legend_label_list,
                  figure_name, fig_type, figure_folder):
    #  plot multi curves in 1D Cartesian
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches as patches
    freq_lower_limit = freq_limits[0]
    freq_upper_limit = freq_limits[1]
    y_mag_lower_limit = y_mag_limits[0]
    y_mag_upper_limit = y_mag_limits[1]

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8

    fig, ax = plt.subplots(figsize=(4.32, 3.24))

    for freq, plot_data, color, ln_type in zip(freq_list, plot_data_list, color_list, ln_type_list):
        freq_in_range = freq[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]
        # freq_in_range[np.where((6.056 <= freq) & (freq <= 12.16))]
        plot_data_in_range = plot_data[np.where(np.logical_and(freq_lower_limit <= freq, freq <= freq_upper_limit))]
        # plot_data_in_range = plot_data[np.where((x_lower_limit <= freq & freq <= x_upper_limit))]

        ax.plot(freq_in_range, plot_data_in_range, color=color, ls=ln_type)

    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)

    ax.set_xlim(freq_lower_limit, freq_upper_limit)
    ax.set_ylim(y_mag_lower_limit, y_mag_upper_limit)
    ax.grid(axis='x', linewidth=1, linestyle='--', color='0.75')
    ax.grid(axis='y', linewidth=1, linestyle='--', color='0.75')
    # x_tick_num = int((x_upper_limit - x_lower_limit)/x_resolution)

    x_ticks = np.arange(freq_lower_limit, freq_upper_limit + x_resolution / 2, x_resolution)
    y_ticks = np.arange(y_mag_lower_limit, y_mag_upper_limit + y_resolution / 2, y_resolution)
    # print(x_ticks, y_ticks)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)

    ax.hlines(y=qualifying_line, xmin=highlight_band[0], xmax=highlight_band[1], linewidth=1, color='r')
    ax.add_patch(patches.Rectangle((highlight_band[0], y_mag_lower_limit),
                                   highlight_band[1] - highlight_band[0],
                                   y_mag_upper_limit - y_mag_lower_limit, facecolor='g', alpha=0.2))

    ax.legend(legend_label_list, fontsize=9)
    fig.tight_layout()
    plot_name = figure_name + fig_type
    fig.savefig(os.path.join(figure_folder, plot_name), figsize=(4.32, 3.24), bbox_inches='tight', dpi=300)  # dpi=500
    plt.close()

def plotmesh2d(X, Y, Z, xlabel, ylabel, cbar_label, fig_type, plot_title, figure_folder, Z_limit, *args):
    if not Z_limit:
        cmin, cmax = np.min(Z), np.max(Z)
    else:
        cmin, cmax = Z_limit[0], Z_limit[1]
    aspect_ratio = (np.max(Y) - np.min(Y)) / (np.max(X) - np.min(X))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.pcolormesh(X, Y, Z, cmap='jet', vmin=cmin, vmax=cmax)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(plot_title)
    cbar = plt.colorbar()
    ctks = [round(item, 2) for item in np.linspace(cmin, cmax, 10, endpoint=True)]
    cbar.set_ticks(ctks)
    cbar.set_ticklabels(ctks)
    plt.tight_layout()
    ax.set_aspect(aspect_ratio)
    cbar.set_label(cbar_label)
    fig_file_title = plot_title + fig_type
    fig_dir = os.path.join(*[figure_folder, fig_file_title])
    plt.savefig(fig_dir, bbox_inches='tight', pad_inches=0.02, dpi=300)
    plt.close()

class PatternPlot(object):
    """

    """
    def __init__(self, filename):
        self.filename = filename