###Code to parse and extract non zeros profile from psiblast output

#!/usr/bin/python

import pandas as pd
import sys
import os



def extract_profile(pssm_file):
    profile = []
    with open(pssm_file, 'rU') as pssm:
        colnames = pssm.readline().split()[20:]
        for line in pssm:
            l = line.strip().split()[22:42]
            for e in range(len(l)):
                l[e] = float(l[e])/100
            profile.append(l)
            
        df = pd.DataFrame(profile, columns = colnames)
        check = df.to_numpy().sum().round(2)
        
        if check != 0 :
            df.to_csv(os.path.basename(pssm_file).rsplit(".", 2)[0]+".profile", sep = '\t', index = False)
            
        else:
            
            print os.path.basename(pssm_file).split(".")[0]






if __name__ == '__main__':
    pssm_file = sys.argv[1]
 #   multifasta = sys.argv[2]
  #  ids_file = sys.argv[3]
    extract_profile(pssm_file)



