import numpy as np

class Sim():
    def __init__(self, x_zone, y_zone, camera_noise, camera_angle):
        self.marks_x, self.marks_y = self.generate_marks(x_zone, y_zone)
        print(self.marks_x, self.marks_y)
    def generate_marks(self, x, y):
        marks_x = np.arange(0,x,0.2)
        marks_y = np.arange(0,y,0.2)
        return marks_x, marks_y
    def get_camera_measurement(self, cam_x, cam_y, cam_alpha):
        a = 1

def main():
    sim = Sim(5,5,0,0)
    

if __name__ == '__main__':
    main()