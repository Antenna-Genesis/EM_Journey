# CPW传输线仿真

鉴于AiP设计中需要用到接地CPW传输线（以下内容中，不严格区分接地CPW和悬空CPW，默认讨论接地CPW），有必要介绍一下CPW传输线的仿真方法。

因为目前组内成员用HFSS较多，第一版本主要介绍HFSS中的CPW馈电。

CPW的结构和关键参数如下。

![image-20211007163817090](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007163817090.png)

阻抗计算可以借助CST中的预制宏来实现，计算界面如下图所示。

![image-20211007163938938](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007163938938.png)

以200um厚、介电常数3.6的基板为例，可以看出w=0.4mm和g=0.15mm时候，CPW的特征阻抗约等于50ohm。这是我们设计传输线的起点，之后还需要略加调整，才可以得到更加准确地参数。

HFSS中，常用的CPW的馈电方法有两种：lumped port和wave port（Driven Modal）。

首先讨论前者。

![image-20211007164629566](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007164629566.png)

利用之前用CST的宏计算出来的参数，构建一段双端口CPW传输线，一对lumped ports分别置于CPW信号线的两端，并且lumped port所在平面要垂直于信号线，从而减少高频段内信号线与port之间的寄生电抗。

![image-20211007164802107](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007164802107.png)

另外，需要注意的是，为了减少信号泄露和干扰，通常需要在CPW附近加金属通孔。但加入众多通孔之后，整个系统的网格划分会变得很密集，网格数量明显增加，从而拖累计算速度。为了模拟金属通孔的效果、而不至于大幅度降低仿真速度，在早期仿真阶段（加工或者流片之前要换成真的通孔做微调），我们通常采用实心金属墙壁来替代金属通孔。

![image-20211007165029864](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007165029864.png)

完成必要的仿真设置后，我们可以对两个最关键的参数做单参数扫描：信号线宽度，信号线与地间距。

在这个设计实例中，我们发现信号线宽度等于0.33mm的时候，1端口的反射系数最小，也就是此时CPW的特征阻抗最接近50ohm。

![image-20211007165519477](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007165519477.png)

在信号线宽度等于0.33mm的前提下，对缝隙做参数扫描，可以发现缝隙等于0.12mm的时候，反射系数最小、且都在-30dB之下，也就是说这个时候的特征阻抗，更加接近50ohm。于是我们可以确定CPW的关键参数，信号线宽度和缝隙，分别为0.33mm和0.12mm。

![image-20211007170033451](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007170033451.png)

PS：在高频段，如果lumped port所在平面和信号线平面一致，馈电端口和CPW主体结构之间的寄生电抗会很明显，导致仿真结果出现明显偏差。仿真过程中需要避免这种馈电方式。

![image-20211007170634278](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007170634278.png)

再来看wave port馈电的情况。

HFSS Help文档中有port尺寸的说明

**Coplanar Transmission Line**

The figure below shows an HFSS model of a coplanar transmission  line. The left and right edges of each port must touch the left and right ground  planes. We recommend that you make the port size 8h x 10w where "w" represents  the width of the trace and "h" represents the height of the substrate.

![image-20211007173203807](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007173203807.png)

按照这一设置准则，以及考虑wave port需要金属背腔（也可以直接贴近辐射边界）的条件，我们构建了如下所示的仿真结构。

![image-20211007174451438](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007174451438.png)

相比于之前的lumped port馈电，现在的wave port馈电，在普通的S参数之外，还可以直接提供CPW传输线特征阻抗的计算数值。这意味着，采用wave port方式，我们可以更快更直接的获得特征阻抗等于50ohm的CPW参数。

![image-20211007174843021](C:\Users\Kai\AppData\Roaming\Typora\typora-user-images\image-20211007174843021.png)