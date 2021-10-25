from matplotlib import colors
import matplotlib . pyplot as plt # type: ignore
import numpy as np

d = np.genfromtxt("thymio\\data\\DataLocationExperiments.csv", delimiter=",", names=["Depth", "x","y","Distance"])
fig = plt.figure ()
ax = fig.gca()

ax. errorbar (d["Depth"], d["Distance"], capsize = 3.0 , marker = 's', )

ax. set_xlabel ('Iteration')
ax. set_ylabel ('Distance to target')
#ax. set_yscale ('log')
ax. legend (['Distance to target'])

plt.show()
#plt.savefig ('Figure StatesVsStateOneCan.png')

