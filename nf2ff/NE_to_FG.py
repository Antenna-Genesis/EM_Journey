import numpy as np
# import cmath
# import math
import plot3d
import seaborn
import matplotlib.pyplot as plt
import heat_plot
from scipy import integrate

# 传输常数
PLT_SHOW = plt.show()
f = 2.4e+9
# f = 7.5e10
k = 2 * np.pi * f / 3e8
# 每行采样点个数
sam_num = 15
# 空间的本征阻抗
Z_0 = 376.7

# def ne_to_fg(M, N, m, n, R, Sx, Sy, filename1, filename2):
#     # 读取E_meas
#     E_measx = np.load(filename1)
#     E_measy = np.load(filename2)
#     Ex = np.array(E_measx).reshape(M * N, 1)
#     Ey = np.array(E_measy).reshape(M * N, 1)
#     theta = np.linspace(0, np.pi, M * 5)
#     phi = np.linspace(0, 2 * np.pi, M * 5)
#     P_nearfield = 0.8898  # 近场功率
#     # 求远场功率，先求E，再使用波印廷矢量得到未归一化的P
#     # 求E
#     L_theda = np.zeros((theta.shape[0], theta.shape[0]), dtype=np.complex128)
#     L_phi = np.zeros((phi.shape[0], phi.shape[0]), dtype=np.complex128)
#     # 测量点中心坐标(-0.35+num%file_num*0.05,0.35+num//file_num*0.05,0.125)
#     # 由于距离十分远，故使用中心点(0,0,0)作为偶极子的位置
#     # 遍历theta和phi
#     for theda_ in range(theta.shape[0]):
#         for phi_ in range(phi.shape[0]):
#             # 遍历Ey
#             for every_Ey in range(M * N):
#                 # 测量点距离测量面中心的距离
#                 '''r_ = math.sqrt(
#                     (-Sx/2 + (every_Mx % file_num) * (Sx / (m - 1)) ** 2
#                      + (-Sy/2+ (every_Mx // file_num) * (Sy / (n - 1))) ** 2)'''

#                 # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi)
#                 r_cos = abs(-Sx / 2 + (every_Ey // N) * (Sx / (m - 1))) * np.sin(theta[theda_]) * np.cos(
#                     phi[phi_]) + abs(-Sy / 2 + (every_Ey % M) * (Sy / (n - 1))) * np.sin(theta[theda_]) \
#                         * np.sin(phi[phi_])
#                 # r_cos = abs(-Sx / 2 + (every_Ey % N) * (Sx / (m - 1))) * np.cos(phi[phi_]) * np.sin(theta[theda_]) +\
#                         #abs(-Sy / 2 + (every_Ey // M) * (Sy / (n - 1))) * np.cos(theta[theda_])
#                 L_theda[theda_][phi_] += 2 * (Ey[every_Ey] * np.cos(theta[theda_]) * math.cos(phi[phi_])
#                                           - Ex[every_Ey] * math.cos(theta[theda_]) * math.sin(phi[phi_])) \
#                                          * cmath.exp(1j * k * r_cos)
#                 L_phi[theda_][phi_] += 2 * (-Ey[every_Ey] * math.sin(phi[phi_])
#                                         - Ex[every_Ey] * math.cos(phi[phi_])) * cmath.exp(1j * k * r_cos)


#                 '''
#                 L_phi[theda_][phi_] += (-Mx[every_Mx] * math.sin(phi[phi_])
#                                         + My[every_Mx] * math.cos(phi[phi_])) * cmath.exp(1j * k * r_cos)
#                 '''
#     plt1 = plt.figure(1)
#     seaborn.heatmap(np.abs(L_theda))
#     # plt.show()
#     plt.figure(2)
#     seaborn.heatmap(np.abs(L_phi))
#     plt.show()

#     E_theda = -(1j * k * cmath.exp(-1j * k * R) / (4 * np.pi * R)) * L_phi
#     E_phi = (1j * k * cmath.exp(-1j * k * R) / (4 * np.pi * R)) * L_theda
#     # 求功率
#     P_AUT = (np.abs(E_theda) ** 2 + np.abs(E_phi) ** 2) / Z_0  # 波印廷矢量

#     # Gain = G = PAUT/P参考
#     P_ref = 10 * np.log10(P_nearfield / (4 * np.pi * R * R))
#     Gain = 10 * np.log10(np.abs(P_AUT)) - P_ref
#     return Gain


if __name__ == "__main__":
    # M采样面的长的点个数，N采样面的宽的点个数，m等效面的长的点个数
    # n等效面的宽的点个数，d近场距离等效面的距离
    # Sx等效面的长，Sy等效面的宽
    # filename1 储存Emeasx的文件，filename2 储存Emeasy的文件
    M = sam_num
    N = sam_num
    m = sam_num
    n = sam_num
    d = 0.625
    Sx = 0.7
    Sy = 0.7
    R = 1000
    filename1 = 'Emeasx625.npy'
    filename2 = 'Emeasy625.npy'
    # Gain = ne_to_fg(M, N, m, n, R, Sx, Sy, filename1, filename2)
    # # np.save('Gain.npy', Gain)
    # plot3d.plot_3D(Gain)

    E_measx = np.load(filename1)
    E_measy = np.load(filename2)
    Ex = np.array(E_measx).reshape(M, N)
    Ey = np.array(E_measy).reshape(M, N)
    theta = np.linspace(0, np.pi/2, M)
    phi = np.linspace(0, 2 * np.pi, M)
    P_nearfield = 0.8898  # 近场功率
    # 求远场功率，先求E，再使用波印廷矢量得到未归一化的P
    # 求E
    L_theda = np.zeros((theta.shape[0], theta.shape[0]), dtype=np.complex128)
    L_phi = np.zeros((phi.shape[0], phi.shape[0]), dtype=np.complex128)
    # 测量点中心坐标(-0.35+num%file_num*0.05,0.35+num//file_num*0.05,0.125)
    # 由于距离十分远，故使用中心点(0,0,0)作为偶极子的位置
    # 遍历theta和phi
    for theda_ in range(theta.shape[0]):
        for phi_ in range(phi.shape[0]):
            # 遍历Ey，固定x积分y
            for every_Ey in range(N):
                # 测量点距离测量面中心的距离
                '''r_ = math.sqrt(
                    (-Sx/2 + (every_Mx % file_num) * (Sx / (m - 1)) ** 2 
                     + (-Sy/2+ (every_Mx // file_num) * (Sy / (n - 1))) ** 2)'''
                # 遍历的x
                dx = np.arange(-Sx / 2, Sx / 2 + 1e-5, (Sx / (m - 1)))
                # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi)，是一个矩阵
                r_cos = (dx) * np.sin(theta[theda_]) * np.cos(phi[phi_]) + \
                        (-Sy / 2 + (every_Ey % M) * (Sy / (n - 1))) * np.sin(theta[theda_]) * np.sin(phi[phi_])
                # r_cos = abs(-Sx / 2 + (every_Ey % N) * (Sx / (m - 1))) * np.cos(phi[phi_]) * np.sin(theta[theda_]) +\
                # abs(-Sy / 2 + (every_Ey // M) * (Sy / (n - 1))) * np.cos(theta[theda_])
                '''
                L_theda[theda_][phi_] += 2 * (Ey[every_Ey] * np.cos(theta[theda_]) * np.cos(phi[phi_])
                                              - Ex[every_Ey] * np.cos(theta[theda_]) * np.sin(phi[phi_])) \
                                         * np.exp(1j * k * r_cos)
                L_phi[theda_][phi_] += 2 * (-Ey[every_Ey] * np.sin(phi[phi_])
                                            - Ex[every_Ey] * np.cos(phi[phi_])) * np.exp(1j * k * r_cos)
                '''
                L_theda[theda_][phi_] += 2 * integrate.trapz(
                    (Ey[:, every_Ey] * np.cos(theta[theda_]) * np.cos(phi[phi_])
                     - Ex[:, every_Ey] * np.cos(theta[theda_]) * np.sin(phi[phi_])) \
                    * np.exp(1j * k * r_cos), dx)
                L_phi[theda_][phi_] += 2 * integrate.trapz((-Ey[:, every_Ey] * np.sin(phi[phi_])
                                                            - Ex[:, every_Ey] * np.cos(phi[phi_])) * np.exp(
                    1j * k * r_cos), dx)
    # 固定y对x积分
    for theda_ in range(theta.shape[0]):
        for phi_ in range(phi.shape[0]):
            # 遍历Ey，固定x积分y
            for every_Ex in range(M):
                # 测量点距离测量面中心的距离
                '''r_ = math.sqrt(
                    (-Sx/2 + (every_Mx % file_num) * (Sx / (m - 1)) ** 2 
                     + (-Sy/2+ (every_Mx // file_num) * (Sy / (n - 1))) ** 2)'''
                # 遍历的x
                dy = np.arange(-Sy / 2, Sy / 2 + 1e-5, (Sy / (n - 1)))
                # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi)，是一个矩阵
                r_cos = (-Sx / 2 + (every_Ex // N) * (Sx / (m - 1))) * np.sin(theta[theda_]) * np.cos(phi[phi_]) + \
                        (dy) * np.sin(theta[theda_]) * np.sin(phi[phi_])
                # r_cos = abs(-Sx / 2 + (every_Ey % N) * (Sx / (m - 1))) * np.cos(phi[phi_]) * np.sin(theta[theda_]) +\
                # abs(-Sy / 2 + (every_Ey // M) * (Sy / (n - 1))) * np.cos(theta[theda_])
                L_theda[theda_][phi_] += 2 * integrate.trapz(
                    (Ey[every_Ex, :] * np.cos(theta[theda_]) * np.cos(phi[phi_])
                     - Ex[every_Ex, :] * np.cos(theta[theda_]) * np.sin(phi[phi_])) \
                    * np.exp(1j * k * r_cos), dy)
                L_phi[theda_][phi_] += 2 * integrate.trapz((-Ey[every_Ex, :] * np.sin(phi[phi_])
                                                            - Ex[every_Ex, :] * np.cos(phi[phi_])) * np.exp(
                    1j * k * r_cos), dy)
    # plt1 = plt.figure(1)
    # seaborn.heatmap(np.abs(L_theda))
    # plt.figure(2)
    # seaborn.heatmap(np.abs(L_phi))
    # plt.show()
    heat_plot.heat_plot(np.abs(L_theda), np.abs(L_phi), theta, phi, 'L_theda', 'L_phi', 'phi/deg', 'theta/deg')
    # plt.show()
    E_theda = -(1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_phi #* (Sx / (m - 1)) * (Sy / (n - 1))
    E_phi = (1j * k * np.exp(-1j * k * R) / (4 * np.pi * R)) * L_theda #* (Sx / (m - 1)) * (Sy / (n - 1))
    heat_plot.heat_plot(np.abs(E_theda), np.abs(E_phi), theta, phi, 'E_theda', 'E_phi', 'phi/deg', 'theta/deg')
    # 求功率
    P_AUT = (np.abs(E_theda) ** 2 + np.abs(E_phi) ** 2) / Z_0  # 波印廷矢量
    # heat_plot.heat_plot(np.abs(P_AUT), np.abs(E_phi), theta, phi, 'P_AUT', 'E_phi')
    # Gain = G = PAUT/P参考
    P_ref = 10 * np.log10(P_nearfield / (4 * np.pi * R * R))
    Gain = 10 * np.log10(np.abs(P_AUT)) - P_ref
    heat_plot.heat_plot(np.abs(P_AUT), Gain, theta, phi, 'P_AUT', 'Gain', 'phi/deg', 'theta/deg')
    np.save('Gain.npy', Gain)
    plt.show()
    # plot3d.plot_3D(Gain)
