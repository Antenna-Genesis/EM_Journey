# -*- coding: utf-8 -*-
"""
@author: bht
"""

import matplotlib.pyplot as plt
import matplotlib
import scipy.stats as st
import random
from base import SkoBase
from HFSS import HFSS
import numpy as np
import LHSampling
import math
import FindOptimumPoint
import shutil
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C  # REF就是高斯核函数

class forSADEA(SkoBase):

    def __init__(self, Optimization_variables,costfunc,
                 n_dim=None, initpop=100, tau=100, lamda=50, max_iter=150,
                 lb=-1e5, ub=1e5, accu=2,
                 constraint_eq=tuple(), constraint_ueq=tuple() ):

        self.Optimization_variables=Optimization_variables #优化对象
        self.accu=accu         #精度
        self.costfunc=costfunc #代价函数
        self.initpop = initpop #初始种群数
        self.tau = tau   #模型纳点数
        self.lam = lamda #引入DE的最先种群数

        self.n_dim = n_dim     #维度
        self.max_iter = max_iter  # max iter

        self.NFE=0 #电磁计算次数

        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'

        self.current_iter = 0
        self.has_constraint = bool(constraint_ueq)
        self.constraint_ueq = constraint_ueq

        self.is_feasible = np.array([True] * self.initpop)

        namm=list(self.Optimization_variables)
        bb=np.array([list(self.lb),list(self.ub)]).T
        qq=LHSampling.DoE_LHS(N=self.initpop,bounds=bb,name_value=namm)
        qqp=np.array(qq.ParameterArray)
        for i in range(len(qqp)):
            qqp[i][:]=qqp[i][:].round(self.accu)

        self.X=qqp
        print(self.X) #拉丁超立方随机采样生成
        self.Y = self.cal_y0()  # y = f(x) for all particle
        self.dataset=np.zeros((self.initpop,n_dim+1))
        for i in range(self.initpop):
            self.dataset[i][:-1]=self.X[i]
            self.dataset[i][n_dim]=self.Y[i][0]
        #print(self.dataset)
        self.dataset_sorted = sorted(self.dataset, key=lambda x: x[self.n_dim])
        #print(self.dataset_sorted)

        # record verbose values
        self.record_mode = False
        self.record_value = {'X': [], 'V': [], 'Y': []}
        print('Init_ Finished')
        print(' ')
    #约束

    def cal_y0(self):
        # 初始化节点运算
        # calculate y for every x in X
        self.Y=np.ones((self.initpop,1))*float("inf")

        for i in range(0, self.initpop):
            cost_function_value=self.costfunc(self.Optimization_variables,self.X[i])
            self.NFE=self.NFE+1
            self.Y[i,0]=cost_function_value

        self.argymin = self.X[np.argmin(self.Y)]
        self.ymin = min(self.Y)[0] #目前找到的最优值
        return self.Y

    def insert_sorted_dataset(self, np):
        # 对于有序的dataset进行二分插入
        ds=self.dataset_sorted
        n = len(ds)
        m = len(np)
        l = 0;
        r = n - 1
        # for i in range(10):
        while True:
            if l + 1 >= r:
                break
            else:
                mid = int((r + l) / 2)
                if ds[mid][m - 1] < np[m - 1]:
                    l = mid
                else:
                    r = mid
        self.dataset_sorted.insert(r, np)

    def DE_generate(self,pop):  # 差分进化算法生成新种群
        F = 0.8  # 缩放率
        CR = 0.8  # 变异率
        npop = pop
        D = len(pop[0])
        for i in range(len(pop)):  # 遍历整个种群
            # * DE/rand/1
            r = random.sample(range(len(pop) - 1), 3)  # 随机选三个除了 i 以外的数字，作为选出的三个个体的索引
            for j in range(3):  # 选择方法使用 sample 先从 [0, PS-1) 中不重复的随机选择三个数字
                if r[j] >= i:  # 再将三个数字中，超过当前个体 i 的数字进行 +1
                    r[j] += 1  # 实现避免选择到第 i 个个体的效果

            v = pop[r[0]] + F * (pop[r[1]] - pop[r[2]])
            # * :math:`V_i(t)=X_{r1}(t) + F * (X_{r2}(t) - X_{r3}(t))`
            # print("v",v)
            # * bin
            jrand = random.randint(1, D)  # * 随机 [1, D] 的整数作为 rand_j，因为 bin 交叉必须保证 U 有至少一个基因来自于 V
            u = np.array(
                [(pop[i][j], v[j])[random.random() < CR or jrand == j] for j in range(D)]
            )  # 交叉操作，使用特殊的三目运算写法实现交叉
            # print("u",u)
            npop[i] = np.clip(u, self.lb, self.ub).round(self.accu) #避免越界
        return npop

    def build_GPmodel(self):
        kernel = RBF(2, (1e-4, 100))  # 创建高斯过程回归,并训练
        self.GPreg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=100,alpha=0.01)
        utrs=min(self.NFE,self.tau)
        self.GPreg.fit(self.X[-utrs:], self.Y[-utrs:,0])

    def check_constraint(self, x):
        # gather all unequal constraint functions
        for constraint_func in self.constraint_ueq:
            if constraint_func(x) > 0:
                return False
        return True

    def recorder(self):
        if not self.record_mode:
            return
        self.record_value['X'].append(self.X)
        self.record_value['Y'].append(self.Y)

    def run(self, max_iter=None, precision=1e-5, N=20):
        c=0
        self.max_iter = max_iter or self.max_iter
        for iter_num in range(self.max_iter):
            self.current_iter=iter_num
            arrdatas=np.array(self.dataset_sorted)
            P=arrdatas[-self.lam:,:-1]
            nP=self.DE_generate(P) #生成新点集
            self.build_GPmodel() #更新模型

            pred_y, pred_std = self.GPreg.predict(nP, return_std=True)
            # 模型预测
            minlcb=2147483647
            minP=0
            for i in range(self.lam):
                if pred_y[i]-2*pred_std[i]<minlcb:
                    minlcb=pred_y[i]-2*pred_std[i]
                    minP=i
            print(minP,nP[minP],minlcb)
            cost_function_value = self.costfunc(self.Optimization_variables, nP[minP])
            # 计算新集合中LCB最优的那个点
            self.NFE = self.NFE + 1
            if cost_function_value<self.ymin:
                self.ymin=cost_function_value
                self.argymin=nP[minP]

            gx=nP[minP]
            gx=np.append(gx,cost_function_value) #只有一维的可以这么做
            self.insert_sorted_dataset(gx) #更新有序数据集

            listX=list(self.X)
            listX.append(nP[minP])
            self.X=np.array(listX)
            listY = list(self.Y)
            listY.append([cost_function_value])
            self.Y = np.array(listY)
            listd = list(self.dataset)
            listd.append(gx)
            self.dataset = np.array(listd) #更新数据集

            # self.update_q()
            if precision is not None:
                tor_iter = np.amax(self.Y) - np.amin(self.Y)
                if tor_iter < precision:
                    c = c + 1
                    if c > N:
                        break
                else:
                    c = 0
            print('Iter: {}, Best fit: {} at {}'.format(iter_num, self.ymin,self.argymin))

        self.best_x, self.best_y = self.argymin, self.ymin
        return self.best_x, self.best_y

    fit = run

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")

    Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
    import Costfunction
    sy1 = forSADEA(Optimization_variables, Costfunction.costfunction,
               n_dim=3, initpop=30,tau=100,lamda=20,max_iter=30,
               lb=[8, 16, 4], ub=[12, 24, 14], accu=2)
    hj, kl = sy1.run()
    print(hj, kl)