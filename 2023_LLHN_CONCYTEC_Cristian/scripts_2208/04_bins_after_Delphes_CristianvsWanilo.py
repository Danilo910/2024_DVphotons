import sys
import numpy as np
import re
import glob
import pandas as pd
from scipy.interpolate import interp1d
from my_funcs_vfinal import isolation
from my_funcs_vfinal import overlap_removal_muon_jet
from my_funcs_vfinal import muon_isolation
from my_funcs_vfinal import deltaRcalculation
from my_funcs_vfinal import cone_isolation
#from my_funcs_vfinal import convert_single_element_arrays
from pathlib import Path
import json
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os

def reset_id_by_pt(electrons, muons):
    """
    Sorts the DataFrame by 'pt' within each 'N', then assigns a new 'id' starting from 0 for each group.

    Parameters:
    electrons (DataFrame): The input DataFrame with a multi-index ('N', 'id').

    Returns:
    electrons (DataFrame): The DataFrame with a new multi-index ('N', 'id') sorted by 'pt'.
    """
    # Reset index to treat 'N' and 'id' as columns
    electrons = electrons.reset_index()

    electrons = electrons.drop(columns=['id'])

    muons = muons.reset_index()

    muons = muons.drop(columns=['id'])

    #print("Electrons")
    #print(electrons)
    #print("Muons")
    #print(muons)

    #sys.exit("Salimos")

    leptons = pd.concat([electrons, muons], ignore_index=True)

    #print("Leptons concat")
    #print(leptons)
    # Sort the DataFrame by 'N' and 'pt'
    leptons = leptons.sort_values(by=['N', 'pt'], ascending=[True, False])

    g = leptons.groupby('N', as_index=False).cumcount()

    leptons['id'] = g

    leptons = leptons.set_index(['N', 'id'])

    #print("Fianl leptons")

    #print(leptons)

    return leptons


#import os

#Numero de eventos (recordamos que este archivo tiene un input, que es el # de eventos)
n_events = int(sys.argv[1])

#La eficiencia se maneja de la siguiente forma
#Supongamos que tenemos el foton con una eficiencia de deteccion de 0.85 y sacamos un random number
#si el random number es menor que 0.85 guardas el foton, si es mayor, lo descartas. 

#! Efficiency data
#Importamos eficiencias obtenidas de los graficos de los papers de atlas
#les damos forma de funcion con set_axis
#En el caso del foton, se busca la eficiencia en terminos de z_origin. Mientras mas lejos, disminuye la eficiencia (no tanto)
ph_eff_zo = pd.read_csv(f'./data/z0_eff_points.csv', delimiter=',', header=None).set_axis(['zorigin','eff'], axis=1)
#la eficiencia del muon se hace en base a pt
mu_eff_pt = pd.read_csv('./data/muon_eff_pt.csv',header=0)
#el electron tiene eficiencia por pt y por eta
el_eff_pt = pd.read_csv('./data/electron_eff_pt.csv',header=0)
el_eff_eta = pd.read_csv('./data/electron_eff_eta.csv',header=0)
#! Resolution data
zorigin_res= pd.read_csv(f'./data/z0_res_points.csv', delimiter=',', header=None).set_axis(['zorigin','res'], axis=1)
#todo Me parece que falta la resolucion del time of flight. Entiendo que Cristian grafica analiticamente la curva.
#todo Por esto, comentamos reltof_res
#reltof_res= pd.read_csv(f'./data/z0_res_points.csv', delimiter=',', header=None).set_axis(['zorigin','res'], axis=1)
cutflow_path = "./data/clean/cutflow/"

#Guardamos el crossection al ejecutar madgraph ubicado en el master
#Usamos la formula: #eventos generados = #eventos reales * luminosidad * cross section
scales = pd.read_csv("/Collider/scripts_2208/data/cross_section.dat",delimiter="\t",index_col=0,header=None,squeeze=True)

np.random.seed(0)


photon_eff_zo = interp1d(ph_eff_zo.zorigin, ph_eff_zo.eff, fill_value=tuple(ph_eff_zo.eff.iloc[[0,-1]]),
                        bounds_error=False)

#Hay un factor de normalizacion de eficiencia para cuando se utilizan 2.

## For muon efficiency
mu_func = interp1d(mu_eff_pt.pt,mu_eff_pt.eff, fill_value=tuple(mu_eff_pt.eff.iloc[[0,-1]]), bounds_error=False)
## For electron efciency
el_pt_func = interp1d(el_eff_pt.BinLeft,el_eff_pt.Efficiency, fill_value=tuple(el_eff_pt.Efficiency.iloc[[0,-1]]),
                      bounds_error=False,kind='zero')
el_eta_func = interp1d(el_eff_eta.BinLeft,el_eff_eta.Efficiency, fill_value=tuple(el_eff_eta.Efficiency.iloc[[0,-1]]),
                      bounds_error=False,kind='zero')
el_normal_factor = 1/0.85
## For comparing with the Z mass
m_Z = 91.1876 #GeV
Ecell_factor = 0.35 #factor experimental del deposito en el calorimetro 

zorigin_res_func = interp1d(zorigin_res.zorigin, zorigin_res.res, fill_value=tuple(zorigin_res.res.iloc[[0,-1]]),
                        bounds_error=False)


p0_h = 2.071
p1_h = 0.208

p0_m = 2.690
p1_m = 0.219

def t_res(ecell):
    if ecell >= 25:
        resol= np.sqrt((p0_m/ecell)**2 + p1_m**2)
    else:
        resol= min(np.sqrt((p0_h / ecell) ** 2 + p1_h ** 2), 0.57)

    return resol

def main(variables):
    type = variables[0]
    base_out = variables[1]

    bin_matrix = dict()
    for key, t_bin in t_bins.items():
        bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1)).tolist()

    cutflows = dict()
    scale = scales[type + '_' + base_out] * 1000 * 0.2 * 139 / n_events

    # Define the input file
    input_file = origin + f"full_op_{type}_{base_out}_photons.pickle"
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
    tracks = pd.read_pickle(input_file.replace('photons', 'tracks'))
    towers = pd.read_pickle(input_file.replace('photons', 'towers'))

    if leptons.size == 0 or photons.size == 0:
        return

    print("Muons data frame")
    print(leptons[leptons.pdg == 13])


    # ------------------------------------------------
    # Perform the overlap removal procedure
    # ------------------------------------------------

    leptons.loc[(leptons.pdg == 11), 'el_iso_ph'] = isolation(leptons[leptons.pdg == 11], photons, 'pt', same=False, dR=0.4)
    leptons = leptons[(leptons.pdg == 13) | (leptons['el_iso_ph'] == 0)]

    jets['jet_iso_ph'] = isolation(jets, photons, 'pt', same=False, dR=0.4)
    jets['jet_iso_e'] = isolation(jets, leptons[leptons.pdg == 11], 'pt', same=False, dR=0.2)
    jets = jets[jets['jet_iso_e'] + jets['jet_iso_ph'] == 0]

    leptons.loc[(leptons.pdg == 11), 'el_iso_j'] = isolation(leptons[leptons.pdg == 11], jets, 'pt', same=False, dR=0.4)
    leptons = leptons[(leptons.pdg == 13) | (leptons['el_iso_j'] == 0)]

    jets['jet_iso_mu'] = isolation(jets, leptons[leptons.pdg == 13], 'pt', same=False, dR=0.01)
    jets = jets[jets['jet_iso_mu'] == 0]

    leptons.loc[(leptons.pdg == 13), 'mu_iso_j'] = isolation(leptons[leptons.pdg == 13], jets, 'pt', same=False, dR=0.4)
    leptons.loc[(leptons.pdg == 13), 'mu_iso_ph'] = isolation(leptons[leptons.pdg == 13], photons, 'pt', same=False, dR=0.4)
    leptons = leptons[(leptons.pdg == 11) | ((leptons['mu_iso_j'] + leptons['mu_iso_ph']) == 0)]

    # ------------------------------------------------
    # Save AFTER overlapping
    # ------------------------------------------------
    # Save muons, electrons, jets, and photons as pickle files
    muons = leptons[leptons.pdg == 13]
    electrons = leptons[leptons.pdg == 11]

    output_dir = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd/"
    os.makedirs(output_dir, exist_ok=True)

    output_path_muons2 = os.path.join(output_dir, f"muons_filtered_Cristian_{type}.pkl")
    output_path_electrons2 = os.path.join(output_dir, f"electrons_filtered_Cristian_{type}.pkl")
    output_path_jets2 = os.path.join(output_dir, f"jets_filtered_Cristian_{type}.pkl")
    output_path_photons2 = os.path.join(output_dir, f"photons_filtered_Cristian_{type}.pkl")

    muons.to_pickle(output_path_muons2)
    print(f"Muons DataFrame saved to {output_path_muons2}")

    electrons.to_pickle(output_path_electrons2)
    print(f"Electrons DataFrame saved to {output_path_electrons2}")

    jets.to_pickle(output_path_jets2)
    print(f"Jets DataFrame saved to {output_path_jets2}")

    photons.to_pickle(output_path_photons2)
    print(f"Photons DataFrame saved to {output_path_photons2}")

    return


print("Entramos a 04_bins")
# For bin classification
#z esta en milimetros
z_bins = [0,50,100,200,300,2000.1]
#Recordemos que el analisis se dividio en 2 canales: canal con 1 foton y canal con 2 a mas fotones
#t_gamma esta en nanosegundos
t_bins = {'1': [0,0.2,0.4,0.6,0.8,1.0,1.5,12.1], '2+': [0,0.2,0.4,0.6,0.8,1.0,12.1]}
#de 0 a 30, de 30 a 50, de 50 hasta arriba
#met en GeV
met_bins = [0, 30, 50, np.inf]

origin = f"/Collider/scripts_2208/data/clean/"
#origin = "/Collider/2023_LLHN_CONCYTEC/"
destiny = f"./data/matrices/"
types = ['ZH', 'WH', 'TTH']
tevs = [13]

#creamos el destiny folder con mkdir
Path(destiny).mkdir(exist_ok=True, parents=True)

#bases es una acumulacion de newcases
#newcases toma 3 valores diferentes: ZH, WH, TTH
#newcases es una lista con 3 elementos. Hay 3 variaciones del newcases: primero toma los ZH, el segundo los WH y el tercero los TTH
#bases junta todo estas 3 listas

#glob.glob -> Permite iterar a lo largo de todos los archivos, en cierto folder, que le des como input y los vuelve en lista

bases = []
for xx in types:
    files_in = glob.glob(origin + f"full_op_{xx}*photons.pickle")
    #Recordemos que la estructura de los pickles antes creados son:
    #complete_TTH_M3_Alpha1_13_photons.pickle
    #print(files_in)
    newcases=sorted([[xx, re.search(f'/.*{xx}_(.+)_photons', x).group(1)] for x in files_in])
    #print(newcases)
    
    #The print of newcases is the following:
    #[['ZH', 'M3_Alpha1_13'], ['ZH', 'M3_Alpha2_13']]
    #[['WH', 'M3_Alpha1_13'], ['WH', 'M3_Alpha2_13']]
    #[['TTH', 'M3_Alpha1_13'], ['TTH', 'M3_Alpha2_13']]

    bases.extend(newcases)
print("bases")
print(bases)

if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, bases)
