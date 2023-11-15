import math

from HFSS import HFSS
import numpy as np
import time
import os
import matplotlib.pyplot as plt


def Evaluator_math(X):
    w, l = X[0] * 0.001, X[1] * 0.001  # 统一单位为米
    xxi = 4.4   # 介质介电常数
    h = 1.6 * 0.001     # 介质高度
    c = 3e8     # 光速

    xxi_eff = (xxi + 1)/2 + (xxi - 1) / (2 * math.sqrt(1 + 12*h/w))
    del_L = 0.412 * h * (xxi_eff + 0.3)*(w/h + 0.264)/(xxi_eff - 0.258)/(w/h + 0.8)
    f_ans = c / (2 * (l+del_L) * math.sqrt(xxi_eff)) / 1e9
    return f_ans

def Evaluator_hfss(X):
    st = time.time()
    Optimization_variables = 'w0', 'l0',
    export_result_dir = os.getcwd()
    export_result_file_name = 's11.csv'
    export_result_file_path = export_result_dir + '\\' + export_result_file_name

    h = HFSS()
    h.openProject(os.getcwd(), "Cekui")  # 打开HFSS相关文件
    h.init()

    for k in range(0, len(Optimization_variables)):
        variable = h.getVariablevalue(Optimization_variables[k])
        variable_value, variable_unit = h.convertVariabletovalueandunit(variable)
        h.changeVariablevalue(Optimization_variables[k], X[k], variable_unit)

    h.solve('Setup1')  # 开始仿真
    h.createSpreport('s11', 'Setup1', "dB(S(1,1))")
    h.exportTofile('s11', export_result_dir, export_result_file_name)

    with open(export_result_file_path) as f:
        text=f.readlines()
    data=[]

    for line in text[1:]:
        freq, s11=line.strip().split(',')
        data.append((freq, s11))
    data = np.array(data, dtype=float)
    cost_ans = data[np.argmin(data[:, 1]), 0]    # 得到谐振频率

    h.deleteAllreports()
    h.closeProject()  # 关闭HFSS

    print('---------------- Parameters: ', X, ' fitness: ', cost_ans, ' time: ', round(time.time() - st, 2), 's')
    return cost_ans

if __name__ == '__main__':
   # print(Evaluator_math([38.51, 30.01]))
    print(Evaluator_hfss([39, 31]))
    print(Evaluator_hfss([38, 32]))



