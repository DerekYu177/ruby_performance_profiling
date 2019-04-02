import csv
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

with open('results.csv') as f:
	reader = csv.reader(f, delimiter=',')
	crubyMeans = []
	crubyStdDevs = []
	crubyVersions = []
	jrubyMeans = []
	jrubyStdDevs = []
	jrubyVersions = []
	for row in reader:
		if len(row) == 7:
			times = []
			for i in range(2, 7):
				timeString = row[i].split(" ")[1]
				times.append(float(timeString))

			#Basic stats calculation
			if row[0] == "cruby":
				crubyMeans.append(np.mean(times))
				crubyStdDevs.append(np.std(times))
				crubyVersions.append(row[1])
			else:
				jrubyMeans.append(np.mean(times))
				jrubyStdDevs.append(np.std(times))
				jrubyVersions.append(row[1])
			times.clear
		else:
			if row[0] == "cruby":
				crubyMeans.append(-1)
				crubyStdDevs.append(-1)
				crubyVersions.append("x")
			else:
				jrubyMeans.append(-1)
				jrubyStdDevs.append(-1)
				jrubyVersions.append("x")

	#All manipulations done
	CST=4

	crubyX = [int(i)*CST for i in np.arange(0, len(crubyVersions)/CST)]
	crubyVersionsPlot = itemgetter(*crubyX)(crubyVersions)

	plt.plot(crubyMeans, 'ro')
	plt.xticks(rotation=90)
	plt.xticks(crubyX, crubyVersionsPlot)
	plt.savefig("figRubyMeans.png")
	plt.clf()

	plt.plot(crubyStdDevs, 'ro')
	plt.xticks(rotation=90)
	plt.xticks(crubyX, crubyVersionsPlot)
	plt.savefig("figRubyStdDevs.png")
	plt.clf()

	jrubyX = [int(i)*CST for i in np.arange(0, len(jrubyVersions)/CST)]
	jrubyVersionsPlot = itemgetter(*jrubyX)(jrubyVersions)

	plt.plot(jrubyMeans, 'ro')
	plt.xticks(rotation=90)
	plt.xticks(jrubyX, jrubyVersionsPlot)
	plt.savefig("figJrubyMeans.png")
	plt.clf()

	plt.plot(jrubyStdDevs, 'ro')
	plt.xticks(rotation=90)
	plt.xticks(jrubyX, jrubyVersionsPlot)
	plt.savefig("figJrubyStdDevs.png")
	plt.clf()
	