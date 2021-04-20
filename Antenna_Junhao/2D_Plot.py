# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
import os

_path = os.getcwd()
os.chdir(_path)
sp = pd.read_csv('S Parameter Plot 1.csv')
freq = sp.iloc[:, 0]
dB = sp.iloc[:, 1]
plt.subplot(311)
plt.plot(freq, dB, color='red', lw=5)
plt.xlabel('Freq[GHz]')
plt.ylabel('dB(S(1,1))')

gain = pd.read_csv('Gain Plot 2.csv')
theta = gain.iloc[:, 0]
theta_f = theta.astype(np.float64)
for index in range(len(theta_f)):
    theta_f[index] = math.radians(theta_f[index])
E = gain.iloc[:, 1]

ax = plt.subplot(223, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
ax.set_thetagrids(np.arange(0, 360, 30))
plt.plot(theta_f, E, color='black', lw=2)
plt.title('Phi = 90deg', fontsize=10)

_gain = pd.read_csv('Gain Plot 3.csv')
phi = _gain.iloc[:, 0]
phi_f = phi.astype(np.float64)
for index in range(len(phi_f)):
    phi_f[index] = math.radians(phi_f[index])
r = _gain.iloc[:, 1]

ax = plt.subplot(224, projection='polar')
ax.set_theta_direction(-1)
ax.set_theta_zero_location('N')
ax.set_thetagrids(np.arange(0, 360, 30))
plt.plot(phi_f, r, color='green', lw=2)
plt.title('Theta = 90deg', fontsize=10)
plt.show()
