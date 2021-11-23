from Thymio import Thymio
import time
import csv


def test_colors(thymioController):
    thymioController.set_speed(0, 0)
    thymioController.run()

    for colour in ['red', 'orange', 'blue', 'green', 'purple']:
        time.sleep(3)
        print(colour)
        thymioController.set_colour(colour)
        thymioController.set_speed(0, 0)
        # thymioController.play_tune()
    thymioController.stop()
    del thymioController


def test_movements(thymioController):
    thymioController.set_speed(0, 0)
    thymioController.sleep(2)
    thymioController.set_speed(1, 0)
    thymioController.sleep(2)
    thymioController.set_speed(0, 1)
    thymioController.sleep(2)
    thymioController.set_speed(-2, -2)
    thymioController.sleep(2)
    thymioController.set_speed(0, 0)

def writeCsv(data):
     with open('DataThymioSensorsReading.csv',  'w', newline='') as myfile:
        wr = csv.writer(myfile)
        for run in range(len(data)):
                row = []
                row.append(run)
                for m in data[run]:
                    row.append(m)
                wr.writerow(row)

def test_sensors(thymioController):
    """
    This is for the characterization of the sensors.
    """
    #v = d/t
    t = 0.5
    step = 1  # mm
    distance = 0
    data = [[]]
    run = []
    for i in range(5):
        while distance < 100:
            thymioController.set_colour("red")
            thymioController.set_speed(-step, -step)
            # take messurements and save them in the list
            # run.append(messurement)
            thymioController.sleep(2)
            distance = distance + step
        data.append(run)
        run.clear()
        print("Set the experiment again")
        thymioController.sleep(5)
    
    writeCsv(data)

if __name__ == '__main__':
    # check command-line arguments
    # create and run controller
    thymioController = Thymio()
    # test_colors(thymioController)
    #test_movements(thymioController)
    test_sensors(thymioController)