import matplotlib.pyplot as plt
import numpy as np

OBS_FILE = "./parsable_files/observable_vs_time.txt"

f = open(OBS_FILE, "r")

observable = []
time = []
percentage = 0
dim = 0
obs_type = ''
rule = 0
stats = {}

# Variables that must be changed depending on the regression line we want
show_regression = False
reg_time_limit = 50

count = 0
for line in f:
	data = line.rstrip("\n").split(" ")

	if count == 0:
	    dim = data[0]
	    obs_type = data[1]
	    percentage = data[2]
	elif len(data) == 1:
	    if count > 1:
	        stats[rule]['obs'] = observable
	        stats[rule]['time'] = time
	        observable = []
	        time = []

	    rule = data[0]
	    if not rule in stats:
	        stats[rule] = {}

	else:
	    time.append(float(data[0]))
	    observable.append(float(data[1]))

	count += 1

stats[rule]['obs'] = observable
stats[rule]['time'] = time


# Set the x axis label
plt.xlabel('Time (frames)')

# Set the y axis label
if obs_type == 'Living':
    ylabel = 'Percentage of Living Cells (%)'
else:
    ylabel = 'Maximum displacement from center'
plt.ylabel(ylabel)

# Set a title of the current graph.
plt.title(dim + 'D & ' + percentage + '%: ' + ylabel + ' vs. Time')

for rule in stats:
    observable = stats[rule]['obs']
    time = stats[rule]['time']

    #create scatter plot
    label = 'Rule ' + rule
    plt.plot(time, observable, label=label)

    if show_regression:
        #m = slope, b=intercept
        m, b = np.polyfit(time, observable, 1)

        # Creating the regression line
        regression = []
        for t in time:
            regression.append(m*t + b)

        # Plotting the regression line
        reg_label = 'Regression for rule ' + rule
        plt.plot(time[:reg_time_limit], regression[:reg_time_limit], label=reg_label)

    #Labelling the lines
    plt.legend()

plt.savefig('images/' + dim + 'd' + obs_type + str(percentage) + '.png')
