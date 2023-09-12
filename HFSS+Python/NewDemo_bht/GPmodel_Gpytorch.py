from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF,Sum,Matern, ConstantKernel as C  # REF就是高斯核函数
import numpy as np
from sklearn.preprocessing import scale
from gp import train_gp
import sys
from copy import deepcopy
import gpytorch
import torch
from torch.quasirandom import SobolEngine

# 推荐Gpytorch的GP，更快一点
# 这个教程还真不好找，建议就以这个为蓝本把，更多的解释在gp.py

class GPmodel_Gpytorch():
    def __init__(self, train_x, train_y):
        self.use_ard = True,
        self.max_cholesky_size = 1500,
        self.n_training_steps = 100,
        self.min_cuda = 1024,
        device = "cpu",
        dtype = "float64"
        self.dtype = torch.float32 if dtype == "float32" else torch.float64
        self.device = torch.device("cuda") if device == "cuda" else torch.device("cpu")
        self.updateModel(train_x,train_y)

    def updateModel(self,train_x,train_y):
        if np.ndim(train_y) != 1:   # 处理维度问题，比如有的输入train由于之前的处理会是二维的，为适应库这时把他一维化
            train_y = train_y[:, 0] # 训练

        self.Xmean = np.mean(train_x, axis=0)
        self.Xstd = np.std(train_x, axis=0)
        XL_scale = scale(train_x)

        self.mu_L, self.sigma_L = np.median(train_y), train_y.std()
        self.sigma_L = 1.0 if self.sigma_L < 1e-6 else self.sigma_L
        YL_scale = (deepcopy(train_y) - self.mu_L) / self.sigma_L
        # 标准化
        print("Updating model....")

        # Figure out what device we are running on
        hypers = {}
        # We use CG + Lanczos for training if we have enough data
        device, dtype = self.device, self.dtype
        with gpytorch.settings.max_cholesky_size(self.max_cholesky_size[0]):
            X_torch = torch.tensor(XL_scale).to(device=device, dtype=dtype)
            y_torch = torch.tensor(YL_scale).to(device=device, dtype=dtype)
            self.GPreg = train_gp(
                train_x=X_torch, train_y=y_torch, use_ard=self.use_ard, num_steps=self.n_training_steps[0],
                hypers=hypers)
            hypers = self.GPreg.state_dict()

        self.KEN_modelH= self.GPreg.covar_module.base_kernel
        LCs = self.KEN_modelH.lengthscale.cpu().detach().numpy().ravel()
        self.thetaa = LCs*LCs

    def predict(self, testp):
        if np.ndim(testp) == 1:
            testp = np.array([testp])
            testp = (testp - self.Xmean) / self.Xstd
            # We may have to move the GP to a new device
            with torch.no_grad(), gpytorch.settings.max_cholesky_size(self.max_cholesky_size[0]):
                X_cand_torch = torch.tensor(testp).to(dtype=self.dtype, device=self.device)
                pred_L = self.GPreg(X_cand_torch)

            pred_y, pred_std = np.array(pred_L.mean * self.sigma_L + self.mu_L), np.array(np.sqrt(pred_L.variance) * self.sigma_L)
            return pred_y[0], pred_std[0]
        else:
            testp = (testp - self.Xmean) / self.Xstd
            # We may have to move the GP to a new device
            with torch.no_grad(), gpytorch.settings.max_cholesky_size(self.max_cholesky_size[0]):
                X_cand_torch = torch.tensor(testp).to(dtype=self.dtype, device=self.device)
                pred_L = self.GPreg(X_cand_torch)

            pred_y, pred_std = np.array(pred_L.mean * self.sigma_L + self.mu_L), np.array(
                np.sqrt(pred_L.variance) * self.sigma_L)
            return pred_y, pred_std