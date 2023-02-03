# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:07:14 2020

@author: cyang58
"""

from base import SkoBase
from HFSS import HFSS
import numpy as np
from Costfunction import costfunction



class PSO(SkoBase):
#class PSO(HFSS):

    """
    Do PSO (Particle swarm optimization) algorithm.

    This algorithm was adapted from the earlier works of J. Kennedy and
    R.C. Eberhart in Particle Swarm Optimization [IJCNN1995]_.

    The position update can be defined as: 

    .. math::

       x_{i}(t+1) = x_{i}(t) + v_{i}(t+1)

    Where the position at the current step :math:`t` is updated using
    the computed velocity at :math:`t+1`. Furthermore, the velocity update
    is defined as:

    .. math::

       v_{ij}(t + 1) = w * v_{ij}(t) + c_{p}r_{1j}(t)[y_{ij}(t) − x_{ij}(t)]
                       + c_{g}r_{2j}(t)[\hat{y}_{j}(t) − x_{ij}(t)]

    Here, :math:`cp` and :math:`cg` are the cognitive and social parameters
    respectively. They control the particle's behavior given two choices: (1) to
    follow its *personal best* or (2) follow the swarm's *global best* position.
    Overall, this dictates if the swarm is explorative or exploitative in nature.
    In addition, a parameter :math:`w` controls the inertia of the swarm's
    movement.

    .. [IJCNN1995] J. Kennedy and R.C. Eberhart, "Particle Swarm Optimization,"
    Proceedings of the IEEE International Joint Conference on Neural
    Networks, 1995, pp. 1942-1948.

    Parameters
    --------------------
    Optimization_variables: tuple with a series of variables
        The variables you want to do optimal
    dim : int
        Number of dimension, which is number of optimized variables.
    pop : int
        Size of population, which is the number of Particles. We use 'pop' to keep accordance with GA
    max_iter : int
        Max of iter iterations
    lb : array_like
        The lower bound of every variables
    ub : array_like
        The upper bound of every variables
        
    optimization_target: 
        target for record
    
    export_result_dir, export_result_file_name: 
        path and file for postprocess applied in Cost function
    
    hfss_Optimization_record_dir, hfss_Optimization_record_file_name:
        path and file for recording the optimization history
                 
    constraint_eq : tuple
        equal constraint. Note: not available yet.
    constraint_ueq : tuple
        unequal constraint
    Attributes
    ----------------------
    pbest_x : array_like, shape is (pop,dim)
        best location of every particle in history
    pbest_y : array_like, shape is (pop,1)
        best image of every particle in history
    gbest_x : array_like, shape is (1,dim)
        general best location for all particles in history
    gbest_y : float
        general best image  for all particles in history
    gbest_y_hist : list
        gbest_y of every iteration


    """

    def __init__(self, Optimization_variables, n_dim=None, pop=40, max_iter=150, lb=-1e5, ub=1e5, w=0.8, c1=0.1, c2=0.5,
                 constraint_eq=tuple(), constraint_ueq=tuple(), verbose=False
                 , dim=None, optimization_target=None, export_result_dir=None,export_result_file_name=None,
                 hfss_Optimization_record_dir=None, hfss_Optimization_record_file_name=None):

        self.export_result_file_path = export_result_dir+'\\'+export_result_file_name # the path for those output results
        self.hfss_Optimization_record_file_path = hfss_Optimization_record_dir +'\\'+hfss_Optimization_record_file_name # the path for optimization record
        n_dim = n_dim or dim  # support the earlier version 
        print(optimization_target)
        file=open(self.hfss_Optimization_record_file_path,"a+")
        file.write(optimization_target)
        file.close() 
        self.export_result_dir = export_result_dir
        self.export_result_file_name = export_result_file_name
        self.hfss_Optimization_record_dir = hfss_Optimization_record_dir
        self.hfss_Optimization_record_file_name = hfss_Optimization_record_file_name

        self.Optimization_variables = Optimization_variables
#        self.func = func_transformer(func)
        self.w = w  # inertia
        self.cp, self.cg = c1, c2  # parameters to control personal best, global best respectively
        self.pop = pop  # number of particles
        self.n_dim = n_dim  # dimension of particles, which is the number of optimized variables
        self.max_iter = max_iter  # max iter
        self.verbose = verbose  # print the result of each iter or not

        self.lb, self.ub = np.array(lb) * np.ones(self.n_dim), np.array(ub) * np.ones(self.n_dim)
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


    def check_constraint(self, x):
        # gather all unequal constraint functions
        for constraint_func in self.constraint_ueq:
            if constraint_func(x) > 0:
                return False
        return True

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
            h = HFSS()
            h.init()
            for k in range (0,len(self.Optimization_variables)):
                variable=h.getVariablevalue(self.Optimization_variables[k])
                variable_value,variable_unit=h.convertVariabletovalueandunit(variable)
                h.changeVariablevalue(self.Optimization_variables[k], self.X[i,k], variable_unit)
            cost_function_value=costfunction(self.export_result_dir, self.export_result_file_name, self.export_result_file_path)
#           cost_function_value=9999   #for test
            self.Y[i,0]=cost_function_value
            print('The pop number is', i, ', parameter is',self.X[i], 'and cost function is', cost_function_value)
            pop_result='The pop number is'+ str(i) + ', parameter is' + str(self.X[i]) + 'and cost function is' + str(cost_function_value)
            file=open(self.hfss_Optimization_record_file_path,"a+")
            file.write(pop_result+"\n")
            file.close()
#            print('*** the value of cost function is', cost_function)
        print(self.Y,type(self.Y))
        file=open(self.hfss_Optimization_record_file_path,"a+")
        file.write('The cost result is'+ str(self.Y)+"\n")
        file.close()   
        return self.Y            


    def update_pbest(self):
        '''
        personal best
        :return:
        '''
        self.need_update = self.pbest_y > self.Y
        for idx, x in enumerate(self.X):
            if self.need_update[idx]:
                self.need_update[idx] = self.check_constraint(x)

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
            if self.verbose:
                print('Iter: {}, Best fit: {} at {}'.format(iter_num, self.gbest_y, self.gbest_x))

            self.gbest_y_hist.append(self.gbest_y)
        self.best_x, self.best_y = self.gbest_x, self.gbest_y
        return self.best_x, self.best_y

    fit = run

