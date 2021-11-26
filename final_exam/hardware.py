from camera import camera
from lidar import lidar
from Thymio import Thymio
from camera_analysis import analyse_for_colours
import time
import numpy as np

class input_output(Thymio, camera, lidar):
    def __init__(self):
        camera.__init__(self)
        lidar.__init__(self)
        Thymio.__init__(self)