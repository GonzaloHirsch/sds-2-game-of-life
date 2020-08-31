import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import statistics
import itertools
import numpy as np

STAT_FILE = "./parsable_files/statistics.txt"
LIVING_FILE = "./parsable_files/living_percent_vs_time.txt"
DISPLACEMENT_FILE = "./parsable_files/radius_vs_time.txt"
TIME_FILE = "./parsable_files/time.txt"
LIVING = "Living"
DISPLACEMENT = "Displacement"

# Structure for the times dictionary
# dimension (2/3) -> {} (type)
# type (Living/Displacement) -> {} (rule)
# rule (1,2,3) -> {} (percentage)
# percentage -> time
def retrieveIterationTimes():
    tf = open(TIME_FILE, "r")
    times = {}
    for line in tf:
        data = line.rstrip("\n").split(" ")

        # Retrieving the parameters
        dimension = int(data[0])
        stat_type = data[1]
        percent = float(data[2])
        rule = int(data[3])
        time = int(data[4])

        if not dimension in times:
            times[dimension] = {}
        if not stat_type in times[dimension]:
            times[dimension][stat_type] = {}
        if not rule in times[dimension][stat_type]:
            times[dimension][stat_type][rule] = {}

        times[dimension][stat_type][rule][percent] = time
    return times

# Calculates the slope of the regression
# data -> Array with the values
# n -> Amount of values to be used
def calculateRegressionSlope(data, n):
    # Accounting for the 0
    size = n+1

    # Use num = n + 1 to account for the 0
    x = np.linspace(0, n, num=size)
    # Take items up to index n
    y = np.array(data[:size])

    s_x = np.sum(x)
    s_y = np.sum(y)
    s_xy = np.sum(x*y)
    s_xx = np.sum(x*x)

    top = n * s_xy - s_x * s_y
    bottom = n * s_xx - (s_x ** 2)

    if bottom == 0:
        return 0
    return top / bottom

# Extracts the statistics based on the output files
def extractStats(times):
    stats = {}

    lf = open(LIVING_FILE, "r")
    for line in lf:
        data = line.rstrip("\n").split(" ")

        # Retrieving the parameters
        dimension = int(data[0])
        percent = float(data[1])
        rule = int(data[2])

        if not dimension in stats:
            stats[dimension] = {}
        if not LIVING in stats[dimension]:
            stats[dimension][LIVING] = {}
        if not rule in stats[dimension][LIVING]:
            stats[dimension][LIVING][rule] = {}
        if not percent in stats[dimension][LIVING][rule]:
            stats[dimension][LIVING][rule][percent] = []

        casted_data = [float(x) for x in data[3:]]

        time = times[dimension][LIVING][rule][percent]
        velocity = calculateRegressionSlope(casted_data, time)

        stats[dimension][LIVING][rule][percent].append(velocity)

    sf = open(DISPLACEMENT_FILE, "r")
    for line in sf:
        data = line.rstrip("\n").split(" ")

        # Retrieving the parameters
        dimension = int(data[0])
        percent = float(data[1])
        rule = int(data[2])

        if not dimension in stats:
            stats[dimension] = {}
        if not DISPLACEMENT in stats[dimension]:
            stats[dimension][DISPLACEMENT] = {}
        if not rule in stats[dimension][DISPLACEMENT]:
            stats[dimension][DISPLACEMENT][rule] = {}
        if not percent in stats[dimension][DISPLACEMENT][rule]:
            stats[dimension][DISPLACEMENT][rule][percent] = []

        casted_data = [float(x) for x in data[3:]]

        time = times[dimension][DISPLACEMENT][rule][percent]
        velocity = calculateRegressionSlope(casted_data, time)

        stats[dimension][DISPLACEMENT][rule][percent].append(velocity)

    return stats

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


#Dim Displ/Living Rule percent velocity

times = retrieveIterationTimes()
stats = extractStats(times)

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
        if stat_type == 'Living':
            title = 'Average change in Living Cells for initial cell percentages per rule'
        else:
            title = 'Average expansion velocity for initial cell percentages per rule'

        plt.title(title)

        for rule in stats[dim][stat_type]:
            #Retrieving the data for the given dimension, stat_type and rule
            percentages, velocities, stds = organizeDataForRule(stats[dim][stat_type][rule])

            label = 'Rule ' + str(rule)
            plt.plot(percentages, velocities, label=label)

            plt.errorbar(percentages, velocities, yerr=stds, fmt='o', color='black',
                                 ecolor='lightgray', elinewidth=3, capsize=0)

        #Labelling the lines
        #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=3)
        plt.legend(bbox_to_anchor=(1,0.5), loc="center right", bbox_transform=plt.gcf().transFigure, fontsize=8, ncol=1)
        plt.gca().get_xaxis().set_minor_locator(MultipleLocator(10))
        plt.gca().get_yaxis().set_minor_locator(MultipleLocator(0.5))
        plt.xlim(0, 110)
        save_file = 'images/Dim' + str(dim) + str(stat_type) + 'stats.png'
        plt.savefig(save_file)

