import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import spline
import numpy as np
import csv


Gain_C=np.loadtxt('Gaintest1.csv')
Gain_C=np.array(Gain_C).reshape((181,181))
Gain_C=Gain_C[:,91]
Gain_C1=np.loadtxt('Gaintest2.csv')
Gain_C1=np.array(Gain_C1).reshape((181,181))
Gain_C1=Gain_C1[:,91]
Gain_C2=np.loadtxt('Gaintest3.csv')
Gain_C2=np.array(Gain_C2).reshape((181,181))
Gain_C2=Gain_C2[:,91]
Gain_C3=np.loadtxt('Gaintest4.csv')
Gain_C3=np.array(Gain_C3).reshape((181,181))
Gain_C3=Gain_C3[:,91]

Gain_S=np.array([19.8049,19.7735,19.8286,19.8165,
        19.7861, 19.7524,19.8799,19.9382])
Gain_S=np.array([19.8428, 19.8428,19.8428,19.8428,19.8428,19.8428,19.8428])
with open('dataset/Gain T181.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    column = [float(row['dB(GainTotal)']) for row in reader]
Gain_S = np.array(column)
Gain_S=Gain_S.reshape((181,181))
Gain_S=Gain_S[:,91]
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
x_ = [12.5, 25, 62.5, 125, 250, 375, 500, 625]
x_ = [5, 15, 30, 45, 60, 75,90]
x_=np.linspace(0,90,181)
'''xnew = np.linspace(x_.min(), x_.max(), 300)
GC_smooth = spline(x_, Gain_C, xnew)
GS_smooth = spline(x_, Gain_S, xnew)
ax.plot(x_, Gain_C, 'ko')
ax.plot(x_, Gain_S, 'ko')'''
ax.plot(x_, Gain_C, 'k--', label='Calculation(d=25mm)')
ax.plot(x_, Gain_C1, 'k-.', label='Calculation(d=62.5mm)')
ax.plot(x_, Gain_C2, 'k-', label='Calculation(d=125mm)')
ax.plot(x_, Gain_C3, 'k:', label='Calculation(d=375mm)')
ax.plot(x_, Gain_S, 'k-^', label='Simulation')
ax.legend(fontsize='xx-large', loc='best')
x_ticks=['0.1λ','0.2λ','0.5λ','1λ','2λ','3λ','4λ','5λ']
#x_ticks=['0°','15°','30°','45°','60°','75°','90°']
#ax.set_xticks(x_)
#ax.set_xticklabels(x_ticks, fontsize=16, rotation = 45)

#ax.set_ylim(19.7,20)
plt.tick_params(labelsize=16)
#y_ = np.around(np.arange(19,21.5,1),2)
#ax.set_yticklabels(y_, fontsize=16)
#ax.set_xlabel('Distance', fontsize=16)
ax.set_xlabel("θ(°)", fontsize=16)
ax.set_ylabel('Gain(dBi)', fontsize=16)
# ax.grid()
plt.show()