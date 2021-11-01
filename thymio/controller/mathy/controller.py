from io_robot import io_robot
import dbus
import dbus.mainloop.glib
from plotter import lidar_ploter
from time import sleep, time
from pathfinding import pathfinder
import matplotlib.pyplot as plt
from comp_vision import robot_vision

#constantes
W = 1.92
H = 1.13
speed = 500
thymio = io_robot()

def clean_map(m):
    while [] in m:
        m.remove([])
    while None in m:
        m.remove(None)

    size = 0
    for l in m:
        if size < len(l):
            size = len(l)

    to_return = []
    for l in m:
        b = [2] * size
        for i in range(len(l)):
            b[int((size)*i/len(l))] = l[i]
        for i in range(size):
            if b[i] != 2:
                p = i
            if b[i] == 2:
                n = i
                while b[n] == 2 and n < size - 1:
                    n += 1
                if b[n] == 0 and b[p] == 0:
                    for j in range(p + 1 ,n):
                        b[j] = 0
                else:
                    for j in range(p + 1, n):
                        b[j] = 1
            b[-1] = b[-2]
        to_return.append(b)
    return to_return

def turn(direction = "right", speed = 50, error = 40):
    d = thymio.lidar_output[0] + thymio.lidar_output[180]
    if abs(d - 1900) < abs(d - 1110):
        newx = 1900
        newy = 1110
    else:
        newx = 1110
        newy = 1900
    if direction == "right":
        thymio.set_speed(speed, -speed)
    else:
        thymio.set_speed(-speed, speed)
    while True:
        if abs(newx - thymio.lidar_output[90] - thymio.lidar_output[270]) < error and abs(newy - thymio.lidar_output[0] - thymio.lidar_output[180]) < error:
            thymio.set_speed(0,0)
            return

def correct(direction = "right", speed = 55, error = 50):
    if direction == "right":
        thymio.set_speed(speed, -speed)
    else:
        thymio.set_speed(-speed, speed)
    while abs(thymio.lidar_output[0] + thymio.lidar_output[180] - 1900) < error and abs(thymio.lidar_output[0] + thymio.lidar_output[180] - 1110) < error:
        continue
    thymio.set_speed(0,0)

def rotate(angle, speed = 80):
    if angle < 180:
        rot_time = angle / (speed * 0.4)
        thymio.set_speed(speed, -speed)
        sleep(rot_time)
        thymio.set_speed(0,0)
    else:
        angle = 360 - angle
        rot_time = angle / (speed * 0.4)
        thymio.set_speed(-speed,speed)
        sleep(rot_time)
        thymio.set_speed(0,0)

def go_to_corner():
    #align
    while 180 not in thymio.lidar_output or 0 not in thymio.lidar_output or 90 not in thymio.lidar_output or 270 not in thymio.lidar_output:
        continue
    to_rotate = min(thymio.lidar_output, key=thymio.lidar_output.get)
    to_rotate = (to_rotate + 180) % 360
    rotate(to_rotate)
    #go to closet wall
    moove_straight()
    #rotate 90° right
    turn()
    #rotate(95)
    #go to corner
    moove_straight()
    #rotate 90° right
    turn()

def moove_straight():
    angle = 90
    d = thymio.lidar_output[90]
    if d == -1:
        d = thymio.lidar_output[270]
        angle = 270
    #stop = thymio.get_thymio_sensor()[2]
    line = []
    last_error = ""
    a = time()
    while thymio.lidar_output[180] > 200 and thymio.lidar_output[179] > 200:#stop == 0 or stop > 2900:
        ground = thymio.get_ground_sensor()
        if time() - a > 0.5:
            a = time()
            if ground[0] < 300 or ground[1] < 300:
                line.append(1)
            else:
                line.append(0)
        test = thymio.lidar_output[angle]
        if abs(test - d) < 5:
            if last_error == "":
                thymio.set_speed(speed, speed)
            elif last_error == "right":
                correct("left")
                last_error = ""
            else:
                correct("right")
                last_error = ""
        elif test > d:
            thymio.set_speed(0.9 * speed, speed)
            last_error = "right"
        else:
            thymio.set_speed(speed, 0.9 * speed)
            last_error = "left"
        #stop = thymio.get_thymio_sensor()[2]
    thymio.set_speed(0,0)
    return line

def map():
    lines = []
    while True:
        lines.append(moove_straight())
        turn()
        thymio.set_speed(speed,speed)
        if thymio.lidar_output[180] < 200:
            return lines
        sleep(0.9)
        thymio.set_speed(0,0)
        if thymio.lidar_output[180] < 200:
            return lines
        turn()
        lines.append(moove_straight().reverse())
        turn("left")
        if thymio.lidar_output[180] < 200:
            return lines
        thymio.set_speed(speed,speed)
        sleep(0.9)
        thymio.set_speed(0,0)
        if thymio.lidar_output[180] < 200:
            return lines
        turn("left")
    return lines

if __name__ == "__main__":
    try:
        #thymio.play_sound(1)
        go_to_corner()
        m = map()
        m = clean_map(m)
        d = thymio.lidar_output[0] + thymio.lidar_output[180]
        if abs(d - 1900) < abs(d - 1110):#y sous liste
            resx = W/len(m)
            resy = H/len(m[0])
            m = pathfinder(m, len(m[0]) - 1, len(m) - 1, 0, 0) 
        else: #x sous liste
            resx = W/len(m[0])
            resy = H/len(m)
            m = pathfinder(m,  len(m) - 1, len(m[0]) - 1, 0, 0)
        m.solve()
        l = m.get_list_of_indices(m.xtarget, m.ytarget)
        print(m.get_list_of_moove(l))
        print(m)

        print(m)
    except KeyboardInterrupt:
        print("keyboard interupt detected")
        print("shuting down")
        thymio.set_speed(0,0)
        exit()
