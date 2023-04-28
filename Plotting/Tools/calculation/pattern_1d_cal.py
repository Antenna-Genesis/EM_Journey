# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:48:57 2018

@author: kai.lu
"""

def find_max_sidelobe(angle_list_deg, radiation_1d_db):
    import numpy as np
    import sys
    if len(angle_list_deg) != len(radiation_1d_db):
        sys.exit('Input vectors v and x must have same length')
    radiation_1d_db = np.asarray(radiation_1d_db)
    angle_list_deg = np.asarray(angle_list_deg)
    (peaks_info, vallies_info) = peakdet(radiation_1d_db, 3)
    # 3 means 3dB threshold, variation less than 3dB is ignored
    peaks = peaks_info[:,1]
    
    gain_db_max = max(radiation_1d_db)
    max_sidelobe_level = peaks[np.argsort(peaks)[-2:]][0]
    print(peaks[np.argsort(peaks)[-2:]])
    # second largest value
    max_sidelobe_level = max_sidelobe_level - gain_db_max
    max_sidelobe_pos = np.argsort(peaks)[-2:][0]
    print('The max SLL is {} at {}'.format(max_sidelobe_level, angle_list_deg[max_sidelobe_pos]))
    

def peakdet(v, delta, x = None):
    '''
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays
    
    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %      
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.
    
    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    '''
    import sys
    from numpy import NaN, Inf, arange, isscalar, asarray, array

    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab) 

def find_beamwidth(angle_list_deg, radiation_1d_db, backoff_db):
    import numpy as np
    # angle_list_deg, radiation_1d_db should be array type vector
    # backoff_db is the threshold of the beamwidth boundary
    sampling_points = len(angle_list_deg)
#    print('Overall sample points on the cutting plane is {}'.format(sampling_points))
    ang_delta = angle_list_deg[1] - angle_list_deg[0]

    if abs(radiation_1d_db[0] - radiation_1d_db[-1]) < 1e-5 and \
            abs((sampling_points - 1) * ang_delta - 360) < 1e-5:
        # to check whether the beginning and end overlap
        radiation_1d_db = radiation_1d_db[0:-1] 
        angle_list_deg = angle_list_deg[0:-1]
        sampling_points -= 1
        # delete the last element

    gain_db_max = max(radiation_1d_db)
    gain_max_position = np.argmax(radiation_1d_db)
    gain_max_angle = int(angle_list_deg[gain_max_position])
    # find the max value for the cutting plane
    print('Max gain is at the angle of ' + str(gain_max_angle))
    #    get the index of max gain value
    radiation_1d_db_norm = radiation_1d_db - gain_db_max
    #  qualified_points = 0
    bit_ring = []
    for direction_indx in range(0, len(angle_list_deg)):
        # change the analog count into logical count
        if radiation_1d_db_norm[direction_indx] >= -backoff_db:
            bit_ring.append(1)
#            qualified_points += 1
        else:
            bit_ring.append(0)
    qualified_points = sum(bit_ring)

    ones_list, longest_indx = countringbit(bit_ring)
    longest_start_indx = ones_list[longest_indx][0]
    longest_end_indx = ones_list[longest_indx][1]
    total_qualified_points = ones_list[longest_indx][2]
#    print(type(ang_delta))
    if total_qualified_points == sampling_points:
        #  omnidirectional pattern is special
        bw = int(total_qualified_points * ang_delta)
        print('Omnidirectional pattern with a beamwidth of {} degree'.format(bw))
        # overall_bw = qualified_points * ang_delta
        # print('Cumulative beamwidth is {}'.format(overall_bw))
    else:
        beam_start = int(ones_list[longest_indx][0] * ang_delta)
        beam_end = int(ones_list[longest_indx][1] * ang_delta)
        bw = int((total_qualified_points - 1) * ang_delta)
        print('Main beamwidth is {} degree'.format(bw))
        print('The main beam begins at {} degree and stop at {} degree'.format(beam_start, beam_end))
        overall_bw = int((qualified_points - 1) * ang_delta)
        print('Cumulative beamwidth is {} degree'.format(overall_bw))
#    print(type(bw))  
#    bw = np.asscalar(bw) #  convert the datatype to scalar
#    print(bw)
    return bw, longest_start_indx, longest_end_indx

####################


# first choice as it is concise  
def countringbit(binary_data):
    #  find the length of longest consecutive 1s
    #  the binary array must have no overlapping on two ends
    onelen = 0
    first = 0
    last = 0
    info_list = []
    datalen = len(binary_data)
    allonelen = sum(binary_data)
    if allonelen == datalen:
        # skip the calculation if all_height 1 is found
        last = datalen - 1
        info_list = [[first, last, datalen]]
        # must be nested list
        print('All directions are qualified')
    else:
        if allonelen == 0:
            info_list = [[first, last, 0]]
            print('Non direction is qualified')
        else:
            for indx in range(datalen):
                if binary_data[indx]:
                    onelen += 1
                    last = indx
                    if indx == datalen - 1:
                        first = last - onelen + 1
                        info_list.append([first, last, onelen])
                        print('The last element in the data list is qualified')
                    else:
                        pass
                else:
                    if onelen == 0:
                        #  print('Element with and index {} is unqualified'.format(indx))
                        pass
                    else:
                        first = last - onelen + 1
                        info_list.append([first, last, onelen])
                        # add latest group to the info_list    
                    onelen = 0
    ones_grp_num = len(info_list)
    # find how many groups in the list
    if ones_grp_num == 1:
        print('Only one beam exists')
    else:
        if info_list[0][0] == info_list[-1][1] - datalen + 1:
            # in case the consecutive one cross the start and end
            info_list[0][0] = info_list[-1][0]
            info_list[0][2] = info_list[0][2] + info_list[-1][2]
            # mergy two groups into one
            info_list.pop()
            ones_grp_num -= 1
            # delete redundance 
#    print('There are {} groups of consecutive ones (including one element)'.format(ones_grp_num))

    len_col = 2
    # column of the ones length
    onescolist = []
    # create a list to store the last column
    for i in range(ones_grp_num):
        onescolist += [info_list[i][len_col]]
    longest_ones = max(onescolist)
    # find the number of the longest consecutive ones
    longest_indx = onescolist.index(longest_ones)
    # locate the max in the list
    return info_list, longest_indx 
####################
    # second choice if the first doesn't work well
####################

def ringbitcount(binary_data):
    #  find the length of longest consecutive 1s
    #  the binary array must have no overlapping on two ends
    #  the elements must be 0 or 1
    # first_location = 0
    # last_location = 0
    ones_list = []
    # initialize location variables and statistic list
    # one_list is a nested list, with element format [first_location, last_location, ones_len]
    data_len = len(binary_data)
    # find the binary_data length
    data_indx = 0
    while data_indx in range(data_len):
        # make sure the index is in the data range
        if binary_data[data_indx]:  # check the value is 1 or not
            first_location = data_indx
            last_location = data_indx
            # initialization
            if last_location == data_len - 1:
                # check whether it is the end of the list
                # if only the last value is 1
                #  data_indx = last_location
                ones_len = last_location - first_location + 1
                ones_list.append([first_location, last_location, ones_len])
                # append the current group info to the whole info list
                break

            else:
                
                while last_location <= data_len - 2:
                    last_location = last_location + 1
                    # only excute before the end
                    if last_location != data_len - 1:
                        if binary_data[last_location]:
                            pass
                        else:  # first 0 ppears after 1, an group ends
                            data_indx = last_location
                            last_location = last_location - 1
                            ones_len = last_location - first_location + 1
                            ones_list.append([first_location, last_location, ones_len])
                            break 
                    else:  # when the bitring ends with 1
                        if binary_data[last_location]:
                            data_indx = last_location + 1  # make the main lopp ends
                            last_location = last_location
                            
                            ones_len = last_location - first_location + 1
                            ones_list.append([first_location, last_location, ones_len])
                            print('The bit ring ends with one')
                            break
                        else:  # the bitring end with a 0
                            data_indx = last_location
                            last_location = last_location - 1
                            ones_len = last_location - first_location + 1
                            ones_list.append([first_location, last_location, ones_len])
                            break           
                
        else:
            data_indx += 1  # go for the next
#            print('zero apears at position of {}'.format(data_indx-1))
#        print('Zero appears at the location of {}'.format(data_indx))
#    print('The satitistic information of consecutive ones is {}'.format(ones_list))    
    ones_grp_num = len(ones_list)
    # find how many groups in the list
    if ones_grp_num == 1:
        print('Only one beam exists')
    else:
        if ones_list[0][0] == ones_list[-1][1] - data_len + 1:
            # in case the consecutive one cross the start and end
            ones_list[0][0] = ones_list[-1][0]
            ones_list[0][2] = ones_list[0][2] + ones_list[-1][2]
            # mergy two groups into one
            ones_list.pop()
            ones_grp_num -= 1
            # delete redundance 
#    print('There are {} groups of consecutive ones (including one element)'.format(ones_grp_num))

    len_col = 2
    # column of the ones length
    onescolist = []
    # create a list to store the last column
    for i in range(ones_grp_num):
        onescolist += [ones_list[i][len_col]]
    longest_ones = max(onescolist)
    # find the number of the longest consecutive ones
    longest_indx = onescolist.index(longest_ones)
    # locate the max in the list
    return ones_list, longest_indx 
####################


if __name__ == '__main__':
    import scipy as sp
    angle_list_deg = np.linspace(0, 360, 19)
    radiation_1D_dB = 6 * np.cos(1 * angle_list_deg * sp.pi / 180)
    backoff_db = 3
    beamwidth3db = find_beamwidth(angle_list_deg, radiation_1D_dB, backoff_db)