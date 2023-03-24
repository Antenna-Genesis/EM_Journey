# -*- coding: utf-8 -*-
"""
@author: bht
"""

import Costfunction
from base import SkoBase
from HFSS import HFSS
import LHSampling
import math
from scipy.linalg import norm, pinv
from scipy.stats import norm
from matplotlib import pyplot as plt
import numpy as np
from sko.GA import GA
import shutil

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C  # REF就是高斯核函数

def SKO_Opti(Model,lb,ub,ac,style,q,theta,ymin): #style原则下 前q个最优点
    #理解参考论文
    RecX = []
    RecY = []
    def costfunction(p):
        testp=np.array([p])
        pred_y, pred_std = Model.predict(testp, return_std=True)
        # 预测均值 预测标准差
        v_=0# 参数
        if style == 'EI':  # 预期改进
            if pred_std == 0:
                return 0
            else:
                tu = (ymin - pred_y - v_) / pred_std
                ans = (ymin - pred_y - v_) * norm.cdf(tu, 0, 1) + pred_std * norm.pdf(tu, 0, 1)
            ans=-ans
        if style == 'LCB':  # 置信下界
            alpha = 5  # 参数
            ans = pred_y - alpha * pred_std
        if style == 'PI':   # 改进概率
            if pred_std == 0:
                return 0
            else:
                tu = (ymin - pred_y - v_) / pred_std
                ans = norm.cdf(tu, 0, 1)
            ans=-ans
        if qi > 0: #除了第一个数之外
            for ii in range(qi):
                ru = np.exp(-theta * np.linalg.norm(p - RecX[ii][:], 2))
                ans = ans * (1 - ru)  # 乘入影响函数
                #print()
        #print(ans)
        return ans[0]

    for qi in range(q):
        ga = GA(func=costfunction, n_dim=len(lb), size_pop=60, max_iter=600, prob_mut=0.01, lb=lb, ub=ub,precision=1e-3)
        qq,wq = ga.run()
        RecX.append(np.array(qq))
        RecY.append([wq])
    RecX=np.array(RecX)
    op=Model.predict(RecX, return_std=True)
    #print("predict",op)

    return [RecX.round(ac),op]

class BO_q(SkoBase):

    def __init__(self, Optimization_variables,costfunc,
                 n_dim=None, initpop=40, max_iter=150,
                 lb=-1e5, ub=1e5, accu=2, q=[1,0,0],
                 constraint_eq=tuple(), constraint_ueq=tuple()
                  ):

        self.Optimization_variables=Optimization_variables #优化对象
        self.accu=accu         #精度 小数点后几位
        self.costfunc=costfunc #代价函数
        self.initpop = initpop #初始种群
        self.n_dim = n_dim     #维度
        self.max_iter = max_iter  # max iter

        self.NFE=0 #电磁计算次数
        self.q = q #q[0][1][2] 分别表示每次迭代基于 EI、LCB、PI 选点个数
        # q=[1,0,0]既是最简单的EI贝叶斯优化
        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'

        self.current_iter = 0
        self.has_constraint = bool(constraint_ueq)
        self.constraint_ueq = constraint_ueq #约束，没完成的
        self.is_feasible = np.array([True] * initpop)

        namm=list(self.Optimization_variables)
        bb=np.array([list(self.lb),list(self.ub)]).T
        qq=LHSampling.DoE_LHS(N=self.initpop,bounds=bb,name_value=namm)
        qqp=np.array(qq.ParameterArray)
        for i in range(len(qqp)):
            qqp[i][:]=qqp[i][:].round(self.accu)
        self.X=qqp
        print(self.X) #拉丁超立方随机采样生成初始点

        self.Y = self.cal_y0()  #计算初始点
        # X、Y事实上就是数据集

        self.record_mode = False
        self.record_value = {'X': [], 'V': [], 'Y': []} #记录？但这里没用上
        print('Init_ Finished')
        print(' ')

    def cal_y0(self):
        # 计算初始点所用 过程
        self.Y=np.ones((self.initpop,1))*float("inf")

        for i in range(0, self.initpop):
            cost_function_value=self.costfunc(self.Optimization_variables,self.X[i])
            self.NFE=self.NFE+1
            self.Y[i,0]=cost_function_value

        self.argymin = self.X[np.argmin(self.Y)] #初始化找到的最优结构
        self.ymin = min(self.Y)[0] #初始化找到的最优值
        return self.Y

    def build_GPmodel(self):
        # 搭建、更新高斯模型
        kernel = RBF(2, (1e-4, 30))  # 创建高斯过程回归,并训练
        self.GPreg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=100,alpha=0.001)
        self.GPreg.fit(self.X, self.Y[:,0])

        KK = self.GPreg.K_  # 返回协方差矩阵
        distij = np.linalg.norm(self.X[0][:] - self.X[1][:], 2)
        self.theta = -distij * distij / np.log(KK[0][1])  # 高斯建模内部生成 的高斯内核theta=1/2l^2

    def OffspringAcquisition(self):
        #每次迭代中探索模型中的最优点更新
        NpX=[]
        Npy=[]
        style=['EI','LCB','PI']
        for k in range(3):
            if self.q[k]>0:
                # 找出并更新三种采集函数下的前q[k]个最优点
                Np,ppp =SKO_Opti(self.GPreg,self.lb,self.ub,self.accu,style[k],self.q[k],self.theta,self.ymin)
                                #SKO_Opti(Model,lb,ub,ac,style,q,theta,ymin)

                for i in range(self.q[k]):
                    cost_function_value = self.costfunc(self.Optimization_variables, Np[i])
                    # 调用HFSS计算
                    self.NFE = self.NFE + 1
                    NpX.append(Np[i])
                    Npy.append([cost_function_value])
                    #记录
                    if cost_function_value<self.ymin:
                        self.argymin=Np[i]
                        self.ymin=cost_function_value #更新最优点和最优结构

        listX = list(self.X)
        listY = list(self.Y)
        for i in range(len(NpX)):
            listX.append(NpX[i])
            listY.append(Npy[i])
        self.X = np.array(listX)
        self.Y = np.array(listY) #更新数据集

    def check_constraint(self, x):
        # 没用上
        for constraint_func in self.constraint_ueq:
            if constraint_func(x) > 0:
                return False
        return True
    def recorder(self):
        # 记录 没用上
        if not self.record_mode:
            return
        self.record_value['X'].append(self.X)
        self.record_value['Y'].append(self.Y)


    def run(self, max_iter=None, precision=1e-5, N=200):
        c=0
        self.max_iter = max_iter or self.max_iter
        self.build_GPmodel()
        for iter_num in range(self.max_iter):
            self.current_iter=iter_num
            self.OffspringAcquisition()
            self.build_GPmodel()  # 更新模型和theta

            if precision is not None:
                #判断收敛，即输出最小值最近N次迭代仍然不变就停止迭代
                tor_iter = np.amax(self.ymin) - np.amin(self.ymin)
                if tor_iter < precision:
                    c = c + 1
                    if c > N:
                        break
                else:、
                    c = 0
            print('Iter: {}, Best fit: {} at {}'.format(iter_num, self.ymin,self.argymin))
            #shutil.rmtree("D:\MonoPoleTest\Temp\monop.hfssresults\HFSSDesign1.results") #清空内存

        self.best_x, self.best_y = self.argymin, self.ymin
        return self.best_x, self.best_y

    fit = run

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")

    Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
    import Costfunction
    pso = BO_q(Optimization_variables=Optimization_variables,costfunc=Costfunction.costfunction,
               n_dim=3, initpop=20, max_iter=50,
               lb=[8, 16, 4], ub=[12, 24, 14], accu=2, q=[1,0,0])
    pso.run()