import csv
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

NOVERSION = None
NOJUMP = -10
TRIPLEPERFO = 60
crubyMeans = []
crubyStdDevs = []
crubyVersions = []
crubyVersionsLine = []
crubyVersionsLineX = []
crubyJumps = []
sortedCrubyJumps = []
jrubyMeans = []
jrubyStdDevs = []
jrubyVersions = []
jrubyJumps = []
sortedJrubyJumps = []

for i in ['results.csv', 'jruby_results_flags.csv']:

	with open(i) as f:

		reader = csv.reader(f, delimiter=',')

		if i == 'jruby_results_flags.csv' :
			#try:
			#	reader = sorted(reader, key = lambda s: list(map(int, str(s[1])[6:].split('.'))))
			#except ValueError:
			#	print("x")
			#	reader = sorted(reader, key = lambda s: list(map(int, str(s[1])[6:].split('.'))))
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
				if row[0] == "cruby":
					crubyMeans.append(np.mean(times))
					crubyStdDevs.append(np.std(times))
					crubyVersions.append(row[1][5:])
					crubyVersionsLine.append(np.mean(times))
					crubyVersionsLineX.append(ind)
				else:
					jrubyMeans.append(np.mean(times))
					jrubyStdDevs.append(np.std(times))
					jrubyVersions.append(row[1])
				times.clear
			else:
				if row[0] == "cruby":
					crubyMeans.append(NOVERSION)
					crubyStdDevs.append(NOVERSION)
					crubyVersions.append(row[1][5:])
				else:
					jrubyMeans.append(NOVERSION)
					jrubyStdDevs.append(NOVERSION)
					jrubyVersions.append("x")
##cRuby

#Get Jump Values
crubyJumps.append(NOJUMP)
for i in range(1, len(crubyMeans)) :
	if (crubyMeans[i] != NOVERSION and crubyMeans[i-1] != NOVERSION) :
		crubyJumps.append(crubyMeans[i] - crubyMeans[i-1])
	else : 
		crubyJumps.append(NOJUMP)

#Finding max jump versions
print("cRuby:")
sortedCrubyJumps = crubyJumps.copy()
sortedCrubyJumps.sort(reverse = True)
for i in range(0, 10) :
	jumpVal = sortedCrubyJumps[i]
	print(jumpVal, end=', ')
	print(crubyVersions[crubyJumps.index(jumpVal)])


#Linear INterpolation
#xValsCruby = []

#for i in range(0, len(crubyVersions)) :
#	xValsCruby.append(i)
m, b = np.polyfit(crubyVersionsLineX, crubyVersionsLine, 1)

crubyLine = []

for i in crubyVersionsLineX :
	crubyLine.append(m*i + b)

#When to reach triple performance?

#goalVersion = (TRIPLEPERFO-b)/m
goalVersion = (2*b)/m
print("formula is y={}x + {}".format(m, b))
print("We wil reach 3x3 goal at version {}.".format(goalVersion))
print("This is in {} versions.".format(goalVersion-crubyVersionsLineX[len(crubyVersionsLineX)-1]))
print()


##jRuby

#Get Jump Values
jrubyJumps.append(NOJUMP)
for i in range(1, len(jrubyMeans)) :
	if (jrubyMeans[i] != NOVERSION and jrubyMeans[i-1] != NOVERSION) :
		jrubyJumps.append(jrubyMeans[i] - jrubyMeans[i-1])
	else : 
		jrubyJumps.append(NOJUMP)

#Finding max jump versions
print("jRuby:")
sortedJrubyJumps = jrubyJumps.copy()
sortedJrubyJumps.sort(reverse = True)
for i in range(0, 10) :
	jumpVal = sortedJrubyJumps[i]
	print(jumpVal, end=', ')
	print(jrubyVersions[jrubyJumps.index(jumpVal)])



#All manipulations done
CST=6

crubyX = [int(i)*CST for i in np.arange(0, len(crubyVersions)/CST)]
crubyVersionsPlot = (itemgetter(*crubyX)(crubyVersions))

plt.figure(figsize=(10, 7.6))
plt.plot(crubyMeans, 'ro', markersize=12)
plt.plot(crubyVersionsLineX, crubyLine, linewidth=6)
plt.yticks(fontsize=17)
plt.xticks(rotation=45, ha='right', fontsize=17)
plt.xticks(crubyX, crubyVersionsPlot)
plt.xlabel("cRuby Versions", fontsize=24)
plt.ylabel("Measured Result (fps)", fontsize=24)
#plt.title()
plt.tight_layout()
plt.savefig("figRubyMeans.png")
plt.show()
plt.clf()

plt.plot(crubyStdDevs, 'ro')
plt.xticks(rotation=90)
plt.xticks(crubyX, crubyVersionsPlot)
plt.savefig("figRubyStdDevs.png")
plt.clf()

plt.plot(crubyJumps, 'ro')
plt.xticks(rotation=90)
plt.xticks(crubyX, crubyVersionsPlot)
plt.savefig("figRubyJumps.png")
plt.clf()

jrubyX = [int(i)*CST for i in np.arange(0, len(jrubyVersions)/CST)]
jrubyVersionsPlot = itemgetter(*jrubyX)(jrubyVersions)

plt.plot(jrubyMeans, 'ro')
plt.xticks(rotation=30)
plt.xticks(jrubyX, jrubyVersionsPlot)
plt.savefig("figJrubyMeans.png")
plt.clf()

plt.plot(jrubyStdDevs, 'ro')
plt.xticks(rotation=90)
plt.xticks(jrubyX, jrubyVersionsPlot)
plt.savefig("figJrubyStdDevs.png")
plt.clf()

plt.plot(jrubyJumps, 'ro')
plt.xticks(rotation=90)
plt.xticks(jrubyX, jrubyVersionsPlot)
plt.savefig("figJrubyJumps.png")
plt.clf()
	