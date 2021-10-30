from io_robot import io_robot
import dbus
import dbus.mainloop.glib
from plotter import lidar_ploter
from time import sleep, time
from Map import Map

#constantes
W = 1.92
H = 1.13
speed = 350
thymio = io_robot()


def average_len(l_l):
    ret = 0
    for l in l_l:
        ret += len(l)
    return ret / len(l_l)

def generate_map(first_map):
    while [] in first_map:
        first_map.remove([])
    while None in first_map:
        first_map.remove(None)
    a = average_len(first_map)
    if a > len(first_map): #sous liste plus grande que liste donc parcour en longueur 
        ret = Map(H, W, W/a)
        for i in range(len(first_map)):
            for j in range(len(first_map[i])):
                if first_map[i][j] == True:
                    ret.setDanger([W * j / len(first_map[i]) - W/2, H * i / len(first_map) - H/2])
    else:
        ret = Map(H, W, H/a)
        for i in range(len(first_map)):
            for j in range(len(first_map[i])):
                if first_map[i][j] == True:
                    ret.setDanger([W * i / len(first_map) - W/2, H * j / len(first_map[i]) - H/2])
    return ret

def turn(direction = "right", speed = 40, error = 40):
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
            break
    thymio.set_speed(0,0)

def rotate(angle, speed = 80):
    if angle < 180:
        rot_time = angle / (speed * 0.4)
        thymio.set_speed(speed, -speed)
        sleep(rot_time)
        thymio.set_speed(0,0)
    else:
        angle -= 180
        rot_time = angle / (speed * 0.4)
        thymio.set_speed(-speed,speed)
        sleep(rot_time)
        thymio.set_speed(0,0)

def average(l, n):
    somme = 0
    for i in range(n):
        somme += l[i]
    return somme/n

def go_to_corner():
    #align
    while len(thymio.lidar_output) < 300:
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
    stop = thymio.get_thymio_sensor()[2]
    line = []
    while stop == 0 or stop > 2900:
        ground = thymio.get_ground_sensor()
        if ground[0] < 300 or ground[1] < 300:
            line.append(True)
        else:
            line.append(False)
        test = thymio.lidar_output[angle]
        if abs(test - d) < 5:
            thymio.set_speed(speed, speed)
        elif test > d:
            
            thymio.set_speed(0.9 * speed, speed)
        else:
            thymio.set_speed(speed, 0.9 * speed)
        stop = thymio.get_thymio_sensor()[2]
    thymio.set_speed(0,0)
    return line

def map():
    lines = []
    while True:
        lines.append(moove_straight())
        turn()
        thymio.set_speed(speed,speed)
        if thymio.get_thymio_sensor()[2] != 0:
            return lines
        sleep(1)
        thymio.set_speed(0,0)
        if thymio.get_thymio_sensor()[2] != 0:
            return lines
        turn()
        lines.append(moove_straight().reverse())
        turn("left")
        if thymio.get_thymio_sensor()[2] != 0:
            return lines
        thymio.set_speed(speed,speed)
        sleep(1)
        thymio.set_speed(0,0)
        if thymio.get_thymio_sensor()[2] != 0:
            return lines
        turn("left")
    

if __name__ == "__main__":
    try:
        go_to_corner()
        m = map()
        nico_map = generate_map(m)
        print(nico_map)
    except KeyboardInterrupt:
        print("keyboard interupt detected")
        print("shuting down")
        thymio.set_speed(0,0)
        exit()
