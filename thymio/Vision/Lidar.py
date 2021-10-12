import math
from simple_kinematic_simulator import li
current = [1, 2, 3, 4, 5, 6]
p1 = [0, 2, 3, 4, 5, 6]
p2 = [0, 0, 3, 4, 5, 6]
p3 = [0, 0, 0, 4, 5, 6]

simulated = [p1, p2, p3]

def compare(current, simulated):
    differences = []
    for view in simulated:
        aux = []
        for i in range(view):
            aux.append(current[i] - simulated[i])
        differences.append(aux)
    sum  = []
    small = 0 
    for dif in differences:
        for i in range(dif):
            sum[i] = sum[i] + dif[i]
        print(sum)


if __name__ == "__main__":
    rest = 
    compare(current, simulated)
