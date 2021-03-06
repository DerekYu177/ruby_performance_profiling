import csv
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

THRESHOLD = 25
NOVERSION = None
NOJUMP = -10
TRIPLEPERFO = 60
crubyMeans = []
crubyStdDevs = []
crubyVersions = []
crubyVersionsLine = []
crubyVersionsLineX = []
crubyVersionsX = []
crubyJumps = []

newLineX = []
newLine = []
newLineVals = []

belowThresh = []
aboveThresh = []

sortedCrubyJumps = []
jrubyMeans = []
jrubyStdDevs = []
jrubyVersions = []
jrubyJumps = []
sortedJrubyJumps = []


for file in ['jruby_results3.csv', 'jruby_results_flags3.csv']:

	with open(file) as f:

		reader = csv.reader(f, delimiter=',')

		reader = sorted(reader, key = lambda s: list(map(int, ((str((s[1].split('-'))[1])).split('.'))[:3])))
		
		ind = 0

		for row in reader:
			ind+=1
			if len(row) == 7:
				times = []
				for i in range(2, 7):
					timeString = row[i].split(" ")[1]
					times.append(float(timeString))

				#Basic stats calculation
				if file == 'jruby_results3.csv':
					crubyMeans.append(np.mean(times))
					crubyStdDevs.append(np.std(times))
					crubyVersions.append(row[1][6:])
					newLine.append(np.mean(times))
					newLineX.append(ind-1)
				else:
					#withFlags
					jrubyMeans.append(np.mean(times))
					jrubyStdDevs.append(np.std(times))
					jrubyVersions.append(row[1][6:])
					if np.mean(times) > THRESHOLD :
						aboveThresh.append(row[1])
					else :
						belowThresh.append(row[1])
				times.clear
			else:
				if file == 'jruby_results3.csv':
					crubyMeans.append(NOVERSION)
					crubyStdDevs.append(NOVERSION)
					crubyVersions.append(row[1][6:])
				else:
					jrubyMeans.append(NOVERSION)
					jrubyStdDevs.append(NOVERSION)
					jrubyVersions.append(row[1][6:])

##jRuby

print("Versions below Threshold of {}:".format(THRESHOLD))

for i in belowThresh :
	print(i)
print()
print("Versions above Threshold of {}:".format(THRESHOLD))

for i in aboveThresh :
	print(i)

m, b = np.polyfit(newLineX, newLine, 1)

print(m)

for i in newLineX :
	newLineVals.append(m*i + b)


#Get Jump Values
#jrubyJumps.append(NOJUMP)
#for i in range(1, len(jrubyMeans)) :
#	if (jrubyMeans[i] != NOVERSION and jrubyMeans[i-1] != NOVERSION) :
#		jrubyJumps.append(jrubyMeans[i] - jrubyMeans[i-1])
#	else : 
#		jrubyJumps.append(NOJUMP)

#Finding max jump versions
#print("jRuby:")
#sortedJrubyJumps = jrubyJumps.copy()
#sortedJrubyJumps.sort(reverse = True)
#for i in range(0, 10) :
#	jumpVal = sortedJrubyJumps[i]
#	print(jumpVal, end=', ')
#	print(jrubyVersions[jrubyJumps.index(jumpVal)])



#All manipulations done
CST=6

crubyX = [int(i)*CST for i in np.arange(0, len(crubyVersions)/CST)]
crubyVersionsPlot = (itemgetter(*crubyX)(crubyVersions))

allXs = [i for i in range(2131)]

plt.figure(figsize=(10, 7.6))
plt.plot(crubyVersions, crubyMeans, 'ro', markersize=12)
plt.plot(jrubyVersions, jrubyMeans, 'bo', markersize=12, alpha = 0.5)
#plt.plot(newLineX, newLineVals, linewidth=7)
plt.yticks(fontsize=17)
plt.xticks(fontsize=17)
plt.xticks(rotation=45, ha='right', fontsize=17)
plt.xticks(crubyX, crubyVersionsPlot)
plt.xlabel("jRuby Versions", fontsize=24)
plt.ylabel("Performance (fps)", fontsize=24)
#plt.title()
plt.tight_layout()
plt.ylim(top=36)
plt.savefig("figRubyMeans.png")
plt.show()
plt.clf()