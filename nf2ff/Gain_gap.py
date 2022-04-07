import csv
import matplotlib.pyplot as plt
import numpy
import numpy as np
import heat_plot
from numpy import unravel_index
with open('Gain Plot 2.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    column = [float(row['dB(GainTotal)']) for row in reader]
M = 16
# print(column)
# column = float(column)
Gain = np.array(column)
# Gain = np.float(Gain)
Gain = np.array(Gain).reshape(M, M)
Gain1 = loadcsv.load('Gain.csv')
print('phi=180deg时的增益', Gain1[:,7])
Gain_p = abs(Gain1 - Gain)
dataset = Gain_p[:4, :]
#print(dataset)
print('theta<30deg时增益的最大差距：', np.max(dataset))
print('增益最大差距点所在的位置：', unravel_index(dataset.argmax(), dataset.shape))
theta = np.linspace(0, np.pi/2, M)
phi = np.linspace(0, 2 * np.pi, M)
# Gain=np.abs(Gain)
heat_plot.heat_plot(Gain, Gain_p, theta, phi,'HFSS_Gain/dB', 'Gain_gap/dB', 'phi', 'theta')
plt.show()