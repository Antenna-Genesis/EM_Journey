import numpy as np
import scipy as sp
import sys


def sphere_qualified_percentage(theta_rad_list, phi_rad_list, pattern_matrix_db, averaged_gain_db, gain_variation):
    """ to calculate the percentage of the qualified gain on a unit sphere
        theta_list and phi_list are in radian,
        pattern_matrix_db is in dB, column for the same phi, row for the same theta
        averaged_gain_db and gain_variation are in dB
        return value in linear, but not in percentage
    """
    #  calculate the angle steps
    theta_step = theta_rad_list[1] - theta_rad_list[0]
    phi_step = phi_rad_list[1] - phi_rad_list[0]
    phi_num = len(phi_rad_list)  # measure the list length of phi
    theta_num = len(theta_rad_list)  # measure the list length of theta
    (pattern_row, pattern_col) = pattern_matrix_db.shape
    # measure the pattern matrix
    if pattern_row != theta_num or pattern_col != phi_num:
        sys.exit('The dimensions of the pattern matrix is inconsistent with phi and theta list!')

    #  pick up the limits for both theta and phi
    theta_limit_list = np.array([np.amin(theta_rad_list), np.amax(theta_rad_list)])
    phi_limit_list = np.array([np.amin(phi_rad_list), np.amax(phi_rad_list)])
    phi_min_index = int(sp.floor(phi_limit_list[0] / phi_step))
    phi_max_index = int(sp.ceil(phi_limit_list[1] / phi_step))
    theta_min_index = int(sp.floor(theta_limit_list[0] / theta_step))
    theta_max_index = int(sp.ceil(theta_limit_list[1] / theta_step))
    #  calculate a key constant value during the integration
    temp = theta_step * phi_step * sp.cos(theta_step / 2)
    qualified_angle = 0  # initialization
    for phi_index in range(phi_min_index, phi_max_index):
        for theta_index in range(theta_min_index, theta_max_index):
            gain_single_direction = pattern_matrix_db[theta_index, phi_index]
            if (averaged_gain_db - gain_variation) <= gain_single_direction <= (averaged_gain_db + gain_variation):
                #  the requirement from Arris is for the gain variation
                qualified_angle += temp * sp.sin((theta_rad_list[theta_index] + 0.5 * theta_step))
                #  the qualified region is added piece by piece
    interested_angle = (sp.cos(theta_limit_list[0]) - sp.cos(theta_limit_list[1])) *\
                       (phi_limit_list[1] - phi_limit_list[0])
    #  calculate the overall interested region
    qualified_percentage = qualified_angle / interested_angle
    print('Qualified percentage on the sphere is {}%'.format(qualified_percentage*100))
    return qualified_percentage


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
    pattern_matrix_db = np.zeros((theta_size, phi_size))
    averaged_gain_db = 0
    gain_variation = 1
    sphere_qualified_percentage(theta_rad_list, phi_rad_list, pattern_matrix_db, averaged_gain_db, gain_variation)
