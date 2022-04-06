import numpy as np

def load(filename):
    # filename = 'Ex.csv'  # csv数据为复数
    temp = np.genfromtxt(filename, delimiter=',', dtype='str')
    mapping = np.vectorize(lambda t: complex(t.replace('i', 'j')))
    p1 = mapping(temp)
    return p1
