from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

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

################################################################################################
########################################## 3D METHODS ##########################################
################################################################################################

def color_function(dist, max_distance):
    return (1/max_distance) * dist

def color_for_cell(x, y, z):
    x_center, y_center, z_center = X_LIM / 2, Y_LIM / 2, Z_LIM / 2
    distance = math.sqrt((x - x_center)**2 + (y - y_center)**2 + (z-z_center)**2)
    color_r = color_function(distance, x_center)
    if color_r > 1:
        color_r = 0.999
    return [color_r, 20/255, 69/255]

# Function to transform into a cube given a set of coordinates
def cuboid_data(o, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(o)
    return X

# Function to plot a cube at a certain coordinate
def plotCubeAt(positions,sizes=None,colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( cuboid_data(p, size=s) )
    return Poly3DCollection(np.concatenate(g),
                            facecolors=np.repeat(colors,6, axis=0), **kwargs)

def prepareAxis(ax):
    ax.set_xlim([0,X_LIM])
    ax.set_ylim([0,Y_LIM])
    ax.set_zlim([0,Z_LIM])
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

def init_3d():
    #pc = plotCubeAt(positions, colors=colors,edgecolor="k")
    ax.add_collection3d(data[0])
    return ax,

def update_3d(frame):
    #c1[0] = (c1[0] + 1) % 50
    #positions = np.c_[[c1, c2, c3]]
    #pc = plotCubeAt(positions, colors=colors,edgecolor="k")
    ax.cla()
    prepareAxis(ax)
    ax.add_collection3d(data[frame])
    return ax,

def parse_dynamic_points():
    data = {}

    # Parsing the static file to get the the dimensions and type of dimensions
    df = open(DYNAMIC_FILE, "r")
    current_processed, expected_processed, iteration = 0, 0, -1
    processed_points = []
    is_first_iteration, has_iter, has_expected = True, False, False
    for line in df:
        if current_processed == expected_processed:
            if not has_iter:
                if iteration >= 0:
                    if len(processed_points) > 0:
                        colors = np.c_[[color_for_cell(x[0], x[1], x[2]) for x in processed_points]]
                        print(colors)
                        positions = np.c_[processed_points]
                        pc = plotCubeAt(positions, colors=colors,edgecolor="k")
                        data[iteration] = pc
                    else:
                        data[iteration] = []
                iteration = int(line.rstrip("\n"))
                has_iter = True
                processed_points = []
            elif not has_expected:
                has_expected = True
                current_processed = 0
                expected_processed = int(line.rstrip("\n"))
        else:
            has_iter, has_expected = False, False
            point = [int(x) for x in line.rstrip("\n").split(" ")]
            processed_points.append(point)
            current_processed += 1

    # Add the last of the processed set
    if len(processed_points) > 0:
        colors = np.c_[[color_for_cell(x[0], x[1], x[2]) for x in processed_points]]
        positions = np.c_[processed_points]
        print(colors)
        pc = plotCubeAt(positions, colors=colors,edgecolor="k")
        data[iteration] = pc

    return data

# Determine the code to execute if the plot is 2D or 3D
if DIMS == 3:
    # Parsing the dynamic points
    data = parse_dynamic_points()
    x,y,z = np.indices((X_LIM, Y_LIM, Z_LIM))-.5

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('auto')
    prepareAxis(ax)

    ani = FuncAnimation(fig, update_3d, frames=np.linspace(start=0, stop=len(data) - 1, num=len(data)),
                        init_func=init_3d, blit=True)

    plt.show()