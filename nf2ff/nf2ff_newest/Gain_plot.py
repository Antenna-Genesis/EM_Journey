import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import spline
import numpy as np


Gain_C=np.array([19.751534374956435,19.72760782635639,19.809479291334526,19.868491043947074,
        19.815699360135596, 19.781438011104953,20.028336193327007,20.189472750585225])
Gain_C=np.array([19.87259089564128,19.87078919948408,19.871892627422568,19.84820882359176 ,19.86866079696361,19.82834894893162,19.806558311499842])
Gain_S=np.array([19.8049,19.7735,19.8286,19.8165,
        19.7861, 19.7524,19.8799,19.9382])
Gain_S=np.array([19.8428, 19.8428,19.8428,19.8428,19.8428,19.8428,19.8428])
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
x_ = [12.5, 25, 62.5, 125, 250, 375, 500, 625]
x_ = [5, 15, 30, 45, 60, 75,90]
'''xnew = np.linspace(x_.min(), x_.max(), 300)
GC_smooth = spline(x_, Gain_C, xnew)
GS_smooth = spline(x_, Gain_S, xnew)
ax.plot(x_, Gain_C, 'ko')
ax.plot(x_, Gain_S, 'ko')'''
ax.plot(x_, Gain_C, 'ko--', label='Calculation')
ax.plot(x_, Gain_S, 'ko-', label='Simulation')
ax.legend(fontsize='xx-large', loc='best')
# x_ticks=['0.1λ','0.2λ','0.5λ','1λ','2λ','3λ','4λ','5λ']
ax.set_xticks(x_)
#ax.set_xticklabels(x_ticks, fontsize=16, rotation = 45)

ax.set_ylim(19.7,20)
plt.tick_params(labelsize=16)
#y_ = np.around(np.arange(19,21.5,1),2)
#ax.set_yticklabels(y_, fontsize=16)
ax.set_xlabel('Distance', fontsize=16)
ax.set_xlabel("Sampling interval(mm)", fontsize=16)
ax.set_ylabel('Gain(dBi)', fontsize=16)
# ax.grid()
plt.show()