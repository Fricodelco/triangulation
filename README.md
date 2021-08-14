# Description
Implementation of the geometric triangulation method described in C. D. McGillem and T. S. Rappaport, "A beacon navigation method for autonomous vehicles," in IEEE Transactions on Vehicular Technology, vol. 38, no. 3, pp. 132-139, Aug. 1989, doi: 10.1109/25.45466.  
Package consists of simple simulator (triangulation/sim.py) and localization algorithm (triangulation/localization.py).  
You can configure simulator with triangulation/config.json file.  
# Config.json description
x_min, x_max, y_min, y_max - defines the boundaries of the field   
markers_count - the number of randomly generated markers  
camera_noise - standard deviation of angle measurements  
camera_vision_angle - camera angle of view  
camera_x, camera_y, camera_alpha - position of camera  
seed - seed for random.random  
show_config - enable data visualisation using matplotlib  
outlier_border - defines the boundary at which a measurement is considered to be faulty   
# Usage
Configurate /triangulation/config.json  
Install package with pip3  
In terminal run triangulation-cli  

