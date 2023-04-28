"""
Waveguide Calculation
by Kai Lu, Apr. 22, 2020
kai.lu@my.cityu.edu.hk

jnyn_zeros:
Compute nt zeros of Bessel functions Jn(x), Jn’(x), Yn(x), and Yn’(x).
Returns 4 arrays of length nt, corresponding to the first nt zeros of
Jn(x), Jn’(x), Yn(x), and Yn’(x), respectively.
"""
import numpy as np
from scipy.special import jnyn_zeros


def cylindrical_wg_cutoff_freq(_te_or_tm, _n, _m, _radius):
    '''

    :param _te_or_tm:
    :param _n: order of Bessel function, circle number
    :param _m: _m th zero, radial number
    :param _radius: radius of cylindrical tube, in mm
    :return: cutoff frequency, in GHz
    '''
    import numpy as np
    import warnings
    from scipy.constants import speed_of_light
    if _te_or_tm.lower() == 'te':
        _jn_indx = 1
    elif _te_or_tm.lower() == 'tm':
        _jn_indx = 0
    else:
        warnings.warn("_te_or_tm can be either te or tm")
        exit()
    _jn_zero = jnyn_zeros(n, _m)[_jn_indx][0]
    _cutoff_freq = _jn_zero * (speed_of_light / 1e6) / np.pi / _radius / 2
    print(f"For radius of {_radius} mm, cutoff frequency of the {_te_or_tm}_{_n}_{_m} mode is: {_cutoff_freq:.3f} GHz")
    return _cutoff_freq


if __name__ == '__main__':
    import time
    import sys
    import os

    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')
    ###############################################################################
    for n in range(3):
        tmp1 = cylindrical_wg_cutoff_freq('te', n, 1, 7)
        tmp2 = cylindrical_wg_cutoff_freq('tm', n, 1, 7)
        # bessel_zeros = jnyn_zeros(n, 1)
        # print(f"Values for zeros of Bessel and its derivative are {bessel_zeros[0]} and {bessel_zeros[1]}")

    ###############################################################################
    elapsed_time = time.time() - start_time
    print(f'Overall time for this post-processing is: {elapsed_time:.3f}s')
    print('Finished all!')
