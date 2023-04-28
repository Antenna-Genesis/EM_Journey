from HFSS import HFSS
import math

f0="2.4GHZ"

lamda0=3*10**8/(2.4*10**9)*1000

w0=3.0836;distance1=68;l_monopole=22;d_network=1;d_50ohm=w0;
l_sub=150;h_sub=1;lk1=64;lk2=16;lk3=25;dt=10;di=20;
h1=HFSS()
h1.launch()
h1.setVariable('d_monopole',w0,'mm')
h1.setVariable('distance1',distance1,'mm')
h1.setVariable('l_monopole',l_monopole,'mm')
h1.setVariable('d_network',d_network,'mm')
h1.setVariable('d_50ohm',d_50ohm,'mm')
h1.setVariable('l_sub',l_sub,'mm')
h1.setVariable('w_sub','distance1+d_monopole+2*d_monopole','')
h1.setVariable('h_sub',h_sub,'mm')
h1.setVariable('lk1',lk1,'mm')
h1.setVariable('lk2',lk2,'mm')
h1.setVariable('lk3',lk3,'mm')
h1.setVariable('dt',dt,'mm')
h1.setVariable('di',di,'mm')
h1.createBox('-l_sub/2','-w_sub/2','0','l_sub','w_sub','h_sub','substrate',"Rogers RT/duroid 5880 (tm)",'T')
h1.createRectangle('l_sub/2','-w_sub/2','0','-l_sub+l_monopole','w_sub','Z','GND')
h1.createRectangle('-l_sub/2','-distance1/2-d_monopole/2','h_sub','l_monopole+dt','d_monopole','z','Monopole1')
h1.createRectangle('-l_sub/2','distance1/2+d_monopole/2','h_sub','l_monopole+dt','-d_monopole','z','Monopole2')
h1.createRectangle('-l_sub/2+l_monopole+dt','-distance1/2-d_50ohm/2','h_sub','lk1','d_50ohm','z','ms1')
h1.createRectangle('-l_sub/2+l_monopole+dt','distance1/2-d_50ohm/2','h_sub','lk1','d_50ohm','z','ms2')
h1.createRectangle('-l_sub/2+l_monopole+dt+lk1','-distance1/2+d_50ohm/2','h_sub','-d_50ohm','lk2','z','ms1_2')
h1.createRectangle('-l_sub/2+l_monopole+dt+lk1','distance1/2-d_50ohm/2','h_sub','-d_50ohm','-lk2','z','ms2_2')
h1.createRectangle('-l_sub/2+l_monopole+dt+lk1','-distance1/2+d_50ohm/2+lk2','h_sub','l_sub-l_monopole-lk1-dt','-d_50ohm','z','ms1_3')
h1.createRectangle('-l_sub/2+l_monopole+dt+lk1','distance1/2-d_50ohm/2-lk2','h_sub','l_sub-l_monopole-lk1-dt','d_50ohm','z','ms2_3')


#三维去耦网络建模
n0=7

h1.setVariable('posx','-l_sub/2+l_monopole+dt+lk1+lk3',' ')
h1.setVariable('posy','-distance1/2+d_50ohm/2+lk2',' ')
h1.setVariable('dll','distance1-d_50ohm-2*lk2',' ')
h1.setVariable('dd',-3,'mm')

for i in range(n0):
    if i % 2 == 0:
        h1.createRectangle('posx','posy+'+str(i)+'*dll/'+str(n0),'h_sub','-d_network','dll/'+str(n0),'Z','net'+str(i))
    else:
        h1.createRectangle('posx+dd','posy+'+str(i)+'*dll/'+str(n0),'h_sub','-d_network','dll/'+str(n0),'Z','net'+str(i))
    if i != 0:
        h1.unitef('net0','net'+str(i))
for i in range(1,n0):
    if i % 2 != 0:
        h1.createRectangle('posx-d_network','posy+'+str(i)+'*dll/'+str(n0),'h_sub','dd','-d_network','Z','con'+str(i))
    else:
        h1.createRectangle('posx+dd','posy+'+str(i)+'*dll/'+str(n0),'h_sub','-dd','-d_network','Z','con'+str(i))

    if i != 0:
        h1.unitef('net0','con'+str(i))


h1.unitefn('Monopole1','ms1','ms1_3','ms1_2','net0','ms2','Monopole2','ms2_2','ms2_3')
h1.changename('Monopole1','MS')
h1.assignPerfectE('MS','pec0')
h1.assignPerfectE('GND','pecg')
#端口设置
h1.createRectangle('l_sub/2','-distance1/2+d_50ohm/2+lk2','0','-d_50ohm','h_sub','x','port1')
h1.createRectangle('l_sub/2','distance1/2-d_50ohm/2-lk2','0','d_50ohm','h_sub','x','port2')
h1.assignlumpport('port1','p1',str(l_sub/2)+'mm',str(-distance1/2+lk2)+'mm','0',str(l_sub/2)+'mm',str(-distance1/2+lk2)+'mm',str(h_sub)+'mm')
h1.assignlumpport('port2','p2',str(l_sub/2)+'mm',str(distance1/2-lk2)+'mm','0',str(l_sub/2)+'mm',str(distance1/2-lk2)+'mm',str(h_sub)+'mm')


h1.createRegion(str(1/4*lamda0)+'mm')
h1.assignRadiationRegion()
h1.fitAll()
h1.insertSetup("setup1","2.4GHz")
h1.insertFrequencysweep("setup1","2.1GHz","2.7GHz",50,"Interpolating")
# h1.solve('setup1')
h1.saveProject('D:\decouple_result','decouple_test01_'+str(n0))
