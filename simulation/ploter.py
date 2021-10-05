import matplotlib.pyplot as plt
from math import cos, sin

file1 = open("trajectory.dat", "r")
lines = file1.readlines()
cornersx = [-1, -1, 1, 1]
cornersy = [-1, 1, -1, 1]
x = []
y = []
dx = []
dy = []

step = [0]
angle = []
i = 0
for line in lines:
    if i % 5 == 0:
        a, b, angle = line.split(",")
        plt.arrow(float(a),float(b), 0.5 * cos(float(angle)), 0.5 * sin(float(angle)), width=0.01)
    i += 1

plt.scatter(cornersx,cornersy)
plt.show()
plt.savefig("test.png")

