import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
# TODO:  might want to do a test wether the data quality is sufficient

def lidar_to_points(sensor_data):
     points = []
     precision = len(sensor_data)
     angle_step = 2 * math.pi / precision

     for idx, dist in enumerate(sensor_data):
        x_coord = math.cos((360-idx) * angle_step) * dist
        y_coord = math.sin((360-idx) * angle_step) * dist

        points.append((float(x_coord), float(y_coord)))
     return np.array(points, dtype=np.float32)

def get_global_coords(sensor_data, wall):
    points = lidar_to_points(sensor_data)
    x=[]
    y=[]

    for e in points:
        x.append(e[0])
        y.append(e[1])

    rect = cv2.minAreaRect(points)
    if rect[-2][0] < rect[-2][1]:
        switch_coords = False
        add_rot = 0
        if wall in (1,2):
            #oriented correctly
            add_rot = 0
        else:
            add_rot = math.pi
            #
            # we need to rotate the whole thing by 180 degr
    else:
        switch_coords = True
        if wall in (2,3):
            # need to change x and y!
            add_rot = math.pi/2
            # we need to rot by pos 90 degr
        else:
            add_rot = - math.pi/2
            # we need to rot by neg 90
        # either rot by 90 or - 90
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    print(box)

    x_mean = 0
    y_mean = 0
    rotation = - math.radians(rect[-1]) #+ add_rot
    print(add_rot)
    print(rect)
    print(math.radians(rect[-1]))
    for x,y in box:
        plt.scatter(x,y,color="red")
        xr,yr = rotate_point(x,y, rotation)
        plt.scatter(xr,yr,color="black")
        x_mean += xr/4
        y_mean += yr/4

    plt.scatter(0,0,color="red")
    plt.show()
    print('rotation')
    print(rotation)

    # neg because they are offsets
    if switch_coords:
        return -y_mean, -x_mean, (rotation + math.pi) % (2*math.pi)
    else:
        return -x_mean, -y_mean, (rotation + math.pi) % (2*math.pi)

def polar_to_cartesian(r, theta):
   xx = r * math.cos(theta)
   yy = r * math.sin(theta)
   return(xx, yy)

def cartesian_to_polar(x, y):
   rr = math.sqrt(x**2 + y**2)
   theta = math.atan2(y, x)
   return(rr, theta)

def rotate_point(x,y,theta): #rotate x,y around oringin
    rr,ang = cartesian_to_polar(x,y)
    ang = ang + theta
    xr,yr = polar_to_cartesian(rr,ang)
    return [xr,yr]


if __name__ == '__main__':

    W = 1.92
    H = 1.13
    x = W/2 - 0.40
    y = H/2 - 0.53

    print(x,y)

    realValues = [757.25, 758.5, 764.0, 769.5, 777.5, 778.25, 785.25, 794.0, 797.25, 804.75, 813.5, 823.5, 826.5, 837.25, 846.0, 849.25, 861.0, 521.5, 517.75, 512.0, 508.5, 509.0, 509.0, 515.0, 967.75, 993.25, 1009.0, 1007.25, 1031.0, 1057.0, 1063.25, 1084.25, 1115.75, 1149.75, 1156.5, 1185.25, 1224.0, 1262.75, 1270.75, 1308.25, 1353.25, 1369.75, 1408.0, 1466.0, 1525.5, 1548.0, 1561.5, 1539.75, 1538.5, 1525.5, 1509.5, 1490.25, 1488.25, 1482.5, 1468.25, 1462.75, 1457.75, 1452.0, 1440.5, 1440.0, 1430.75, 1424.75, 1421.5, 1418.0, 1413.75, 1411.75, 1402.5, 1404.75, 1399.75, 1404.25, 1401.25, 1391.25, 1390.75, 1397.0, 1399.0, 1399.0, 1400.75, 1399.75, 1402.75, 1403.0, 1408.25, 1415.5, 1419.5, 1420.0, 1426.75, 1439.25, 1442.5, 1449.0, 1446.75, 1466.25, 1434.5, 1341.25, 1243.0, 1231.0, 1157.5, 1080.25, 1064.25, 1019.25, 952.5, 942.5, 905.0, 858.75, 849.75, 820.25, 784.25, 774.5, 752.0, 723.0, 711.5, 695.75, 672.25, 661.75, 651.0, 630.5, 611.75, 609.5, 593.5, 580.0, 575.75, 560.25, 550.75, 547.5, 537.5, 525.5, 523.75, 514.5, 504.5, 501.5, 494.5, 486.5, 483.5, 478.75, 469.5, 466.5, 462.5, 456.5, 450.75, 448.25, 444.0, 439.75, 438.25, 434.75, 429.75, 429.25, 425.25, 422.0, 418.75, 418.25, 416.0, 413.5, 412.25, 410.0, 408.25, 406.0, 405.5, 404.5, 402.75, 402.5, 402.25, 399.75, 400.0, 399.75, 399.25, 399.75, 400.75, 402.25, 402.5, 402.0, 403.25, 403.0, 404.25, 405.5, 405.0, 406.5, 406.5, 407.5, 409.5, 412.0, 415.75, 415.75, 418.0, 420.75, 420.0, 425.75, 429.0, 430.5, 433.25, 437.5, 442.5, 443.75, 447.5, 454.0, 459.0, 460.25, 465.0, 471.5, 479.75, 482.25, 486.75, 495.5, 504.5, 507.25, 514.75, 524.5, 528.5, 535.0, 547.0, 559.75, 563.5, 572.0, 586.5, 601.5, 606.75, 618.25, 635.75, 619.0, 691.75, 646.75, 638.25, 634.0, 623.25, 612.0, 613.0, 609.0, 598.75, 591.25, 588.25, 584.5, 576.5, 575.0, 571.5, 565.5, 559.5, 557.75, 554.75, 551.5, 548.75, 546.0, 543.75, 542.5, 540.25, 537.75, 534.5, 533.75, 532.25, 531.25, 529.25, 529.75, 528.25, 526.5, 528.25, 528.0, 527.25, 527.25, 528.0, 525.5, 528.25, 529.25, 529.25, 531.5, 532.5, 533.5, 536.75, 539.0, 539.75, 542.75, 544.5, 545.75, 549.75, 552.75, 556.0, 559.5, 562.0, 567.75, 566.5, 572.75, 577.5, 584.75, 587.25, 591.5, 599.25, 602.5, 606.5, 614.5, 624.75, 629.0, 634.0, 646.0, 656.75, 662.25, 668.75, 681.75, 695.0, 700.25, 708.75, 725.5, 743.5, 749.25, 760.25, 780.5, 788.25, 801.5, 825.0, 848.0, 857.75, 873.0, 832.75, 891.5, 885.0, 878.25, 863.25, 857.0, 848.75, 835.5, 832.25, 823.0, 812.25, 810.0, 803.25, 793.5, 785.75, 783.0, 777.5, 770.5, 767.0, 763.5, 757.0, 754.0, 750.5, 746.25, 743.25, 741.75, 737.75, 735.0, 733.5, 731.5, 728.0, 727.5, 725.75, 726.25, 723.0, 726.75, 725.5, 724.0, 725.5, 722.75, 721.75, 723.5, 723.5, 725.25, 729.25, 730.25, 731.5, 735.75, 734.75, 740.75, 742.5, 744.25, 746.5, 749.75]

    print(get_global_coords(realValues, 1))

