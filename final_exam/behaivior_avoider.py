import numpy as np

def get_behavioral_moves(observation, must_leave=False):
    lidar = observation[:20]
    camera_obs = observation[20:45]
    if must_leave:
        if sum(camera_obs[:5])>= 1:
            return [(-300,-300,2)]
        else:
            return [(300, 300, 2)]

    if max(lidar) == 0:
        return [(0, 0, 2)]
    if sum(camera_obs[16:18])>1:
        print('i see green')
        x = 400
        y = 400
        return [(400, 400, 1)]
    if sum(camera_obs[:5])>= 1:
        print('i see red')
        x = -500
        y = -300
        for idx, e in enumerate(camera_obs[:5]):
            if e == 1:
                if idx < 3:
                    return [(x,y - (100 * idx), 1)]
                else:
                    return [(x + ((idx-2)*100), x, 1)]
    closest_thing = np.argmax(lidar)
    if max(lidar) > 0.7:
        if closest_thing <5:
            return [(-300,-500, 1)]
        if closest_thing <10:
            return [(300,500, 1)]
        if closest_thing <15:
            return [(300,400, 1)]
        if closest_thing <20:
            return [(500,300, 1)]
    # when he sees red
        # if he sees green
    if sum(camera_obs[16:18])>1:
        print('i see green')
        x = 400
        y = 400
        return [(400, 400, 1)]
    if max(lidar[:-5]+lidar[16:]) > 0.7:
        return [(500, 500, 4)]
    if max(lidar[5:16]) > 0.6:
        if np.random.random() > 0.5:
            return [(-350, -500, 3)]
        else:
            return [(-500, -350, 3)]
    if np.random.random() > 0.5:
        return [(500, 400, 1)]
    else:
        return [(400, 500, 1)]

def get_simu_behavior(obs):
    ret = get_behavioral_moves(obs)
    l,r,s = ret[0]
    return l,r
