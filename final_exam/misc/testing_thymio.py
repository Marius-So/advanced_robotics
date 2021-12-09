from Thymio import Thymio
import time
import csv
import numpy as np


def test_colors(thymioController):
    thymioController.set_speed(0, 0)
    #thymioController.run()

    for colour in ['red', 'orange', 'blue', 'green', 'purple']:
        time.sleep(3)
        print(colour)
        thymioController.set_colour(colour)
        thymioController.set_speed(0, 0)
        thymioController.get_sensor_values()
        # thymioController.play_tune()


def test_movements(thymioController):
    l = int(input('l_speed :'))
    r = int(input('r_speed :'))
    thymioController.set_speed(l, r)
    time.sleep(5)
    thymioController.set_speed(0, 0)

def writeCsv(data, name='DataThymioSensorsReading.csv'):
     with open(name,  'w', newline='') as myfile:
        wr = csv.writer(myfile)
        #for i in range()
        wr.writerow([i * 5 for i in range(len(data[0]))])
        for run in data:
            wr.writerow(run)

def test_sensors(thymioController):
    """
    This is for the characterization of the sensors.
    """
    #v = d/t
    d = 30/1.83

    d1 = []
    d2 = []
    d3 = []
    r1 = []
    r2 = []
    r3 = []
    for i in range(5):
        for j in range(26):
            thymioController.set_colour("red")
            thymioController.set_speed(-d*1.1, -d)
            time.sleep(1)
            thymioController.set_speed(0, 0)
            time.sleep(0.5)
            step = thymioController.get_sensor_values()[0]
            print(thymioController.get_sensor_values())
            # take messurements and save them in the list
            r1.append(step[0])
            r2.append(step[2])
            r3.append(step[4])

        thymioController.set_speed(d, d)
        time.sleep(30)
        thymioController.set_speed(0, 0)

        d1.append(np.array(r1,dtype= np.int32))
        d2.append(np.array(r2,dtype= np.int32))
        d3.append(np.array(r3,dtype= np.int32))
        r1 = []
        r2 = []
        r3= []

        thymioController.set_colour("blue")
        print("Set the experiment again")
        time.sleep(1)

    writeCsv(d1, 'd1.csv' )
    writeCsv(d2, 'd2.csv')
    writeCsv(d3, 'd3.csv')

if __name__ == '__main__':
    # check command-line arguments
    # create and run controller
    thymioController = Thymio()
    test_colors(thymioController)
    thymioController.set_colour('red')
    for i in range(10):
        test_movements(thymioController)
    #for i in range(1):
    #    test_colors(thymioController)
    #test_movements(thymioController)
    #test_sensors(thymioController)
    #while True:
     #   time.sleep(1)
     #   print(np.array(thymioController.get_sensor_values()[0]))


