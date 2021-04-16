###Python script to filter out from pdb(csv or tab format)

#!/usr/bin/python

import pandas as pd
import sys


def parse_csv(csv):
    pdb_fasta = pd.read_csv(csv)
    for i in pdb_fasta.index:
        if pd.isnull(pdb_fasta.loc[i,"Entry ID"]):
            pdb_fasta.loc[i, "Entry ID"] = pdb_fasta.loc[i-1, "Entry ID"] #replace empty ID

    #delete those sequence containing "X"
    pdb_fasta = pdb_fasta[pdb_fasta["Sequence"].str.contains("X") == False]
    pdb_fasta.reset_index(drop = True, inplace = True)

    #select those sequences between 50 and 300 in chain length
    pdb_fasta=pdb_fasta[pd.to_numeric(pdb_fasta["Chain Length"],errors="coerce")>50]
    pdb_fasta=pdb_fasta[pd.to_numeric(pdb_fasta["Chain Length"],errors="coerce")<300]
    
##multifasta format

    out = open(out, 'wa')
    for j in pdb_fasta.index:
        firstline = ">" + pdb_fasta.loc[j,"Entry ID"] + "_" + pdb_fasta.loc[j, "Chain ID"].split(",")[0]
   #     print firstline
        secondline = pdb_fasta.loc[j, "Sequence"]
    #    print secondline
        out.write(firstline + "\n")
        out.write(secondline + "\n")
    out.close()
  

def parse_tab(csv):
    
    tab = pd.read_csv(csv, header = None, sep = "\t")
    tab = tab[pd.to_numeric(tab[2], errors = "coerce") > 30.000]
    with open(out, 'w') as f:
        for item in tab[0]:
            print >> f, item
        


if __name__ == '__main__':
    csv = sys.argv[1]
    out = sys.argv[-1]

    parse_tab(csv)
#    parse_csv(file)
