from hardware import input_output
from camera_analysis import analyse_for_colours, get_all_detections
import time
from PIL import Image
import numpy as np


def test_camera_detection(robot):
    count = 0
    while True:
        user_input = input()
        count += 1
        if user_input == 'E':
            break
            return
        if user_input in ['red', 'orange', 'blue', 'green', 'purple']:
            robot.set_colour(user_input)
            robot.set_speed(0,0)
            prox_horizontal, ground_reflected, left_speed, right_speed, rx = robot.get_sensor_values()
            time.sleep(1)
            pic = robot.take_picture()
            im = Image.fromarray(pic)
            colour_masks = analyse_for_colours(pic,1)
            img_2 = np.concatenate(colour_masks)
            img_2 = Image.fromarray(img_2)
            im.save(f"test/camera_test_{count}.jpg")
            img_2.save(f"test/detection_test_{count}.jpg")

            print(get_camera_output(robot))


def get_camera_output(robot):
	picture = robot.take_picture()
	colour_masks = analyse_for_colours(picture,1)
	return get_all_detections(colour_masks, bins=5)

if __name__ == '__main__':
    robot = input_output()
    test_camera_detection(robot)
