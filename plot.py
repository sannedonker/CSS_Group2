from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

import pickle
from Experiment1 import DataTest, DataRun
import pandas as pd
import seaborn as sn


def make_df(data):
    # Make Dataframe
    lines = []
    for d in data:
        names = ['angle', 'moment']
        line = [d.angle, d.moment]
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
    return df

def make_plots(data):
    folder = r'figures\\'

    for key in data[0].properties.keys():
        try:
            fig = plt.figure()

            for d in data:
                plt.scatter(d.properties[key], d.moment, alpha=0.4)

            plt.title('moment')
            plt.xlabel(key)
            plt.ylabel('FRACTION')
            fig.savefig(folder + 'full' + key + '.png')

        except :

            for i in range(len(d.properties[key])) :
                fig = plt.figure()
                for d in data:
                    plt.scatter(d.properties[key][i], d.moment, alpha=0.4)

                plt.title('moment')
                plt.xlabel(key + ' ' + str(i))
                plt.ylabel('FRACTION')
                fig.savefig(folder + 'full' + key + str(i) + '.png')

if __name__ == '__main__':
    data = pickle.load(open('output\\RUN_DATA_most_random.p', 'rb'))
    df = make_df(data)

    # Make corr matrix
    corr_matrix = df.corr()
    fig = plt.figure(figsize=(16,16))
    sn.heatmap(corr_matrix, annot=True)

    make_plots(data)

    plt.show()


