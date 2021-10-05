from matplotlib import colors
import matplotlib . pyplot as plt  # type: ignore
import numpy as np


whiteData = np.genfromtxt("experiments\\Exp01.csv",
                          delimiter=",", names=["dist", "amb", "ref"])
fig = plt.figure()

ax = fig.gca()

ax. errorbar(whiteData['dist'], whiteData['amb'], capsize=3.0, marker='o')
ax. errorbar(whiteData['dist'], whiteData['ref'], capsize=3.0, marker='o')

ax. set_xlabel('Distance [$mm$]')
ax. set_ylabel('Ambient, Reflection')
#ax. set_yscale ('log')
ax. legend(['Ambient ', 'Reflection '])
plt.axvline(2, color='black', linestyle='--', linewidth=1)
plt.axvline(16, color='black', linestyle='--', linewidth=1)
#plt.show()
plt.savefig ('experiments\\Results01.png')
