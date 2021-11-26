#simple one
import time
from hardware import input_output
from camera_analysis import analyse_for_colours, get_bin_detection
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    io = input_output()
    pic = io.take_picture()
    masks = analyse_for_colours(pic)
    print(get_bin_detection(masks[3], 12))
    plt.imshow(pic)
    plt.show()
