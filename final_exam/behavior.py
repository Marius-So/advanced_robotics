#simple one
import time
from hardware import input_output
from camera_analysis import analyse_for_colours, get_bin_detection
import matplotlib as plt

if __name__ == '__main__':
    io = input_output()
    pic = io.take_picture()
    plt.imshow(pic)
    plt.show()
    
    #print(io.lidar_output)
    #test_Comunications(io,1)
