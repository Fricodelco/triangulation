import numpy as np
import matplotlib.pyplot as plt
from math import sin, tan, pi, atan2, cos
import random


class Sim():
    def __init__(self, x_min, y_min, x_max, y_max, markers_count, camera_noise, camera_vision_angle, camera_pose_x, camera_pose_y, camera_alpha, seed):
        random.seed(seed)
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.markers_count = markers_count
        self.cam_x = camera_pose_x
        self.cam_y = camera_pose_y
        self.cam_alpha = camera_alpha
        self.camera_vision_angle = camera_vision_angle
        self.camera_noise = camera_noise
        self.marks_x, self.marks_y = self.generate_marks()

    """ Method for generating marks in random positions
        Count of marks depends on markers_count, location area
        of marks depends on x and y limits
    """
    def generate_marks(self):
        marks_x = []
        marks_y = []
        multiplier_x = self.x_max - self.x_min
        multiplier_y = self.y_max - self.y_min
        for i in range(0, self.markers_count, 1):
            mark_x = random.random()*multiplier_x - abs(self.x_min)
            mark_y = random.random()*multiplier_y - abs(self.y_min)
            marks_x.append(mark_x)
            marks_y.append(mark_y)
        marks_x = np.asarray(marks_x)
        marks_y = np.asarray(marks_y)
        return marks_x, marks_y

    """ Method for generating measurement of camera with given noise
        measurement generates with gauss noise and std = camera_noise
    """
    def get_camera_measurement(self):
        angle_1 = self.cam_alpha + self.camera_vision_angle/2
        angle_2 = self.cam_alpha - self.camera_vision_angle/2
        k1 = tan(angle_1)
        b1 = -k1*self.cam_x + self.cam_y
        k2 = tan(angle_2)
        b2 = -k2*self.cam_x + self.cam_y
        marks_touched_x = []
        marks_touched_y = []
        angles = []
        for i in range(0, self.markers_count, 1):
            x = self.marks_x[i]
            y = self.marks_y[i]
            condition_first = self.check_first_line(angle_1, x, y, k1, b1)
            condition_second = self.check_second_line(angle_2, x, y, k2, b2)
            if condition_first is True and condition_second is True:
                angle = atan2((y - self.cam_y), (x - self.cam_x)
                              ) - self.cam_alpha
                if abs(angle) > self.camera_vision_angle/2:
                    angle = angle + 2*pi
                marks_touched_x.append(x)
                marks_touched_y.append(y)
                sigma = self.camera_noise
                angle += random.gauss(0, sigma)
                angles.append(angle)
        return np.asarray(marks_touched_x), np.asarray(marks_touched_y), np.asarray(angles)

    """ Checking if the marker under or above first line
        checking condition depends on the angle 
    """
    def check_first_line(self, angle, x, y, k, b):
        if cos(angle) > 0 and y < k*x + b:
            return True
        if cos(angle) < 0 and y > k*x + b:
            return True
        return False

    """ Checking if the marker under or above second line
        checking condition depends on the angle 
    """
    def check_second_line(self, angle, x, y, k, b):
        if cos(angle) < 0 and y < k*x + b:
            return True
        if cos(angle) > 0 and y > k*x + b:
            return True
        return False
    
    """ Method for visualize givven config with matplotlib
    """
    def show_config(self):
        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        marks_touched_x, marks_touched_y, _ = self.get_camera_measurement()
        plt.plot(self.marks_x, self.marks_y, 'ro')
        plt.plot(marks_touched_x, marks_touched_y, 'bo')
        plt.plot(self.cam_x, self.cam_y, 'go')
        if cos(self.cam_alpha) < 0:
            x_0 = self.x_min
        else:
            x_0 = self.x_max
        y_0 = tan(self.cam_alpha)*(x_0 - self.cam_x) + self.cam_y
        plt.plot((self.cam_x, x_0),  (self.cam_y, y_0), 'g-')

        if cos(self.cam_alpha + self.camera_vision_angle/2) < 0:
            x_1 = self.x_min
        else:
            x_1 = self.x_max
        y_1 = tan(self.cam_alpha + self.camera_vision_angle/2) * \
            (x_1 - self.cam_x) + self.cam_y
        plt.plot((self.cam_x, x_1),  (self.cam_y, y_1), 'b-')

        if cos(self.cam_alpha - self.camera_vision_angle/2) < 0:
            x_2 = self.x_min
        else:
            x_2 = self.x_max
        y_2 = tan(self.cam_alpha - self.camera_vision_angle/2) * \
            (x_2 - self.cam_x) + self.cam_y
        plt.plot((self.cam_x, x_2),  (self.cam_y, y_2), 'b-')
        plt.show()


def main():
    sim = Sim(-2, -2, 3, 3, 40, 0.01, pi/3, 0.9, 0.9, 4, 100)


if __name__ == '__main__':
    main()
