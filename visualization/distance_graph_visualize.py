import matplotlib.pyplot as plt
import numpy as np

DISPLACEMENT_FILE = "./parsable_files/displacement.txt"

f = open(DISPLACEMENT_FILE, "r")

displacement = []
time = []
percentage = 0

count = 0
for line in f:
	data = line.rstrip("\n").split(" ")

	if count == 0:
	    percentage = data[0]
	else:
	    time.append(float(count - 1))
	    displacement.append(float(data[0]))

	count += 1


# Set the x axis label
plt.xlabel('Time (frames)')
# Set the y axis label
plt.ylabel('Maximum displacement from center')
# Set a title of the current graph.
plt.title('Maximum displacement from center vs. Time')

#create scatter plot
plt.plot(time, displacement, 'o')

#m = slope, b=intercept
m, b = np.polyfit(time, displacement, 1)

# Creating the regression line
regression = []
for t in time:
    regression.append(m*t + b)

# Plotting the regression line
label = 'Initial living cells = ' + str(percentage) + '%'
plt.plot(time, regression, label=label)

#Labelling the lines
plt.legend()

plt.savefig('images/displacement.png')
