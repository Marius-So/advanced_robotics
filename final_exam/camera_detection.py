from hardware import input_output
from camera_analysis import analyse_for_colours, get_all_detections
import time
from PIL import Image


def test_camera_detection(robot):
    count = 0
    while True:
        user_input = input()
        count += 1
        if user_input == 'E':
            return
        if user_input in ['red', 'orange', 'blue', 'green', 'purple']:
            robot.set_colour(user_input)
            time.sleep(1)
            pic = robot.take_picture()
            im = Image.fromarray(pic)
            im.save(f"camera_test_{count}.jpg")
	        masks = analyse_for_colours(pic)
	        print(get_all_detections(masks, 12))


if __name__ == '__main__':
    robot = input_output()
    test_camera_detection(robot)
