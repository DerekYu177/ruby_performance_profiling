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

for file in ['jruby_results3_date.csv', 'jruby_results_flags2_date.csv']:

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
				if file == 'jruby_results3_date.csv':
					crubyMeans.append(np.mean(times))
					crubyVersions.append(row[1][5:])
					
					crubyVersionsLine.append(np.mean(times))
					crubyVersionsLineX.append(int(row[2])-144)

					crubyVersionsX.append(int(row[2]))


				else:
					jrubyVersionsLine.append(np.mean(times))
					jrubyVersionsLineX.append(int(row[2])-144)
				times.clear

#Get Jump Values
crubyJumps.append(NOJUMP)
for i in range(1, len(crubyMeans)) :
	if (crubyMeans[i] != NOVERSION and crubyMeans[i-1] != NOVERSION) :
		crubyJumps.append(crubyMeans[i] - crubyMeans[i-1])
		#if crubyMeans[i] < crubyMeans[i-1] :
			#print("Version {}, value: {}".format(crubyVersions[len(crubyJumps)-1], crubyMeans[i] - crubyMeans[i-1]))
	else : 
		crubyJumps.append(NOJUMP)

#Finding max jump versions
print("cRuby:")
sortedCrubyJumps = crubyJumps.copy()
sortedCrubyJumps.sort()
for i in range(0, 10) :
	jumpVal = sortedCrubyJumps[i]
	print(jumpVal, end=', ')
	print(crubyVersions[crubyJumps.index(jumpVal)])


#Linear INterpolation
#xValsCruby = []

#for i in range(0, len(crubyVersions)) :
#	xValsCruby.append(i)

#true if dates
if False :
	m, b = np.polyfit(newLineX, newLine, 1)
else:
	m, b = np.polyfit(crubyVersionsLineX, crubyVersionsLine, 1)

crubyLine = []

for i in crubyVersionsLineX :
	crubyLine.append(m*i + b)

#When to reach triple performance?



goalVersion = (73.05055-b)/m
#goalVersion = (2*b)/m
print("formula is y={}x + {}".format(m, b))
print("We wil reach 3x3 goal at version {}.".format(goalVersion))
print("This is in {} versions.".format(goalVersion-crubyVersionsLineX[len(crubyVersionsLineX)-1]))
print()

#All manipulations done
CST=6

crubyX = [int(i)*CST for i in np.arange(0, len(crubyVersions)/CST)]
crubyVersionsPlot = (itemgetter(*crubyX)(crubyVersions))

allXs = [i for i in range(2131)]



#print(jrubyVersionsLine)

plt.figure(figsize=(10, 7.6))
#plt.plot(crubyMeans, 'ro', markersize=12) #NODATE
plt.plot(crubyVersionsLineX, crubyVersionsLine, 'ro', markersize=12, alpha = 1)
#plt.plot(jrubyVersionsLineX, jrubyVersionsLine, 'bo', markersize=12)
plt.plot(crubyVersionsLineX, crubyLine, linewidth=6, alpha=1)
plt.yticks(fontsize=17)
plt.xticks(fontsize=17)
#plt.xticks(rotation=45, ha='right', fontsize=17) #NODATE
#plt.xticks(crubyX, crubyVersionsPlot) #NODATE
plt.xlabel("Time Since Original Version (days)", fontsize=24) #DATE
#plt.xlabel("cRuby Versions", fontsize=24) #NODATE
plt.ylabel("Performance (fps)", fontsize=24)
#plt.title()
plt.ylim(top=36)
plt.tight_layout()
plt.savefig("figRubyMeans.png")
plt.show()
plt.clf()
	