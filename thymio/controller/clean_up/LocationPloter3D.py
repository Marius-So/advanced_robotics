import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


d = np.genfromtxt("thymio\\data\\DataLocationExperiments.csv", delimiter=",", names=["Depth", "x","y","Distance"])
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
#X = np.arange(-5, 5, 0.25)
#Y = np.arange(-5, 5, 0.25)
#X, Y = np.meshgrid(X, Y)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)
X = d["x"]
Y = d["y"]
Z = d["Depth"]

#https://superuser.com/questions/1328448/3d-plot-with-matplotlib-from-imported-data here is the solution

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
#ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()