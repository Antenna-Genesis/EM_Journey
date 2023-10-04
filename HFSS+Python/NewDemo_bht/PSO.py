# -*- coding: utf-8 -*-
"""
@author: cyang58
modify: bht
"""

from base import SkoBase
from HFSS import HFSS
import numpy as np
from Costfunction import costfunction

class PSO(SkoBase):

    def __init__(self, Optimization_variables, costfunc,
                 n_dim=None, pop=40, max_iter=150, lb=-1e5, ub=1e5, w=0.8, c1=0.1, c2=0.5,
                 constraint_eq=tuple(), constraint_ueq=tuple(), verbose=False
                 , dim=None):

        n_dim = n_dim or dim    # support the earlier version
        self.Optimization_variables = Optimization_variables
        self.costfunc=costfunc  # 改将cost引入参数

        self.w = w  # inertia
        self.cp, self.cg = c1, c2  # parameters to control personal best, global best respectively
        self.pop = pop  # number of particles
        self.n_dim = n_dim  # dimension of particles, which is the number of optimized variables
        self.max_iter = max_iter  # max iter
        self.verbose = verbose  # print the result of each iter or not

        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
        print(len(self.lb))
        assert self.n_dim == len(self.lb) == len(self.ub), 'dim == len(lb) == len(ub) is not True'
        assert np.all(self.ub > self.lb), 'upper-bound must be greater than lower-bound'
        self.current_iter = 0
        self.has_constraint = bool(constraint_ueq)
        self.constraint_ueq = constraint_ueq
        self.is_feasible = np.array([True] * pop)

        self.X = np.random.uniform(low=self.lb, high=self.ub, size=(self.pop, self.n_dim)).round(1)
        v_high = self.ub - self.lb
        self.V = np.random.uniform(low=-v_high, high=v_high, size=(self.pop, self.n_dim))  # speed of particles
        self.Y = self.cal_y()  # y = f(x) for all particles
        self.pbest_x = self.X.copy()  # personal best location of every particle in history
        self.pbest_y = np.array([[np.inf]] * pop)  # best image of every particle in history
        self.gbest_x = self.pbest_x.mean(axis=0).reshape(1, -1)  # global best location for all particles
        self.gbest_y = np.inf  # global best y for all particles
        self.gbest_y_hist = []  # gbest_y of every iteration
        self.update_gbest()

        # record verbose values
        self.record_mode = False
        self.record_value = {'X': [], 'V': [], 'Y': []}
        self.best_x, self.best_y = self.gbest_x, self.gbest_y  # history reasons, will be deprecated

    def update_V(self):
        r1 = np.random.rand(self.pop, self.n_dim)
#        r1 = np.random.rand(self.pop, self.n_dim).round(1)
#        r1 = np.around(np.random.rand(self.pop, self.n_dim), decimals=1)
        r2 = np.random.rand(self.pop, self.n_dim)
        self.V = self.w * self.V + \
                 self.cp * r1 * (self.pbest_x - self.X) + \
                 self.cg * r2 * (self.gbest_x - self.X)


    def update_X(self):
        self.X = self.X + self.V
        self.X = np.clip(self.X, self.lb, self.ub).round(1)


    def cal_y(self):
        # calculate y for every x in X
        self.Y=np.ones((self.pop,1))*float("inf")
        for i in range(0, self.pop):
            # 改
            cost_function_value=self.costfunc(self.X[i])
            self.Y[i,0]=cost_function_value
            print('The pop number is', i, ', parameter is',self.X[i], 'and cost function is', cost_function_value)
        return self.Y


    def update_pbest(self):
        '''
        personal best
        :return:
        '''
        self.need_update = self.pbest_y > self.Y
        self.pbest_x = np.where(self.need_update, self.X, self.pbest_x)
        self.pbest_y = np.where(self.need_update, self.Y, self.pbest_y)

    def update_gbest(self):
        '''
        global best
        :return:
        '''
        idx_min = self.pbest_y.argmin()
        if self.gbest_y > self.pbest_y[idx_min]:
            self.gbest_x = self.X[idx_min, :].copy()
            self.gbest_y = self.pbest_y[idx_min]

    def recorder(self):
        if not self.record_mode:
            return
        self.record_value['X'].append(self.X)
        self.record_value['V'].append(self.V)
        self.record_value['Y'].append(self.Y)

    def run(self, max_iter=None, precision=1e-5, N=20):
        '''
        precision: None or float
            If precision is None, it will run the number of max_iter steps
            If precision is a float, the loop will stop if continuous N difference between pbest less than precision
        N: int
        '''
        self.max_iter = max_iter or self.max_iter
        c = 0
        for iter_num in range(self.max_iter):
            self.current_iter=iter_num
            self.update_V()
            self.recorder()
            self.update_X()
            self.cal_y()
            self.update_pbest()
            self.update_gbest()
            if precision is not None:
                tor_iter = np.amax(self.pbest_y) - np.amin(self.pbest_y)
                if tor_iter < precision:
                    c = c + 1
                    if c > N:
                        break
                else:
                    c = 0
            print('Iter: {}, Best fit: {} at {}'.format(iter_num, self.gbest_y, self.gbest_x))

            self.gbest_y_hist.append(self.gbest_y)
        self.best_x, self.best_y = self.gbest_x, self.gbest_y
        return self.best_x, self.best_y

    fit = run

if __name__ == '__main__':
    Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
    pso = PSO(Optimization_variables=Optimization_variables,costfunc=costfunction,
              n_dim=3, pop=3, max_iter=3,
              lb=[8, 16, 4], ub=[12, 24, 14], w=0.8, c1=0.5, c2=0.5,)
    xbest,ybest = pso.run()
    print(xbest,ybest)