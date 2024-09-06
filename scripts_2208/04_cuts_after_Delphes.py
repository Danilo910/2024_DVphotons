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
#import os

#la variable 1 es el numero de eventos
n_events = int(sys.argv[1])

#ponemos eficiencias por bims, mientras mas lejos es el z, mas baja es la eficiencia. Como son pocos datos y no
#los vamos a editar, los podemos guardar en los csv.
#debes dejar que la aleatoridad mande, si te sale 10 a la 3 y tu eficiencia es de 0.8 en ese intervalo,
#entonces se mantiene despues de tirar un dado probabilistico (si sale mayor a 10 ala 3 por 0.8 entonces lo eliminamos)
ph_eff_zo = pd.read_csv(f'./data/z0_eff_points.csv', delimiter=',', header=None).set_axis(['zorigin','eff'], axis=1)
mu_eff_pt = pd.read_csv('./data/muon_eff_pt.csv',header=0)
el_eff_pt = pd.read_csv('./data/electron_eff_pt.csv',header=0)
el_eff_eta = pd.read_csv('./data/electron_eff_eta.csv',header=0)
#debido a elementos fisicos tendremos una variacion en los valores la cual se considera en la resolucion
zorigin_res= pd.read_csv(f'./data/z0_res_points.csv', delimiter=',', header=None).set_axis(['zorigin','res'], axis=1)
reltof_res= pd.read_csv(f'./data/z0_res_points.csv', delimiter=',', header=None).set_axis(['zorigin','res'], axis=1)
cutflow_path = "./data/clean/cutflow/"

#scales = pd.read_csv("/Collider/scripts_2208/data/cross_section.dat",delimiter="\t",index_col=0,header=None,squeeze=True)

np.random.seed(0)

## For photonresolution
#generamos una interpolacion de la data cpm el eje x ph_eff_zo.zorigin y eje y ph_eff_zo.eff
#si se escoje un valor fuera del rango de informacion lo llenamos con el ultimo valor disponible
#no es una interpolacion lineal, mas bien como si fuera un histograma
#no hay que verlo como graficos, mas bien como funciones que nos dan la eficiencia
photon_eff_zo = interp1d(ph_eff_zo.zorigin, ph_eff_zo.eff, fill_value=tuple(ph_eff_zo.eff.iloc[[0,-1]]),
                        bounds_error=False)
## For muon efficiency
mu_func = interp1d(mu_eff_pt.pt,mu_eff_pt.eff, fill_value=tuple(mu_eff_pt.eff.iloc[[0,-1]]), bounds_error=False)
## For electron efciency
el_pt_func = interp1d(el_eff_pt.BinLeft,el_eff_pt.Efficiency, fill_value=tuple(el_eff_pt.Efficiency.iloc[[0,-1]]),
                      bounds_error=False,kind='zero')
el_eta_func = interp1d(el_eff_eta.BinLeft,el_eff_eta.Efficiency, fill_value=tuple(el_eff_eta.Efficiency.iloc[[0,-1]]),
                      bounds_error=False,kind='zero')

#usamos este valor de factorizacion debido a la multiplicacion de probabilidades
el_normal_factor = 1/0.85
## For comparing with the Z mass
m_Z = 91.1876 #GeV
#factor experimental de la energia del deposito en el calorimetro de la celda que tiene mas energia
#que es de 0.35
Ecell_factor = 0.35
## For photon's z origin resolution (esta es dada de forma experimental)
zorigin_res_func = interp1d(zorigin_res.zorigin, zorigin_res.res, fill_value=tuple(zorigin_res.res.iloc[[0,-1]]),
                        bounds_error=False)

## For photon's relative tof resolution
p0_h = 1.962
p1_h = 0.262

p0_m = 3.650
p1_m = 0.223

#formulas de la tesis para calcular la resolucion
def t_res(ecell):
    if ecell >= 25:
        resol= np.sqrt((p0_m/ecell)**2 + p1_m**2)
    else:
        resol= min(np.sqrt((p0_h / ecell) ** 2 + p1_h ** 2), 0.57)

    return resol

def main(variables):

    #extraemos los dos elementos de la lista entrante, por ejemplo de
    #'ZH', 'M3_Alpha1_13', recordar que luego los valores van corriendo en el pool
    type = variables[0]
    base_out = variables[1]
    atlas_mode = variables[2]

    

    #scale = scales[type + '_' + base_out] * 1000 * 0.2 * 139 / n_events
    if(atlas_mode == ""):
        input_file = origin + f"full_op_{type}_{base_out}_photons.pickle"
        print("input_file inside function: " ,input_file)
    else:
        input_file = origin + f"{atlas_mode}_full_op_{type}_{base_out}_photons.pickle"
        print("input_file inside function: " ,input_file)
    
    """
    photons = pd.read_pickle(input_file)
    #analizamos los leptones ya que sirven para los triggers.
    leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
    #print(photons)
    #sys.exit()

    
    if leptons.size == 0 or photons.size == 0:
        return

    photons['zo_smeared'] = \
        photons.apply(lambda row:
        #usamos valor absoluto porque lo que se analiza es la magnitud de z. Esto es por el bineado que es positivo
                      np.abs(row['z_origin'] + zorigin_res_func(row['z_origin']) * np.random.normal(0, 1)),
                    axis=1)

    ## relative time of flight
    ## rel_tof es el relative time of flight
    #procedimiento similar al anterior, solo que ahora t_res es una funcion definida y ya no proviene de una interpolacion
    photons['rt_smeared'] = \
        photons.apply(lambda row: row['rel_tof'] + t_res(Ecell_factor * row['E']) * np.random.normal(0, 1), axis=1)

    ### Applying efficiencies

    ## leptons
    #primero aplicamos para los electrones
    #loc permite seleccionar sobre los leptones que son electrones
    leptons.loc[(leptons.pdg==11),'eff_value'] = \
        leptons[leptons.pdg==11].apply(lambda row:
                                       el_normal_factor*el_pt_func(row.pt)*el_eta_func(row.eta), axis=1)
    leptons.loc[(leptons.pdg == 13), 'eff_value'] = \
        leptons[leptons.pdg == 13].apply(lambda row: mu_func(row.pt), axis=1)

    #aqui realizamos el corte debido a la eficiencia de la deteccion la cual, aleatoriamente
    #te permite detectar o no las particulas
    #creamos un booleano, para cada row saldra verdad o falso
    #esta sera nuestra mascara de trues y falses
    leptons['detected'] = leptons.apply(lambda row: np.random.random_sample() < row['eff_value'], axis=1)
    #la sintaxis leptons.detected es lo mismo que leptons['detected']
    #estamos conservando todos los trues y elminando los falses
    leptons = leptons[leptons.detected]

    
    ## photons
    #seguimos un procedimiento similar al de leptons
    photons['detected'] = \
        photons.apply(lambda row: np.random.random_sample() < photon_eff_zo(row['zo_smeared']), axis=1)
    # print(df[['zo_smeared','detected']])

    #aca lo escribimos de la otra forma posible, es equivalente a photons = photons[photons.detected]
    photons = photons[photons['detected']]
   
    leptons = leptons[leptons.pt > 27]
    """
    return




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

bases = [item + [""] for item in bases]

print(bases)


for iteration in ["", "zsimp"]:  # First iteration with True, second with False

    print("We are in iteration: ")
    print(iteration)
    if iteration == "":
        # First iteration: yes_zatlas = True
        # Modify allcases to include `True` for the yes_zatlas parameter
        #allcases = [[file_inx, typex, True] for file_inx, typex, _ in allcases]

        # Run the pool with yes_zatlas set to True
        if __name__ == '__main__':
            with Pool(1) as pool:
                pool.map(main, bases)
    else:
        # Second iteration: Ask the user if they want to generate the hepmc with zsimpl
        user_input = input("Do you want to analyze the piclkes with zsimpl? (yes/no): ").strip().lower()

        if user_input == "no":
            print("Exiting the program.")
            break  # Exit the loop if the user doesn't want to continue
        elif user_input == "yes":
            origin = f"/Collider/scripts_2208/data/clean{iteration}/"
            #origin = "/Collider/2023_LLHN_CONCYTEC/"
            destiny = f"/Collider/scripts_2208/data/clean{iteration}/"
            # Get zsimp value from the user
            bases = [item[:-1] + ["zsimp"] for item in bases]
            print(bases)
            #sys.exit("Salimos")
            # Run the pool with yes_zatlas set to False
            if __name__ == '__main__':
                with Pool(1) as pool:
                    pool.map(main, bases)