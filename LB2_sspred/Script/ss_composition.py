###Python script to parse dssp files and get ss row. Count and plot pie chart of ss composition.

#!/usr/bin/python
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
from pandas.plotting import table



def get_ss_list(filelist, path_dssp):
    c = 0
    list_ss = str()
    id_list = open(filelist)
    ids = [line.rstrip('\n') for line in id_list]
    files_list = [f for f in os.listdir(path_dssp)]
    for id in ids:
        filepath = os.path.join(path_dssp, id+'.dssp')
        with open(filepath, 'r') as s:
            line = s.readline()
            nextline = next(s)
            residues = nextline.strip()
            residues = residues.replace('-', 'C')
            list_ss = list_ss + residues
    return list_ss

def ss_plot(path):
    list_ss = get_ss_list(filelist, path)
    helix=0
    coil=0
    strands=0
    for i in list_ss:
        if i == 'H':
            helix += 1
        elif i == 'C':
            coil += 1
        elif i == 'E':
            strands += 1
    print ('Helices: %s' %helix
            + "\n" + 'Strands: %s' %strands +
            "\n" + 'Coils: %s' %coil)
    
    x = [coil, strands, helix]
    tot=sum(x)
    labels = ['Coil', 'Strand', 'Helix']
   
    for i in range(len(x)):        
        pct = float(x[i])/tot*100
        c = labels[i] + " " + str('%.0f' %pct) + "%"
        labels[i] = c
    
    colors = ['cornflowerblue', 'yellow', 'red']
    my_circle = plt.Circle((0,0), 0.7, color='white')

    data = {'Total coils': [coil],                
            'Total strands': [strands],
            'Total helices':  [helix]}

    df = pd.DataFrame(data)
    fig, (ax, ax1) = plt.subplots(2,1, subplot_kw=dict(aspect='equal'))

    wedges, texts = ax.pie(x, wedgeprops={'linewidth':2, 'edgecolor':'white'}, colors=colors, startangle=90)

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

    df['Total #residues'] = tot
    
    
    # plot table
    ax1.axis('off')
    tbl = ax1.table(cellText=df.values, colLabels=df.keys(), loc='center')
    tbl.scale(2,2) 
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    ax.set_title("SS composition", fontsize = 36)
    ax.add_artist(my_circle)
    plt.show()



if __name__ == '__main__':
    filelist = sys.argv[1]
    path_dssp = sys.argv[2]
    ss_plot(path_dssp)
