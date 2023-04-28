import numpy as np


def load(filename):
    """
    读取具有复数的csv文件并输出numpy数组
    :param filename: 需要读取的csv文件
    :return: numpy array
    """
    temp = np.genfromtxt(filename, delimiter=',', dtype='str')
    mapping = np.vectorize(lambda t: complex(t.replace('i', 'j')))
    p1 = mapping(temp)
    return p1


def load_s21(filename):
    """
    读取具有复数的csv文件并输出numpy数组，此时csv文件是numpy复数数组直接保存的
    :param filename: 需要读取的csv文件
    :return: numpy array
    """
    p1 = np.loadtxt(filename).view(complex).reshape(-1)
    return p1

