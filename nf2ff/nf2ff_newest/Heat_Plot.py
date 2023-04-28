import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def heat_plot(Gain, x_, y_, title, x_label, y_label, num, change='Y'):
    """
    将得到的数据用热图画出来，图像个数可选
    :param Gain: 列表，需要用热图展示的数据
    :param x_: x轴坐标
    :param y_: y轴坐标
    :param title: 数据图标题列表
    :param x_label: x轴标签
    :param y_label: y轴标签
    :param num: 数据图个数
    :param change: xy坐标是否需要转化成角度
    :return: None
    """
    # 是否需要从弧度转化成角度
    if change == 'Y':
        x_ = np.around(x_ * 180 / np.pi, 1)
        y_ = np.around(y_ * 180 / np.pi, 1)
    x_ = np.around(x_, 1)
    y_ = np.around(y_, 1)
    fig, ax = plt.subplots(1, num)
    ax = ax.flatten()
    im = [0 for x in range(0, num)]
    for i in range(num):
        im[i] = ax[i].imshow(Gain[i])
    # 这里是修改标签
    for i in range(num):
        ax[i].set_xticks(np.arange(len(y_)))
        ax[i].set_yticks(np.arange(len(x_)))
    # ... and label them with the respective list entries
    for i in range(num):
        ax[i].set_xticklabels(y_)
        ax[i].set_yticklabels(x_)
    # 因为x轴的标签太长了，需要旋转一下，更加好看
    # Rotate the tick labels and set their alignment.
    for i in range(num):
        plt.setp(ax[i].get_xticklabels(), rotation=45, ha="right",
                 rotation_mode="anchor")
    # 加标题
    for i in range(num):
        ax[i].set_title(title[i], fontsize=16)
    fig.tight_layout()
    # 加colorbar
    for i in range(num):
        fig.colorbar(im[i], ax=ax[i], fraction=0.05)
    # 加xy轴标签
    for i in range(num):
        ax[i].set_xlabel(x_label, fontsize=16)
        ax[i].set_ylabel(y_label, fontsize=16)
    # plt.show()
