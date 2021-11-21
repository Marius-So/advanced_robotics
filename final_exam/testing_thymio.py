from Thymio import Thymio
import time

def main():
    # check command-line arguments
    # create and run controller
    thymioController = Thymio()
    thymioController.set_speed(0,0)
    thymioController.run()

    for colour in ['red','orange','blue','green','purple']:
        time.sleep(3)
        print(colour)
        thymioController.set_colour(colour)
        thymioController.set_speed(0,0)
        #thymioController.play_tune()
    thymioController.stop()
    del thymioController

if __name__ == '__main__':
    main()
