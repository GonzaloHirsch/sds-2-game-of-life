from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

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

X_LIM, Y_LIM, Z_LIM = 100, 100, 100

c1 = [45, 45, 45]
c2 = [45, 45, 46]
c3 = [25, 25, 25]

x,y,z = np.indices((X_LIM, Y_LIM, Z_LIM))-.5
positions = np.c_[[c1, c2, c3]]
colors = np.random.rand(len(positions),3)
print(colors)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('auto')
prepareAxis(ax)

def init():
    pc = plotCubeAt(positions, colors=colors,edgecolor="k")
    ax.add_collection3d(pc)
    return ax,

def update(frame):
    print("FRAME", frame)
    c1[0] = (c1[0] + 1) % 50
    positions = np.c_[[c1, c2, c3]]
    pc = plotCubeAt(positions, colors=colors,edgecolor="k")
    ax.cla()
    prepareAxis(ax)
    ax.add_collection3d(pc)
    return ax,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()


#plotMatrix(ax, ma)
#ax.voxels(ma, edgecolor="k")

plt.show()