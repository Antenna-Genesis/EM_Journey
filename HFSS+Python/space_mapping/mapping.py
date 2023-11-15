import numpy as np
import random
import Costfunction
from cmaes import CMA
import LHSampling
import time

def ParameterExtraction_CMAES(f0, lb, ub):
    def func(x):
        return abs(Costfunction.Evaluator_math(x) - f0)

    ansX_g = (lb + ub) / 2
    ansy_g = np.inf
    bb = np.array([list(lb), list(ub)]).T
    meanX = np.array([ansX_g])

    for meanx in meanX:
        optimizer = CMA(mean=meanx, sigma=(ub[0] - lb[0]) / 3, bounds=bb, population_size=10)
        ansX = (lb + ub) / 2
        ansy = np.inf
        for generation in range(100):
            solutions = []
            Xx = []
            Yy = []
            for _ in range(optimizer.population_size):
                x = optimizer.ask()
                y = func(x)

                Xx.append(np.array(x))
                Yy.append(np.array(y))
            Xx = np.array(Xx)
            Yy = np.array(Yy)

            if np.min(Yy) < ansy:
                ansX = Xx[np.argmin(Yy)]
                ansy = np.min(Yy)
            for _ in range(len(Xx)):
                solutions.append((Xx[_], Yy[_]))
            optimizer.tell(solutions)
            if optimizer.should_stop():
                break
            # print('-------------------GENERATION: ', generation,' BEST: ',ansy)
        if ansy < ansy_g:
            ansX_g = ansX
            ansy_g = ansy

    return ansX_g.round(2)

def Original_Space_Mapping(f0, n0, lb, ub, maxiter = 10):
    # f0: 需要谐振频率    n0: 初始化元素
    xcf0 = ParameterExtraction_CMAES(f0, lb, ub)
    qq = LHSampling.DoE_LHS(N=n0-1, bounds=np.array([list(lb), list(ub)]).T)
    xf0_ = np.array(qq.ParameterArray).round(2)

    xf0 = np.vstack((xcf0, xf0_))
    xc0 = np.zeros((len(xf0), len(lb)))
    for i in range(n0):
        Rf = Costfunction.Evaluator_hfss(xf0[i])
        xc0[i] = ParameterExtraction_CMAES(Rf, lb, ub)

    matrixE = xc0
    matrixD = np.hstack((np.ones((n0,1)), xf0))

    for i in range(maxiter):
        print("E: ", matrixE)
        print("D: ", matrixD)

        matrixA = (np.linalg.inv(matrixD.T @ matrixD) @ (matrixD.T @ matrixE)).T
        print("A: ", matrixA)
        ci = matrixA[:, 0]
        matrixBi = matrixA[:, 1:]

        xfi = np.clip(np.linalg.inv(matrixBi) @ (xcf0 - ci), lb, ub)
        Rfi = Costfunction.Evaluator_hfss(xfi)
        xci = ParameterExtraction_CMAES(Rfi, lb, ub)

        matrixE = np.vstack((matrixE, xci))
        matrixD = np.vstack((matrixD, np.append(1,xfi)))

def Aggressive_Space_Mapping(f0, lb, ub, maxiter = 5):
    # f0: 需要谐振频率
    xcf0 = ParameterExtraction_CMAES(f0, lb, ub)
    Rf0 = Costfunction.Evaluator_hfss(xcf0)
    xc0 = ParameterExtraction_CMAES(Rf0, lb, ub)
    fi = xc0 - xcf0
    print(fi)
    matrixB = np.identity(len(lb))

    xfi_ = xcf0
    for i in range(maxiter):
        print("B: ", matrixB)
        hi = - np.linalg.inv(matrixB) @ fi
        print("hi: ", hi)
        xfi = xfi_ + hi
        Rfi = Costfunction.Evaluator_hfss(xfi)
        xci = ParameterExtraction_CMAES(Rfi, lb, ub)
        fi = xci - xcf0
        print("fi: ", fi)
        matrixB = matrixB + fi @ hi.T / (hi.T @ hi)
        xfi_ = xfi

if __name__ == '__main__':
    Original_Space_Mapping(2.45, 3, np.array([35, 25]), np.array([45, 35]), 10)
    # Aggressive_Space_Mapping(2.45, np.array([35, 25]), np.array([45, 35]), 5)