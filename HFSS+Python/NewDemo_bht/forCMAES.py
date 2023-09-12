
from base import SkoBase
from HFSS import HFSS
import numpy as np
from Costfunction import costfunction
from cmaes import CMA

def CMAES(func,  lb, ub , population_size= 10, max_iter=50):
    # 库解释 https://pypi.org/project/cmaes/
    bb = np.array([list(lb), list(ub)]).T
    optimizer = CMA(mean=(lb+ub)/2, sigma=(ub[0] - lb[0]) / 5, bounds=bb, population_size = population_size)
    ansX = (lb + ub) / 2
    ansy = np.inf
    for generation in range(max_iter):
        solutions = []
        for _ in range(optimizer.population_size):
            x = optimizer.ask()
            y = func(x)
            if y<ansy:
                ansy=y
                ansX=x
            solutions.append((x, y))
        optimizer.tell(solutions)
        print('Generation: {}, Best fit: {} at {}'.format(generation, ansy, ansX))
        if optimizer.should_stop():
            break
    return ansX, ansy

if __name__ == '__main__':
    xbest,ybest = CMAES(func=costfunction,
              lb=[8, 16, 4], ub=[12, 24, 14],
              population_size=10, max_iter=50 )
    print(xbest,ybest)