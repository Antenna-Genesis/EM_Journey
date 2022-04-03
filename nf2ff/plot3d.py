import numpy as np
from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import seaborn


def plot_3D(Gain):
    phi = np.linspace(0, 2 * np.pi, Gain.shape[0])
    theta = np.linspace(0, np.pi, Gain.shape[0])
    x = Gain * np.outer(np.cos(phi), np.sin(theta))
    y = Gain * np.outer(np.sin(phi), np.sin(theta))
    z = Gain * np.outer(np.ones(np.size(phi)), np.cos(theta))
    # plot
    fig1 = plt.figure()
    ax = fig1.gca(projection='3d')
    #
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
    ax.contour(x, y, z, zdim='z', offset=-2, cmap='rainbow')
    #ax.set_xlim(-70, 70)
    #ax.set_ylim(-70, 70)
    ax.set_title('Gain Plot (3D Polar Plot)')
    ax.set_xlabel('Theda')
    ax.set_ylabel('Phi')
    ax.set_zlabel('Gain')
    fig1.colorbar(surf, shrink=0.5, aspect=5)


    # 另外画一个
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta_another = np.linspace(0, np.pi, Gain.shape[0])
    phi_another = np.linspace(0, 2 * np.pi, Gain.shape[0])
    theta_another, phi_another = np.meshgrid(theta_another, phi_another)
    surf = ax.plot_surface(theta_another, phi_another, Gain, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)
    # 设置xy坐标的范围
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, 2 * np.pi)
    ax.set_title('Gain Plot (3D Rectangular Plot)')
    ax.set_xlabel('Theda')
    ax.set_ylabel('Phi')
    ax.set_zlabel('Gain')
    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.figure()
    plt.contourf(x, y, z, cmap=plt.cm.hot)
    plt.show()