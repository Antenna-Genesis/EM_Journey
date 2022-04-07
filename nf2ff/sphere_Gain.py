import numpy as np
# import cmath
# import math
import plot3d
import seaborn
import matplotlib.pyplot as plt
import heat_plot
from scipy import integrate
import loadcsv

# 传输常数
PLT_SHOW = plt.show()
f = 2.4e+9
# f = 7.5e10
k = 2 * np.pi * f / 3e8
# 每行采样点个数
sam_num = 16
# 空间的本征阻抗
Z_0 = 376.7

if __name__ == "__main__":
    # M采样面的长的点个数，N采样面的宽的点个数，m等效面的长的点个数
    # n等效面的宽的点个数，d近场距离等效面的距离
    # Sx等效面的长，Sy等效面的宽
    # filename1 储存Emeasx的文件，filename2 储存Emeasy的文件
    M = sam_num
    N = sam_num
    m = sam_num
    n = sam_num
    d = 0.025
    Sx = 0.9
    Sy = 0.9
    R = 100000
    filename1 = 'Ex.csv'
    filename2 = 'Ey.csv'
    filename3 = 'Ez.csv'
    # Gain = ne_to_fg(M, N, m, n, R, Sx, Sy, filename1, filename2)
    # # np.save('Gain.npy', Gain)
    # plot3d.plot_3D(Gain)

    E_measx = loadcsv.load(filename1)
    E_measy = loadcsv.load(filename2)
    E_measz = loadcsv.load(filename3)
    # E_measx = np.load('Emeasx50.npy')
    # E_measy = np.load('Emeasy50.npy')
    Ex = np.array(E_measx).reshape(M, N)
    Ey = np.array(E_measy).reshape(M, N)
    # Ez = np.array(E_measz).reshape(M, N)
    theta = np.linspace(0, np.pi / 2, M)
    phi = np.linspace(0, 2 * np.pi, M)
    # P_nearfield = 1.2  # 近场功率
    P_nearfield = 0
    for i in range(M):
        for j in range(N):
            P_nearfield += (np.abs(Ex[i][j]) ** 2 + np.abs(Ey[i][j]) ** 2) / Z_0 * (Sx / (m - 1)) * (Sy / (n - 1))
    # 求远场功率，先求E，再使用波印廷矢量得到未归一化的P
    # 求E
    L_theda = np.zeros((theta.shape[0], theta.shape[0]), dtype=np.complex128)
    L_phi = np.zeros((phi.shape[0], phi.shape[0]), dtype=np.complex128)
    # 测量点中心坐标(-0.35+num%file_num*0.05,0.35+num//file_num*0.05,0.125)
    # 由于距离十分远，故使用中心点(0,0,0)作为偶极子的位置
    # 遍历theta和phi
    for theda_ in range(theta.shape[0]):
        for phi_ in range(phi.shape[0]):
            # 建立一个矩阵储存第一次分部积分的结果
            E_intTheta = np.linspace(1j, 1j, M)
            E_intPhi = np.linspace(1j, 1j, M)
            # 遍历Ey，固定x积分y
            # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi) ,对于每一个theta和phi建立一个矩阵
            r_cos = np.zeros((M, N), dtype=np.complex128)
            for row_ in range(M):
                for col_ in range(N):
                    r_cos[row_][col_] = (-Sx / 2 + row_ * (Sx / (m - 1))) * np.sin(theta[theda_]) * np.cos(
                        phi[phi_]) + (-Sy / 2 + col_ * (Sy / (n - 1))) * np.sin(theta[theda_]) \
                                        * np.sin(phi[phi_])
            for every_Ey in range(N):
                # 遍历的x
                dx = np.arange(-Sx / 2, Sx / 2 + 1e-5, (Sx / (m - 1)))
                E_intTheta[every_Ey] = 2 * integrate.trapz(
                    (Ey[:, every_Ey] * np.cos(theta[theda_]) * np.cos(phi[phi_])
                     - Ex[:, every_Ey] * np.cos(theta[theda_]) * np.sin(phi[phi_])) \
                    * np.exp(1j * k * r_cos[:, every_Ey]), dx)
                E_intPhi[every_Ey] = 2 * integrate.trapz((-Ey[:, every_Ey] * np.sin(phi[phi_])
                                                            - Ex[:, every_Ey] * np.cos(phi[phi_])) * np.exp(
                    1j * k * r_cos[:, every_Ey]), dx)

            dy = np.arange(-Sy / 2, Sy / 2 + 1e-5, (Sy / (n - 1)))
            L_theda[theda_][phi_] = integrate.trapz(E_intTheta, dy)
            L_phi[theda_][phi_] = integrate.trapz(E_intPhi, dy)

    heat_plot.heat_plot(np.abs(L_theda), np.abs(L_phi), theta, phi, 'L_theda', 'L_phi', 'phi/deg', 'theta/deg')
    # plt.show()
    E_theda = -(1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_phi
    E_phi = (1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_theda
    heat_plot.heat_plot(np.abs(E_theda), np.abs(E_phi), theta, phi, 'E_theda', 'E_phi', 'phi/deg', 'theta/deg')
    # 求功率
    P_AUT = (np.abs(E_theda) ** 2 + np.abs(E_phi) ** 2) / Z_0  # 波印廷矢量
    # heat_plot.heat_plot(np.abs(P_AUT), np.abs(E_phi), theta, phi, 'P_AUT', 'E_phi')
    # Gain = G = PAUT/P参考
    P_ref = 10 * np.log10(P_nearfield / (4 * np.pi * R * R))
    Gain = 10 * np.log10(np.abs(P_AUT)) - P_ref
    #print(Gain[:, 7])
    heat_plot.heat_plot(np.abs(P_AUT), Gain, theta, phi, 'P_AUT', 'Gain', 'phi/deg', 'theta/deg')
    np.save('Gain.npy', Gain)
    np.savetxt('Gain.csv', Gain)
    print('最大增益：', np.max(Gain))
    plt.show()
    # plot3d.plot_3D(Gain)
