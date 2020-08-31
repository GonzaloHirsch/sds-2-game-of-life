import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Must specify the name of the file to parse and the type being parsed: Living or Radius")
    exit(1)

file_name = sys.argv[1]
y_type = sys.argv[2]

f = open(file_name, "r")

# Parsing -> Dimension porcentaje regla valores

evolution = []
time = []
stats = {}
repetitions = {}

# Variables that must be changed depending on the regression line we want
show_regression = False
reg_time_limit = 50

for line in f:
    time = 0
    data = line.rstrip("\n").split(" ")
    dim = data[0]
    percentage = data[1]
    rule = int(data[2])

    if dim not in stats:
        stats[dim] = {}
        repetitions[dim] = {}
    if percentage not in stats[dim]:
        stats[dim][percentage] = {}
        repetitions[dim][percentage] = {}
    if rule not in stats[dim][percentage]:
        stats[dim][percentage][rule] = {}
        stats[dim][percentage][rule]['evolution'] = []
        stats[dim][percentage][rule]['time'] = []
        repetitions[dim][percentage][rule] = {}
        repetitions[dim][percentage][rule]['evolution'] = 0

        evolution_data = []
        time_data = []

        while time < (len(data) - 3):
            evolution_data.append(float(data[time + 3]))
            time_data.append(float(time))
            time += 1

        stats[dim][percentage][rule]['evolution'].append(evolution_data)
        stats[dim][percentage][rule]['time'].append(time_data)
        repetitions[dim][percentage][rule]['evolution'] += 1

for dim in stats:
    for percentage in stats[dim]:
        plt.clf()

        # Set the x axis label
        plt.xlabel('Time (frames)')

        # Set the y axis label
        if y_type == 'Living':
            ylabel = 'Percentage of Living Cells (%)'
        else:
            ylabel = 'Maximum displacement from center'
        plt.ylabel(ylabel)

        # Set a title of the current graph.
        plt.title(dim + 'D & ' + str(int(float(percentage))) + '%: ' + ylabel + ' vs. Time')

        for rule in stats[dim][percentage]:
            evolution = stats[dim][percentage][rule]['evolution']
            time = stats[dim][percentage][rule]['time']

            evolution_mean = np.zeros(len(evolution[0]))
            time_mean = np.zeros(len(time[0]))

            elems_count = repetitions[dim][percentage][rule]['evolution']

            for sub_evolution in evolution:
                sub_evolution = np.array(sub_evolution)
                evolution_mean = evolution_mean + sub_evolution

            for time_evolution in time:
                time_evolution = np.array(time_evolution)
                time_mean = time_mean + time_evolution

            evolution = [x/elems_count for x in evolution_mean]
            time = [x/elems_count for x in time_mean]

            #create scatter plot
            label = 'Rule ' + str(rule)
            plt.plot(time, evolution, label=label)

            if show_regression:
                #m = slope, b=intercept
                m, b = np.polyfit(time, evolution, 1)

                # Creating the regression line
                regression = []
                for t in time:
                    regression.append(m*t + b)

                # Plotting the regression line
                reg_label = 'Regression for rule ' + str(rule)
                plt.plot(time[:reg_time_limit], regression[:reg_time_limit], label=reg_label)

            #Labelling the lines
            plt.legend()

        plt.savefig('images/mean' + dim + 'd' + y_type + str(int(float(percentage))) + '.png')
