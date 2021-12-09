import numpy as np

def get_behavioural_moves(observation, must_leave=False):
    lidar = observation[:18]
    camera_obs = observation[18:43]

    # if we see red
    if sum(camera_obs[:5])>= 1:
        if np.random.random() < 0.2:
            return [(500,-500, 1.5),(500,500, 3)]
        for idx, e in enumerate(camera_obs[:5]):
            if e == 1:
                if idx < 3:
                    return [(500,200, 1), (500,500, 2)]
                else:
                    return [(200,500, 1),(500,500, 2)]

    # if we see green
    if camera_obs[17] > 0:
        return [(400, 400, 1)]

    closest_thing = np.argmax(lidar)
    if max(lidar) > 0.7:
        if closest_thing <5:
            return [(200,500, 1)]
        if closest_thing <9:
            return [(400,500, 1)]
        if closest_thing <14:
            return [(500,400, 1)]
        if closest_thing <19:
            return [(500,200, 1)]

    if max(lidar) < 0.7:
        return [(-150, 150, 0)]

    if np.random.random() > 0.5:
        return [(150, 200, 1)]
    else:
        return [(200, 150, 1)]

def get_simu_behaviour(obs):
    ret = get_behavioural_moves(obs)
    l,r,s = ret[0]
    return l,r
