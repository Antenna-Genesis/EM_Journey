import random
import numpy as np
import math

def CostfuncMath1_Ackley(Opv,X):
    K=len(X)
    c=20
    sum1=0; sum2=0
    for i in range(K):
        sum1=sum1+X[i]*X[i]
        sum2=sum2+math.cos(2*math.pi*X[i])
    anss=-c*math.exp(-0.2*math.sqrt(sum1/K))-math.exp(sum2/K)+c+math.exp(1)
    return anss

def CostfuncMath2_Ellipsoid(Opv,X):
    K=len(X)
    anss=0
    for i in range(K):
        anss=anss+(i+1)*X[i]*X[i]
    return anss

if __name__ == "__main__":
    dimm = 10
    rangee = 30
    Optimization_variables = np.array(['x1', 'x2', 'x3','x4', 'x5', 'x6','x7', 'x8', 'x9','x10'])
    Opv=Optimization_variables[:dimm]

    from forSADEA import forSADEA

    sy1 = forSADEA(Opv, CostfuncMath1_Ackley,
                   n_dim=dimm, initpop=100, tau=100, lamda=50, max_iter=2000,
                   lb=-np.ones(dimm)*rangee, ub=np.ones(dimm)*rangee, accu=3)
    hj, kl = sy1.run()
    print(hj, kl)

    from PBO_q import PBO_q

    sy1 = PBO_q(Optimization_variables=Optimization_variables, costfunc=CostfuncMath1_Ackley,
                n_dim=dimm, initpop=30, max_iter=200,
                lb=-np.ones(dimm) * rangee, ub=np.ones(dimm) * rangee, accu=3, q=np.array([1, 0, 0]))
    hj, kl = sy1.run()
    print(hj, kl)