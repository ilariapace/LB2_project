###create the right input format for libsvm 

#!/usr/bin/python



import gor_train as gt
import sys
import os
import pandas as pd
import numpy as np


def svm_prep(ids_list, path_dssp, path_pssm):
    classes = {'H':1,'E':2,'C':3}
    
    list_dssp = [f for f in os.listdir(path_dssp)]
    list_pssm = [f for f in os.listdir(path_pssm)]
    id_list = open(ids_list)
    ids = [line.rstrip('\n') for line in id_list]
    out = open(output, 'w+')
    
    check = 0

    for id in ids:
        if os.path.exists(os.path.join(path_pssm, id+'.profile')):
            filename_dssp = os.path.join(path_dssp, id+'.dssp')
            filename_pssm = os.path.join(path_pssm, id+'.profile')

            profile = gt.padding(filename_pssm)
    
            with open(filename_dssp, 'r') as s:
                liness = s.readline()
                nextliness = next(s)
                ss = nextliness.strip()
                ss = ss.replace('-', 'C')
    
            check += len(ss)

            for i in range(len(ss)):
                submatrix =  profile.loc[i-8:i+8,]
                submatrix = submatrix.reset_index(drop = True)

                k = 0
                v = str(classes[ss[i]])    
                for row in range(len(submatrix.index)):
                    for feature in range(len(submatrix.columns)):
                        k += 1
                        v += ' %r:%r'%(k,submatrix.loc[row][feature])
                out.write(v + "\n")
    print check

    out.close()
 




if __name__ == '__main__':
    ids_list = sys.argv[1]
    path_dssp = sys.argv[2]
    path_pssm = sys.argv[3]
    output = sys.argv[-1]
    
    svm_prep(ids_list, path_dssp, path_pssm)


