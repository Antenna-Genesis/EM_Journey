# 代理模型辅助优化DEMO

#### 介绍
之前是从cyang58 学长手搓（？）的PSO作为demo开始学习HFSS和python的联合仿真优化的。事实上，学长这个PSO槽点很多，当然也有可能我没能理解它的高深思想。
简而言之就是具体的仿真软件上的控制原则上应该独立于优化算法，而学长的PSO把他们揉在了一起。
所以结合这几个月的经验，对这个demo的一些地方做出一些改动，另外附上自己在python上复现可以作为实验对照组的两种简单的*代理模型辅助优化算法*，并行贝叶斯优化（PBO）以及代理模型辅助差分演化（SADEA）。

在HFSS自带的Optimetrics 中，基本上是一些直接方法和GA。在对于高维度下的优化时，直接方法基本上没有任何效果，而GA由于迭代中种群每个结构都要计算使得耗时过多，PSO和DE作为相似的进化算法也是同理。
这时，机器学习搭建下的辅助模型的引入尤为重要，就有了简单的 **贝叶斯算法BO** （自己百度），以及各种各样的 “模型-搜索引擎-预筛选方法” 排列组合。在天线设计这个领域，matlab中的Antenna Toolbox库中采用的 **SADEA** 就常被拿来讨论。也因为它是一个比较老（2014）而且朴素（它的排列组合是“高斯过程-差分演化-采集函数最优”）的算法，可以被用作一个合适的对照组凸显宁的成果。
![输入图片说明](.idea/%E5%9B%BE%E7%89%871(1)(1).png)

#### 引用
Optimetrics介绍：[https://blog.csdn.net/qq_41542947/article/details/108104890](http://)

Antenna Toolbox库介绍：[https://ww2.mathworks.cn/products/antenna.html?s_eid=PEP_15027](http://)

PBO天线例子论文：Bayesian Optimization for Antenna Design via Multi-Point Active Learning 

PBO数学方法论文：Pseudo expected improvement criterion for parallel EGO algorithm

SADEA 论文：An Effificient Method for Antenna Design Optimization Based on Evolutionary Computation and Machine Learning Techniques


#### 注意事项

言归正传，这只是一个简单的Readme，不是写论文，接下来我就只是简单介绍具体的改动和代码结构大概如何。
1. 首先要解释的是模型的搭建方面。我个人认为有必要在一开始熟悉脚本的时候自己用脚本搭建一两个天线模型。但是事实上脚本搭建的效率远低于手动搭建，而且有的结构脚本并没被录入HFSS.py中，要自己录下再调用，这明显的不必要的做法。
所以我将各个算法函数的调用都移到了该算法.py的主函数上。只是另保留一个搭建demo所需的DRA模型的Example_a_cylinder_DRA.py。只用运行一下 **生成模型就完了** 。
2. 那么我就在costfunction函数前后加上hfss工程的打开和关闭代码，每次需要仿真时打开HFSS。血泪教训，如果一直打开着HFSS运行会造成严重卡顿，以及生成一堆结果文件挤占空间。注意，当调用你自己已搭建好的仿真project时，在costfunction函数中更改路径即可，不用打开hfss（会被警告重复打开）。
3. 原先PSO中带入costfunction参数里面一堆文件路径，这非常没必要，只用在cf里自己设置就好。同时，学习python本身sko库以及很多优化库里函数的做法，把costfunction也作为PSO形参导入。这样更换costfunction时只需更换它的参数而不用做内部调整。
4. 原本Demo的costfunction的计算我没改，也懒得看懂，就这样吧。
5. 原先学长的PSO里面的记录数据的代码写的太乱太复杂，而且我认为没有必要记录这么多东西，或者说不符合我的习惯，所以在我写的PBO和SADEA中并不会出现下图这些，原来的PSO就懒得改了：
![输入图片说明](.idea/%E5%9B%BE%E7%89%872.png)
怎么去记录实在是很难统一规制，大家还是怎么方便怎么来罢

6. PSO原来里面的记录record和约束constraint都是写了个空壳子，没用的。我也懒得加（优质回答），所以你在PBO和SADEA中看到的仍然是一个空壳子。有需要研究约束的话自己去找方法加进去。
7. PBO中关键的q数组中 q[0][1][2] 分别表示每次迭代基于 EI、LCB、PI 选点个数。 q=[1,0,0]既是最简单的EI贝叶斯优化。
8. LHS是拉丁超立方采样，一个初始化采样方式，具体见百度。
9. 因为PBO要导出高斯过程的协方差矩阵K，而K在GaussianProcess Regressor 中不是公开的。 **所以要改 _gpr.py** ，在320行处加上一句将它公开，可能会有权限问题，这个不是大问题，自己调一下：
![输入图片说明](.idea/%E5%9B%BE%E7%89%873.png)

10. SADEA基本上是按照论文搭建的。由于DE的超参数较多，论文中也有讨论。我只做了一个改动，就是原文中 初始种群数量=建模粒子数量tau，这一定程度上限制了算法的灵活度。所以我将 **初始种群数量单独设置** ，当已计算的例子不足tau时仍能建模，超过tau后依然照论文方式。