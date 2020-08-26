from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

# Name of the dynamic and static files to be used
STATIC_FILE = "./parsable_files/static.txt"
DYNAMIC_FILE = "./parsable_files/dynamic.txt"

# Dimensions for the plot
X_LIM, Y_LIM, Z_LIM = 100, 100, 100
DIMS = 2

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
    #return [color_r, 20/255, 69/255]
    return [color_r, 1 - color_r, 69/255]

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
    #ax.set_xticks([])
    #ax.set_yticks([])
    #ax.set_zticks([])

def init_3d():
    ax.set_title('Iteration 0')
    if data[0]["len"] > 0:
        ax.add_collection3d(data[0]["data"])
    return ax,

def update_3d(frame):
    ax.cla()
    prepareAxis(ax)
    ax.set_title('Iteration ' + str(frame))
    if data[frame]["len"] > 0:
        ax.add_collection3d(data[frame]["data"])
    ax.view_init(elev=10., azim=frame * 2)
    return ax,

def parse_dynamic_points():
    data = {}

    # Parsing the static file to get the the dimensions and type of dimensions
    df = open(DYNAMIC_FILE, "r")
    iteration = -1
    processed_points = []
    for line in df:
        if len(line.rstrip("\n").split(" ")) == 1:
            if iteration >= 0:
                if len(processed_points) > 0:
                    sub_data = {}
                    colors = np.c_[[color_for_cell(x[0], x[1], x[2]) for x in processed_points]]
                    positions = np.c_[processed_points]
                    pc = plotCubeAt(positions, colors=colors,edgecolor="k")
                    sub_data["data"] = pc
                    sub_data["len"] = len(processed_points)
                    data[iteration] = sub_data
                else:
                    sub_data["data"] = []
                    sub_data["len"] = len(processed_points)
                    data[iteration] = sub_data
            iteration = int(line.rstrip("\n"))
            processed_points = []
        else:
            point = [int(x) for x in line.rstrip("\n").split(" ")]
            processed_points.append(point)

    # Add the last of the processed set
    if len(processed_points) > 0:
        sub_data = {}
        colors = np.c_[[color_for_cell(x[0], x[1], x[2]) for x in processed_points]]
        positions = np.c_[processed_points]
        pc = plotCubeAt(positions, colors=colors,edgecolor="k")
        sub_data["data"] = pc
        sub_data["len"] = len(processed_points)
        data[iteration] = sub_data

    return data

# Determine the code to execute if the plot is 2D or 3D
if DIMS == 3:
    # Parsing the dynamic points
    print("Processing simulation data...")
    data = parse_dynamic_points()
    print("Preparing visualization...")
    x,y,z = np.indices((X_LIM, Y_LIM, Z_LIM))-.5
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(7,7))
    ax = fig.gca(projection='3d')
    ax.set_aspect('auto')
    prepareAxis(ax)
    print("Rendering visualization...")
    ani = animation.FuncAnimation(fig, update_3d, frames=np.linspace(start=0, stop=len(data) - 1, num=len(data)),
                        init_func=init_3d)

    ani.save("render.avi", fps=5, extra_args=['-vcodec', 'libx264'])
    #plt.show()