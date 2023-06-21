from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,Sum,Matern, ConstantKernel as C  # REF就是高斯核函数
import numpy as np
from sklearn.preprocessing import scale

class GPmodel():
    import warnings
    warnings.filterwarnings("ignore")
    def __init__(self, train_x, train_y):
        self.updateModel(train_x,train_y)

    def updateModel(self,train_x,train_y):
        print("Updating GP Model")
        kernel = Sum( RBF(2, (1e-4, 30)), C(2,(1e-3,1000)) ) # 创建高斯过程回归,并训练
        self.Xmean=np.mean(train_x)
        self.Xstd=np.std(train_x)
        x_c=scale(train_x)

        self.GPreg = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=100,normalize_y=True)
        if np.ndim(train_y) == 1:
            self.GPreg.fit(x_c, train_y)
        else:
            self.GPreg.fit(x_c, train_y[:, 0])

        lensca = self.GPreg.kernel_.get_params()['k1__length_scale']
        self.thetaa = lensca*lensca

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