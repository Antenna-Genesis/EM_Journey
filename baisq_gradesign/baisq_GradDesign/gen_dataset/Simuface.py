import time
import os
import shutil
from HFSS import HFSS
ser_path="D://baisq//2022_12_06"
def sim(height,fsolve,farfieldflag,count,rad_name1='1',rad_name2='2'):
    start_time = time.time()
    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print(f'This program started at: {time_string}')

    hfss_file_dir = ser_path+"//temp//temp"+str(count)
    if not os.path.exists(hfss_file_dir):
        os.makedirs(hfss_file_dir)
    hfss_file_name = 'Build_dataset'+str(count)
    hfss_result_file_path = hfss_file_dir +'//'+hfss_file_name+'.aedtresults'

    export_result_dir = ser_path+"//result//sim"+str(count)
    if not os.path.exists(export_result_dir):
        os.makedirs(export_result_dir)
    export_result_file_name = 'S Parameter'+str(count)+'.csv'
    # rad_name1 = 'rad_pat1'+str(count)+'.csv'
    # rad_name2 = 'rad_pat2' + str(count) + '.csv'
    export_result_file_path = export_result_dir+'//'+export_result_file_name

    hfss_Optimization_record_dir = ser_path+"//record"
    if not os.path.exists(hfss_Optimization_record_dir):
        os.makedirs(hfss_Optimization_record_dir)
    hfss_Optimization_record_file_name = 'Record for simulations.txt'

    h = HFSS()
    # Launch ANSYS Electronics Desktop
    h.launch()
    print('Successfully open ANSYS Electronics Desktop')
    h.oDesign.SetSolutionType("HFSS Modal Network",
                            [
                                "NAME:Options",
                                "EnableAutoOpen:=", False
                            ])

    # Set all variables in HFSS
    h.setVariable('hsub', 1.52, 'mm')
    h.setVariable('ws', 3.6, 'mm')
    h.setVariable('ls', 20, 'mm')
    h.setVariable('w', 7.2, 'mm')
    h.setVariable('a', 24.4, 'mm')
    h.setVariable('b', 16.8, 'mm')
    h.setVariable('c', 14, 'mm')
    h.setVariable('wf', 3.3, 'mm')
    h.setVariable('gw', 140, 'mm')
    print('Successfully Set all variables')
    h.addMaterial('DK10', 9.8, 0.0001)
    #Python变量，方便计算
    w=7.2
    #介质板
    h.createBox('0mm','0mm','0mm','gw','gw','hsub','Tac','Taconic RF-35 (tm)','')
    h.Color('Tac', 85, 102, 0)
    #介质板表面的金属层
    h.createRectangle('0mm','0mm','hsub','gw','gw','Z','Ground')
    h.Assignpecbound('PEC2', 'Ground')
    h.Color('Ground', 255, 153, 18)
    #DR
    for i in range(4):
        for j in range(4):
            h.createBox('55.6mm'+'+'+str(i*w)+'mm', '55.6mm'+'+'+str(j*w)+'mm', 'hsub+0.01mm', 'w', 'w', height[i][j], 'DR'+str(i+1)+'_'+str(j+1), 'DK10', '')
            h.TransChange( 'DR'+str(i+1)+'_'+str(j+1), 1)
        # slot
    h.createBox('gw/2-ws/2', 'gw/2-ls/2', 'hsub', 'ws', 'ls', '0.01mm', 'slot', 'pec', 'F')
    h.subtractf('Ground', 'slot')
    # 微带线
    h.createRectangle('gw', 'gw/2-wf/2', '0mm', 'a/2-gw/2', 'wf', 'Z', 'microstrip')
    h.createRectangle('gw/2+a/2', 'gw/2+b/2', '0mm', 'c/2-b/2', '-b', 'Z', 'microstrip2')
    # h.createBox('gw/2-a/2', 'gw/2+b/2', '0mm', 'a', 'c/2-b/2', '-0.01mm', 'microstrip3', 'copper', 'F')
    # h.createBox('gw/2-a/2', 'gw/2+b/2-b/2-c/2', '0mm', 'a', 'c/2-b/2', '-0.01mm', 'microstrip4', 'copper', 'F')
    h.createRectangle('gw/2+a/2', 'gw/2+b/2', '0mm', '-a', 'c/2-b/2', 'Z', 'microstrip3')
    h.createRectangle('gw/2+a/2', 'gw/2+b/2-b/2-c/2', '0mm', '-a', 'c/2-b/2', 'Z', 'microstrip4')
    # h.createBox('gw', 'gw/2-wf/2', '0mm', 'ws/2-gw/2+a', 'wf', '-0.01mm', 'microstrip', 'copper', 'F')
    # h.createBox('gw/2+ws/2+a', 'gw/2+b/2', '0mm', 'c/2-b/2', '-b', '-0.01mm', 'microstrip2', 'copper', 'F')
    # h.createBox('gw/2+ws/2', 'gw/2+b/2', '0mm', 'a', 'c/2-b/2', '-0.01mm', 'microstrip3', 'copper', 'F')
    # h.createBox('gw/2+ws/2', 'gw/2+b/2-b/2-c/2', '0mm', 'a', 'c/2-b/2', '-0.01mm', 'microstrip4', 'copper', 'F')
    h.unitef('microstrip', 'microstrip2')
    h.unitef('microstrip', 'microstrip3')
    h.unitef('microstrip', 'microstrip4')
    h.Assignpecbound('PEC3', 'microstrip')
    h.Color('microstrip', 255, 128, 0)
    # port
    h.createRectangle('gw','gw/2-wf/2','0mm','wf', 'hsub', 'X', 'Port' )
    h.Assignpecbound('PEC1','Port')
    h.Color('Port', 255, 0, 0)
    face_id = h.getFacebyposition('Port', 'gw', 'gw/2', '-0mm')
    x1 = str(140) + 'mm'
    y1 = str(70) + 'mm'
    z1 = '0mm'
    x2 = x1
    y2 = y1
    z2 = str(1.52) + 'mm'
    # print(x1)
    # print(y1)
    # print(z1)
    # print(x2)
    # print(y2)
    # print(z2)
    h.assignLumport(face_id, x1, y1, z1, x2, y2, z2)
    h.createRegion('30mm')
    h.assignRadiationRegion()
    print('Successfully set Model, exciation and radiation boundary')
    # Set setup and analysis and solve
    h.insertSetup('Setup1', str(fsolve)+'GHZ')
    if farfieldflag==0:
        h.insertFrequencysweep('Setup1', '2.5GHz', '4GHz', '50MHz', 'Fast')
    if farfieldflag==1:
        h.insertFrequencysweep('Setup1', str(fsolve-0.5)+'GHz', str(fsolve+0.5)+'GHz', '50MHz', 'Fast')
    #插入远场
    if farfieldflag==1:
        h.insertRadiationsphere()
    h.saveProject(hfss_file_dir, hfss_file_name)
    h.fitAll()
    hfss_run_start_time = time.time()
    h.solve('Setup1')
    hfss_run_elapsed_time = time.time() - hfss_run_start_time
    print(f'Overall running time of this project is {hfss_run_elapsed_time:.3f}s')
    if farfieldflag==0:
        Result_items=['dB(S11)']
        h.createSpreport('Sparameter','Setup1',Result_items)
        h.exportTofile('Sparameter', export_result_dir, export_result_file_name)
        print('Successfully Slove and export S11')
    # h.deleteAllreports()
    if farfieldflag==1:
        h.createRectangulzrfarfieldpreportasgaintotal('RadiationPattern1','Setup1','All', 0,str(fsolve)+'Ghz')
        h.exportTofile('RadiationPattern1', export_result_dir, rad_name1)
        h.createRectangulzrfarfieldpreportasgaintotal('RadiationPattern2', 'Setup1', 'All', 90, str(fsolve) + 'Ghz')
        h.exportTofile('RadiationPattern2', export_result_dir, rad_name2)
    h.closeProject()
    elapsed_time = time.time() - start_time
    print(f'Overall time for this script is: {elapsed_time:.3f}s')
    print('Finished all!')
