import numpy as np
import random
import kinem
    #https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56


def QLearning(state_size, action_size):
    # Initialize q-table values to 0
    Q = np.zeros((state_size, action_size))

    # Set the percent you want to explore
    epsilon = 0.2
    if random.uniform(0, 1) < epsilon:
        """
        Explore: select a random action
        """
    else:
        """
        Exploit: select the action with max value (future reward)
        """    

def updateValues(Q,state,action):    
    Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) — Q[state, action])


if __name__ == "__main__":
    state_size = 2
    action_size = 2
    QLearning(state_size, action_size)
