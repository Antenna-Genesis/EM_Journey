import numpy as np
import scipy as sp
import sys
from scipy.integrate import simps
import matplotlib.pyplot as plt


def sphere_integral(_theta_rad_list, _phi_rad_list, _pattern_matrix_linear):
    """to calculate the average gain on a unit sphere

        theta_list and phi_list are in radian, from 0 to pi and from 0 to 2*pi
        pattern_matrix_linear is in linear, column for the same phi, row for the same theta,
        average gain equals the antenna efficiency
    """
    _phi_num = len(_phi_rad_list)  # measure the list length of phi
    _pattern_theta_integration_array = np.zeros(_phi_num)
    # create empty array to store integral along theta for different phi angles
    _theta_num = len(_theta_rad_list)  # measure the list length of theta
    (_pattern_row, _pattern_col) = _pattern_matrix_linear.shape
    # measure the pattern matrix
    if _pattern_row != _theta_num or _pattern_col != _phi_num:
        sys.exit('The dimensions of the pattern matrix is inconsistent with phi and theta list!')
    for _phi_index in range(_phi_num):
        _pattern_theta_integration_array[_phi_index] = simps(sp.sin(_theta_rad_list) *
                                                             _pattern_matrix_linear[:, _phi_index],
                                                             _theta_rad_list)  # integration along theta

    _pattern_integral = simps(_pattern_theta_integration_array, _phi_rad_list)
    #  integration along phi
    #  averaged_gain_db = 10*sp.log10(averaged_gain)  # change the result to be in dB format
    print(f'The integral value (linear value) on the sphere is {_pattern_integral:,4f}')
    return _pattern_integral  # return linear result


def sphere_average(theta_rad_list, phi_rad_list, pattern_matrix_linear):
    """to calculate the average gain on a unit sphere

        theta_list and phi_list are in radian, from 0 to pi and from 0 to 2*pi
        pattern_matrix_linear is in linear, column for the same phi, row for the same theta,
        average gain equals the antenna efficiency
    """
    phi_num = len(phi_rad_list)  # measure the list length of phi
    pattern_theta_integration_array = np.zeros(phi_num)
    # create empty array to store integral along theta for different phi angles
    theta_num = len(theta_rad_list)  # measure the list length of theta
    (pattern_row, pattern_col) = pattern_matrix_linear.shape
    # measure the pattern matrix
    if pattern_row != theta_num or pattern_col != phi_num:
        sys.exit('The dimensions of the pattern matrix is inconsistent with phi and theta list!')
    for phi_index in range(phi_num):
        pattern_theta_integration_array[phi_index] = simps(sp.sin(theta_rad_list) * pattern_matrix_linear[:, phi_index],
                                                           theta_rad_list)  # integration along theta

    averaged_gain = simps(pattern_theta_integration_array, phi_rad_list) / (4 * sp.pi)
    #  integration along phi and do the average step
    #  averaged_gain_db = 10*sp.log10(averaged_gain)  # change the result to be in dB format
    print('The average value (linear value) on the sphere is', averaged_gain)
    return averaged_gain  # return linear result


'''
test the function
'''
if __name__ == '__main__':
    # for module test only
    theta_size = 181
    theta_delta = sp.pi / theta_size
    theta_rad_list = np.linspace(0, sp.pi, theta_size)
    # print(theta_rad_list * 180 / sp.pi)
    phi_size = 361
    phi_delta = 2 * sp.pi / phi_size
    phi_rad_list = np.linspace(0, 2 * sp.pi, phi_size)
    # print(phi_rad_list * 180 / sp.pi)
    pattern_matrix_linear = np.ones((theta_size, phi_size))

    avg = sphere_average(theta_rad_list, phi_rad_list, pattern_matrix_linear)
    # print(avg)
