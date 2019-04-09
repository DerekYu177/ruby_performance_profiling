import csv
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

NOVERSION = None
NOJUMP = -10
TRIPLEPERFO = 18.69 * 3
crubyMeans = []
crubyStdDevs = []
crubyVersions = []

crubyVersionsLine = []
crubyVersionsLineX = []

jrubyVersionsLine = []
jrubyVersionsLineX = []


crubyVersionsX = []
crubyJumps = []

newLineX = []
newLine = []
newLineV = []



sortedCrubyJumps = []
jrubyMeans = []
jrubyStdDevs = []
jrubyVersions = []
jrubyJumps = []
sortedJrubyJumps = []

for file in ['cruby_results2_date.csv', 'jruby_results_flags2_date.csv']:

	with open(file) as f:

		reader = csv.reader(f, delimiter=',')

		
		ind = 0
		localMaxVersion = 0
		max = 8
		min = 3

		for row in reader:
			ind+=1
			if len(row) == max:
				times = []
				for i in range(min, max):
					timeString = row[i].split(" ")[1]
					times.append(float(timeString))

				#Basic stats calculation
				if file == 'cruby_results2_date.csv':
				
					crubyVersionsLine.append(np.mean(times))
					crubyVersionsLineX.append(int(row[2]))
					if int(row[1][7]) >= localMaxVersion:
							localMaxVersion = int(row[1][7])
							newLineX.append(int(row[2]))
							newLine.append(np.mean(times))

				else:
					if np.mean(times) > 24 :
						jrubyVersionsLine.append(np.mean(times))
						jrubyVersionsLineX.append(int(row[2]))
				times.clear

#Linear INterpolation
#xValsCruby = []

#for i in range(0, len(crubyVersions)) :
#	xValsCruby.append(i)

#true if dates

mc, bc = np.polyfit(crubyVersionsLineX, crubyVersionsLine, 1)
mj, bj = np.polyfit(jrubyVersionsLineX, jrubyVersionsLine, 1)
mnew, bnew = np.polyfit(newLineX, newLine, 1)

crubyLine = []
jrubyLine = []
newRubyLine = []

for i in crubyVersionsLineX :
	crubyLine.append(mc*i + bc)

for i in jrubyVersionsLineX :
	jrubyLine.append(mj*i + bj)

for i in newLineX :
	newRubyLine.append(mnew*i + bnew)

#print(jrubyVersionsLine)

plt.figure(figsize=(10, 7.6))
#plt.plot(crubyMeans, 'ro', markersize=12) #NODATE
plt.plot(crubyVersionsLineX, crubyVersionsLine, 'ro', markersize=15, alpha = 0.15)
plt.plot(newLineX, newLine, 'ro', markersize=15, markeredgewidth = 2, markeredgecolor = "k", alpha = 1)
plt.plot(jrubyVersionsLineX, jrubyVersionsLine, 'bo', markeredgewidth = 2, markeredgecolor = "k", markersize=15, alpha = 1)
#plt.plot(jrubyVersionsLineX, jrubyLine, linewidth=7)
#plt.plot(newLineX, newRubyLine, linewidth=7)


plt.yticks(fontsize=17)
plt.xticks(fontsize=17)
#plt.xticks(rotation=45, ha='right', fontsize=17) #NODATE
#plt.xticks(crubyX, crubyVersionsPlot) #NODATE
plt.xlabel("Time Since Original Version (days)", fontsize=24) #DATE
#plt.xlabel("cRuby Versions", fontsize=24) #NODATE
plt.ylabel("Measured Result (fps)", fontsize=24)
#plt.title()
plt.ylim(bottom=21)
plt.tight_layout()
plt.savefig("figRubyMeans.png")
plt.show()
plt.clf()
	