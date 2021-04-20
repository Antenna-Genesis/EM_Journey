# -*- coding: utf-8 -*-
import geatpy as ea
import numpy as np
import Project
import pandas as pd


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 2  # 初始化M（目标维数）
        max_or_min = [1, -1]  # 初始化max_or_min（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 1  # 初始化Dim（决策变量维数）
        varTypes = [0]  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [-180]  # 决策变量下界
        ub = [180]  # 决策变量上界
        lb_in = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ub_in = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, max_or_min, Dim, varTypes, lb, ub, lb_in, ub_in)

    def aimFunc(self, pop):  # 目标函数
        # 得到决策变量矩阵
        epsilon = pop.Phen[:, 0]
        pop.ObjV = np.zeros((pop.Phen.shape[0], self.M))  # 计算目标函数值，赋值给pop种群对象的ObjV属性
        for index in range(pop.Phen.shape[0]):
            Project.Prj(0, epsilon[index], epsilon[index] * 2.0, epsilon[index] * 3.0, epsilon[index] * 4.0,
                        epsilon[index] * 5.0, epsilon[index] * 6.0, epsilon[index] * 7.0)
            # Project.Prj(0, epsilon[0], epsilon[1], epsilon[2], epsilon[3], epsilon[4], epsilon[5], epsilon[6])
            Gain = pd.read_csv('Gain Plot 2.csv')
            number = Gain["dB(RealizedGainTotal) [] - Freq='2.44GHz' Phi='90deg'"].idxmax()
            Theta = Gain.iloc[number, 0]
            # Phi = Gain.iloc[number, 0]
            # pop.ObjV[index] = [abs(Theta - 60.0), abs(Phi - 0.0), Gain.iloc[86640, 2]]
            pop.ObjV[index] = [abs(Theta - 10.0), Gain.iloc[number, 1]]
            # pop.ObjV[index, 1] = Gain.iloc[number, 1]  # 30/492/75810 45/711/81225 60/930/86640


if __name__ == '__main__':
    """===============================实例化问题对象============================"""
    problem = MyProblem()  # 生成问题对象
    """==================================种群设置==============================="""
    Encoding = 'RI'  # 编码方式
    NIND = 15  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.moea_NSGA2_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.mutOper.Pm = 0.2  # 修改变异算子的变异概率
    myAlgorithm.recOper.XOVR = 0.9  # 修改交叉算子的交叉概率
    myAlgorithm.MAXGEN = 20  # 最大进化代数
    myAlgorithm.logTras = 2  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """==========================调用算法模板进行种群进化========================"""
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """=================================输出结果=============================="""
    print('评价次数：%s' % myAlgorithm.evalsNum)
    print('时间已过 %s 秒' % myAlgorithm.passTime)
    if BestIndi.sizes != 0:
        print('最优的目标函数值为：%s' % BestIndi.ObjV)
        print('最优的控制变量值为：')
        ObjV = pd.read_csv('C:/Users/tee/PycharmProjects/Result/ObjV.csv')
        col_name = list(ObjV.columns)
        print(BestIndi.Phen[ObjV[str(col_name[0])].idxmin() + 1, 0])
    else:
        print('没找到可行解。')
