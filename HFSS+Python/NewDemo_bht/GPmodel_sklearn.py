from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,Sum,Matern, ConstantKernel as C  # REF就是高斯核函数
import numpy as np
from sklearn.preprocessing import scale

# sklearn 教程 http://scikit-learn.org.cn/view/86.html#1.7.5%20%E9%AB%98%E6%96%AF%E8%BF%87%E7%A8%8B%E5%86%85%E6%A0%B8

class GPmodel_sklearn():
    import warnings
    warnings.filterwarnings("ignore")

    def __init__(self, train_x, train_y):
        self.updateModel(train_x,train_y)

    def updateModel(self,train_x,train_y):
        print("Updating GP Model")
        kernel = Sum( Matern(10, (1e-2, 1000)), C(2,(1e-3,100)) ) # 创建高斯过程的核
        self.Xmean=np.mean(train_x)
        self.Xstd=np.std(train_x)
        x_c=scale(train_x)      # 标准化输入参数

        self.GPreg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=50, normalize_y=True)
        if np.ndim(train_y) == 1: #处理维度问题，比如有的输入train由于之前的处理会是二维的，为适应库这时把他一维化
            self.GPreg.fit(x_c, train_y)
        else:
            self.GPreg.fit(x_c, train_y[:, 0]) # 训练

        lensca = self.GPreg.kernel_.get_params()['k1__length_scale']
        self.thetaa = lensca*lensca # 提取模型参数长度尺度

    def predict(self,p):
        p=np.array(p)
        if np.ndim(p)==1:
            p=np.array([p])
            p[:]= (p[:]-self.Xmean)/self.Xstd
            yy,ss = self.GPreg.predict(p, return_std=True)
            return yy[0],ss[0]
        else:
            p[:] = (p[:] - self.Xmean) / self.Xstd
            return self.GPreg.predict(p, return_std=True)