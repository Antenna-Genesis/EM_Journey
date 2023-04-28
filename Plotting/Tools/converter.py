# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 15:35:16 2019

@author: Kai
"""
import numpy as np


def pw_linear2db(data_linear):
    data = 10 * np.log10(data_linear)
    return data

def pw_db2linear(data_db):
    data_db[data_db > 0] = -10e-10
    data = 10 ** (data_db / 10)
    return data

def s11db2efflinear(s11_db):
    s11_db[s11_db > 0] = -10e-10
    pw_s11 = 10 ** (s11_db / 10)  # power
    eff = 1 - pw_s11
    return eff

def s11db2vswr(s11_db):
    s11_db[s11_db > 0] = -10e-10
    s11_linear = 10 ** (s11_db / 20)  # voltage
    vswr = (1 + s11_linear) / (1 - s11_linear)
    return vswr
