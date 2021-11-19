import os
import sys
import time
import serial

# Adding the src folder in the current directory as it contains the script
# with the Thymio class
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from Thymio import Thymio

th = Thymio.serial(port="/dev/ttyACM0", refreshing_rate=0.1)

dir(th)


time.sleep(1)

variables = th.variable_description()

for var in variables :
    print(var)

th.set_var_array("leds.top", [255, 0, 0])

