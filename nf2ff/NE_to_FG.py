import numpy as np
import cmath
import plot3d

# 传输常数
f = 2.4e+9
# f = 7.5e10
k = 2 * np.pi * f / 3e8
# 每行采样点个数
sam_num=15
# 空间的本征阻抗
Z_0 = 376.7


def ne_to_fg(M, N, m, n, R, Sx, Sy, filename1, filename2):
    # 读取E_meas
    E_measx = np.load(filename1)
    E_measy = np.load(filename2)
    E_measx = np.array(E_measx).reshape(M * N, 1)
    E_measy = np.array(E_measy).reshape(M * N, 1)
    theta = np.linspace(0, np.pi, M * 5)
    phi = np.linspace(0, 2 * np.pi, M * 5)
    P_nearfield = 0.8898  # 近场功率
    # 求远场功率，先求E，再使用波印廷矢量得到未归一化的P
    # 求E
    F_theda = np.zeros((theta.shape[0], theta.shape[0]), dtype=np.complex128)
    # L_phi = np.zeros((phi.shape[0], phi.shape[0]), dtype=np.complex128)
    # 测量点中心坐标(-0.35+num%file_num*0.05,0.35+num//file_num*0.05,0.125)
    # 由于距离十分远，故使用中心点(0,0,0)作为偶极子的位置
    # 遍历theta和phi
    for theda_ in range(theta.shape[0]):
        for phi_ in range(phi.shape[0]):
            # 遍历Ey
            for every_Ey in range(M * N):
                # 测量点距离测量面中心的距离
                '''r_ = math.sqrt(
                    (-Sx/2 + (every_Mx % file_num) * (Sx / (m - 1)) ** 2 
                     + (-Sy/2+ (every_Mx // file_num) * (Sy / (n - 1))) ** 2)'''
                # 注：cos(90-theta)=sin(theta)
                # r_*cos(p)=x_*sin(theta)*cos(phi)+y_*sin(theta)sin(phi)
                r_cos = abs(-Sx / 2 + (every_Ey // N) * (Sx / (m - 1))) * np.sin(theta[theda_]) * np.cos(
                    phi[phi_]) + abs(-Sy / 2 + (every_Ey % M) * (Sy / (n - 1))) * np.sin(theta[theda_]) \
                        * np.sin(phi[phi_])
                # r_cos = abs(-Sx / 2 + (every_Ey % N) * (Sx / (m - 1))) * np.cos(phi[phi_]) * np.sin(theta[theda_]) +\
                        #abs(-Sy / 2 + (every_Ey // M) * (Sy / (n - 1))) * np.cos(theta[theda_])
                F_theda[theda_][phi_] += np.sin(theta[theda_]) / (2 * np.pi * R) * cmath.exp(-1j * k * R) * cmath.exp(
                    -1j * k * r_cos) * E_measy[every_Ey]
                '''
                L_phi[theda_][phi_] += (-Mx[every_Mx] * math.sin(phi[phi_])
                                        + My[every_Mx] * math.cos(phi[phi_])) * cmath.exp(1j * k * r_cos)
                '''
    E_theda = 0
    E_phi = 1j * k * F_theda
    # 求功率
    P_AUT = (np.abs(E_theda) ** 2 + np.abs(E_phi) ** 2) / Z_0  # 波印廷矢量

    # Gain = G = PAUT/P参考
    P_ref = 10 * np.log10(P_nearfield / (4 * np.pi * R * R))
    Gain = 10 * np.log10(np.abs(P_AUT) + 1e-5) - P_ref
    return Gain


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
    R = 10000
    filename1 = 'Emeasx625.npy'
    filename2 = 'Emeasy625.npy'
    Gain = ne_to_fg(M, N, m, n, R, Sx, Sy, filename1, filename2)
    # np.save('Gain.npy', Gain)
    plot3d.plot_3D(Gain)
