#!/usr/bin/python

out = open("species_replaced.txt", 'wt')
with open("species.txt" , 'r') as s:
    for line in s:
        if line.strip() == "Escherichia":
            out.write(line.replace("Escherichia", "E.coli"))
        elif line.strip() == "Homo":
            out.write(line.replace("Homo", "H.sapiens"))
        elif line.strip() == "Thermus":
            out.write(line.replace("Thermus", "T.thermophilus"))
        elif line.strip() == "Saccharomyces":
            out.write(line.replace("Saccharomyces", "S.cereviasiae"))
        elif line.strip() == "Mus":
            out.write(line.replace("Mus", "M.musculus"))
        elif line.strip() == "Bacillus":
            out.write(line.replace("Bacillus", "B.subtilis"))
        elif line.strip() == "Mycobacterium":
            out.write(line.replace("Mycobacterium", "M.tuberculosis"))
        elif line.strip() == "Pseudomonas":
            out.write(line.replace("Pseudomonas", "P.aeruginosa"))
        else:
            out.write("Other\n")


    out.close()



'''
Escherichia, Homo, Thermus, Saccharomyces, Mus, Bacillus, Mycobacterium, Pseudomonas

E.coli, H.sapiens, T.thermophilus, S.cereviasiae, M.musculus, B.subtilis, M.tuberculosis, P.aeruginosa

'''
