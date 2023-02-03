from HFSS import HFSS
import os
import numpy as np
h1=HFSS()
h1.init()
# face1=h1.getFacebyposition('substrate', '0 mm', '0 mm', '1 mm')
# h1.insertSetup('setup1','3.5GHz')
# h1.insertFrequencysweep('setup1', '3 GHz', '4 GHz', 50, 'Interpolating')
len='l_die'
wide='w_die'
hei='posz'
rad='rad1'

def test01(val,range0):
    item=1
    for i in range0:
        h1.changeVariablevalue(val, str(i), 'mm')
        h1.solve('setup1')
        h1.createSpreport11('plot111')
        h1.createSpreport12('plot112')
        h1.combine('plot112','plot111')
        h1.turnblue('plot111',"dB(S(1,2))")
        hfss_file_dir = "F:\ydl\plot\\"+val
        if not os.path.exists(hfss_file_dir):
            os.makedirs(hfss_file_dir)
        h1.exportimage('plot111',"F:\ydl\plot\\"+val,val+'='+str(i)+'mm')
        h1.deleteAllreports()
        print('num'+str(item)+':'+val+'='+str(i)+'mm'+' finished')
        item+=1
    print('optimizition finished!')
# test01('distance1',range(10,20,2))
# test01('w_sub',range(30,55,5))
test01('l_monopole',np.arange(13,17.5,0.5))
