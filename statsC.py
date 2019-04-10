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

for file in ['cruby_results2.csv', 'jruby_results_flags2.csv']:

	with open(file) as f:

		if file == 'cruby_results2.csv' :
			reader = reversed(list(csv.reader(f, delimiter=',')))
		else :
			reader = csv.reader(f, delimiter=',')

		if file == 'jruby_results_flags2.csv' :
			#try:
			#	reader = sorted(reader, key = lambda s: list(map(int, str(s[1])[6:].split('.'))))
			#except ValueError:
			#	print("x")
			#	reader = sorted(reader, key = lambda s: list(map(int, str(s[1])[6:].split('.'))))
			reader = sorted(reader, key = lambda s: list(map(int, ((str((s[1].split('-'))[1])).split('.'))[:3])))
		
		ind = 0
		max = 7
		min = 2
		localMaxVersion = 0
		if file == 'cruby_results2_date.csv' :
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
				if row[0] == "cruby":
					crubyMeans.append(np.mean(times))
					crubyStdDevs.append(np.std(times))
					crubyVersions.append(row[1][5:])
					
					crubyVersionsLine.append(np.mean(times))
					if file == 'cruby_results2_date.csv' :
						crubyVersionsLineX.append(int(row[2]))
						crubyVersionsX.append(int(row[2]))
						if int(row[1][7]) >= localMaxVersion:
							localMaxVersion = int(row[1][7])
							newLineX.append(int(row[2]))
							newLine.append(np.mean(times))
							newLineV.append(row[1])
					else :
						crubyVersionsLineX.append(ind)
						if int(row[1][7]) > 2 or (int(row[1][7]) == 2 and int(row[1][9]) >= 6) or (int(row[1][7]) == 2 and len(row[1]) == 11) :
							newLineX.append(ind-1)
							newLine.append(np.mean(times))
							newLineV.append(row[1])

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
					if file == 'cruby_results2_date.csv' :
						crubyVersionsX.append(int(row[2]))
				else:
					jrubyMeans.append(NOVERSION)
					jrubyStdDevs.append(NOVERSION)
					jrubyVersions.append("x")

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
if True :
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

plt.figure(figsize=(10, 7.6))
plt.plot(crubyMeans, 'ro', markersize=12) #NODATE
#plt.plot(crubyVersionsX, crubyMeans, 'ro', markersize=12) #DATE
#plt.plot(newLineX, newLine, 'go', markersize=12, markeredgewidth=2, markeredgecolor='g') #MAYBE
plt.plot(crubyVersionsLineX, crubyLine, linewidth=6, alpha=0)
plt.yticks(fontsize=17)
plt.xticks(fontsize=17)
plt.xticks(rotation=45, ha='right', fontsize=17) #NODATE
plt.xticks(crubyX, crubyVersionsPlot) #NODATE
#plt.xlabel("Time Since Original Version (days)", fontsize=24) #DATE
plt.xlabel("cRuby Versions", fontsize=24) #NODATE
plt.ylabel("Performance (fps)", fontsize=24)
#plt.title()
plt.ylim(bottom=21)
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
	