import random
import numpy as np
import math

# 数学基准测试函数介绍网站： https://www.sfu.ca/~ssurjano/index.html
# 其中第三个测试函数DixonPrice是一个测试跳出鞍点的函数，建议在小维度下设置。
# 几乎所有资料都是错的，DixonPrice并不是单峰函数，这能很轻易证明。如果您有异议并证实你正确，本人愿意组会表演钻桌底。

def CostfuncMath1_Ackley(X):
    K=len(X)
    c=20
    sum1=0; sum2=0
    for i in range(K):
        sum1=sum1+X[i]*X[i]
        sum2=sum2+math.cos(2*math.pi*X[i])
    anss=-c*math.exp(-0.2*math.sqrt(sum1/K))-math.exp(sum2/K)+c+math.exp(1)
    return anss

def CostfuncMath2_Ellipsoid(X):
    K=len(X)
    anss=0
    for i in range(K):
        anss=anss+(i+1)*X[i]*X[i]
    return anss

def CostfuncMath3_DixonPrice(X):
    K = len(X)
    ans0 = (X[0]-1)**2
    for i in range(1,K):
        ans0 = ans0+(i+1)*(2*X[i]**2-X[i-1])**2
    return ans0

def CostfuncMath4_Levy(X):
    sum1=0
    sf = 1
    K = len(X)
    w1 = 1 + (X[0]-1)/4
    wk = 1 + (X[K-1] - 1) / 4
    for i in range(K):
        wi=1+(X[i]-1)/4
        sum1=sum1+(wi-1)**2*(1+10*(math.sin(sf*math.pi*wi+1))**2)
    anss=(math.sin(sf*math.pi*w1))**2 + sum1 + (wk-1)**2*(1+(math.sin(2*sf*math.pi*w1))**2)
    return anss

def CostfuncMath5_StyblinskiTang(X):
    K = len(X)
    anss = 0
    for i in range(K):
        anss = anss+0.5*(X[i]**4-16*X[i]**2+5*X[i])
    return anss

if __name__ == "__main__":
    dimm = 5
    rangee = 3
    lb_test = -np.ones(dimm) * rangee
    ub_test = np.ones(dimm) * rangee

    Optimization_variables = np.array(['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8', 'x9','x10'])
    Opv=Optimization_variables[:dimm]

    from forSADEA import forSADEA
    from PBO_q import PBO_q
    from PSO import PSO
    from forCMAES import CMAES
    choose_algorithm = 'CMAES'

    if choose_algorithm == 'PSO':
        Optimization_variables = 'DR_radius', 'DR_height', 'Monopole_height'
        pso = PSO(Optimization_variables=Opv, costfunc=CostfuncMath1_Ackley,
                  n_dim=dimm, pop=30, max_iter=100,
                  lb=lb_test, ub=ub_test, w=0.8, c1=0.5, c2=0.5, )
        hj, kl = pso.run()
        print(hj, kl)

    if choose_algorithm == 'SADEA':
        sy1 = forSADEA(Opv, CostfuncMath1_Ackley,
                       n_dim=dimm, initpop=100, tau=100, lamda=50, max_iter=2000,
                       lb=lb_test, ub=ub_test, accu=3)
        hj, kl = sy1.run()
        print(hj, kl)

    if choose_algorithm == 'PBO':
        sy1 = PBO_q(Optimization_variables=Opv, costfunc=CostfuncMath1_Ackley,
                    n_dim=dimm, initpop=30, max_iter=200,
                    lb=lb_test, ub=ub_test, accu=3, q=np.array([0, 1, 0])) #推荐LCB,更易于辅助寻优
        hj, kl = sy1.run()
        print(hj, kl)

    if choose_algorithm == 'CMAES':
        xbest, ybest = CMAES(func=CostfuncMath1_Ackley,
                             lb=lb_test, ub=ub_test,
                             population_size=10, max_iter=50)
        print(xbest, ybest)