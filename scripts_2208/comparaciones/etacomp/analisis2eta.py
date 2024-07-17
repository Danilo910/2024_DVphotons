import json
import sys
import glob
import re
import numpy as np
# Use the name of your text file
file_name = 'etayz_new.txt'
f = open("eta_histo.txt", "a")

with open(file_name, 'r') as file:
    lines = file.readlines()

for sentence in lines:
    line = sentence.split()
    R1 = float(line[0])
    R2 = float(line[1])
    zsimpl_value = float(line[4])
    zcrisitan = float(line[5])
    z_atlas_value = np.abs(float(line[6]))
    deltaz = np.abs((zsimpl_value - z_atlas_value)/z_atlas_value)*100
    line3 = f"{z_atlas_value} {deltaz}\n"
    f.write(line3)
    #if( R1 < 1500 or R1 > 1590 or R2 < 1590):
    #    print("R1, R2, anomalo: ", R1,R2)
    #else:
    #    print("No hay R1 R2 anomalo")
