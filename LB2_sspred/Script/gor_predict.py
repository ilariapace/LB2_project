#!/usr/bin/python

import gor_train
import sys
import pandas as pd
import numpy as np
import operator
import os


def gor_predict(predict_id, path_pssm):
#    cc = pd.read_csv(cc1, sep = "\t")
#    ee = pd.read_csv(ee1, sep = "\t")
#    hh = pd.read_csv(hh1, sep = "\t")
#    rr = pd.read_csv(rr1, sep = "\t")

    for ss in p_s:
        if ss == "H":
            h_infunc = np.log(hh/rr.multiply(p_s["H"]).values)

        elif ss == "E":
            e_infunc = np.log(ee/rr.multiply(p_s["E"]).values)

        elif ss == "C":
            c_infunc = np.log(cc/rr.multiply(p_s["C"]).values)

    

    list_pssm = [f for f in os.listdir(path_pssm)]
    id_list = open(predict_id)
    ids_pssm = [line.rstrip('\n') for line in id_list]

    for id in ids_pssm:
        pssm = os.path.join(path_pssm, id+'.profile')
        profile = gor_train.padding(pssm)
        nrow_profile =  profile.shape[0] - 16
        predicted_ss = ""

        for i in range(nrow_profile):
            PW = profile.loc[i-8:i+8,]
            I = {'C' : 0, 'E' : 0, 'H' : 0}

            I_H = h_infunc * PW.values
            I_E = e_infunc * PW.values
            I_C = c_infunc * PW.values

        
            I["H"] = I_H.values.sum()
            I["E"] = I_E.values.sum()
            I["C"] = I_C.values.sum()

            s_s = max(I.iteritems(), key=operator.itemgetter(1))[0]
        
            if all(value == 0.0 for value in I.values()):
                predicted_ss += "C"
            else:
                predicted_ss += s_s

        with  open(os.path.join(save_path,id + ".dsspr"), 'wa') as sp:
            sp.write(">" + id + "\n")
            sp.write(predicted_ss + "\n")

if __name__ == '__main__':
    id_train = sys.argv[1]
    train_dssp = sys.argv[2]
    train_pssm = sys.argv[3]
    predict_id = sys.argv[4]
    path_pssm = sys.argv[5]
    save_path = sys.argv[-1]
    cc, ee, hh, rr, p_s = gor_train.gor_train(id_train, train_dssp, train_pssm)

#    cc1 = sys.argv[1]
#    ee1 = sys.argv[2]
#    hh1 = sys.argv[3]
#    rr1 = sys.argv[4]
#    pssm = sys.argv[5]
#    p_s = {'H': 0.3589878298836035, 'C': 0.4293868015954788, 'E': 0.22394340334805718}
    
    gor_predict(predict_id, path_pssm)




