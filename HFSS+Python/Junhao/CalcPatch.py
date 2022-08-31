# -*- coding: utf-8 -*-
import math
import numpy as np
from scipy import integrate
from scipy import special


class Patch:
    def __init__(self, freq, h, er):
        self.freq = freq
        self.h = h
        self.er = er
        self.hp = np.zeros(8)
        self.length, self.w, self.xf, self.d = None, None, None, None

    def Calc(self):
        c = 3e2  # freq = 2.44e9  # hz 工作频率
        lambda0 = c / self.freq  # mm 真空波长
        # 贴片宽度
        # er = 1.006  # 介质相对介电常数， 空气
        # h = 5  # mm 介质板厚度
        self.w = 0.5 * lambda0 * math.sqrt(2 / (self.er + 1))  # 高于产生高次模场畸变，低于辐射效率降低
        # 贴片长度
        a = self.w / self.h
        er_eff = 0.5 * (self.er + 1) + 0.5 * (self.er - 1) * math.pow((1 + 12 / a), -0.5)  # 等效介电常数
        lambda1 = lambda0 / math.sqrt(er_eff)  # 介质波长
        delta_l = 0.412 * self.h * ((er_eff + 0.3) / (er_eff - 0.258)) * ((a + 0.264) / (a + 0.8))  # 边缘场等效伸长长度
        self.length = 0.5 * lambda1 - 2 * delta_l
        # 谐振输入电阻求馈入深度
        k0 = 2 * np.pi / lambda0  # h/lambda0 <0.1
        G1 = integrate.quad(lambda x: 1 / 120 / math.pow(math.pi, 2) * math.pow(math.sin(k0 * self.w / 2.0 * math.cos(x)) / math.cos(x), 2) * math.pow(math.sin(x), 3), 0, np.pi)
        G12 = integrate.quad(lambda x: 1 / 120 / math.pow(math.pi, 2) * math.pow(math.sin(k0 * self.w * math.cos(x) / 2.0) / math.cos(x), 2) * special.j0(self.length * math.sin(x) * k0) * math.pow(math.sin(x), 3), 0, np.pi)
        g1 = G1[0]
        g12 = G12[0]
        Rin0 = 0.5 / (g1 + g12)
        Y0 = (self.length / np.pi) * np.arccos(math.sqrt(50 / Rin0))
        self.xf = self.length * 0.5 - Y0
        # 贴片天线尺寸理论值
        self.length = round(self.length, 5)
        self.w = round(self.w, 5)
        self.xf = round(self.xf, 5)
        self.d = (300 / self.freq) * 0.5
        for index in range(len(self.hp)):
            self.hp[index] = round(self.w / 2.0 + (index + 1) * self.d, 3)
        print(self.length, self.w, self.xf, self.hp, round(self.d, 5))
        return self.length, self.w, self.xf, self.hp, round(self.d, 5)


if __name__ == '__main__':
    cp = Patch(2.44, 5, 1.006)
    cp.Calc()
