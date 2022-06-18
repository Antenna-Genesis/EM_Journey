import Heat_Plot
import matplotlib.pyplot as plt
import numpy as np
import loadcsv


def nf_test(Ex, Ey, M, S):
    """
    得到近场Delta_E_Total = Max(E_total on plane) - Max(E_total on edges)
    看是否符合<20dB的条件并画出电场场分布图
    :param Ex: 储存Ex的array
    :param Ey: 储存Ey的array
    :param M: 数据矩阵的行数
    :param S: 测量面的长和宽
    :return: None
    """
    x_ = np.arange(-S/2, S/2 + 1e-5, S/(M-1))
    y_ = x_

    Heat_Plot.heat_plot([20 * np.log10(abs(Ex)), 20 * np.log10(abs(Ey)),
                        20 * np.log10(np.sqrt(abs(Ex) ** 2 + abs(Ey) ** 2))], x_, y_,
                        ['E_x(dB)', 'E_y(dB)', 'E_total(dB)'], 'x(mm)', 'y(mm)', 3, 'N')
    E_to = 20 * np.log10(np.sqrt(abs(Ex) ** 2 + abs(Ey) ** 2))
    # 取最外层一圈上的电场
    E1 = E_to[0][:]
    E2 = E_to[M - 1][:]
    E3 = E_to[:][0]
    E4 = E_to[:][M - 1]
    a1 = np.max(E1)
    a2 = np.max(E2)
    a3 = np.max(E3)
    a4 = np.max(E4)
    print('Delta_E_Total:', np.max(E_to) - max(a1, a2, a3, a4), 'dB')
    # plt.show()
