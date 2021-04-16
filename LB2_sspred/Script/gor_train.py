#!/usr/bin/python


import sys
import os
import pandas as pd
import numpy as np

def padding(path_pssm):
    pssm_file = pd.read_csv(path_pssm, sep = "\t")
#    print pssm_file.shape[0]
    pad = pd.DataFrame(np.zeros((8,20)), index = [-8, -7, -6, -5, -4, -3, -2, -1], columns = pssm_file.columns)
    pssm = pssm_file.append(pad, ignore_index = True)
    pssm = pad.append(pssm)
#    print pssm.shape[0]
    return pssm

    


def gor_train(ids_list, path_dssp, path_pssm):
    
        ## initialize C,E,H matrices with size=17, counter of ss, and tot of residues
    
    counter = {'C' : 0, 'E' : 0, 'H' : 0, 'R' : 0}
    residues = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    C = pd.DataFrame(index = index, columns = residues)
    C = C.fillna(0)
    E = pd.DataFrame(index = index, columns = residues)
    E = E.fillna(0)
    H = pd.DataFrame(index = index, columns = residues)
    H = H.fillna(0)
    R = pd.DataFrame(index = index, columns = residues)
    R = R.fillna(0)


    list_dssp = [f for f in os.listdir(path_dssp)]
    list_pssm = [f for f in os.listdir(path_pssm)]
    id_list = open(ids_list)
    ids = [line.rstrip('\n') for line in id_list]

    for id in ids:
        filename_dssp = os.path.join(path_dssp, id+'.dssp')
        filename_pssm = os.path.join(path_pssm, id+'.profile')

        
        with open(filename_dssp, 'r') as s:
            liness = s.readline()
            nextliness = next(s)
            ss = nextliness.strip()
            ss = ss.replace('-', 'C')

        profile = padding(filename_pssm)
    
        for i in range(len(ss)):
            submatrix =  profile.loc[i-8:i+8,]

            if ss[i] == "C":
                C = C + submatrix.values
                R = R + submatrix.values
                counter["C"] += 1

                if profile.loc[i].sum() != 0:
                    counter["R"] += 1


            elif ss[i] == "E":
                E = E + submatrix.values
                R = R + submatrix.values
                counter["E"] += 1

                if profile.loc[i].sum() != 0:
                    counter["R"] += 1


            elif ss[i] == "H":                
                H = H + submatrix.values
                R = R + submatrix.values
                counter["H"] += 1

                if profile.loc[i].sum() != 0:
                    counter["R"] += 1


    norm = counter["R"]
    cc = C.div(norm)
    ee = E.div(norm)
    hh = H.div(norm)
    rr = R.div(norm)

#    final = cc.append(ee)
 #   final = final.append(hh)
    p_s = {k: counter[k]/float(counter["R"]) for k in counter if k != "R"}

#    cc.to_csv("cc_matrix.csv", index = False, header = True, sep = "\t")
#    ee.to_csv("ee_matrix.csv", index = False, header = True, sep = "\t")
#    hh.to_csv("hh_matrix.csv", index = False, header = True, sep = "\t")
#    rr.to_csv("rr_matrix.csv", index = False, header = True, sep = "\t")

  #  print p_s

    return cc, ee, hh, rr, p_s
    

if __name__ == '__main__':
    ids_list = sys.argv[1]
    path_dssp = sys.argv[2]
    path_pssm = sys.argv[3]
    gor_train(ids_list, path_dssp, path_pssm)


