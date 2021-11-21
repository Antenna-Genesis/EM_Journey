# -*- coding: utf-8 -*-
""" PySNF Version 0.1

Notes
-----
Version 0.1 has very limited documentation.
More documentation is planned for Version 0.2

References
----------
[1] J.E. Hansen, Spherical Near-Field Antenna Measurements, 1988
"""

# ---------------------
# IMPORTS
# ---------------------
import math
import numpy
import scipy.special as sps
import fractions
import matplotlib.pyplot as plt

# ---------------------
# GLOBAL VARIABLES
# ---------------------
INF = numpy.inf
PI = numpy.pi

# ---------
# SELF TEST
# ---------
if __name__ == '__main__':
    # Self-test code goes here...
    dum = 0

# ---------------------
# FUNCTIONS AND METHODS
# ---------------------
# ------------------------------------------------------------------------


def nearfield2farfield(nearfield, dtheta_out, dphi_out, probe=None, probe_pol='x', ka=INF,
                       n_max=None, m_max=None, nu_max=None):

    # Calculate the spherical wave coefficients of the UUT
    q_n_m_s = field2wavecoeffs(nearfield, probe, probe_pol, ka, n_max, m_max, nu_max)

    # From the spherical wave coefficients, calculate the far-field
    theta, phi = wavecoeffs2farfield_uniform(q_n_m_s, dtheta_out, dphi_out)

    # Organize into a dictionary
    farfield = {'theta':theta, 'phi':phi, 'dT':dtheta_out, 'dP':dphi_out}

    return farfield


# ------------------------------------------------------------------------


def field2wavecoeffs(uut, probe=None, probe_pol='x', ka=INF, n_max=None, m_max=None, nu_max=None):

    # Get the values for w_n_m_mu
    w_n_m_mu = field2w_n_m_mu(uut, n_max, m_max, probe_pol)

    # If n_max was passed into this function as None, determine n_max
    if n_max is None:
        n_max = numpy.size(w_n_m_mu, 0)

    # If m_max was passed into this function as None, determine m_max
    if m_max is None:
        m_max = (numpy.size(w_n_m_mu, 1) - 1)/2

    # Get the probe response constants
    if (probe is None) and (probe_pol is 'x') and (ka is INF):
        p_n_mu_s = dipole_probe_response_constants(n_max)
    elif (probe is None) and (probe_pol is 'y') and (ka is INF):
        raise Exception("nearfield2farfield has not yet implemented the infinitely "
                        "remote y-polarized electric dipole option")
    elif (probe is None) and (probe_pol is 'x') and (ka < INF):
        raise Exception("nearfield2farfield has not yet implemented the finitely "
                        "remote x-polarized electric dipole option")
    elif (probe is None) and (probe_pol is 'y') and (ka < INF):
        raise Exception("nearfield2farfield has not yet implemented the finitely "
                        "remote y-polarized electric dipole option")
    else:
        # If nu_max was passed into this function as None, determine nu_max
        if nu_max is None:
            nu_max = numpy.size(probe['theta'], axis=0)/2
        t_p = field2wavecoeffs(probe, n_max=nu_max, m_max=1)  # t_p is nu, mu, sig
        t_p_rot = rotate_wavecoeffs_about_axis(t_p,'x')  # t_p_rot is nu, mu, sig
        r_p = reciprocity(t_p_rot)  # r_p is nu, mu, sig
        r_p = numpy.swapaxes(r_p, 0, 2)  # r_p is now sig, mu, nu
        p_n_mu_s = probe_response_constants(r_p, n_max, ka)

    # Initialize the wave coefficient matrix
    q_n_m_s = numpy.zeros((n_max, 2*m_max+1, 2), dtype='complex')

    # Pull out and reshape the necessary values of the probe response constants
    p_n_neg1_1 = numpy.reshape(p_n_mu_s[:, 0, 0], (n_max,1))  # mu = -1 , s = 1
    p_n_pos1_1 = numpy.reshape(p_n_mu_s[:, 1, 0], (n_max,1))  # mu = +1 , s = 1
    p_n_neg1_2 = numpy.reshape(p_n_mu_s[:, 0, 1], (n_max,1))  # mu = -1 , s = 2
    p_n_pos1_2 = numpy.reshape(p_n_mu_s[:, 1, 1], (n_max,1))  # mu = +1 , s = 2

    # Solve for q_n_m_s as described in [1],(4.133) and [1],(4.134), AND A FUTURE BLOG POST
    # Note: Give Jeffrey Hyman developer credit here.
    determinant = p_n_pos1_1*p_n_neg1_2 - p_n_neg1_1*p_n_pos1_2
    q_n_m_s[:, :, 0] = (p_n_neg1_2*w_n_m_mu[:, :, 1] - p_n_pos1_2*w_n_m_mu[:, :, 0])/determinant
    q_n_m_s[:, :, 1] = (p_n_pos1_1*w_n_m_mu[:, :, 0] - p_n_neg1_1*w_n_m_mu[:, :, 1])/determinant

    return q_n_m_s

# ------------------------------------------------------------------------


def wavecoeffs2farfield_uniform(q_n_m_s, dtheta, dphi):

    # Determine n_max and m_max from q_n_m_s
    n_max, m_max, s_max = numpy.shape(q_n_m_s)
    m_max = (m_max - 1)/2

    # Determine the number of theta and phis points required based on dT and dP
    numthetas = int(180.0/dtheta + 1)
    numphis = int(360.0/dphi)

    # Get the dipole probe response constants
    # (N x 2 x 2, where dim 0 = n, dim 1 = mu, dim 2 = s)
    p_n_mu_s = dipole_probe_response_constants(n_max)

    # Copy out the mu==1, s==1 probe response constants
    p_n = numpy.reshape(p_n_mu_s[:, 0, 0], (n_max,1,1))  # N x M x Theta

    # Calculate the rotation coefficients
    # (N x 3 x M x numThetas)
    d_n_mu_m = rotation_coefficients(n_max, m_max, 1, numpy.linspace(0, PI, numthetas))

    # Calculate the addition and subtraction of the rotation coefficients
    # (N x M x numThetas)
    dp1_plus_dm1 = d_n_mu_m[:, 2, :, :] + d_n_mu_m[:, 0, :, :]  # N x M x Theta
    dp1_minus_dm1 = d_n_mu_m[:, 2, :, :] - d_n_mu_m[:, 0, :, :]

    # Reshape the spherical wave coefficients to get ready for multiplication
    q_n_m_s = numpy.reshape(q_n_m_s, (n_max,2*m_max+1,s_max,1))  # N x M x S x Theta

    # Perform the N summation as detailed in [1], (4.135), AND A FUTURE BLOG POST
    temp = p_n*(q_n_m_s[:, :, 0, :]*dp1_plus_dm1 + q_n_m_s[:, :, 1, :]*dp1_minus_dm1)  # N x M x Theta
    n_sum_chi_0 = numpy.swapaxes(numpy.sum(temp, 0), 0, 1)  # Theta x M

    # Perform the M summations as detailed in [1], (4.135), using an FFT
    n_sum_chi_0 = numpy.fft.ifftshift(n_sum_chi_0, axes=1)
    temp = numpy.zeros((numthetas,numphis),dtype='complex')
    temp[:,0:m_max+1] = n_sum_chi_0[:,0:m_max+1]
    temp[:,numphis-m_max:] = n_sum_chi_0[:,m_max+1:]
    theta_pol = fft(temp, axis=1)

    # Perform the N summation as detailed in [1], (4.135), AND A FUTURE BLOG POST
    temp = 1j*p_n*(q_n_m_s[:, :, 0, :]*dp1_minus_dm1 + q_n_m_s[:, :, 1, :]*dp1_plus_dm1)  # N x M x Theta
    n_sum_chi_90 = numpy.swapaxes(numpy.sum(temp, 0), 0, 1)  # Theta x M

    # Perform the M summations as detailed in [1], (4.135), using an FFT
    n_sum_chi_90 = numpy.fft.ifftshift(n_sum_chi_90, axes=1)
    temp = numpy.zeros((numthetas,numphis),dtype='complex')
    temp[:,0:m_max+1] = n_sum_chi_90[:,0:m_max+1]
    temp[:,numphis-m_max:] = n_sum_chi_90[:,m_max+1:]
    phi_pol = fft(temp, axis=1)

    return theta_pol, phi_pol

# ------------------------------------------------------------------------


def field2w_n_m_mu(uut, n_max=None, m_max=None, probe_pol='x'):

    # Make a copy of the UUT data so that we don't change the original data.
    # This is needed since dictionaries are mutable objects.
    aut = uut.copy()

    # AUT is a single sphere of data, i.e., 0 <= theta <= 180 and 0 <= phi < 360.
    # Use symmetry relationship in [1],Page 192 to create a double sphere of data,
    # i.e., 0 <= theta < 360 and 0 <= phi < 360.

    aut['theta'] = singlesphere2doublesphere(aut['theta'])
    aut['phi'] = singlesphere2doublesphere(aut['phi'])

    num_th = numpy.size(aut['theta'], axis=0)
    num_ph = numpy.size(aut['theta'], axis=1)

    if n_max is None:
        n_max = num_th/2  # This works because num_th should always be even after
                          # the singlesphere2doublesphere function
    elif n_max > num_th/2:
        raise Exception("n_max must be less than or equal to num_th/2")

    if m_max is None:
        m_max = num_ph/2  # This works because num_ph should always be even after
                          # the singlesphere2doublesphere function
    elif m_max > num_ph/2:
        raise Exception("m_max must be less than or equal to num_ph/2")

    # Perform (4.126)
    w_th_ph_mu = numpy.zeros((num_th, num_ph, 2), dtype='complex')
    if probe_pol is 'x':
        w_th_ph_mu[:, :, 1] = (1./2.)*(aut['theta'] - 1j*aut['phi'])  # mu = +1
        w_th_ph_mu[:, :, 0] = (1./2.)*(aut['theta'] + 1j*aut['phi'])  # mu = -1
    elif probe_pol is 'y':
        w_th_ph_mu[:, :, 1] = (1./2.)*(aut['phi'] - 1j*-aut['theta'])  # mu = +1
        w_th_ph_mu[:, :, 0] = (1./2.)*(aut['phi'] + 1j*-aut['theta'])  # mu = -1
    else:
        raise Exception("probePol must either be 'x' or 'y'")

    # Perform (4.127)
    temp = ifft(w_th_ph_mu, axis=1)

    # Reorganize such that m runs from -m_max to m_max
    w_th_m_mu = numpy.zeros((num_th, 2*m_max+1, 2), dtype='complex')
    temp = numpy.fft.fftshift(temp, axes=(1,))
    if num_ph/2.0 == m_max:
        w_th_m_mu[:, :-1, :] = temp
        w_th_m_mu[:, -1, :] = temp[:, 0, :]
    elif num_ph/2.0 > m_max:
        w_th_m_mu[:, :, :] = temp[:, num_ph/2-m_max:num_ph/2+m_max+1, :]
    else:
        raise Exception("Bad value for num_ph.")

    # Perform (4.128)
    temp = ifft(w_th_m_mu, axis=0)

    # Reorganize such that n runs from -n_max to n_max
    b_l_m_mu = numpy.zeros((2*n_max+1, 2*m_max+1, 2), dtype='complex')
    temp = numpy.fft.fftshift(temp, axes=(0,))
    if num_th/2.0 == n_max:
        b_l_m_mu[:-1, :, :] = temp
        b_l_m_mu[-1, :, :] = temp[0, :, :]
    elif num_th/2.0 > n_max:
        b_l_m_mu[:, :, :] = temp[num_th/2-n_max:num_th/2+n_max+1, :, :]
    else:
        raise Exception("Bad value for num_th.")

    # Calculate the pi_wiggle array with [1],(4.84) and [1],(4.86)
    pi_wig = pi_wiggle(n_max)

    # Calculate the b_l_m_mu_wiggle array from b_l_m_mu using [1],(4.87)
    b_l_m_mu_wiggle = b_wiggle(b_l_m_mu)

    # Calculate k_mp with fast convolution via FFT methods as explained in [1],(4.89).
    # However, note that [1],(4.89) has a typo. If correct, [1],(4.89) should read:
    #
    #   K(m') = IDFT{ DFT{ PI_wiggle(i) | i = 0,1,...,4N-1 } *
    #                 DFT{ b_j_m_mu_wiggle | j = 0,1,...,4N-1 } }
    #
    k_mp = ifft(fft(pi_wig, axis=0) * fft(b_l_m_mu_wiggle, axis=0), axis=0)

    # Keep only the values of k_mp where -n_max <= m' <= n_max.
    # This is required prior to the evaluation of [1],(4.92)
    temp = numpy.zeros((2*n_max+1, 2*m_max+1, 2), dtype='complex')
    temp[0:n_max, :, :] = k_mp[3*n_max:, :, :]
    temp[n_max:, :, :] = k_mp[0:n_max+1, :, :]
    k_mp = temp

    # Pull out k_mp for mu == -1 and mu == +1
    k_mp_m1 = numpy.reshape(k_mp[:, :, 0], (1, 2*n_max+1, 2*m_max+1))
    k_mp_p1 = numpy.reshape(k_mp[:, :, 1], (1, 2*n_max+1, 2*m_max+1))

    # Initialize the n and m arrays
    n_array = numpy.reshape(numpy.linspace(1, n_max, n_max), (n_max, 1))
    m_array = numpy.reshape(numpy.linspace(-m_max, m_max, 2*m_max+1), (1, 2*m_max+1))

    # Initialize a delta pyramid helper function
    def get_mi(m_): return m_ + n_max  # This returns the m index of the deltas

    # Get the deltas for 1 <= n <= n_max and -m_max <= m <= m_max
    deltas = delta_pyramid(n_max)
    deltas = deltas[1:, :, get_mi(-m_max):get_mi(m_max)+1]

    # Update the delta pyramid helper function
    def get_mi(m_): return m_ + m_max  # This returns the m index of the revised deltas

    # Get the deltas for only mu == -1 or 1
    deltas_mu_m1 = numpy.reshape(deltas[:, :, get_mi(-1)], (n_max, 2*n_max+1, 1))
    deltas_mu_p1 = numpy.reshape(deltas[:, :, get_mi(+1)], (n_max, 2*n_max+1, 1))

    # Calculate w_n_m_mu as shown in [1],(4.92)
    w_n_m_mu = numpy.zeros((n_max, 2*m_max+1, 2), dtype='complex')
    w_n_m_mu[:, :, 0] = (
        (2.0*n_array+1.0)/2.0 *
        1j**(-1-m_array) *
        numpy.sum(deltas_mu_m1*deltas*k_mp_m1, axis=1)
    )
    w_n_m_mu[:, :, 1] = (
        (2.0*n_array+1.0)/2.0 *
        1j**(+1-m_array) *
        numpy.sum(deltas_mu_p1*deltas*k_mp_p1, axis=1)
    )

    return w_n_m_mu


# ------------------------------------------------------------------------


def incomplete_farfield_pattern_functions(n_max, m_max, thetas, delta=1.0e-6):

    # Check to make sure that thetas are between 0 and pi
    if numpy.any(thetas < 0) or numpy.any(thetas > PI):
        raise Exception("thetas must all be greater than or equal to 0, and less than or equal to pi.")

    # If any theta value is less than the delta/10.0, add the delta
    zero_inds = thetas < delta/10.0
    thetas[zero_inds] += delta

    # If any theta value is within delta/10.0 of pi, subtract the delta
    pi_inds = thetas > (PI - delta/10.0)
    thetas[pi_inds] -= delta

    # Calculate the normalized associated Legendre function values,
    # and the values of the derivative with respect to cos(theta)
    lpmn, dlpmn = lpmn_norm(n_max, m_max, thetas)  # n_max+1 by m_max+1 by len(thetas)

    # Extend the Lpmn_norm array to negative values of m,
    # such that Lpmn_norm of -m is equal to Lpmn_norm of m.
    # Also remove the n == 0 part of the array.
    lpmn_norm_extended = numpy.zeros((n_max, 2*m_max+1, len(thetas)))
    lpmn_norm_extended[:, 0:m_max, :] = numpy.fliplr(lpmn[1:, 1:, :])
    lpmn_norm_extended[:, m_max:, :] = lpmn[1:, :, :]  # n_max by 2*m_max+1 by len(thetas)
    lpmn_norm_extended = lpmn_norm_extended.reshape((n_max, 2*m_max+1, len(thetas)))

    # Extend the dLpmn_norm array to negative values of m,
    # such that dLpmn_norm of -m is equal to dLpmn_norm of m.
    # Also remove the n == 0 part of the array.
    dlpmn_norm_extended = numpy.zeros((n_max, 2*m_max+1, len(thetas)))
    dlpmn_norm_extended[:, 0:m_max, :] = numpy.fliplr(dlpmn[1:, 1:, :])
    dlpmn_norm_extended[:, m_max:, :] = dlpmn[1:, :, :]  # n_max by 2*m_max+1 by len(thetas)
    dlpmn_norm_extended = dlpmn_norm_extended.reshape((n_max, 2*m_max+1, len(thetas)))

    # Create arrays that hold the n and m indices. Also promote
    # the thetas and phis to 4-dimensional arrays. This will come in handy
    # when later multiplying the matrices (due to numpy's "broadcasting" feature).
    n_vec = numpy.linspace(1, n_max, n_max)
    n_array = numpy.reshape(n_vec, (n_max, 1, 1))
    m_vec = numpy.linspace(-m_max, m_max, 2*m_max+1)
    m_array = numpy.reshape(m_vec, (1, 2*m_max+1, 1))
    thetas = numpy.reshape(thetas, (1, 1, len(thetas)))

    # Calculate the (-m/m)**m factor, using [1],(2.19) to handle
    # the case when m==0
    nonzeroinds = m_array != 0
    mm = numpy.ones(numpy.shape(m_array))
    mm[nonzeroinds] = (-m_array[nonzeroinds] /
                       abs(m_array[nonzeroinds]))**m_array[nonzeroinds]

    # Initialize the incomplete farfield pattern function arrays,
    # one for theta polarization and one for phi polarization
    k_n_m_s_theta = numpy.zeros((n_max, 2*m_max+1, numpy.size(thetas), 2), dtype='complex')
    k_n_m_s_phi = numpy.zeros((n_max, 2*m_max+1, numpy.size(thetas), 2), dtype='complex')

    # Calculate some common terms
    term1 = numpy.sqrt(2.0/(n_array*(n_array+1.0))) * mm
    term2a = (-1j)**(n_array+1.0)
    term2b = (-1j)**n_array
    term3a = 1j*m_array*lpmn_norm_extended/numpy.sin(thetas)
    term3b = dlpmn_norm_extended
    term_1_2a = term1*term2a
    term_1_2b = term1*term2b

    # Calculate the incomplete farfield pattern function for theta-pol when s = 1, according to [1],(A1.59)
    # and a FUTURE BLOG POST
    k_n_m_s_theta[:, :, :, 0] = term_1_2a * term3a

    # Calculate the incomplete farfield pattern function for theta-pol when s = 2, according to [1],(A1.60)
    # and a FUTURE BLOG POST
    k_n_m_s_theta[:, :, :, 1] = term_1_2b * term3b

    # Calculate the incomplete farfield pattern function for phi-pol when s = 1, according to [1],(A1.59)
    # and a FUTURE BLOG POST
    k_n_m_s_phi[:, :, :, 0] = term_1_2a * -term3b

    # Calculate the incomplete farfield pattern function for phi-pol when s = 2, according to [1],(A1.60)
    # and a FUTURE BLOG POST
    k_n_m_s_phi[:, :, :, 1] = term_1_2b * term3a

    # Swap axes
    k_n_m_s_theta = numpy.swapaxes(k_n_m_s_theta, 2, 3)
    k_n_m_s_phi = numpy.swapaxes(k_n_m_s_phi, 2, 3)

    return k_n_m_s_theta, k_n_m_s_phi

# ------------------------------------------------------------------------


def delta_pyramid(n_max):
    # Function used to calculate the delta pyramid.
    # The delta pyramid is defined in [1], Section A2.4

    # Region Diagram
    #
    #      |<--(-m)---m---(+m)-->|
    #  -    ---------------------
    #  ˄   |          |          |
    #  |   |          |          |
    # -m'  |    IV    |   III    |
    #  |   |          |          |
    #  |   |          |          |
    #  m'  |---------------------|
    #  |   |          |          |
    #  |   |          |          |
    # +m'  |    II    |    I     |
    #  |   |          |          |
    #  ˅   |          |          |
    #  -    ---------------------

    # Set mp_max and m_max equal to n_max in order to simplify calculations
    mp_max = m_max = n_max

    # Initialize the matrix to store the entire delta pyramid
    deltas = numpy.zeros((n_max+1, 2*mp_max+1, 2*m_max+1))

    # Initialize two "helper" functions
    def get_mp_index(mp_): return mp_max + mp_

    def get_m_index(m_): return m_max + m_

    # Initialize the delta values for n==0 and n==1, [1],Section A2.6
    deltas[0, get_mp_index(0), get_m_index(0)] = 1.0
    deltas[1, get_mp_index(0), get_m_index(1)] = -numpy.sqrt(2.0)/2.0
    deltas[1, get_mp_index(1), get_m_index(0)] = numpy.sqrt(2.0)/2.0
    deltas[1, get_mp_index(1), get_m_index(1)] = 1.0/2.0

    # Initialize positive values of mp and m
    mp_vec = numpy.linspace(0, mp_max, mp_max+1)
    m_vec = numpy.linspace(0, m_max, m_max+1)

    # Promote mp_vec and m_vec to 2 dimensions
    # (this will facilitate broadcasting later)
    mp_array = numpy.reshape(mp_vec, (mp_max+1, 1))
    m_array = numpy.reshape(m_vec, (1, m_max+1))

    # Copy two common indices to their own variables
    ind_mp_0 = get_mp_index(0)
    ind_m_0 = get_m_index(0)

    # Traverse through each n level from n==2 to n==N
    for n in xrange(2, n_max+1):

        # Copy two more common indices to their own variables
        ind_mp_n = get_mp_index(n)
        ind_m_n = get_m_index(n)

        # Calculate this particular n level using the previous two n levels.
        # [1],(A2.35)
        term1 = -1.0/(numpy.sqrt((n+mp_array[0:n, :]) *
                                 (n-mp_array[0:n, :]) *
                                 (n+m_array[:, 0:n]) *
                                 (n-m_array[:, 0:n]))*(n-1))
        term2 = numpy.sqrt((n+mp_array[0:n, :]-1) *
                           (n-mp_array[0:n, :]-1) *
                           (n+m_array[:, 0:n]-1) *
                           (n-m_array[:, 0:n]-1))*n
        term3 = (2*n-1)*mp_array[0:n, :]*m_array[:, 0:n]

        deltas[n, ind_mp_0:ind_mp_n, ind_m_0:ind_mp_n] = term1*(
            term2*deltas[n-2, ind_mp_0:ind_mp_n, ind_m_0:ind_mp_n] +
            term3*deltas[n-1, ind_mp_0:ind_mp_n, ind_m_0:ind_mp_n])

        # Initialize the vector full of this iteration's n value
        n_vec = n*numpy.ones(n+1)
        # Calculate the bottom edge of Region I, [1],(A2.41)
        temp = 1/(2.0**n)*numpy.sqrt(sps.binom(2*n_vec, n_vec - m_vec[0:n+1]))
        deltas[n, ind_mp_n, ind_m_0:ind_m_n+1] = temp
        # Copy the bottom edge of Region I to the right edge of Region I
        # using the symmetry relationship [1],(A2.26) with m set equal to n.
        deltas[n, ind_mp_0:ind_mp_n, ind_m_n] = (-1)**(mp_vec[0:n] + n)*temp[0:n]

    # Create new n_vec, mp_vec, and m_vec vectors
    n_vec = numpy.linspace(0, n_max, n_max+1)
    mp_vec = numpy.linspace(-mp_max, mp_max, 2*mp_max+1)
    m_vec = numpy.linspace(-m_max, m_max, 2*m_max+1)

    # Promote n_vec, mp_vec, and m_vec to 3 dimensions
    # (this will facilitate broadcasting later)
    n_array = numpy.reshape(n_vec, (n_max+1, 1, 1))
    mp_array = numpy.reshape(mp_vec, (1, 2*mp_max+1, 1))
    m_array = numpy.reshape(m_vec, (1, 1, 2*m_max+1))

    # Compute Region II using symmetry relation [1],(A2.32)
    temp1 = ((-1)**(n_array + mp_array[:, get_mp_index(0):, :]) *
             deltas[:, get_mp_index(0):, get_m_index(1):])
    temp1 = temp1[:, :, ::-1]
    deltas[:, get_mp_index(0):, 0:get_m_index(0)] = temp1

    # Compute Region III using symmetry relation [1],(A2.28)
    temp2 = ((-1)**(n_array + m_array[:, :, get_m_index(0):]) *
             deltas[:, get_mp_index(1):, get_m_index(0):])
    temp2 = temp2[:, ::-1, :]
    deltas[:, 0:get_mp_index(0), get_m_index(0):] = temp2

    # Compute Region IV using symmetry relation [1],(A2.30)
    temp3 = deltas[:, get_mp_index(1):, get_m_index(1):]
    temp3 = temp3[:, ::-1, ::-1].transpose((0, 2, 1))
    deltas[:, 0:get_mp_index(0), 0:get_m_index(0)] = temp3

    # Return the deltas from the function
    return deltas


# ------------------------------------------------------------------------


def lpmn_norm(n_max, m_max, thetas):
    # Returns the normalized associated Legendre function values of
    # cos(theta), as defined in [1],(A1.25). Also returns the derivative
    # of the normalized associated Legendre function values, where the
    # derivative is taken with respect to cos(theta).

    # Make sure that the thetas variable is a numpy array
    if isinstance(thetas, float):
        thetas = numpy.array([thetas])
    else:
        thetas = numpy.array(thetas)

    # Make sure that M <= N
    if m_max > n_max:
        raise Exception('M must be less than or equal to N.')

    # Make sure that all theta values are between 0 and pi
    if numpy.any(thetas < 0) or numpy.any(thetas > PI):
        raise Exception('theta values must be between 0 and pi, inclusive.')

    # Initialize the matrices which will store the associated Legendre
    # function values. legendre_m_n_thetas will contain the associated Legendre
    # function values, whereas dlegendre_m_n_thetas will contain the derivative
    # of the associated Legendre function ( derivative taken with
    # respect to cos(theta) )
    legendre_m_n_thetas = numpy.zeros((m_max+1, n_max+1, len(thetas)))
    dlegendre_m_n_thetas = numpy.zeros((m_max+1, n_max+1, len(thetas)))

    # Loop through all theta values, using the scipy.special.lpmn
    # function to calculate the associated Legendre function values.
    for tt in xrange(len(thetas)):
        legendre_m_n_thetas[:, :, tt], dlegendre_m_n_thetas[:, :, tt] = sps.lpmn(m_max, n_max, numpy.cos(thetas[tt]))
        dlegendre_m_n_thetas[:, :, tt] = dlegendre_m_n_thetas[:, :, tt]*-numpy.sin(thetas[tt])

    # Next, we wish to obtain the normalized associated Legendre functions
    # (and the derivatives) from the associated Legendre functions.
    # Therefore, we must calculate the normalization factors,
    # as given in [1],(A1.25). The math.factorial and fractions.Fraction
    # functions are used to prevent numerical overflow from occurring.
    # Also, it should be noted that [1] defines the associated Legendre
    # function differently than the scipy.special package. Therefore,
    # we must multiply the scipy.special values by (-1)**m in order
    # to have our normalized associated Legendre function values agree
    # with those given in the table in [1],pg.322
    normfactor = numpy.zeros((m_max+1, n_max+1, 1))
    for m in range(m_max+1):
        for n in range(n_max+1):
            if m > n:
                continue
            temp1 = math.factorial(n-m)
            temp2 = math.factorial(n+m)
            temp3 = fractions.Fraction(temp1, temp2)
            normfactor[m, n, 0] = (-1)**m*math.sqrt((2*n+1)/2.0*float(temp3))

    # Multiply the associate Legendre function values by the
    # normalization factors to obtain the normalized associated
    # Legendre function values. Also, take this opportunity to copy
    # the values such that legendre_m_n_thetas has dimensions N x (2*M+1) x len(thetas)
    legendre_m_n_thetas = legendre_m_n_thetas*normfactor
    legendre_m_n_thetas = legendre_m_n_thetas.transpose((1, 0, 2))  # now arranged as (N, M, THETA)

    # Multiply the associate Legendre function derivative values by the
    # normalization factors to obtain the derivative of the normalized
    # associated Legendre function values ( derivative taken with respect
    # to cos(theta) ). Also, take this opportunity to copy
    # the values such that dlegendre_m_n_thetas has dimensions N x (2*M+1) x len(thetas)
    dlegendre_m_n_thetas = dlegendre_m_n_thetas*normfactor
    dlegendre_m_n_thetas = dlegendre_m_n_thetas.transpose((1, 0, 2))  # now arranged as (N, M, THETA)

    return legendre_m_n_thetas, dlegendre_m_n_thetas


# ------------------------------------------------------------------------


def rotation_coefficients(n_max, m_max, mu_max, thetas):
    # Function used to calculate the rotation coefficients.
    # The rotation coefficients are defined in [1],Section A2.3

    # Make sure that the thetas variable is a numpy array
    if isinstance(thetas, float):
        thetas = numpy.array([thetas])
    else:
        thetas = numpy.array(thetas)

    # Make sure that MU <= M <= N
    if not(mu_max <= m_max <= n_max):
        raise Exception('MU must be less than or equal to M, '
                        'which in turn must be less than or '
                        'equal to N.')

    # Also make sure that MU >= 1
    if mu_max < 1:
        raise Exception('MU must be greater than or equal to 1.')

    # Make sure that all theta values are between 0 and pi
    if numpy.any(thetas < 0) or numpy.any(thetas > PI):
        raise Exception('theta values must be between 0 and pi, inclusive.')

    # For mu == -1, 0, or 1, calculate the rotation coefficients using [1],(A2.17),
    # (A2.18), and (A2.19). This is done to improve computation speed.
    ## print 'Calculating rotation coefficients for mu = -1, 0, and 1'

    # Calculate the normalized associated Legendre function values,
    # and the values of the derivative with respect to cos(theta)
    legendre_norm, dlegendre_norm = lpmn_norm(n_max, m_max, thetas)

    # Extend the legendre_norm array to negative values
    # of m (to ease future calculations), but set the arrays
    # such that legendre_norm of -m is equal to legendre_norm of m.
    # Also remove the n == 0 part of the array.
    lpmn_norm_extended = numpy.zeros((n_max, 2*m_max+1, len(thetas)))
    lpmn_norm_extended[:, 0:m_max, :] = numpy.fliplr(legendre_norm[1:, 1:, :])
    lpmn_norm_extended[:, m_max:, :] = legendre_norm[1:, :, :]

    # Extend the dlegendre_norm array to negative values
    # of m (to ease future calculations), but set the arrays
    # such that legendre_norm of -m is equal to legendre_norm of m.
    # Also remove the n == 0 part of the array.
    dlpmn_norm_extended = numpy.zeros((n_max, 2*m_max+1, len(thetas)))
    dlpmn_norm_extended[:, 0:m_max, :] = numpy.fliplr(dlegendre_norm[1:, 1:, :])
    dlpmn_norm_extended[:, m_max:, :] = dlegendre_norm[1:, :, :]

    # Initialize the matrix that will hold the rotation coefficients
    d = numpy.zeros((n_max, 3, 2*m_max+1, len(thetas)))

    # Create arrays that hold the n, m, and mu indices. Also promote
    # the thetas to a 4-dimensional array. This will come in handy
    # when later multiplying the matrices. No need to perform
    # a matrix replication because of the way that Numpy "broadcasts"
    # the arrays during multiplication.
    n_vec = numpy.linspace(1, n_max, n_max)
    n_array = numpy.reshape(n_vec, (n_max, 1, 1, 1))
    mu_vec = numpy.linspace(-1, 1, 3)
    mu_array = numpy.reshape(mu_vec, (1, 3, 1, 1))
    m_vec = numpy.linspace(-m_max, m_max, 2*m_max+1)
    m_array = numpy.reshape(m_vec, (1, 1, 2*m_max+1, 1))

    # Calculate the (-m/m)**m factor, using [1],(2.19) to handle
    # the case when m==0
    nonzeroinds = m_array != 0
    mm = numpy.ones(numpy.shape(m_array))
    mm[nonzeroinds] = (-m_array[nonzeroinds] /
                       abs(m_array[nonzeroinds]))**m_array[nonzeroinds]

    # Calculate leading terms that are used in [1],(A2.17),(A2.18),
    # and (A2.19)
    c1 = mm*numpy.sqrt(2.0/(2.0*n_array+1))
    c2 = -2.0/numpy.sqrt(n_array*(n_array+1.0))

    # Calculate the mu==0 rotation coefficients according to (A2.17)
    d_0 = c1[:, 0, :, :]*lpmn_norm_extended

    # Initialize the d_plus1 and d_minus1 arrays
    d_plus1 = numpy.zeros([n_max, 2*m_max+1, len(thetas)])
    d_minus1 = numpy.zeros([n_max, 2*m_max+1, len(thetas)])

    # Calculate the mu==-1 and mu==1 rotation coefficients by
    # solving for d_-1 and d_+1 using equations (A2.18) and (A2.19).
    # Only calculate for values of theta where 1e-6 <= theta <= pi-1e-6.
    inds = numpy.logical_and((thetas >= 1e-6), (thetas <= PI-1e-6))
    d_plus1__plus__d_minus1 = (c2[:, 0, :, :]*m_array[:, 0, :, :])*d_0[:, :, inds]/numpy.sin(thetas[inds])
    d_plus1__minus__d_minus1 = (c1[:, 0, :, :]*c2[:, 0, :, :])*dlpmn_norm_extended[:, :, inds]
    d_minus1[:, :, inds] = (d_plus1__plus__d_minus1 - d_plus1__minus__d_minus1)/2.0
    d_plus1[:, :, inds] = (d_plus1__plus__d_minus1 + d_plus1__minus__d_minus1)/2.0

    # Assign d_minus1, d_0, and d_plus1 back into the d array
    d[:, 0, :, :] = d_minus1
    d[:, 1, :, :] = d_0
    d[:, 2, :, :] = d_plus1

    # Calculate the special cases when theta < 1e-6 or theta > pi-1e-6
    inds = thetas < 1e-6
    d[:, :, :, inds] = mu_array == m_array
    inds = thetas > PI-1e-6
    d[:, :, :, inds] = (-1)**(n_array+m_array)*(mu_array == -m_array)

    # If MU > 1, calculate the mu != -1, 0, or 1 rotation coefficients using [1],(A2.11)
    if mu_max > 1:

        # Store d for mu == -1,0,1 to a temp variable
        d_temp = d

        # Output shaped like this: (n,mu,m,theta)
        d = numpy.zeros((n_max, 2*mu_max+1, 2*m_max+1, len(thetas)))

        # Define a helper function
        def get_mu_index(mu_): return mu_max + mu_

        # Place d_temp back inside of d
        d[:, get_mu_index(-1):get_mu_index(1)+1, :, :] = d_temp

        # Calculate the delta pyramid
        deltas = delta_pyramid(n_max)

        # Create the mp and m vectors
        mp_vec = numpy.linspace(-n_max, n_max, 2*n_max+1)
        m_vec = numpy.linspace(-m_max, m_max, 2*m_max+1)

        # Remove the extra m values from the delta pyramid, if necessary
        extra = (len(mp_vec)-len(m_vec))/2
        if extra > 0:
            deltas = deltas[:, :, extra:-extra]

        # promote mp_vec to 4 dimensions
        mp_array = numpy.reshape(mp_vec, (1, 2*n_max+1, 1, 1))

        # Assign len(thetas) to a variable before we promote it to 4 dimensions
        numthetas = len(thetas)

        # promote thetas to 4 dimensions
        thetas = numpy.reshape(thetas, (1, 1, 1, len(thetas)))

        # Delete n==0 in deltas
        deltas = numpy.delete(deltas, 0, 0)

        # promote the deltas to 4 dimensions
        deltas4d = numpy.reshape(deltas, (n_max, 2*n_max+1, 2*m_max+1, 1))

        # Calculate the exponent matrix
        expon = numpy.exp(-1j*mp_array*thetas)

        # promote the m_vec to 2 dimensions
        m_array = numpy.reshape(m_vec, (1, 2*m_max+1))

        # define a helper function
        def get_m_index(m_): return m_max + m_

        # Calculate the summation for mu != -1,0,1
        mu_vec = numpy.linspace(-mu_max, mu_max, 2*mu_max+1)
        mu_vec = mu_vec[numpy.logical_or(mu_vec < -1, mu_vec > 1)]
        for mu in mu_vec:
            ## print 'Calculating rotation coefficients for mu =', mu
            # Calculate the kernel
            temp = numpy.reshape(deltas4d[:, :, get_m_index(mu), :], (n_max, 2*n_max+1, 1, 1))
            kernel = temp*deltas4d
            for nt in xrange(numthetas):
                d[:, get_mu_index(mu), :, nt] = ((1j**(mu-m_array))*numpy.sum(kernel[:, :, :, 0] *
                                                                              expon[:, :, :, nt], 1)).real

        #######################################################

        # This was my attempt to implement [1],(A2.14). With the recurrence relation, we should
        # be able to calculate the rotation coefficients for higher order mu modes based on
        # lower order mu modes. In theory, this should be much faster than the method implemented
        # above. However, I was not able to make the recurrence relations work due to the zeros
        # in the denominators, which lead to nan's and inf's. This may be worth investigating
        # in the future.

##        # Store d for mu == -1,0,1 to a temp variable
##        d_temp = d
##
##        # Output shaped like this: (n,mu,m,theta)
##        d = numpy.zeros((N,2*MU+1,2*M+1,len(thetas)))
##
##        # Define a helper function
##        get_mu_index = lambda mu: MU+mu
##
##        # Place d_temp back inside of d
##        d[:,get_mu_index(-1):get_mu_index(1)+1,:,:] = d_temp
##
##        # Set d_temp to None to force garbage collection of memory
##        d_temp = None
##
##        # promote thetas to 3 dimensions
##        thetas = thetas.reshape((1,1,len(thetas)))
##
##        # Create n_vec and promote to 3 dimensions
##        n_vec = numpy.linspace(1,N,N)
##        n_array = n_vec.reshape((N,1,1))
##
##        # Create m_vec and promote to 3 dimensions
##        m_vec = numpy.linspace(-M,M,2*M+1)
##        m_array = m_vec.reshape((1,2*M+1,1))
##
##        # Calculate the rotation coefficients for mu != -1,0,1 using recurrence relation
##        mu_vec = numpy.linspace(-MU,MU,2*MU+1)
##        mu_vec = mu_vec[ numpy.logical_or(mu_vec<-1,mu_vec>1) ]
##        for mu in mu_vec:
##            print 'Calculating rotation coefficients for mu =',mu
##            if mu < -1:
##                d[:,get_mu_index(mu),:,:] = -1./(numpy.sqrt((n_array+mu)*(n_array-mu+1))*numpy.sin(thetas))*(
##                    (2*m_array-2*mu*numpy.cos(thetas))*d[:,get_mu_index(mu)+1,:,:] +
##                    numpy.sqrt((n_array+mu+1)*(n_array-mu))*numpy.sin(thetas)*d[:,get_mu_index(mu)+2,:,:])
##            if mu > 1:
##                d[:,get_mu_index(mu),:,:] = -1./(numpy.sqrt((n_array+mu+1)*(n_array-mu))*numpy.sin(thetas))*(
##                    (2*m_array-2*mu*numpy.cos(thetas))*d[:,get_mu_index(mu)-1,:,:] +
##                    numpy.sqrt((n_array+mu)*(n_array-mu+1))*numpy.sin(thetas)*d[:,get_mu_index(mu)-2,:,:])
##
    return d

# ------------------------------------------------------------------------


def translation_coefficients(n_max, nu_max, ka):

    # Initialize and calculate the B'(J) array
    b_prime = numpy.zeros(2*n_max+2*nu_max+1)
    b_prime[0] = 1.0
    for J in range(0, 2*n_max+2*nu_max, 2):
        b_prime[J+2] = (J + 1.0)/(J + 2.0)*b_prime[J]

    # Initialize the c_s_n_sig_nu_mu matrix
    c_s_n_sig_nu_mu = numpy.zeros((2, n_max, 2, nu_max, 2), dtype='complex')

    # Calculate the necessary values of the spherical Hankel function of the first kind
    hn = sph_hankel_first_kind(n_max+nu_max, ka)

    # Calculate the translation coefficients as detailed in [1],(x.xxx), AND A FUTURE BLOG POST

    for sig in [1]:

        sigi = sig - 1

        for mu in [-1, 1]:

            if mu == 1:
                mui = 1
            else:
                mui = 0

            for nu in range(1, nu_max+1):

                nui = nu - 1

                for s in [1, 2]:

                    si = s - 1

                    for n in range(1, n_max+1):

                        ni = n - 1

                        temp = 0.0 + 1j*0.0

                        front_terms = (1./4. *
                                       1j**n * (numpy.sqrt(2.0*n+1.0)/(n*(n+1.0))) *
                                       1j**(-nu) * (numpy.sqrt(2.0*nu+1.0)/(nu*(nu+1.0)))
                                       )

                        for p in range(abs(n-nu), n+nu+2, 2):

                            d1 = n*(n+1.0) + nu*(nu+1.0) - p*(p+1.0)

                            d2 = n + nu + p + 1.0

                            if s == sig:
                                term1 = d1**2/d2
                            else:
                                term1 = 0.0

                            if 3-s == sig:
                                term2 = 2.0*1j*ka*d1/d2
                            else:
                                term2 = 0.0

                            term3 = b_prime[-n+nu+p]*b_prime[n-nu+p]*b_prime[n+nu-p]/b_prime[n+nu+p]

                            term4 = 1j**(-p) * (2.0*p + 1.0)

                            temp += (term1 + term2) * term3 * term4 * hn[p]

                        if mu == 1:
                            coeff = 1.0
                        else:
                            coeff = (-1.0)**(s + sig)

                        c_s_n_sig_nu_mu[si,ni,sigi,nui,mui] = coeff * front_terms * temp

    c_s_n_sig_nu_mu[1,:,1,:,:] = c_s_n_sig_nu_mu[0,:,0,:,:]
    c_s_n_sig_nu_mu[0,:,1,:,:] = c_s_n_sig_nu_mu[1,:,0,:,:]

    return c_s_n_sig_nu_mu

# ------------------------------------------------------------------------


def sph_hankel_first_kind(n, x):

    jn, djn = sps.sph_jn(n, x)

    yn, dyn = sps.sph_yn(n, x)

    return jn + 1j*yn

# ------------------------------------------------------------------------


def fft(c, n=None, axis=-1):

    if n is None:
        n = numpy.size(c, axis)

    c_k = n*numpy.fft.ifft(c, n, axis)

    return c_k


# ------------------------------------------------------------------------


def ifft(c, n=None, axis=-1):

    if n is None:
        n = numpy.size(c, axis)

    c_m = (1.0/n)*numpy.fft.fft(c, n, axis)

    return c_m


# ------------------------------------------------------------------------


# def PI(l, mp):
#     if (l-mp) % 2 == 1:
#         return 0.0
#     elif (l-mp) % 2 == 0:
#         return 2.0/(1.0 - (l - mp)**2.0)
#     else:
#         raise Exception("error in pysnf.PI")


# ------------------------------------------------------------------------


def pi_wiggle(n_max):

    jj = numpy.linspace(-2*n_max+1, 2*n_max, 4*n_max)

    even_indices = jj % 2 == 0

    pi_wig = numpy.zeros(4*n_max)

    pi_wig[even_indices] = 2.0/(1.0 - jj[even_indices]**2)

    pi_wig = numpy.roll(pi_wig, -2*n_max+1)

    pi_wig = numpy.reshape(pi_wig,(4*n_max,1,1))

    return pi_wig

# ------------------------------------------------------------------------


def b_wiggle(b_l_m_mu):

    numrows, numcolumns, numpages = numpy.shape(b_l_m_mu)
    n_max = (numrows-1)/2
    m_max = (numcolumns-1)/2

    b_l_m_mu_wiggle = numpy.zeros((4*n_max, 2*m_max+1, 2), dtype='complex')

    def get_l_index(l_): return l_ + 2*n_max - 1

    b_l_m_mu_wiggle[get_l_index(-n_max):get_l_index(n_max)+1, :, :] = b_l_m_mu

    b_l_m_mu_wiggle = numpy.roll(b_l_m_mu_wiggle, shift=-2*n_max+1, axis=0)

    return b_l_m_mu_wiggle

# ------------------------------------------------------------------------


def db(a):
    return 20*numpy.log10(numpy.absolute(a))

# ------------------------------------------------------------------------


def plot_spherical_wave_coefficients_mag_db(q_in):

        q = q_in.copy()

        qmax = numpy.max((numpy.absolute(q[:,:,0])**2 +
                          numpy.absolute(q[:,:,1])**2).ravel())
        q = q/qmax

        fig1, (ax1, ax2) = plt.subplots(nrows=2)

        m_max = (numpy.size(q, 1)-1)/2
        n_max = numpy.size(q, 0)

        ax1.imshow(db(q[:, :, 0]).T,
                   extent=[1, n_max, -m_max, m_max], aspect='auto', interpolation='none', vmin=-120, vmax=0)
        ax2.imshow(db(q[:, :, 1]).T,
                   extent=[1, n_max, -m_max, m_max], aspect='auto', interpolation='none', vmin=-120, vmax=0)

        fig2, ax3 = plt.subplots(nrows=1)
        ax3.imshow((10*numpy.log10(numpy.absolute(q[:,:,0])**2 + numpy.absolute(q[:,:,1])**2)).T,
                   extent=[1, n_max, -m_max, m_max], aspect='auto', interpolation='none', vmin=-120, vmax=0)

        plt.show()

# ------------------------------------------------------------------------


def dipole_probe_response_constants(n_max, ka=INF, direction='+x', dipole_type='electric'):

    # Initialize the array to hold the dipole probe response constants
    p_n_mu_s = numpy.zeros((n_max, 2, 2), dtype='complex')

    # Create the n_array and s_array arrays
    n_array = numpy.linspace(1, n_max, n_max)

    if ka == INF:

        if (direction == '+x') and (dipole_type == 'electric'):

            temp = -numpy.sqrt(6.0)/8.0*numpy.sqrt(2.0*n_array+1.0)*1j**(-n_array)
            p_n_mu_s[:, 1, 0] = temp
            p_n_mu_s[:, 1, 1] = temp
            p_n_mu_s[:, 0, 0] = temp
            p_n_mu_s[:, 0, 1] = -temp

        if (direction == '+x') and (dipole_type == 'magnetic'):

            raise Exception("Code not yet implemented for kA==INF, +x magnetic dipole.")

        if (direction == '+y') and (dipole_type == 'electric'):

            raise Exception("Code not yet implemented for kA==INF, +y electric dipole.")

        if (direction == '+y') and (dipole_type == 'magnetic'):

            raise Exception("Code not yet implemented for kA==INF, +y magnetic dipole.")

    if ka < INF:

        if (direction == '+x') and (dipole_type == 'electric'):

            raise Exception("Code not yet implemented for kA<INF, +x electric dipole.")

        if (direction == '+x') and (dipole_type == 'magnetic'):

            raise Exception("Code not yet implemented for kA<INF, +x magnetic dipole.")

        if (direction == '+y') and (dipole_type == 'electric'):

            raise Exception("Code not yet implemented for kA<INF, +y electric dipole.")

        if (direction == '+y') and (dipole_type == 'magnetic'):

            raise Exception("Code not yet implemented for kA<INF, +y magnetic dipole.")

    return p_n_mu_s


# ------------------------------------------------------------------------


def reciprocity(trans_coeffs):

    # [1],(2.104)

    # T is nu, mu, sig

    n_max, m_max, s_max = numpy.shape(trans_coeffs)

    if m_max > 2:
        m_max = (m_max-1)/2

        receive_coeffs = numpy.zeros((n_max, 2*m_max+1, 2), dtype='complex')

        for m in range(-m_max, m_max+1):

            mi = m + m_max
            neg_mi = m_max - m

            receive_coeffs[:, mi, :] = (-1)**m * trans_coeffs[:, neg_mi, :]

    else:

        receive_coeffs = numpy.zeros((n_max, 2, 2), dtype='complex')

        receive_coeffs[:, 1, :] = -1*trans_coeffs[:, 0, :]
        receive_coeffs[:, 0, :] = -1*trans_coeffs[:, 1, :]

    return receive_coeffs

# ------------------------------------------------------------------------


def rotate_wavecoeffs_about_axis(q, ax):

    # [1],(5.67)

    # Q is n, m, s

    n_max, m_max, s_max = numpy.shape(q)

    n_vec = numpy.linspace(1.0, n_max, n_max)
    n_vec = numpy.reshape(n_vec, (n_max, 1))

    if ax == 'x':

        if m_max > 2:

            m_max = (m_max-1)/2

            q_rot = numpy.zeros((n_max, 2*m_max+1, 2), dtype='complex')

            for m in range(-m_max, m_max+1):

                mi = m + m_max
                neg_mi = m_max - m

                q_rot[:, mi, :] = (-1)**n_vec * q[:, neg_mi, :]

        else:

            q_rot = numpy.zeros((n_max, 2, 2), dtype='complex')

            q_rot[:, 1, :] = (-1)**n_vec * q[:, 0, :]
            q_rot[:, 0, :] = (-1)**n_vec * q[:, 1, :]

    else:

        raise Exception("Code not yet implemented for rotations about y or z axes.")

    return q_rot

# ------------------------------------------------------------------------


def probe_response_constants(r_p, n_max, ka, c=None):

    # Assumes that R_p is entered as sig, mu, nu

    if ka > 1e4:
        raise Exception("kA > 1e4 not yet implemented")

    sig_max, mu_max, nu_max = numpy.shape(r_p)

    if sig_max != 2:
        raise Exception("First dimension (sigma) of receiving coefficients must have a size of exactly 2.")

    if mu_max < 2:
        raise Exception("Second dimension (mu) of receiving coefficients must have a size of at least 2.")
    elif mu_max > 2:
        temp = r_p.copy()
        r_p = numpy.zeros((2,2,nu_max),dtype='complex')
        r_p[:,0,:] = temp[:,(mu_max-1)/2-1,:]
        r_p[:,1,:] = temp[:,(mu_max-1)/2+1,:]

    if c is None:
        c = translation_coefficients(n_max, nu_max, ka)  # s, n, sig, nu, mu

    r_p = numpy.swapaxes(r_p, 1, 2)  # R_p is now sig, nu, mu

    r_p = numpy.reshape(r_p, (1, 1, 2, nu_max, 2))  # R_p is now s, n, sig, nu, mu

    temp = numpy.sum(c*r_p, axis=3)  # Sum over nu. temp is s, n, sig, mu

    p = 0.5*numpy.sum(temp, axis=2)  # Sum over sigma. P is s, n, mu

    p = numpy.swapaxes(p, 1, 2)  # P is now s, mu, n

    p = numpy.swapaxes(p, 0, 2)  # P is now n, mu, s

    return p

# ------------------------------------------------------------------------


def singlesphere2doublesphere(singlesphere):

    numthetas = numpy.size(singlesphere, axis=0)
    numphis = numpy.size(singlesphere, axis=1)

    if numphis % 2 == 1:
        ss = interpft(singlesphere, numphis-1)
        numphis -= 1
    else:
        ss = singlesphere.copy()

    doublesphere = numpy.zeros((2*(numthetas-1), numphis), dtype='complex')

    doublesphere[:numthetas, :] = ss[:, :]
    doublesphere[numthetas:, :] = -numpy.roll(ss[-2:0:-1, :], numphis/2, axis=1)

    return doublesphere


# ------------------------------------------------------------------------


def interpft(a, ny):

    # Operates on the last axis of a 2D array
    axis = -1

    # Get initial length and width of the 2D array
    n, m = numpy.shape(a)

    # Ensure that ny is an integer
    ny = numpy.floor(ny)

    # If necessary, increase ny by an integer multiple to make ny > size(a,axis)
    if ny <= 0:
        raise Exception("n must be an integer greater than 0.")
    elif numpy.size(a, axis) > m:
        incr = 1
    else:
        incr = numpy.floor(m/ny) + 1
        ny *= incr

    b = fft(a, axis=axis)

    nyqst = numpy.ceil((m + 1.0)/2.0)

    c = numpy.zeros((n, ny), dtype='complex')
    c[:, 0:nyqst] = b[:, 0:nyqst]
    c[:, nyqst+(ny-m):] = b[:, nyqst:]

    if numpy.remainder(m, 2) == 0:
        c[:, nyqst-1] = c[:, nyqst-1]/2.0
        c[:, nyqst+ny-m-1] = c[:, nyqst-1]

    d = ifft(c, axis=axis)

    d *= float(ny)/float(m)

    d = d[:, 0::incr]  # Skip over extra points when original ny <= m

    return d
