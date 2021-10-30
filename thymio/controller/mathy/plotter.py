import matplotlib.pyplot as plt
import math

def lidar_ploter(sensor_data):
    print(len(sensor_data))
    xlist = []
    ylist = []
    for angle in sensor_data.keys():
        xlist.append(math.cos(angle / 57.296) * sensor_data[angle])
        ylist.append(math.sin(angle / 57.296) * sensor_data[angle])
    plt.scatter(xlist,ylist)
    plt.scatter(0,0,color="red")
    plt.show()


