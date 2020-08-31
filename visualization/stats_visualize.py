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

def organizeDataForRule(data):
    percentages = []
    means = []
    stds = []

    for percent in data:
        percentages.append(percent)
        means.append(data[percent]['mean'])
        stds.append(data[percent]['std'])

    percentages, velocities, stds = zip(*sorted(zip(percentages, means, stds)))
    return percentages, velocities, stds


STAT_FILE = "./parsable_files/statistics.txt"

#Dim Displ/Living Rule percent velocity

sf = open(STAT_FILE, "r")

stats = {}
percentages = []
velocities = []
stds = []

for line in sf:
	data = line.rstrip("\n").split(" ")

	# Retrieving the parameters
	dimension = data[0]
	stat_type = data[1]
	rule = data[2]
	percent = float(data[3])
	velocity = float(data[4])
	
	if not dimension in stats:
    		stats[dimension] = {}
	if not stat_type in stats[dimension]:
		stats[dimension][stat_type] = {}
	if not rule in stats[dimension][stat_type]:
		stats[dimension][stat_type][rule] = {}
	if not percent in stats[dimension][stat_type][rule]:
		stats[dimension][stat_type][rule][percent] = []

	stats[dimension][stat_type][rule][percent].append(velocity)

for dimension in stats:
    for stat_type in stats[dimension]:
        for rule in stats[dimension][stat_type]:
            for percent in stats[dimension][stat_type][rule]:
                mean = calculateVelocityMean(stats[dimension][stat_type][rule][percent])
                std = calculateVelocitySD(stats[dimension][stat_type][rule][percent], mean)
                stats[dimension][stat_type][rule][percent] = {'mean': mean, 'std': std}

for dim in stats:
    # For each dimension and each stat_type (displacement or living)
    # a separate graph will be created
    for stat_type in stats[dim]:
        plt.clf()

        # Set the x axis label
        plt.xlabel('Initial Living Cells (%)')

        # Set the y axis label
        if stat_type == 'Living':
            y_label = 'Average change in Living Cells (cells/frames)'
        else:
            y_label = 'Average expansion velocity (displacement/frames)'

        plt.ylabel(y_label)

        # Set a title of the current graph.
        plt.title('TO BE DETERMINED DEPENDING ON THE CASE')

        for rule in stats[dim][stat_type]:
            #Retrieving the data for the given dimension, stat_type and rule
            percentages, velocities, stds = organizeDataForRule(stats[dim][stat_type][rule])

            label = 'Rule ' + rule
            plt.plot(percentages, velocities, label=label)

            #Labelling the lines
            plt.legend()

            plt.errorbar(percentages, velocities, yerr=stds, fmt='o', color='black',
                                 ecolor='lightgray', elinewidth=3, capsize=0);

        save_file = 'images/Dim' + dim + stat_type + 'stats.png'
        plt.savefig(save_file)

