import FF_Compare
import Gain_Calculation
import Heat_Plot
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    # filename1 = 'dataset_E/E_greater6205x.csv'
    # filename2 = 'dataset_E/E_greater6205y.csv'
    # filename3 = 'dataset_E/E_greater6205z.csv'
    filename1 = 'dataset/E_25x.csv'
    filename2 = 'dataset/E_25y.csv'
    Gain, Gain_theta, Gain_phi = Gain_Calculation.sphere_gain(filename1, filename2, 'test', 16, 0.9, 0.9)
    filename3 = 'dataset/Gain Total 2.csv'
    filename4 = 'dataset/Gain Theta 2.csv'
    filename5 = 'dataset/Gain Phi 2.csv'
    FF_Compare.ff_compare(Gain, Gain_theta, Gain_phi, 16, filename3, filename4, filename5)
    plt.show()
