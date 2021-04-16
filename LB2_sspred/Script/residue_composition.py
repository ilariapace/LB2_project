#!/usr/bin/python


import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import PercentFormatter
matplotlib.use


def residue_matrix(filelist, path_dssp, path_fasta):
    index=['C', 'E', 'H']
    columns=['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

    df = pd.DataFrame(index=index, columns=columns)
    df = df.fillna(0)

    list_dssp = [f for f in os.listdir(path_dssp)]
    list_fasta = [f for f in os.listdir(path_fasta)]
    id_list = open(filelist)
    ids = [line.rstrip('\n') for line in id_list]

    for id in ids:
        filename_dssp = os.path.join(path_dssp, id+'.dssp')
        filename_fasta = os.path.join(path_fasta, id+'.fasta')
        
        
        with open(filename_fasta, 'r') as s:
            linef = s.readline()
            nextlinef = next(s)
            fasta = nextlinef.strip()

        with open(filename_dssp, 'r') as s:
            liness = s.readline()
            nextliness = next(s)
            ss = nextliness.strip()
            ss = ss.replace('-', 'C')
        
        for i in range(len(fasta)):
            
            if fasta[i] == 'X':
                i +=1
            else:
                
                cind = df.columns.get_loc(fasta[i])
                rind = df.index.get_loc(ss[i])

                df.iloc[rind, cind] +=1

    return df

def ss_fraction(filelist):
    
    df = residue_matrix(filelist, path_dssp, path_fasta)
    my_color = ['cornflowerblue', 'yellow', 'red']
    plt.style.use(['ggplot', 'seaborn-whitegrid'])
    ax = df.T.plot.bar(rot = 0, color = my_color)
   # ax.set_frame_on(False)
    max = df.values.max() + 2000
    plt.ylim(0, max)
    ax.yaxis.set_major_formatter(PercentFormatter(218418))
    ax.legend(['Coil', 'Strand', 'Helix'])
    ax.set_ylabel('SS frequency (%)')
    ax.set_xlabel('Residues')
    ax.set_title('Residue composition', fontsize = 18, fontweight="bold")
    
    plt.show()


def dataset_composition(filelist):
    df = residue_matrix(filelist, path_dssp, path_fasta)
    df = df.T
    df['Tot']  = df.sum(axis = 1)
    df = df.iloc[:,-1:]

    plt.style.use(['ggplot', 'seaborn-whitegrid'])
    ax = df.plot.bar(rot = 0, color = 'limegreen')
    ax.yaxis.set_major_formatter(PercentFormatter(218418))
    ax.get_legend().remove()
    ax.set_ylabel('Residue frequency (%)')
    ax.set_xlabel('Residues')
    ax.set_title('Dataset composition', fontsize = 18, fontweight="bold")

    plt.show()


                
if __name__ == '__main__':
    filelist = sys.argv[1]
    path_dssp = sys.argv[2]
    path_fasta = sys.argv[3]
    ss_fraction(filelist)
 #   dataset_composition(filelist, path_dssp, path_fasta)

