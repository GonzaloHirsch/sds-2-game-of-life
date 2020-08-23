# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Name of the dynamic and static files to be used
STATIC_FILE = "./static.txt"
DYNAMIC_FILE = "./dynamic.txt"

# Dimensions for the plot
X_LIM, Y_LIM, Z_LIM = 100, 100, 100
DIMS = 2

# Parsing the static file to get the the dimensions and type of dimensions
sf = open(STATIC_FILE, "r")
index = 0
for line in sf:
    if index == 0:
        DIMS = int(line.rstrip("\n"))
    else:
        dimensions = [int(x) for x in line.rstrip("\n").split(" ")]
        X_LIM = dimensions[0]
        Y_LIM = dimensions[1]
        if DIMS == 3:
            Z_LIM = dimensions[2]
    index += 1

ALIVE = 255
DEAD = 0

def empty_grid(N, M):

    """returns a grid of NxM with DEAD cells"""
    return np.full((N, M), DEAD)

def add_living_cells(cells, grid):
    for cell in cells:
        	grid[cell[0], cell[1]] = ALIVE

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
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = empty_grid(X_LIM, Y_LIM)
    add_living_cells(data[0], grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, data, X_LIM, Y_LIM),
                                  frames=np.linspace(start=0, stop=len(data) - 1, num=len(data)),
                                  interval=updateInterval,
                                  save_count=50)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

# call main
if __name__ == '__main__':
    main()



