from HFSS import HFSS
import math

f0="3.5GHZ"
lamda0=3*10**8/(3.5*10**9)*1000
w0=3.08;distance1=42;l_monopole=21;d_50ohm=w0;l_sub=2*l_monopole;w_sub=60;h_sub=1;
d_monopole=w0;
h1=HFSS()
h1.launch()
h1.setVariable('distance1',distance1,'mm')
h1.setVariable('l_monopole',l_monopole,'mm')
h1.setVariable('d_monopole',d_monopole,'mm')
h1.setVariable('d_50ohm',d_50ohm,'mm')
h1.setVariable('l_sub',l_sub,'mm')
h1.setVariable('w_sub',w_sub,'mm')
h1.setVariable('h_sub',h_sub,'mm')

#天线建模
h1.createBox('-l_sub/2','-w_sub/2','0','l_sub','w_sub','h_sub','substrate',"Rogers RT/duroid 5880 (tm)",'T')
h1.createRectangle('l_sub/2','-w_sub/2','0','-l_sub+l_monopole','w_sub','Z','GND')
h1.createRectangle('-l_sub/2','-distance1/2-d_monopole/2','h_sub','l_sub','d_monopole','z','Monopole1')
h1.createRectangle('-l_sub/2','distance1/2+d_monopole/2','h_sub','l_sub','-d_monopole','z','Monopole2')
h1.assignPerfectE('Monopole1','pec1')
h1.assignPerfectE('Monopole2','pec2')
h1.assignPerfectE('GND','pecg')
#端口设置
h1.createRectangle('l_sub/2','-distance1/2-d_50ohm/2','0','d_50ohm','h_sub','x','port1')
h1.createRectangle('l_sub/2','distance1/2+d_50ohm/2','0','-d_50ohm','h_sub','x','port2')
h1.assignlumpport('port1','p1',str(l_sub/2)+'mm',str(-distance1/2)+'mm','0',str(l_sub/2)+'mm',str(-distance1/2)+'mm',str(h_sub)+'mm')
h1.assignlumpport('port2','p2',str(l_sub/2)+'mm',str(distance1/2)+'mm','0',str(l_sub/2)+'mm',str(distance1/2)+'mm',str(h_sub)+'mm')


h1.createRegion(str(1/4*lamda0)+'mm')
h1.assignRadiationRegion()
h1.fitAll()
h1.insertSetup("setup1","3.5GHz")
h1.insertFrequencysweep("setup1","3.0GHz","4.0GHz",50,"Interpolating")

h1.saveProject('D:\decouple_result','Dielectric_loading_test01_')
# h1.solve('setup1')