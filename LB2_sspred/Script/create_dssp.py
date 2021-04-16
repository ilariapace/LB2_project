###parse files from dssp program and create a fasta-like file

#!/usr/bin/python

import pandas as pd
import sys
import os


def parse_dssp(dssp_file, ids_file):

    id_list = open(ids_file)
    ids = [line.rstrip('\n') for line in id_list]
    ss_line = []

    for i in ids:
        if os.path.basename(dssp_file).split(".")[0] in i:
            with open(dssp_file, 'rU') as dssp:
                idssp = iter(dssp)
                for line in idssp:
                    if line[11] == i.split("_")[1]:
                        ss = line[16]

                        if ss == "H" or ss == "G" or ss == "I": ss = "H"
                        elif ss == "B" or ss == "E" : ss = "E"
                        elif ss== "T" or ss == "S" or ss == " " : ss = "C"

                        ss_line.append(ss)
             

            with open(multifasta, "rU") as fasta:
                ifasta = iter(fasta)
                for l in ifasta:
                    if l.startswith(">") and i in l:
                        seq = ifasta.next().strip()
                        if len(seq) == len(ss_line):
                            with open(i + ".fasta", 'wa') as f:
                                f.write(l.strip() + "\n")
                                f.write(seq+"\n")

                            with open(i + ".dssp", 'wa') as s:
                                s.write(">"+i+"\n")
                                s.write(''.join(ss_line)+"\n")

      
if __name__ == '__main__':
    dssp_file = sys.argv[1]
    multifasta = sys.argv[2]
    ids_file = sys.argv[3]
    parse_dssp(dssp_file, ids_file)


