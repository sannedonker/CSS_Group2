from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import pickle
from Experiment1 import DataTest, DataRun
import pandas as pd


data = pickle.load(open('output\\RUN_DATA_100_more_random.p', 'rb'))



lines = []
for d in data:
    names = ['angle', 'moment', 'links', 'n_camp', 'nodes']
    line = [d.angle, d.moment, d.links, d.n_camp, d.nodes]
    pre_line = d.properties
    for key, i in pre_line.items():
        if type(i) == list or type(i) == tuple:
            for j in i:
                names.append(key)
                line.append(j)
        else:
            names.append(key)
            line.append(i)
    lines.append(line)


df = pd.DataFrame(lines)
df.columns = names

# fig1 = plt.figure()
#
# corr_matrix = df.corr()
# import seaborn as sn
# fig = plt.figure(figsize=(16,16))
# sn.heatmap(corr_matrix, annot=True)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for xs, ys, zs in zip(df['moment'], df['min_dist'], df['av_path']):
    ax.scatter(float(xs), float(ys), float(zs))

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()