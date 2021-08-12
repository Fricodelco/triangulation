from sim import Sim
from pathlib import Path
import json
from math import sqrt, tan, atan2, sin, cos, pi
import numpy as np


class Localizer(Sim):
    def __init__(self):
        data = self.get_json_config()
        super().__init__(data["x_min"], data["y_min"],
                         data["x_max"], data["y_max"], data["markers_count"],
                         data["camera_noise"], data["camera_vision_angle"],
                         data["camera_pose_x"], data["camera_pose_y"],
                         data["camera_alpha"], data["seed"])
        self.show_config = data["show_config"]
        self.seen_x, self.seen_y, self.seen_alpha = super().get_camera_measurement()
        self.outlier_border = 2
        self.localize()

    def get_json_config(self):
        path = Path(__file__).resolve().parent
        path = str(path)+"/config.json"
        with open(path, "r") as read_file:
            data = json.load(read_file)
        return data

    def localize(self):
        if self.seen_alpha.shape[0] > 2:
            x, y, alpha = self.sort_seens(
                self.seen_x, self.seen_y, self.seen_alpha)
            cam_x = []
            cam_y = []
            cam_alpha = []
            for i in range(x.shape[0]-2):
                for j in range(i+2, x.shape[0]):
                    x_3, y_3 = x[i], y[i]
                    x_2, y_2 = x[i+1], y[i+1]
                    x_1, y_1 = x[j], y[j]
                    phi_2 = abs(alpha[i+1] - alpha[i])
                    phi_1 = abs(alpha[j] - alpha[i+1])
                    cam_x_, cam_y_ = self.find_camera(
                        x_1, y_1, x_2, y_2, x_3, y_3, phi_1, phi_2)
                    cam_alpha_ = atan2(y_1 - cam_y_, x_1 - cam_x_) - alpha[j]
                    if cam_alpha_ < 0:
                        cam_alpha_ += 2*pi
                    cam_x.append(cam_x_)
                    cam_y.append(cam_y_)
                    cam_alpha.append(cam_alpha_)
            cam_x = np.asarray(cam_x)
            cam_y = np.asarray(cam_y)
            cam_alpha = np.asarray(cam_alpha)
            cam_filtered_x, cam_filtered_y, cam_filtered_alpha, std_x, std_y, std_alpha = self.filter_pose(
                cam_x, cam_y, cam_alpha)
            print("estimated camera pose:", cam_filtered_x,
                  cam_filtered_y, cam_filtered_alpha)
            print("std of estimated pose:", std_x, std_y, std_alpha)
            print("real camera pose:", self.cam_x, self.cam_y, self.cam_alpha)
            if self.show_config:
                super().show_config()
        else:
            print("not enough data to localize")
            return None

    def filter_pose(self, x, y, alpha):
        median_x = np.median(x)
        median_y = np.median(y)
        x_filtered = x.copy()
        y_filtered = y.copy()
        alpha_filtered = alpha.copy()
        j = 0
        for i in range(x.shape[0]):
            if abs(x[i] - median_x) > self.outlier_border or abs(y[i] - median_y) > self.outlier_border:
                x_filtered = np.delete(x_filtered, j)
                y_filtered = np.delete(y_filtered, j)
                alpha_filtered = np.delete(alpha_filtered, j)
                j -= 1
            j += 1
        return(np.median(x_filtered), np.median(y_filtered),
               np.median(alpha_filtered), np.std(x_filtered), np.std(y_filtered), np.std(alpha_filtered))

    def find_camera(self, x_1, y_1, x_2, y_2, x_3, y_3, phi_1, phi_2):
        ab = sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2)
        bc = sqrt((x_3 - x_2)**2 + (y_3 - y_2)**2)
        sigma_1 = -atan2((y_2 - y_1), (x_2 - x_1))
        sigma_2 = -atan2((y_3 - y_2), (x_3 - x_2))
        r_1 = ab / (2*sin(phi_1))
        r_2 = bc / (2*sin(phi_2))
        x_n = x_1 - r_1 * sin(sigma_1 - phi_1)
        y_n = y_1 - r_1 * cos(sigma_1 - phi_1)
        x_m = x_2 - r_2 * sin(sigma_2 - phi_2)
        y_m = y_2 - r_2 * cos(sigma_2 - phi_2)
        n = (r_2**2 - r_1**2 - x_m**2 + x_n**2 -
             y_m**2 + y_n**2) / (2*(x_n - x_m))
        m = (y_m - y_n) / (x_n - x_m)
        y = ((2*m*x_n + 2*y_n - 2*m*n) / (1 + m**2)) - y_2
        x = m*y + n
        return x, y

    def sort_seens(self, x, y, alpha):
        for i in range(alpha.shape[0]):
            for j in range(alpha.shape[0]-i-1):
                if alpha[j] > alpha[j+1]:
                    alpha[j], alpha[j+1] = alpha[j+1], alpha[j]
                    x[j], x[j+1] = x[j+1], x[j]
                    y[j], y[j+1] = y[j+1], y[j]
        return x, y, alpha


def main():
    localizer = Localizer()


if __name__ == '__main__':
    main()
