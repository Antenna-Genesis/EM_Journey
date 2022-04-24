import numpy as np
import matplotlib.pyplot as plt
import Heat_Plot
from scipy import integrate
import loadcsv
import NF_Test

# 传输常数
f = 2.4e+9
# f = 7.5e10
k = 2 * np.pi * f / 3e8
# 空间的本征阻抗
Z_0 = 376.7
# 误差数据
e = 1e-5


def sphere_gain(filename1, filename2, d, sam_num, Sx, Sy, csv_type='E'):
    """
    计算天线远场球面任意一点的增益
    :param filename1: 存储Ex或者SX21的文件
    :param filename2: 存储Ey或者SY21的文件
    :param d: 近场测量面离口径面的距离
    :param sam_num: 采样点个数
    :param Sx: 测量面的长
    :param Sy: 测量面的宽
    :param csv_type: csv文件的类型
    :return:天线在远场的总增益GainTotal，Theta角增益GainTheta，Phi角增益GainPhi
    """
    Sx_sam = sam_num
    Sy_sam = sam_num
    # d = 0.125
    # Sx = 0.9
    # Sy = 0.9
    R = 100000  # 远场距离
    if csv_type == 'E':
        Ex = loadcsv.load(filename1)
        Ey = loadcsv.load(filename2)
        # E_measz = loadcsv.load(filename3)
        Ex = np.array(Ex).reshape(Sx_sam, Sy_sam)
        Ey = np.array(Ey).reshape(Sx_sam, Sy_sam)
        # Ez = np.array(E_measz).reshape(M, N)
    else:
        S21x = loadcsv.load_s21(filename1)
        S21y = loadcsv.load_s21(filename2)
        S21x = np.array(S21x).reshape(Sx_sam, Sy_sam)
        S21y = np.array(S21y).reshape(Sx_sam, Sy_sam)
        # 由偶极子有效口径可以求得测量面上的电场分布
        S = (Sx / (Sx_sam - 1)) * (Sy / (Sy_sam - 1))
        Ex = sqrt(1 / (0.13 * 0.1 * 0.1) * S21x * S * Z_0)
        Ey = sqrt(1 / (0.13 * 0.1 * 0.1) * S21y * S * Z_0)
    # 得到的近场进行衡量是否适合近远场变换
    NF_Test.nf_test(Ex, Ey, Sx_sam, Sx)
    theta = np.linspace(0, np.pi / 2, 16)
    phi = np.linspace(0, 2 * np.pi, 16)
    # P_nearfield = 1.2  # 近场功率
    P_nearfield = 0
    for i in range(Sx_sam):
        for j in range(Sy_sam):
            P_nearfield += (np.abs(Ex[i][j]) ** 2 + np.abs(Ey[i][j]) ** 2) / Z_0 * (Sx / (Sx_sam - 1)) * (
                    Sy / (Sy_sam - 1))
    # 求远场功率，先求E，再使用波印廷矢量得到未归一化的P
    # 求E
    L_theda = np.zeros((theta.shape[0], theta.shape[0]), dtype=np.complex128)
    L_phi = np.zeros((phi.shape[0], phi.shape[0]), dtype=np.complex128)
    # 测量点中心坐标(-0.35+num%file_num*0.05,0.35+num//file_num*0.05,0.125)
    # 由于距离十分远，故使用中心点(0,0,0)作为偶极子的位置
    # 遍历theta和phi
    # 实现Balanis(12-12c)和(12-12d)
    for theda_ in range(theta.shape[0]):
        for phi_ in range(phi.shape[0]):
            # 建立一个矩阵储存第一次分部积分的结果
            E_intTheta = np.linspace(1j, 1j, Sx_sam)
            E_intPhi = np.linspace(1j, 1j, Sx_sam)
            # 遍历Ey，固定x积分y
            # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi) ,对于每一个theta和phi建立一个矩阵
            r_cos = np.zeros((Sx_sam, Sy_sam), dtype=np.complex128)
            for row_ in range(Sx_sam):
                for col_ in range(Sy_sam):
                    r_cos[row_][col_] = (-Sx / 2 + row_ * (Sx / (Sx_sam - 1))) * np.sin(theta[theda_]) * np.cos(
                        phi[phi_]) + (-Sy / 2 + col_ * (Sy / (Sy_sam - 1))) * np.sin(theta[theda_]) \
                                        * np.sin(phi[phi_])
            for every_Ey in range(Sy_sam):
                # 遍历的x
                dx = np.arange(-Sx / 2, Sx / 2 + 1e-5, (Sx / (Sx_sam - 1)))
                E_intTheta[every_Ey] = 2 * integrate.trapz(
                    (Ey[:, every_Ey] * np.cos(theta[theda_]) * np.cos(phi[phi_])
                     - Ex[:, every_Ey] * np.cos(theta[theda_]) * np.sin(phi[phi_]))
                    * np.exp(1j * k * r_cos[:, every_Ey]), dx)
                E_intPhi[every_Ey] = 2 * integrate.trapz((-Ey[:, every_Ey] * np.sin(phi[phi_])
                                                          - Ex[:, every_Ey] * np.cos(phi[phi_])) * np.exp(
                    1j * k * r_cos[:, every_Ey]), dx)

            dy = np.arange(-Sy / 2, Sy / 2 + 1e-5, (Sy / (Sy_sam - 1)))
            L_theda[theda_][phi_] = integrate.trapz(E_intTheta, dy)
            L_phi[theda_][phi_] = integrate.trapz(E_intPhi, dy)

    Heat_Plot.heat_plot([np.abs(L_theda), np.abs(L_phi)], theta, phi, ['L_theda', 'L_phi'], 'φ(deg)', 'θ(deg)', 2)
    # plt.show()
    E_theda = -(1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_phi
    E_phi = (1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_theda
    Heat_Plot.heat_plot([np.abs(E_theda), np.abs(E_phi)], theta, phi, ['E_theda', 'E_phi'], 'φ(deg)', 'θ(deg)', 2)
    # 求功率
    P_AUT = (np.abs(E_theda) ** 2 + np.abs(E_phi) ** 2) / Z_0  # 波印廷矢量
    P_theta_AUT = np.abs(E_theda) ** 2 / Z_0
    P_phi_AUT = np.abs(E_phi) ** 2 / Z_0
    # heat_plot.heat_plot(np.abs(P_AUT), np.abs(E_phi), theta, phi, 'P_AUT', 'E_phi')
    # Gain = G = P_AUT/P参考
    P_ref = 10 * np.log10(P_nearfield / (4 * np.pi * R * R))
    Gain = 10 * np.log10(np.abs(P_AUT)) - P_ref
    Gain_theta = 10 * np.log10(np.abs(P_theta_AUT)) - P_ref
    Gain_phi = 10 * np.log10(np.abs(P_phi_AUT)) - P_ref
    # print(Gain[:, 7])
    Heat_Plot.heat_plot([np.abs(P_AUT), np.abs(P_theta_AUT), np.abs(P_phi_AUT)],
                        theta, phi, ['P_AUT(W)', 'P_theta_AUT(W)', 'P_phi_AUT(W)'], 'φ(deg)', 'θ(deg)', 3)
    # np.save('Gain.npy', Gain)
    np.savetxt('Gain' + str(d) + '.csv', Gain)
    # print('最大增益：', np.max(Gain))
    # plt.show()
    # print(Gain[:, 40])
    return Gain, Gain_theta, Gain_phi
    # plot3d.plot_3D(Gain)
