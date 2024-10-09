import sys
import numpy as np
import re
import glob
import pandas as pd
from scipy.interpolate import interp1d
from my_funcs import isolation
from pathlib import Path
import json
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os

def clean_impostor_jets(phs, obs):

    #0 significa que no es un jet impostor, 1 significa que si lo es
    
    phs_list = []
    for ix in phs.index.get_level_values(0).unique()[:]:
        event_ph = phs.loc[ix]
        #print(f"Evento numero: '{ix}'")

        #print("Jets")
        #print(event_ph)

        for index_ph, row_ph in event_ph.iterrows():
            #print(f"Estamos analizando el jet con indice '{index_ph}'\n")
            df_constitu1 = row_ph[obs]
            jet_impostor = 0
            #print("df_constitu1")
            #print(type(df_constitu1))
            
            if (isinstance(df_constitu1, list) and len(df_constitu1) == 1 and df_constitu1[0] in [13, -13]) or (isinstance(df_constitu1, float) and df_constitu1 == 13.0):
                jet_impostor = 1

            phs_list.append(jet_impostor)
    
    return phs_list


def main(variables):

    type = variables[0]
    base_out = variables[1]

    input_file = origin + f"full_op_{type}_{base_out}_photons.pickle"
   
    print(type)

    photons = pd.read_pickle(input_file)
    #analizamos los jets para eliminar el double counting.
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
    
    #print("Jets antes del corte")
    #print(jets)
    #sys.exit("Salimos")


    jets['impostor_jet'] = clean_impostor_jets(jets, 'Constituents')
    
    print("Jets con impostor antes de hacer el corte")
    #print(jets)

    # Count the total number of rows where impostor_jet column exists (not NaN or missing)
    total_rows = jets['impostor_jet'].count()

    # Print the result
    print("Total number of rows in the 'impostor_jet' column:", total_rows)


    jets = jets[jets['impostor_jet'] == 0]

    print("Jets despues del corte de impsotor")

    # Count the total number of rows where impostor_jet column exists (not NaN or missing)
    total_rows = jets['impostor_jet'].count()

    # Print the result
    print("Total number of rows in the 'impostor_jet' column:", total_rows)


    #print(jets)

    #sys.exit("Salimos")


origin = f"/Collider/scripts_2208/data/clean/"
#origin = "/Collider/2023_LLHN_CONCYTEC/"
destiny = f"/Collider/scripts_2208/data/clean/"
types = ['ZH', 'WH', 'TTH']
tevs = [13]

Path(destiny).mkdir(exist_ok=True, parents=True)

bases = []

for xx in types:
    #los .pickle se distinguen por el WH, TTH O ZH
    #complete_WH_M3_Alpha3_13_jets.pickle
    #complete_ZH_M3_Alpha1_13_leptons.pickle
    #con esto nos quedamos con toda la direccion de los .picke completes
    files_in = glob.glob(origin + f"full_op_{xx}*photons.pickle")
    #print(files_in)
    #ahora extraemos solo lo que nos importa y lo ponemos en uan lista
    #en la primera tiene ZH, luego WH y en la ultima los TTH
    newcases=sorted([[xx, re.search(f'/.*{xx}_(.+)_photons', x).group(1)] for x in files_in])
    #print(newcases)
    # Bases junta los tres casos: ZH, WH y TTH
    bases.extend(newcases)

#print(bases)

# Filter the list to only keep elements where the first item is 'ZH'
#esto lo hago en mi caso, en el caso de Walter no es necesario pues el si pudo correr todos los tipso de evento
# (ZH, WH y TTH), en mi caso solo pude generar los que eran ZH y de alli mi compu muere
zh_list = [item for item in bases if item[0] == 'ZH']

# Print the final filtered list
#print(zh_list)

#bases = zh_list
#sys.exit("Salimos")


if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, bases)