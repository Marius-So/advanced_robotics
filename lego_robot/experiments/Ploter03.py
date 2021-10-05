from matplotlib import colors
import matplotlib . pyplot as plt  # type: ignore
import numpy as np


data = np.genfromtxt("experiments\\Exp03.csv",
                          delimiter=",", names=["dist", "amb", "ref", "color"])


fig = plt.figure()

ax = fig.gca()

ax. errorbar(data['dist'], data['amb'], capsize=3.0, marker='o')
ax. errorbar(data['dist'], data['ref'], capsize=3.0, marker='o')

ax. set_xlabel('Advance [$mm$]')
ax. set_ylabel('Ambient, Reflection')
#ax. set_yscale ('log')
ax. legend(['Ambient ', 'Reflection '])
start = 28
width = 50 
plt.axvline(start, color='black', linestyle='--', linewidth=1)
plt.axvline(start + width, color='black', linestyle='--', linewidth=1)
#plt.show()
plt.savefig ('experiments\\Results03.png')
