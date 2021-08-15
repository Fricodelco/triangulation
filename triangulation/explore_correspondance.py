from triangulation.localization import Localizer
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


def explore_std():
    stds = np.arange(0,0.5,0.01)
    x_stds = []
    y_stds = []
    alpha_stds = []
    x = []
    y = []
    alpha = []
    for std in stds:
        localizer = Localizer(camera_noise=std, markers_count=100)
        try:
            x_, y_, alpha_, x_std, y_std, alpha_std = localizer.localize()
        except:
            continue
        x_stds.append(x_std)
        y_stds.append(y_std)
        alpha_stds.append(alpha_std)
        x.append(x_)
        y.append(y_)
        alpha.append(alpha_)
        del localizer
    x = np.asarray(x)
    y = np.asarray(y)
    alpha = np.asarray(alpha)
    localizer = Localizer(camera_noise=0.0 ,markers_count=1)
    x_real = localizer.cam_x
    err_x = get_sqrt((x - x_real)**2)
    y_real = localizer.cam_y
    err_y = get_sqrt((y - y_real)**2)
    alpha_real = localizer.cam_alpha
    err_alpha = get_sqrt((alpha - alpha_real)**2)
    fig, axs = plt.subplots(2)
    axs[0].plot(stds, x_stds, 'g-', label='std_x')
    axs[0].plot(stds, y_stds, 'r-', label='std_y')
    axs[0].plot(stds, alpha_stds, 'b-', label='std_alpha')
    axs[1].plot(stds, err_x, 'g-', label='err_x')
    axs[1].plot(stds, err_y, 'r-', label='err_y')
    axs[1].plot(stds, err_alpha, 'b-', label='err_alpha')
    axs[0].legend()
    axs[1].legend()
    axs[0].grid()
    axs[1].grid()
    plt.show()

def explore_count():
    count = np.arange(30, 800, 20)
    x_stds = []
    y_stds = []
    alpha_stds = []
    x = []
    y = []
    alpha = []
    for mark in count:
        localizer = Localizer(camera_noise=0.02 ,markers_count=mark)
        try:
            x_, y_, alpha_, x_std, y_std, alpha_std = localizer.localize()
        except:
            continue
        x_stds.append(x_std)
        y_stds.append(y_std)
        alpha_stds.append(alpha_std)
        x.append(x_)
        y.append(y_)
        alpha.append(alpha_)
        del localizer
    x = np.asarray(x)
    y = np.asarray(y)
    alpha = np.asarray(alpha)
    localizer = Localizer(camera_noise=0.01 ,markers_count=mark)
    x_real = localizer.cam_x
    err_x = get_sqrt((x - x_real)**2)
    y_real = localizer.cam_y
    err_y = get_sqrt((y - y_real)**2)
    alpha_real = localizer.cam_alpha
    err_alpha = get_sqrt((alpha - alpha_real)**2)
    fig, axs = plt.subplots(2)
    axs[0].plot(count, x_stds, 'g-', label='std_x')
    axs[0].plot(count, y_stds, 'r-', label='std_y')
    axs[0].plot(count, alpha_stds, 'b-', label='std_alpha')
    axs[1].plot(count, err_x, 'g-', label='err_x')
    axs[1].plot(count, err_y, 'r-', label='err_y')
    axs[1].plot(count, err_alpha, 'b-', label='err_alpha')
    axs[0].legend()
    axs[1].legend()
    axs[0].grid()
    axs[1].grid()
    plt.show()

def get_sqrt(arr):
    for i in range(0, arr.shape[0], 1):
        arr[i] = sqrt(arr[i])
    return arr


def main():
    # explore_std()
    explore_count()

if __name__ == '__main__':
    main()

