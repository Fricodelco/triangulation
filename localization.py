from sim import Sim
from pathlib import Path
import json
from math import sqrt, tan, atan2, sin, cos, pi


class Localizer(Sim):
    def __init__(self):
        data = self.get_json_config()
        super().__init__(data["x_min"], data["y_min"],
                    data["x_max"], data["y_max"], data["markers_count"],
                    data["camera_noise"], data["camera_vision_angle"],
                    data["camera_pose_x"], data["camera_pose_y"],
                    data["camera_alpha"], data["seed"])
        self.seen_x, self.seen_y, self.seen_alpha = super().get_camera_measurement()
        self.localize()

    def get_json_config(self):
        path = Path(__file__).resolve().parent        
        path = str(path)+"/config.json"
        with open(path, "r") as read_file:
            data = json.load(read_file)
        return data

    def localize(self):
        if self.seen_alpha.shape[0] > 2:
            x, y, alpha = self.sort_seens(self.seen_x, self.seen_y, self.seen_alpha)
            x_3, y_3 = x[0], y[0]
            x_2, y_2 = x[1], y[1]
            x_1, y_1 = x[2], y[2]
            phi_2 = abs(alpha[1] - alpha[0])
            phi_1 = abs(alpha[2] - alpha[1])
            x_cam, y_cam = self.find_camera(x_1, y_1, x_2, y_2, x_3, y_3, phi_1, phi_2)
            print(x_cam, y_cam)
            super().show_config()
        else:
            print("not enough data to localize")
            return None
    
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
        n = (r_2**2 - r_1**2 - x_m**2 + x_n**2 - y_m**2 + y_n**2) / (2*(x_n - x_m))
        m = (y_m - y_n) / (x_n - x_m)
        y = ((2*m*x_n + 2*y_n - 2*m*n) / (1 + m**2)) - y_2
        x = m*y + n
        return x,y


    def sort_seens(self, x, y, alpha):
        for i in range(alpha.shape[0]-1):
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