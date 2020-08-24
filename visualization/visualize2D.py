# Python code to implement Conway's Game Of Life
import argparse
from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import math

# Name of the dynamic and static files to be used
STATIC_FILE = "./parsable_files/static.txt"
DYNAMIC_FILE = "./parsable_files/dynamic.txt"

DEAD = 0

# Parsing the static file to get the the dimensions and type of dimensions
sf = open(STATIC_FILE, "r")
index = 0
for line in sf:
    if index == 0:
        DIMS = int(line.rstrip("\n"))
    elif index == 1:
        dimensions = [int(x) for x in line.rstrip("\n").split(" ")]
        X_LIM = dimensions[0]
        Y_LIM = dimensions[1]
        if DIMS == 3:
            Z_LIM = dimensions[2]

    index += 1

def distance_to_origin(x, y):
    x_center, y_center = X_LIM / 2, Y_LIM / 2
    distance = int(math.sqrt((x - x_center)**2 + (y - y_center)**2))
    return distance + 4

def empty_grid(N, M):

    """returns a grid of NxM with DEAD cells"""
    return np.full((N, M), DEAD)

def add_living_cells(cells, grid):
    for cell in cells:
        	grid[cell[0], cell[1]] = distance_to_origin(cell[0], cell[1])

def update(frames, img, grid, data, N, M):

    new_grid = empty_grid(N, M)
    add_living_cells(data[int(frames)], new_grid)

    # update data
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return img

def parse_dynamic_points():
    data = {}

    # Parsing the static file to get the the dimensions and type of dimensions
    df = open(DYNAMIC_FILE, "r")

    current_iteration = 0;

    for line in df:

        line_data = line.rstrip("\n").split(" ")

        # On a new time frame iteration
        if len(line_data) == 1:
            current_iteration = int(line_data[0]);
            data[current_iteration] = []
        elif len(line_data) > 2:
            print("Specified data is not in 2 dimensions")
        elif len(line_data) == 2:
            data[current_iteration].append([int(line_data[0]), int(line_data[1])])

    return data

# main() function
def main():

    data = parse_dynamic_points()

    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    args = parser.parse_args()

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid and adding the first state
    grid = empty_grid(X_LIM, Y_LIM)
    add_living_cells(data[0], grid)

    # Getting the maximum distance of a cell from origin
    # to know how many colors I need
    max_distance = distance_to_origin(X_LIM, Y_LIM)

    # Getting a named colormap which returns a ListedColormap object.
    # The second argument gives the size of the list of colors used to define the colormap
    inferno = cm.get_cmap('inferno', max_distance)
    colors = inferno(np.linspace(0, 1, max_distance))

    # Creating the color map and setting asociated boundaries with the colors
    cmap = mcolors.ListedColormap(colors)
    bounds=[x for x in range(0, max_distance)]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, data, X_LIM, Y_LIM),
                                  frames=np.linspace(start=0, stop=len(data) - 1, num=len(data)),
                                  interval=updateInterval,
                                  save_count=50)

    # set output file
    if args.movfile:
        ani.save('animations/2d/' + args.movfile, fps=8, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()



