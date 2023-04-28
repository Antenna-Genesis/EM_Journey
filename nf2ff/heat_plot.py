import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def heat_plot(Gain1, Gain2, x_, y_, title1, title2, x_label, y_label):
    # x轴范围，y轴范围，标题
    # 这里是创建一个数据

    """x_ = np.around(np.arange(x1,x2,xinterval), 2)
    y_ = np.around(np.arange(y1,y2,yinterval), 2)"""

    x_ = np.around(x_ * 180 / np.pi, 1)
    y_ = np.around(y_ * 180 / np.pi, 1)
    fig, ax = plt.subplots(1, 2)
    ax = ax.flatten()
    im1 = ax[0].imshow(Gain1)
    im2 = ax[1].imshow(Gain2)
    # 这里是修改标签
    # We want to show all ticks...
    ax[0].set_xticks(np.arange(len(y_)))
    ax[0].set_yticks(np.arange(len(x_)))
    ax[1].set_xticks(np.arange(len(y_)))
    ax[1].set_yticks(np.arange(len(x_)))
    # ... and label them with the respective list entries
    ax[0].set_xticklabels(y_)
    ax[0].set_yticklabels(x_)
    ax[1].set_xticklabels(y_)
    ax[1].set_yticklabels(x_)
    # 因为x轴的标签太长了，需要旋转一下，更加好看
    # Rotate the tick labels and set their alignment.
    plt.setp(ax[0].get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.setp(ax[1].get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # 添加每个热力块的具体数值
    # Loop over data dimensions and create text annotations.
    ''' for i in range(len(x_)):
        for j in range(len(y_)):
            text = ax.text(j, i, Gain[i, j],
                           ha="center", va="center", color="w")'''
    ax[0].set_title(title1)
    ax[1].set_title(title2)
    fig.tight_layout()
    fig.colorbar(im1, ax = ax[0])
    fig.colorbar(im2, ax = ax[1])
    ax[0].set_xlabel(x_label)
    ax[1].set_xlabel(x_label)
    ax[0].set_ylabel(y_label)
    ax[1].set_ylabel(y_label)
    # plt.show()
