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
from pathlib import Path
import json
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt


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
    #Comenzamos con ZH, pues así está el formato
    base_out = variables[1]

    #Imaginar el bin como una matriz
    # Example of 2D Binned Data (z and t):
    #
    # | z (position) | t = 0-5 sec | t = 5-10 sec | t = 10-15 sec |
    # |--------------|-------------|--------------|---------------|
    # | 0 - 1        |      10     |      5       |       0       |
    # | 1 - 2        |      3      |     12       |       5       |
    # | 2 - 3        |      1      |      8       |       5       |

    #El met le agrega colores de intensidad a cada uno de los numeros (una posible forma de verlo)
    bin_matrix = dict()
    for key, t_bin in t_bins.items():
    
        bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1)).tolist()
        #bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1))

    cutflows = dict()

    #scales[type + '_' + base_out]: This represents the cross-section (likely in picobarns) for the production process (e.g., ZH, WH, TTH channels).
    #1000: Converts the cross-section from picobarns (pb) to femtobarns (fb) for consistency with the units used in the integrated luminosity.
    #0.2: ?
    #139: The integrated luminosity of the experiment, probably in fb⁻¹.
    #n_events: The number of generated events in the simulation.
    #faltaria NxCuts
    scale = scales[type + '_' + base_out] * 1000 * 0.2 * 139 / n_events

    
    #Definimos el inputfile
    input_file = origin + f"full_op_{type}_{base_out}_photons.pickle"
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photons', 'leptons')) #Lo mismo pero en lugar de photons dice leptones
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
    tracks = pd.read_pickle(input_file.replace('photons', 'tracks'))
    towers = pd.read_pickle(input_file.replace('photons', 'towers'))

    if leptons.size == 0 or photons.size == 0:
        return

    print("leptons antes de isolation muon")
    print(leptons)


    print("Begin muon isolation")

    muons = muon_isolation(leptons[leptons.pdg == 13], tracks, towers, 0.16)
    
    print("End muon isolation")


    #reiniciamos leptons para que tenga la estructura de siempre, pero con los muones filtrados
    #este leptons ya tiene el isolation muon, se usara este a partir de ahora
    leptons = reset_id_by_pt(leptons[leptons.pdg == 11], muons)
    
    #botamos los jets que esten cerca del muon pues estos seran probablemente muones que se reconstruyeron como jets accidentalmente
    jets['jet_iso_mu'] = isolation(jets, leptons[leptons.pdg == 13], 'pt', same=False, dR=0.00001)
  
    jets = jets[jets['jet_iso_mu'] == 0] 


    photons['zo_smeared'] = \
        photons.apply(lambda row:
                      np.abs(row['z_origin'] + zorigin_res_func(row['z_origin']) * np.random.normal(0, 1)),
                    axis=1)

    ## relative time of flight
    #Recordemos que el relative tof se calcula con la energia de la celda. Por ello, multiplicamos el row de la energia 'E' por el Ecell_factor.
    #'rel_tof' -> nombre que le hemos dado al relative time of flight
    
    #Hallamos el tiempo de resolucion en base a la energia, pero la energia se multiplica por el factor 0.35 recogido del detector.
    #eso lo sumamos al relative time of flight y lo normalizamos
    photons['rt_smeared'] = \
        photons.apply(lambda row: row['rel_tof'] + t_res(Ecell_factor * row['E']) * np.random.normal(0, 1), axis=1)

    

    #eficiencias y resoluciones
    leptons.loc[(leptons.pdg==11),'eff_value'] = \
        leptons[leptons.pdg==11].apply(lambda row:
                                       el_normal_factor*el_pt_func(row.pt)*el_eta_func(row.eta), axis=1)
    #Para los muones hacemos lo mismo pero solo tenemos un tipo de eficiencia (pt)
    leptons.loc[(leptons.pdg == 13), 'eff_value'] = \
        leptons[leptons.pdg == 13].apply(lambda row: mu_func(row.pt), axis=1)

    leptons['detected'] = leptons.apply(lambda row: np.random.random_sample() < row['eff_value'], axis=1)

    leptons = leptons[leptons.detected]

 
    photons['detected'] = \
        photons.apply(lambda row: np.random.random_sample() < photon_eff_zo(row['zo_smeared']), axis=1)
    # print(df[['zo_smeared','detected']])

    photons = photons[photons['detected']] #Esta ultima sintaxis es equivalente a  = photons[photons.detected]
 

    ## Overlapping
    """
    An overlap removal procedure is performed in order to
    avoid double counting of objects. First, electrons over-
    lapping with photons within ΔR < 0.4 are removed. Jets
    overlapping with photons (ΔR < 0.4) and electrons -> CORRRECCION DEBERIA SER OR EN VEZ DE AND
    Jones envio correo para preguntar sobre eso
    (ΔR < 0.2) are removed. Electrons overlapping with the
    remaining jets (ΔR < 0.4) are removed, to match the
    requirements imposed when measuring isolated electron
    efficiencies. Finally, muons overlapping with photons or
    jets (ΔR < 0.4) are removed.
    """


    #Leptones
    #First, electrons over-lapping with photons within ΔR < 0.4 are removed.
    leptons.loc[(leptons.pdg==11),'el_iso_ph'] = isolation(leptons[leptons.pdg==11],photons,'pt',same=False,dR=0.4)
   
    leptons = leptons[(leptons.pdg==13)|(leptons['el_iso_ph']==0)]

    ## Luego jets
    #Jets overlapping with photons (ΔR < 0.4) and electrons
    jets['jet_iso_ph'] = isolation(jets,photons,'pt',same=False,dR=0.4)
    jets['jet_iso_e'] = isolation(jets, leptons[leptons.pdg==11], 'pt', same=False, dR=0.2)
    jets = jets[jets['jet_iso_e'] + jets['jet_iso_ph']==0]

    ## Electrones de nuevo
    #Electrons overlapping with the remaining jets (ΔR < 0.4) are removed
    leptons.loc[(leptons.pdg == 11), 'el_iso_j'] = isolation(leptons[leptons.pdg == 11], jets, 'pt', same=False,
                                                              dR=0.4)
    leptons = leptons[(leptons.pdg == 13) | (leptons['el_iso_j'] == 0)]

    #Descartar muones que esten a deltaR = 0.4 de algun jet o foton.
    #Finally, muons overlapping with photons or jets (ΔR < 0.4) are removed.
    leptons.loc[(leptons.pdg == 13), 'mu_iso_j'] = isolation(leptons[leptons.pdg == 13], jets, 'pt', same=False,
                                                                 dR=0.4)
    leptons.loc[(leptons.pdg == 13), 'mu_iso_ph'] = isolation(leptons[leptons.pdg == 13], photons, 'pt', same=False,
                                                                 dR=0.4)
    leptons = leptons[(leptons.pdg == 11) | ((leptons['mu_iso_j'] + leptons['mu_iso_ph']) == 0)]
    
    #Comenzamos con los trigger
   
    leptons = leptons[leptons.pt > 27]
    print("Photons")
    print(photons)

    #sys.exit("Salimos")
    #nos quedamos con el mas energetico
    photons0 = photons.groupby(['N']).nth(0)
    photons0['px'] = photons0.pt * np.cos(photons0.phi)
    photons0['py'] = photons0.pt * np.sin(photons0.phi)
    photons0['pz'] = photons0.pt / np.tan(2 * np.arctan(np.exp(photons0.eta)))
    #Esto agrega las nuevas columnas de interes eliminando las antiguas
    photons0 = photons0[['E', 'px', 'py', 'pz']]

    #repetimos lo mismo para leptones
    leptons0 = leptons.groupby(['N']).nth(0)
    leptons0['px'] = leptons0.pt * np.cos(leptons0.phi)
    leptons0['py'] = leptons0.pt * np.sin(leptons0.phi)
    leptons0['pz'] = leptons0.pt / np.tan(2 * np.arctan(np.exp(leptons0.eta)))
    leptons0['E'] = np.sqrt(leptons0.mass**2 + leptons0.pt**2 + leptons0.pz**2)
    leptons0 = leptons0[['E','px','py','pz','pdg']]

    #tendremos en una misma fila la informacion del foton y del electron con sufijos ph y l,
    #E_ph	px_ph	py_ph	pz_ph	E_l	px_l	py_l	pz_l
    final_particles = photons0.join(leptons0,how='inner',lsuffix='_ph',rsuffix='_l')


    # M_eg = sqrt((E_ph + E_l)^2 - [(px_ph + px_l)^2 + 
    #                                (py_ph + py_l)^2 + 
    #                                (pz_ph + pz_l)^2])
    #
    # Where:
    # - E_ph, px_ph, py_ph, pz_ph: Energy and momentum components of the photon
    # - E_l, px_l, py_l, pz_l: Energy and momentum components of the lepton
    
    
    final_particles['M_eg'] = np.sqrt((final_particles.E_ph + final_particles.E_l) ** 2 -
                    ((final_particles.px_ph + final_particles.px_l) ** 2 +
                     (final_particles.py_ph + final_particles.py_l) ** 2 +
                         (final_particles.pz_ph + final_particles.pz_l) ** 2))
   

   #esto proviene de Z -> e- e+ pero luego un e puede emitir foton asi Z -> e+ (e- + foton)
   #y estan usando e- + foton mas energeticos y no quieren que provenga del Z (lo mismo para mu)
    final_particles = final_particles[(final_particles.pdg == 13) | (np.abs(final_particles.M_eg - m_Z) > 15)]
    
    #nos quedamos solo con los fotones que cumplen la condicion de que si este es el mas energetico con un
    #lepton mas energetico de ese mismo evento, no reconstruyen la masa del Z
    photons = photons[photons.index.get_level_values(0).isin(
            list(final_particles.index.get_level_values(0)))]
    
    #esto nos da una tabla donde la primera columna hace referencia al evento N y la segunda a la cantidad
    #de filas ( equivalente al numero de fotones) que estan presentes en el evento
    ph_num = photons.groupby(['N']).size()

    #Filter Events with Exactly One Photon and on the other with more than 2 photons.
    dfs = {'1': photons.loc[ph_num[ph_num == 1].index], '2+': photons.loc[ph_num[ph_num > 1].index]}

    print("dfs")
    print(dfs)
    #sys.exit("Salimos")

    #Recordemos que Ecell se define como el 35% de la energia del foton
    for channel, phs in dfs.items():
        ## Keeping the most energetic photon (si hay mas de uno)
        phs = phs.groupby(['N']).nth(0)
        ## Filtering Ecell, zorigin and reltof
        #Aplicamos el corte de que el Ecell debe ser mayor a 10 GeV
        phs = phs[(Ecell_factor * phs['E']) > 10]
        #Recordemos que analizamos el modulo de z origin. Queremos que este de 0 a 2000
        phs = phs[phs['zo_smeared'] < 2000]
        #t_gamma debe ser mayor a cero y menor que 12 nanosegundos
        phs = phs[(0 < phs['rt_smeared']) & (phs['rt_smeared'] < 12)]
        
        #con este codigo se le asigna un bin a cada zo_smeared, por ejemplo
        #           zo_smeared  z_binned
        #    0         0.1         0  # 0.1 falls in the [0, 3) bin (index 0)
        #    1         2.3         0  # 2.3 also in the [0, 3) bin (index 0)
        #    2         5.7         1  # 5.7 in the [3, 6) bin (index 1)
        #    3         8.2         2  # 8.2 in the [6, 9) bin (index 2)
        #    4        12.5         3  # 12.5 in the [9, 12+] bin (index 3
        phs['z_binned'] = np.digitize(phs['zo_smeared'], z_bins) - 1
        phs['t_binned'] = np.digitize(phs['rt_smeared'], t_bins[channel]) - 1
        phs['met_binned'] = np.digitize(phs['MET'], met_bins) - 1
        #Por ejemplo si tenemos
        #    phs = pd.DataFrame({
        #    'z_binned': [0, 0, 1, 1, 2, 2, 2],
        #    't_binned': [1, 1, 0, 0, 2, 2, 2],
        #    'met_binned': [3, 3, 1, 1, 0, 0, 0]
        #})
        #el codigo phs[['z_binned', 't_binned', 'met_binned']].values nos devulve
        #[[0, 1, 3],
        #[0, 1, 3],
        #[1, 0, 1],
        #[1, 0, 1],
        #[2, 2, 0],
        #[2, 2, 0],
        #[2, 2, 0]]
        #despues np.unique(..., axis=0) nos devuelve
        #[[0, 1, 3],
        #[1, 0, 1],
        #[2, 2, 0]]
        #return_counts=True: nos devuleve la cantidad de veces que se repite estas combinaciones
        #[2, 2, 3]
        ixs, tallies = np.unique(phs[['z_binned','t_binned','met_binned']].values,
                        return_counts=True, axis=0)
        
        for ix, tally in zip(ixs, tallies):
            z, t, met = ix
            #Imaginar que dentro de la matriz se tiene
            #Combination: (0, 1, 3) (z-bin 0, t-bin 1, MET-bin 3)
            #Count: 2
            #ahora el scale es necesario pues:
            """
            This scaling ensures that the histogram values represent the expected number of events in each (z, t, MET) 
            bin after accounting for cross-section, efficiency, and luminosity. Without this scaling, the histogram 
            would only reflect raw counts from the simulation, which do not correspond directly to the real-world 
            experimental conditions.
            """
            #con tally finalmente se esta agregando lo que faltaba, la cantidad de eventos Nsig que pasa los cortes
            #esto se realiza para cada configuracion de z,t y met

            bin_matrix[channel][z][t][met] += tally * scale
            #print(scale)
            
    
    #Guardamos output en el destiny 
    with open(destiny + f'bin_matrices-{base_out}-{type}.json', 'w') as file:
        json.dump(bin_matrix, file)
 
    return


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
destiny = f"./data/matrices_15/"
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
#print(bases)

if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, bases)
