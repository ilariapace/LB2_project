###Indeces implementation to evaluate performance. Confusion matrix: MCC, TPR, PPV
###SOV, total one and for secondary structures
##cv_stat function for cross validation evaluation performance
##blind_stat function for blindtest set evaliation performance

#!/usr/bin/env python

import math
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
#from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix
import statistics
import re

def conf_matrix(path_obs, path_pred):
    stat = { 'TPR':{'H':[],'E':[],'C':[]}, 'PPV':{'H':[],'E':[],'C':[]}, 'MCC':{'H':[],'E':[],'C':[]}}

    ss_types = ['H','E','C']
    with open(path_obs, 'r') as ob:
        obs = ob.readline()
    with open(path_pred, 'r') as pr:
        pred = pr.readline()

    cm = confusion_matrix(list(obs), list(pred), labels = ss_types)
     
    Q3 = float(sum(np.diag(cm)))/(np.sum(cm))
    
    for q in range(3):
		ss = ss_types[q]
		indexes = [0,1,2]
		indexes.pop(q)
		i,j = indexes[0],indexes[1]
		a = np.array([cm[i]+cm[j],cm[q]])
		b = np.array((list([a[0][i]+a[0][j],a[0][q]]),list([a[1][i]+a[1][j],a[1][q]])))
		TN, FP, FN, TP = b[0][0], b[0][1], b[1][0], b[1][1]
		d = np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
                stat['MCC'][ss].append(float((TP*TN)-(FP*FN))/d)
                stat['TPR'][ss].append(float(TP)/(TP+FN))
                stat['PPV'][ss].append(float(TP)/(TP+FP))
    
    return stat, Q3
    


def getOverlap(a, b):
	'''Returns 0 if no overlap between the ranges is found,
		otherwise returns the range of the overlap'''
	return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def sov(obs_file, pred_file):
    ss_types = ['H','E','C']
    sov_dict = { 'SOV':{'H':[],'E':[],'C':[]}}
    n_tot = 0
    sov = 0

    with open(obs_file, 'r') as ob:
        obs = ob.readline()
    with open(pred_file, 'r') as pr:
        pred = pr.readline()
    
    for ss in ss_types:
        ss_re = re.compile(ss)
        ss_iter = ss_re.finditer(obs)
        pred_ss_spans = [i.span() for i in ss_re.finditer(pred)]
    
        N = 0
        sov_ss = 0

    
        for segment in ss_iter:
            has_overl = False
            len_seg = segment.end()-segment.start()
		 
            for i in pred_ss_spans:
	        minov = getOverlap(segment.span(),i)
    		# If overlap is present add the term to the growing sov
                if minov!=0:
	            has_overl = True
        	    N += len_seg
		    maxov = max(segment.end(), i[1]) - min(segment.start(), i[0])
		    delta = min(maxov-minov, minov, int(len_seg/2), int((i[1] -i[0])/2))
	            sov_ss += float((minov+delta)/maxov)*len_seg

            if not has_overl:
                N += len_seg
        if N==0:
            return N, sov_ss, np.nan
    
        ss_type_sov = float(sov_ss*100/N)
        sov_dict['SOV'][ss].append(ss_type_sov)
        n_tot += N
        sov += sov_ss
    sov_tot = float(sov*100/n_tot)
    return sov_dict, sov_tot



def cv_stat(path_obs, path_pred):
    stat_tot = { 'TPR':{'H':[],'E':[],'C':[]}, 'PPV':{'H':[],'E':[],'C':[]}, 'MCC':{'H':[],'E':[],'C':[]}, 'SOV':{'H':[],'E':[],'C':[]}}
    sov_tot_dict = {'H':[],'E':[],'C':[]}
    q3_tot = [] 
    SOV = []
    for i in range(5):
        obs_file = os.path.join(path_obs, 'ss_obs'+str(i)+'.txt')
        pred_file = os.path.join(path_pred, 'ss_pred'+str(i)+'.txt')
        stat, q3 = conf_matrix(obs_file, pred_file)
        sov_dict, sov_tot = sov(obs_file, pred_file)
        for k in stat:
            stat_tot[k] = {key: stat_tot[k][key] + stat[k][key] for key in stat[k]}
        stat_tot['SOV'] = {key: stat_tot['SOV'][key] + sov_dict['SOV'][key] for key in sov_dict['SOV']}

        q3_tot.append(float(q3))
        SOV.append(sov_tot)


    for i in stat_tot:
        print '-'+i+':'
        for j in stat_tot[i]:
            print '\t'+j+':','%.2f' %(statistics.mean(stat_tot[i][j])), u"\u00B1", '%.2f' %(statistics.stdev(stat_tot[i][j])/math.sqrt(5))
           
    print  "-Q3:"+'/n'+'/t', "%.2f" %statistics.mean(q3_tot), u"\u00B1", "%.2f" %(statistics.stdev(q3_tot)/math.sqrt(5))
    print "-Sov_tot:"+'/n'+'/t', "%.2f" %statistics.mean(SOV), u"\u00B1", "%.2f" %(statistics.stdev(SOV)/math.sqrt(5))
    return stat_tot, q3_tot, SOV


def blind_stat(file_obs, file_pred):
    stat, q3 = conf_matrix(file_obs, file_pred)
    sov_dict, sov_tot = sov(file_obs, file_pred)
    for i in stat:
        print '-'+i+':'
        for j in stat[i]:
            print '\t'+j+':', "%.2f" %stat[i][j][0]
    for i in sov_dict:
        print '-'+i+':'
        for j in sov_dict[i]:
            print '\t'+j+':', "%.2f" %sov_dict[i][j][0]

    print  "-Q3:"+'\n'+'\t', "%.2f" %q3

    print "-Sov_tot:"+'\n'+'\t', "%.2f" %sov_tot


if __name__ == '__main__':
    path_obs = sys.argv[1]
    path_pred = sys.argv[2]

##for cross-validation  path of directories for observed and predicted ss
    #cv_stat(path_obs, path_pred)

## for blindset not path of directories but observed and predicted files
    blind_stat(path_obs, path_pred)
    

'''

    disp = ConfusionMatrixDisplay(confusion_matrix = cm,
                              display_labels = ss_types)

    disp.plot(include_values = True, cmap = 'Blues', ax = None, xticks_rotation = 'horizontal')
    plt.show()

'''

