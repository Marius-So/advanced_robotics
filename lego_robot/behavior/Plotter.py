from matplotlib import colors
import matplotlib . pyplot as plt # type: ignore
import numpy as np

#For 1 Can.
c10 = np.genfromtxt("ResultsData1can10.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])
c25 = np.genfromtxt("ResultsData1can25.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])
c50 = np.genfromtxt("ResultsData1can50.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])

#For 2 Cans.
cc10 = np.genfromtxt("ResultsData2can10.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])
cc25 = np.genfromtxt("ResultsData2can25.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])
cc50 = np.genfromtxt("ResultsData2can50.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])

#Explored states vs Size of the maze for different infills both 1 and two cans
fig = plt.figure ()
ax = fig.gca()

ax. errorbar (c10["Size"], c10["States"], c10["SSd"], capsize = 3.0 , marker = 's', )
ax. errorbar (c25["Size"], c25["States"], c25["SSd"], capsize = 3.0 , marker = 's', )
ax. errorbar (c50["Size"], c50["States"], c50["SSd"], capsize = 3.0 , marker = 's', )

ax. errorbar (cc10["Size"], cc10["States"], cc10["SSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )
ax. errorbar (cc25["Size"], cc25["States"], cc25["SSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )
ax. errorbar (cc50["Size"], cc50["States"], cc50["SSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )

ax. set_xlabel ('Size of the board $nxn$')
ax. set_ylabel ('Explored States')
ax. set_yscale ('log')
ax. legend ([ '1 Can 10% Infill', '1 Can 25% Infill', '1 Can 50% Infill','2 Cans 10% Infill', '2 Cans 25% Infill', '2 Cans 50% Infill'])

#plt.show()
#plt.savefig ('Figure StatesVsStateOneCan.png')

#Time vs Size of the maze for different infills both 1 and two cans
fig = plt.figure ()
ax = fig.gca()

ax. errorbar (c10["Size"], c10["Time"], c10["TSd"], capsize = 3.0 , marker = 's', )
ax. errorbar (c25["Size"], c25["Time"], c25["TSd"], capsize = 3.0 , marker = 's', )
ax. errorbar (c50["Size"], c50["Time"], c50["TSd"], capsize = 3.0 , marker = 's', )

ax. errorbar (cc10["Size"], cc10["Time"], cc10["TSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )
ax. errorbar (cc25["Size"], cc25["Time"], cc25["TSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )
ax. errorbar (cc50["Size"], cc50["Time"], cc50["TSd"],linestyle="dashed", capsize = 3.0 , marker = 'o', )

ax. set_xlabel ('Size of the board $nxn$')
ax. set_ylabel ('Time[seg]')
ax. set_yscale ('log')
ax. legend ([ '1 Can 10% Infill', '1 Can 25% Infill', '1 Can 50% Infill','2 Cans 10% Infill', '2 Cans 25% Infill', '2 Cans 50% Infill'])

#plt.show()
#plt.savefig ('Time StatesVsStateOneCan.png')

#Time vs States
timeState = np.genfromtxt("StatesvsTime.csv", delimiter=",", names=["Size", "States","SSd","Time", "TSd"])
fig = plt.figure ()
ax = fig.gca()

ax. errorbar (timeState["States"], timeState["Time"], timeState["TSd"], capsize = 3.0 , marker = 'o', )

ax. set_xlabel ('Explored States')
ax. set_ylabel ('Time[seg]')
ax. set_yscale ('log')
#plt.show()
plt.savefig ('TimevsState.png')