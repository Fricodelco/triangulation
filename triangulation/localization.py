from triangulation.sim import Sim
from pathlib import Path
import json
from math import sqrt, atan2, asin, sin, cos, pi
import numpy as np
from scipy.spatial.transform import Rotation


class Localizer(Sim):
    def __init__(self, camera_noise=None, markers_count = None):    
        data = self.get_json_config()
        if camera_noise == None:
            camera_noise = data["camera_noise"]
        if markers_count == None:
            markers_count = data["markers_count"]
        super().__init__(data["x_min"], data["y_min"],
                         data["x_max"], data["y_max"], markers_count,
                         camera_noise, data["camera_vision_angle"],
                         data["camera_pose_x"], data["camera_pose_y"],
                         data["camera_alpha"], data["seed"])
        self.show_config = data["show_config"]
        self.seen_x, self.seen_y, self.seen_alpha = super().get_camera_measurement()
        self.outlier_border = data["outlier_border"]

    """ Get data from config of simulation 
    """
    def get_json_config(self):
        path = Path(__file__).resolve().parent
        path = str(path)+"/config.json"
        with open(path, "r") as read_file:
            data = json.load(read_file)
        return data

    """ Main localization method
        1. Sort measurements by angle
        2. Iterate throw each 3 measurements
        3. Calculate position of the cam and store it to array
        4. Filter positions and get median position and std 
    """
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
                    cam_x_, cam_y_, cam_alpha_ = self.find_camera(
                        x_1, y_1, x_2, y_2, x_3, y_3, phi_1, phi_2, alpha[j])
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
            return cam_filtered_x, cam_filtered_y, cam_filtered_alpha, std_x, std_y, std_alpha
        else:
            print("not enough data to localize")
            return None

    """ Filter array of positions
        1. Delete outliers
        2. Calculate median
    """
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

    """ Calculate position of camera using 3 markers
        Calculations with intersection of circles method
        described in C. D. McGillem and T. S. Rappaport, "A beacon navigation method for autonomous vehicles," 
        in IEEE Transactions on Vehicular Technology, vol. 38, no. 3, pp. 132-139, Aug. 1989, doi: 10.1109/25.45466. 
    """
    def find_camera(self, x_1, y_1, x_2, y_2, x_3, y_3, phi_1, phi_2, alpha):
        if phi_1 < 0 or phi_2 < 0:
            raise ValueError("angles can not be negative")
        if phi_1 == 0.0 or phi_2 == 0.0:
            raise ValueError("angles can not be zero")
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
        cam_alpha_ = atan2(y_1 - y, x_1 - x) - alpha
        if cam_alpha_ < 0:
            cam_alpha_ += 2*pi
        rot = Rotation.from_euler('xyz', [0, 0, cam_alpha_])
        q = rot.as_quat()
        rot = Rotation.from_quat(q)
        cam_alpha_ = rot.as_euler('xyz')[2]
        return x, y, cam_alpha_

    """ Sort measurements by angle
    """
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
    localizer.localize()
    
if __name__ == '__main__':
    main()
