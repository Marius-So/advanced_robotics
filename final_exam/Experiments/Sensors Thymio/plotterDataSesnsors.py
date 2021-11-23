import matplotlib . pyplot as plt # type: ignore
import numpy as np
import csv

with open('dataSensorsThymio.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

distances = data[0]
avg = []
std = []

for m in range(len(data[0])):
    aux = []
    for d in range(1,6):
        measures = data[d][m]
        aux.append(int(measures))
    avg.append(np.mean(aux))
    std.append(np.std(aux))


#nameList = {'Same', 'Increasing', 'Decreasing', 'Permutation'}

fig = plt.figure ()
ax = fig.gca()

ax. errorbar (distances, avg, std, capsize = 3.0,markersize = 4.0, marker = 'o', color = "royalblue" )

plt.grid(axis='y', alpha=0.75)
ax. set_xlabel ('Distance $[mm]$')
ax. set_ylabel ('Value')
#ax. set_yscale ('log')
plt.xticks(rotation=45)
#plt.show()
plt.savefig('FigureThymioSensors.png',bbox_inches="tight")
