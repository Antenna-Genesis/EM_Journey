#### HFSS15+python说明文档

对https://gitee.com/kai-lu/EM_Journey/tree/main/Antenna_Chen/Week_03%20HFSS%20python%E5%BA%93%E5%87%BD%E6%95%B0进行修改和注释，使其适用于hfss15

大体思路为使用win32com模块连接python与hfss，通过代码录制的方式可以record控制hfss中各步操作的具体代码，详细步骤参考OD中周报22_2_27

#### 1.初始化部分(line24)

`def init(self)`      控制当前pro和design（不用`__init__`防止自动运行）

`def launch(self)`	新建文件

`def openProject(self, Path, Projectname)`	打开project

e.g.

```
from HFSS import HFSS
h1=HFSS()
h1.launch()
```

#### 2.变量部分(line76)

设置、更改变量

已知变量名获取值、单位

e.g.

```
h1.setVariable('d_monopole',3,'mm')

distance1=4
h1.setVariable('distance1',distance1,'mm')

h1.setVariable('w_sub','distance1+d_monopole+2*d_monopole','')
```

p.s.

1.使用setVariable创建已有变量时会报错’发生意外‘

2.上面第三例加单位会报错



#### 3.建模部分(line125)

```
def createBox()
def createCylinder()	
def createPolyprism()  #多棱柱
def createRectangle()
def createCircle()
```

e.g.

```
h1.createBox('-l_sub/2','-w_sub/2','0','l_sub','w_sub','h_sub','substrate',"Rogers RT/duroid 5880 (tm)",'T')
h1.createRectangle('1 mm','2 mm','0','1 mm','2 mm','Z','GND')
```

p.s.

1.颜色设置为了默认绿(143 175 143)

2.Ansys HFSS中的Solve Inside是是否对该模型内部进行求解的选项，在选中后将对该模型内部进行网格划分和电场求解，否则将只对模型表面进行网格划分而不会求解内部的电场。对于良导体而言，由于电磁波的趋肤效应，电磁场能量都分布在靠近导体表面的地方，因而无需对导体内部进行电场的计算。在默认设置下，材料为良导体（如铜、银、PEC等）的模型Solve Inside选项都是未选中状态。

因此，当材料为pec时，solvein参数应设为’F‘，虽然建模金属块的情况很少

#### 4.材料部分(line219)

如代码所示\

#### 5.边界设置(line493)

`def assignPerfectE(self, Object, PEC_name)`

#### 6.端口激励设置(line555)

常用：
`def assignWaveport(self, FaceID,Startx,Starty,Startz,Endx,Endy,Endz)`

波端口

`def assignlumpport(self,port,name,sx,sy,sz,ex,ey,ez)`

集总端口  port:模型名称  name：端口名称 

**积分线**      sxyz:起点坐标 exyz：终点坐标

由于积分线坐标设置不能使用HFSS变量，建议使用`getVariablevalue()`获取变量值再设置坐标,或在变量设置时同时创建一组python变量

e.g.

```
#端口设置

#python变量创建
w0=3.0836;distance1=68;l_monopole=22;d_network=1;d_50ohm=w0;
l_sub=150;h_sub=1;lk1=64;lk2=16;lk3=25;dt=10;di=20;

h1.createRectangle('l_sub/2','-distance1/2+d_50ohm/2+lk2','0','-d_50ohm','h_sub','x','port1')

h1.createRectangle('l_sub/2','distance1/2-d_50ohm/2-lk2','0','d_50ohm','h_sub','x','port2')

h1.assignlumpport('port1','p1',str(l_sub/2)+'mm',str(-distance1/2+lk2)+'mm','0',str(l_sub/2)+'mm',str(-distance1/2+lk2)+'mm',str(h_sub)+'mm')

h1.assignlumpport('port2','p2',str(l_sub/2)+'mm',str(distance1/2-lk2)+'mm','0',str(l_sub/2)+'mm',str(distance1/2-lk2)+'mm',str(h_sub)+'mm')

```

#### 7.空气盒子(line245)

`def createRegion(self, Var_region)`	设置空气盒子， `Var_region`大小为1/4波长

`def assignRadiationRegion(self)	`设置辐射边界

可以直接使用以下代码

```
f0=2.4  #单位GHz
lamda0=3*10**8/(f0*10**9)*1000
h1.createRegion(str(1/4*lamda0)+'mm')
h1.assignRadiationRegion()
```

#### 8.求解设置(line265)

`def insertSetup(self, Setupname,Centerfreuency)`设置

`def insertFrequencysweep(self, Setupname, Minfrequency, Maxfrequency, Step, Sweep_type)`扫频

`def solve(self, Setupname)`求解

e.g.

```
h1.insertSetup("setup1","2.4GHz")
h1.insertFrequencysweep("setup1","2.1GHz","2.7GHz",50,"Interpolating")
h1.solve('setup1')
```

#### 9.布尔运算(line326)

unit：模型相加，新增多值函数`unitn()`可传任意数量参数

Subtract：相减，f/t决定是否保留被减去部分

connect:连接两个面形成三维模型，画喇叭天线常用

Intersect:相交取交集

e.g.

```
h1.unitefn('Monopole1','ms1','ms1_3','ms1_2','net0','ms2','Monopole2','ms2_2','ms2_3')
```



#### 10.生成报告(line680)

`def createSpreport(self, Reportname,Setupname,Result_items)`

`def createSpreport(self, Reportname)`（当前）

此函数由于HFSS15版本原因稳定性极差，当传入`Setupname,Result_items`两个变量时会报错’发生异常‘，bug原因无法排查，故将后两个变量用常量代替，将其改为只生成（s(1,1))图表的函数，传参只有`Reportname`有效

e.g.

```
createSpreport(sparameter1)
```

以上改动实属无奈之举，具体情况见OD周报5_6，欢迎协助排查bug原因

若需要其他结果，建议改动类文件

`def exportTofile(self, Reportname, Savepath, Savefilename)`（line774）

用于导出数据为CSV文件

#### 11.保存(line816)

`def saveProjectdefault(self)`默认保存

`def saveProject(self, result_path, file_name):`自定义路径

e.g.

```
h1.saveProject('D:\decouple_result','decouple_test01_'+str(n0))
```

