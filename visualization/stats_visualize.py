import matplotlib.pyplot as plt
import statistics
import itertools
import numpy

def calculateVelocityMean(velocities):
    return statistics.mean(velocities)

def calculateVelocitySD(velocities, mean):
    if len(velocities) > 1:
        return statistics.stdev(velocities, mean)
    else:
        return 0
        

STAT_FILE = "./parsable_files/statistics.txt"

sf = open(STAT_FILE, "r")

percentage_stats = {}
percentages = []
velocities = []
stds = []

for line in sf:
	data = line.rstrip("\n").split(" ")
	percent = data[0]
	velocity = float(data[1])

	if not percent in percentage_stats:
		percentage_stats[percent] = []

	percentage_stats[percent].append(velocity)


# Calculate the average veocity and its standard error for a percentage
for percentage in percentage_stats:
    percentages.append(percentage)
    mean = calculateVelocityMean(percentage_stats[percentage])
    velocities.append(mean)
    stds.append(calculateVelocitySD(percentage_stats[percentage], mean))

# Set the x axis label
plt.xlabel('Initial Living Cells (%)')
# Set the y axis label
plt.ylabel('Average expansion velocity (displacement/frames)')
# Set a title of the current graph.
plt.title('Velocity of system\'s expansion from center\nbased on initial percentage of living cells')

# Ordering the data based on the percentages
percentages, velocities, stds = zip(*sorted(zip(percentages, velocities, stds)))

#Plotting and setting the standard error
plt.plot(percentages, velocities)
plt.errorbar(percentages, velocities, yerr=stds, fmt='o', color='black',
                     ecolor='lightgray', elinewidth=3, capsize=0);

plt.savefig('images/stats.png')
