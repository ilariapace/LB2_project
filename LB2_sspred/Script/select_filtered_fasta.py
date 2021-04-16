###python script to separate a multifasta file in single ones selecting just specific IDs
###or viceversa

#!/usr/bin/python


import sys


def parse(ids_file, multifasta):
    id_list = open(ids_file)
    ids = [line.rstrip('\n') for line in id_list]
    out = open(sys.argv[-1], 'wa')

#    out = open("ktm.txt", 'wa')
#    out = open("blind_selected_blastclust.fasta", 'wa')
#    out = open("blindset.fasta", 'wa')
    


    for id in ids:
        with open(multifasta, "rU") as fasta:                
            ifasta = iter(fasta)
            for line in ifasta:
                if line.startswith(">") and id in line:
                    out.write(line.strip() + "\n")
                    out.write(ifasta.next().strip() + "\n")
        
    out.close()


def divide_multifasta(ids_file, multifasta):
    id_list = open(ids_file)
    ids = [line.rstrip('\n') for line in id_list]
    for id in ids:
        with open(multifasta, "rU") as fasta:
            ifasta = iter(fasta)
            for line in ifasta:
                if line.startswith(">") and id in line:
                    with open(line.strip().split(">")[1] + ".fasta", 'wa') as out:
                        out.write(line.strip() + "\n")
                        out.write(ifasta.next().strip() + "\n")


if __name__ == '__main__':
    ids_file = sys.argv[1]
    multifasta = sys.argv[2]
    parse(ids_file, multifasta)

#    divide_multifasta(ids_file, multifasta)
