import csv
import matplotlib.pyplot as plt
import numpy as np
import Heat_Plot
from numpy import unravel_index


def ff_compare(Gain, Gain_theta, Gain_phi, M, Gain_hfss_f, Gain_theta_hfss_f, Gain_phi_hfss_f):
    """
    将求得的远场和HFSS导出的远场进行比较
    :param Gain: 计算得到的远场增益array
    :param Gain_theta: 计算得到的远场在theta角的增益array
    :param Gain_phi: 计算得到的远场在phi角的增益array
    :param M: 维数
    :param Gain_hfss_f: 仿真得到的远场增益file
    :param Gain_theta_hfss_f: 仿真得到的远场在theta角的增益file
    :param Gain_phi_hfss_f: 仿真得到的远场在phi角的增益file
    :return:
    """
    with open(Gain_hfss_f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [float(row['dB(GainTotal)']) for row in reader]
    Gain_hfss = np.array(column)
    with open(Gain_theta_hfss_f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [float(row['dB(GainTheta)']) for row in reader]
    Gain_theta_hfss = np.array(column)
    with open(Gain_phi_hfss_f, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [float(row['dB(GainPhi)']) for row in reader]
    Gain_phi_hfss = np.array(column)
    # 转化为M*M的矩阵
    Gain_hfss = np.array(Gain_hfss).reshape(M, M)
    Gain_phi_hfss = np.array(Gain_phi_hfss).reshape(M, M)
    Gain_theta_hfss = np.array(Gain_theta_hfss).reshape(M, M)
    # print('phi=180deg时的增益', Gain1[:, 7])
    Gain_p = abs(Gain_hfss - Gain)
    dataset = Gain_p[:int((M-1)/3), :]
    # print(dataset)
    print('计算得到的远场最大增益：', np.max(Gain), 'dB')
    print('仿真得到的远场最大增益：', np.max(Gain_hfss), 'dB')
    # print((np.min(Gain1)))
    print('|Delta_Gain_Max|:', abs(np.max(Gain) - np.max(Gain_hfss)), 'dB')
    print('Theta<30deg时增益的最大差距：', np.max(dataset), 'dB')
    print('增益最大差距点所在的位置：', unravel_index(dataset.argmax(), dataset.shape))
    theta = np.linspace(0, np.pi / 2, M)
    phi = np.linspace(0, 2 * np.pi, M)
    # Gain=np.abs(Gain)
    Heat_Plot.heat_plot([Gain, Gain_hfss, Gain_p], theta, phi,
                        ['Calculation(dBi)', 'Simulation(dBi)', 'Gain_Gap(dB)'], 'φ', 'θ', 3)
    Heat_Plot.heat_plot([Gain_phi, Gain_phi_hfss, Gain_phi - Gain_phi_hfss], theta, phi,
                        ['Calculation(dBi)', 'Simulation(dBi)', 'Gain_phi_Gap(dB)'], 'φ', 'θ', 3)
    Heat_Plot.heat_plot([Gain_theta, Gain_theta_hfss, Gain_theta - Gain_theta_hfss], theta, phi,
                        ['Calculation(dBi)', 'Simulation(dBi)', 'Gain_theta_Gap(dB)'], 'φ',
                        'θ', 3)
    # plt.show()
