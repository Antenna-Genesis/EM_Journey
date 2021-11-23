import numpy as np
import warnings


def cart2sph(x, y, z):
    """
    to convert the Cartesian coordinate to the spherical one
    the input and output can be either a scalar or a matrix (np.array)
    :param x: one number or one np.array
    :param y: one number or one np.array
    :param z: one number or one np.array
    :return: a list including r, theta_rad (deg) and phi_rad (deg) in the spherical coordinate
    r, theta_rad (deg) and phi_rad (deg) can be numbers or np.arrays
    theta_rad from 0 to 180 deg, phi_rad from 0 to 360 deg
    """
    try:
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        phi_deg = np.angle(x + 1j * y) * 180 / np.pi
        # using np.angle, phi_deg ranges from -180 to 180 deg
        theta_deg = np.arccos(z / r) * 180 / np.pi
        if isinstance(x, (int, float, complex)) and \
                isinstance(y, (int, float, complex)) and \
                isinstance(z, (int, float, complex)):
            # another way: all(temp == True for temp in [isinstance(item, (int, float, complex)) for item in [x, y, z]])
            # x, y, z are all scalars
            if phi_deg < 0:
                phi_deg += 360
            # to change phi_deg angle from [-180, 180] to [0, 360]
        elif isinstance(x, np.ndarray) and \
                isinstance(y, np.ndarray) and \
                isinstance(z, np.ndarray):
            phi_deg[np.where(phi_deg < 0)] += 360
            # to change phi_deg angle from [-180, 180] to [0, 360]
        else:
            warnings.warn("x, y, z should be either all scalars or np.arrays")
            exit(0)
        return [r, theta_deg, phi_deg]
    except ValueError:
        print("Oops! x, y, z should have the same dimensions")

def sph2cart(r, theta_rad, phi_rad):
    """
    to convert the spherical coordinate to the Cartesian one
    :param r:
    :param phi_rad:
    :param theta_rad:
    :return:
    """
    x = r * np.sin(phi_rad) * np.cos(theta_rad)
    y = r * np.cos(phi_rad)
    z = r * np.sin(phi_rad) * np.sin(theta_rad)
    return [x, y, z]


'''
test the function
'''
if __name__ == '__main__':

    x, y, z = 1, 2, 3  # [1], [3], [5]
    cart2sph(x, y, z)
