import numpy as np
import scipy as sp
from scipy.integrate import simps


def sphere_average(theta_rad_list, phi_rad_list, pattern_matrix_linear):
    """to calculate the average gain on a unit sphere
        theta_list and phi_list are in radian, from 0 to pi and from 0 to 2*pi
        pattern_matrix_linear is in linear, complex, column for the same phi, row for the same theta, must be np.array format
        average gain equals the antenna efficiency
    """
    import numpy as np
    import warnings
    if not isinstance(pattern_matrix_linear, (np.ndarray, np.generic)):
        warnings.warn('pattern_matrix_linear must be np.array type')
    real_or_complex = 'complex'
    phi_num = len(phi_rad_list)  # measure the list length of phi
    # create empty array to store integral along theta for different phi angles
    theta_num = len(theta_rad_list)  # measure the list length of theta
    (pattern_row, pattern_col) = pattern_matrix_linear.shape
        # measure the pattern matrix
    if pattern_row != theta_num or pattern_col != phi_num:
        warnings.warn('The dimensions of the pattern matrix is inconsistent with phi and theta list!')
        exit()
        
    if real_or_complex.lower() == 'real':
        pattern_theta_integration_array = np.zeros(phi_num)
        for phi_index in range(phi_num):
            pattern_theta_integration_array[phi_index] = simps(np.sin(theta_rad_list) * pattern_matrix_linear[:, phi_index],
                                                               theta_rad_list)  # integration along theta

            averaged_gain = simps(pattern_theta_integration_array, phi_rad_list) # / (4*np.pi)
            # integration along phi and do the average step
    elif real_or_complex.lower()  == 'complex':
        pattern_theta_integration_array_re = np.zeros(phi_num)
        pattern_theta_integration_array_im = np.zeros(phi_num)
        pattern_matrix_linear_re = np.real(pattern_matrix_linear)
        pattern_matrix_linear_im = np.imag(pattern_matrix_linear)
        for phi_index in range(phi_num):
            pattern_theta_integration_array_re[phi_index] = simps(np.sin(theta_rad_list) * pattern_matrix_linear_re[:, phi_index],theta_rad_list)  # integration along theta
            pattern_theta_integration_array_im[phi_index] = simps(np.sin(theta_rad_list) * pattern_matrix_linear_im[:, phi_index],theta_rad_list)  # integration along theta
        averaged_gain = (simps(pattern_theta_integration_array_re, phi_rad_list) + 1j * simps(pattern_theta_integration_array_im, phi_rad_list)) # / (4*np.pi)
    else:
        warnings.warn('real_or_complex must be either real or complex.')
    
# tried np.iscomplexobj(pattern_matrix_linear), not work, stranger

    return averaged_gain  # return linear result

def ecc(theta_rad_list, phi_rad_list, pattern1_vector_linear, pattern2_vector_linear):
    '''
    pattern1_vector_linear, pattern2_vector_linear should be linear vector pattern matrixs
    matrix.shape = theta_num, phi_num, 2 (E_phi, E_theta)
    so that the format is similar to that of class 'pattern_all.SatimoPattern'
    both E_theta, E_phi should be included, in compex format
    https://nl.mathworks.com/help/antenna/ug/correlation-coeffecient.html
    example to stack 2D arrays to 3D array
    a = np.array([[1,2,3],[11,22, 33],[111,222,333]])
    b = np.array([[10,20,30],[110,220,330],[1110,2220,3330]])
    c = np.array([[100,200,300],[1100,2200,3300],[11100,22200,33300]])
    d = np.stack((a, b, c), axis=2) # new axis in the last dimension
    '''
    # temp patterns to store E_theta and E_phi
    p1_phi = pattern1_vector_linear[:, :, 0]
    p2_phi = pattern2_vector_linear[:, :, 0]
    p1_theta = pattern1_vector_linear[:, :, 1]
    p2_theta = pattern2_vector_linear[:, :, 1]
    # element-wise product
    # for NumPy's matrix type, * returns the inner product, not element-wise.
    # for the usual ndarray class, * means element-wise product
    pco_temp = p1_phi * np.conjugate(p2_phi) + p1_theta * np.conjugate(p2_theta)
    p1_temp = np.abs(p1_phi) ** 2 + np.abs(p1_theta) ** 2
    p2_temp = np.abs(p2_phi) ** 2 + np.abs(p2_theta) ** 2
    a = np.abs(sphere_average(theta_rad_list, phi_rad_list, pco_temp)) ** 2
    b = sphere_average(theta_rad_list, phi_rad_list, p1_temp)
    c = sphere_average(theta_rad_list, phi_rad_list, p2_temp)
    ecc = np.real(a / (b * c))
    return ecc
'''
test the function
'''
if __name__ == '__main__':
    import os
    import sys
    os.chdir("..")  # go up one dir layer
    import pattern_all as pattern
    
    
    # result_root_folder = r'C:\Dropbox\WorkStation1\Garen\Measured 3-D RP for 3 ports 0616'
    # pattern1_full_path = os.path.join(result_root_folder, 'Port 1 RP 3D.TXT')
    # pattern2_full_path = os.path.join(result_root_folder, 'Port 2 RP 3D.TXT')
    
    # pattern_temp1 = pattern.SatimoPattern(pattern1_full_path)
    # pattern_temp1.pattern_groupby_freq()
    # pattern_temp1.pattern_format_kai()
    # p1 = pattern_temp1.kai_pattern
    # phi_rad = pattern_temp1.phi_rad_kai
    # theta_rad = pattern_temp1.theta_rad_kai
    # p1 = p1[0, :, :, 1::]
    # p1 = np.reshape(p1, (len(theta_rad), len(phi_rad), 2))
    
    # pattern_temp2 = pattern.SatimoPattern(pattern2_full_path)
    # pattern_temp2.pattern_groupby_freq()
    # pattern_temp2.pattern_format_kai()
    # p2 = pattern_temp2.kai_pattern
    # p2 = p2[0, :, :, 1::]
    # p2 = np.reshape(p2, (len(theta_rad), len(phi_rad), 2))
    
    # ecc_scalar = ecc(theta_rad, phi_rad, p1, p2)
    # print(ecc_scalar)
    
    result_root_folder = r'C:\Temp\CST_Projects'
    pattern1_full_path = os.path.join(result_root_folder, 'ff1.TXT')
    pattern2_full_path = os.path.join(result_root_folder, 'ff2.TXT')
    
    pattern_temp1 = pattern.CST_txt_pattern(pattern1_full_path)
    # sys.exit()

    p1 = pattern_temp1.cst_pattern
    phi_rad = pattern_temp1.phi_rad_kai
    theta_rad = pattern_temp1.theta_rad_kai
    p1 = p1[:, :, 1::]
    p1 = np.reshape(p1, (len(theta_rad), len(phi_rad), 2))
    
    pattern_temp2 = pattern.CST_txt_pattern(pattern2_full_path)
    p2 = pattern_temp2.cst_pattern
    p2 = p2[:, :, 1::]
    p2 = np.reshape(p2, (len(theta_rad), len(phi_rad), 2))
    
    ecc_scalar = ecc(theta_rad, phi_rad, p1, p2)
    print(ecc_scalar)