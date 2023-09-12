# -*- coding: utf-8 -*-
"""
@author: bht
"""

import Costfunction
from base import SkoBase
from HFSS import HFSS
import LHSampling
import math
from scipy.stats import norm
import numpy as np
from GPmodel_sklearn import GPmodel_sklearn
from GPmodel_Gpytorch import GPmodel_Gpytorch

from scipy.optimize import minimize
from scipy.optimize import Bounds
from cmaes import CMA

import torch
device, dtype = torch.device("cpu") ,torch.float64

v=4
xv=np.linspace(-v,v,500)
cdfx = norm.cdf(xv)
pdfx = norm.pdf(xv)
c = np.poly1d(np.polyfit(xv, cdfx, 15))
p = np.poly1d(np.polyfit(xv, pdfx, 16))
print("xx")

def cdf_s(x):
    y = c(x)
    y[x>4] = 1.0
    y[x<-4] = 0.0
    return y

def pdf_s(x):
    y = p(x)
    y[x > 4] = 0.0
    y[x < -4] = 0.0
    return y

def AuxiOpti(func,  lb, ub):
    # 辅助优化器，需要酌情考虑它的运算时间
    ansX_g = (lb + ub) / 2
    ansy_g = np.inf
    bb = np.array([list(lb), list(ub)]).T
    qq = LHSampling.DoE_LHS(N=1, lb=lb, ub=ub) # 在lb，ub中LHS一些mean点，实际效果一般
    qqP = qq.ParameterArray
    meanX = np.array(qqP)
    meanX = np.vstack((meanX, ansX_g)) #再加上中点

    for meanx in meanX: #对每个mean点做CMAES
        optimizer = CMA(mean=meanx, sigma=(ub[0] - lb[0]) / 5, bounds=bb, population_size=60 * len(lb))
        # 为节省时间建议大批量小重复进行predict
        ansX = (lb + ub) / 2
        ansy = np.inf
        for generation in range(20):
            solutions = []
            Xx = []
            for _ in range(optimizer.population_size):
                x = optimizer.ask()
                Xx.append(np.array(x))
            Xx = np.array(Xx)
            Yy = func(Xx)
            if np.min(Yy) < ansy:
                ansX = Xx[np.argmin(Yy)]
                ansy = np.min(Yy)
            for _ in range(len(Xx)):
                solutions.append((Xx[_], Yy[_]))
            optimizer.tell(solutions)
            if optimizer.should_stop():
                break

        if ansy < ansy_g:
            ansX_g = ansX
            ansy_g = ansy

    return ansX_g, ansy_g


class PBO_q(SkoBase):

    def __init__(self, Optimization_variables,costfunc,
                 n_dim=None, initpop=40, max_iter=150,
                 lb=-np.ones(3), ub= np.ones(3), accu=2, q=np.array([1,0,0])):

        self.Optimization_variables=Optimization_variables #优化对象名字
        self.accu=accu         #精度 小数点后几位
        self.costfunc=costfunc #代价函数
        self.initpop = initpop #初始种群
        self.n_dim = n_dim     #维度
        self.max_iter = max_iter  # max iter

        self.NFE=0 #电磁计算次数
        self.q = q #q[0][1][2] 分别表示每次迭代基于 EI、LCB、PI 选点个数
        # 推荐LCB,更易于辅助寻优
        # q=[1,0,0]既是最简单的EI贝叶斯优化
        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'

        self.current_iter = 0
        qq = LHSampling.DoE_LHS(N=self.initpop, lb=self.lb, ub=self.ub)
        self.X = qq.ParameterArray.round(self.accu)
        self.Y = self.cal_y0()  #计算初始点
        # X、Y事实上就是数据集

        print('Init best fit: {} at {}'.format(self.ymin, self.argymin))
        print('Init_ Finished')
        print(' ')

    def SKO_Opti(self, style, q):  # style原则下 前q个最优点
        RecX = []
        ymin1 = self.ymin
        mm = self.GPreg.Xmean
        sstd = self.GPreg.Xstd
        th = self.GPreg.thetaa

        def costfunction(p):
            pred_y, pred_std = self.GPreg.predict(p)
            # 预测均值 预测标准差
            v_ = 0.3  # 参数
            anss = 1
            if style == 'EI':  # 预期改进
                tu = (ymin1 - pred_y - v_) / pred_std
                anss = (ymin1 - pred_y - v_) * cdf_s(tu) + pred_std * pdf_s(tu)
                anss = -anss

            elif style == 'LCB':  # 置信下界
                beta = 2*(qi+1)/(q+1) + 1  # 参数
                anss = pred_y - beta * pred_std - 30

            elif style == 'PI':  # 改进概率
                tu = (ymin1 - pred_y - v_) / pred_std
                anss = cdf_s(tu)
                anss = -anss

            if qi > 0 and style!='LCB':  # 除了第一个数之外
                Pa = (p - mm) / sstd
                for jj in range(len(Pa)):
                    for ii in range(qi):
                        Pb = (RecX[ii] - mm) / sstd
                        hyt = 0
                        for kk in range(len(RecX[0])):
                            hyt = hyt + (Pa[jj][kk] - Pb[kk])**2 / th[kk]
                        ru = np.exp(-hyt / 2)
                        anss[jj] = anss[jj] * (1 - ru)  # 乘入影响函数
            return anss

        for qi in range(q):
            qq,wq = AuxiOpti(costfunction,  self.lb, self.ub)
            RecX.append(np.array(qq))
        RecX = np.array(RecX)

        op = []
        for xx in RecX:
            op.append(self.GPreg.predict(xx))
        op = np.array(op)
        return [RecX.round(self.accu), op]

    def cal_y0(self):
        # 计算初始点所用 过程
        self.Y=np.ones((self.initpop,1))*float("inf")

        for i in range(0, self.initpop):
            cost_function_value=self.costfunc(self.X[i])
            self.NFE=self.NFE+1
            self.Y[i,0]=cost_function_value

        self.argymin = self.X[np.argmin(self.Y)] #初始化找到的最优结构
        self.ymin = min(self.Y)[0] #初始化找到的最优值
        return self.Y

    def OffspringAcquisition(self):
        #每次迭代中探索模型中的最优点更新
        NpX=[]
        Npy=[]
        style=['EI','LCB','PI']
        for k in range(3):
            if self.q[k]>0:
                # 找出并更新三种采集函数下的前q[k]个最优点
                Np,ppp = self.SKO_Opti(style[k],self.q[k])

                for i in range(self.q[k]):
                    cost_function_value = self.costfunc(Np[i])
                    print(Np[i],cost_function_value)
                    # 调用HFSS计算
                    self.NFE = self.NFE + 1
                    NpX.append(Np[i])
                    Npy.append([cost_function_value])
                    #记录
                    if cost_function_value<self.ymin:
                        self.argymin=Np[i]
                        self.ymin=cost_function_value #更新最优点和最优结构

        self.X = np.vstack((self.X, NpX))
        self.Y = np.vstack((self.Y, Npy))

    def run(self, max_iter=None):
        self.max_iter = max_iter or self.max_iter
        self.GPreg = GPmodel_Gpytorch(self.X,self.Y)
        for iter_num in range(self.max_iter):
            self.current_iter=iter_num
            self.OffspringAcquisition()
            self.GPreg.updateModel(self.X,self.Y)  # 更新模型
            print('Iter: {}, Best fit: {} at {}'.format(iter_num, self.ymin,self.argymin))
        self.best_x, self.best_y = self.argymin, self.ymin
        return self.best_x, self.best_y

    fit = run

if __name__ == '__main__':

    Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
    import Costfunction
    pbo = PBO_q(Optimization_variables=Optimization_variables,costfunc=Costfunction.costfunction,
               n_dim=3, initpop=3, max_iter=2,
               lb=np.array([8, 16, 4]), ub=np.array([12, 24, 14]), accu=2, q=np.array([3,0,0]))
    xbest,ybest =pbo.run()
    print(xbest,ybest)