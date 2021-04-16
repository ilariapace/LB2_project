###takes in input a csv file with kingdom/species and counts got from pdb
###used for scop pie chart too

#!/usr/bin/python

import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def tax_plot(count_file):
    data = pd.read_csv(count_file, sep = "\t", header = None)

    labels = list(data[0])
    x = data [1]
    tot = sum(data[1])

    for i in range(len(x)):
        pct = float(x[i])/tot*100
        c = labels[i] + "(" + str('%.0f' %pct) + "%)"
        labels[i] = c

    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(data[1], wedgeprops={'linewidth':2, 'edgecolor':'white'})

#    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y), fontsize=18.0,
                horizontalalignment=horizontalalignment, **kw)

    plt.show()

if __name__ == '__main__':
    count_file = sys.argv[1]
    tax_plot(count_file)

