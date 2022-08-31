# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
from mayavi import mlab
import os

_path = os.getcwd()
os.chdir(_path)
gain = pd.read_csv('Gain Plot 1.csv')

Theta = gain.iloc[:, 1]
theta = Theta.astype(np.float64)
for index in range(len(theta)):
    theta[index] = math.radians(theta[index])
theta = theta.drop_duplicates(keep='first')

i = int(len(gain)/len(theta))
Phi = gain.iloc[:i, 0]
phi = Phi.astype(np.float64)
for index in range(len(phi)):
    phi[index] = math.radians(phi[index])

dB_min = np.min(gain.iloc[:, 2])
scale = abs(dB_min) + 1
dB = gain.iloc[:, 2] + scale
print(type(dB))
dB = np.array(dB.values).reshape(int(len(theta)), int(len(phi)))

phi, theta = np.meshgrid(phi, theta)
r = dB * np.sin(theta)
x = r * np.cos(phi)
y = r * np.sin(phi)
z = dB * np.cos(theta)
mlab.mesh(x, y, z, colormap="Spectral")
mlab.show()
