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

scales = pd.read_csv("/Collider/scripts_2208/data/cross_section.dat",delimiter="\t",index_col=0,header=None,squeeze=True)

#print("First few entries of scales:")
#print(scales.head())

#sys.exit("Salimos")

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

    #bin_matrix = dict()
    #for key, t_bin in t_bins.items():
    #    bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1)).tolist()
    #print(bin_matrix)
    #sys.exit()
    
    #tenemos una matriz de tres dimensiones: tgamma, zorigin y met
    bin_matrix = dict()
    #a_matrix = dict()
    for key, t_bin in t_bins.items():
        #print(key)
        #print(t_bin)
        #a_matrix[key] = np.zeros((2, 2, 2))
        bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1)).tolist()
        #bin_matrix[key] = np.zeros((len(z_bins) - 1, len(t_bin) - 1, len(met_bins) - 1))
    
    #print(bin_matrix)
    #print(a_matrix)
    #sys.exit()

    #a_matrix tendra dos dimensiones externas cuyos elementos estan formados por dos objetos
    # A = [0, 0],  y   B = [0, 0], luego la dimension al medio tiene dos elementos tambien
    #     [0, 0]           [0, 0]
    # En el caso de A: C = [0, 0] y D = [0, 0]. Lo mismo cumple para B. Finalmente, en la dimension interna dentro de cada
    #elemento, por ejemplo C se tiene dos elementos 0 y 0.
    #[
    #   [
    #       [0, 0],
    #       [0, 0]
    #    ],
    #    [
    #        [0, 0],
    #        [0, 0]
    #    ]
    #]

    
    cutflows = dict()
    #el 0.2 se usa para la validacion, un dummy value. 1000 es para pasar de picobarm a femetobarn
    #el 139 es fentobarns a la menos uno
    scale = scales[type + '_' + base_out] * 1000 * 0.2 * 139 / n_events
    #print(n_events)
    #sys.exit()
    
    #with open(destiny + f'bin_matrices-{base_out}-{type}.1.txt', 'w') as file:
    #    file.write(scale)
    #with open(destiny + f'bin_matrices-{base_out}-{type}.2.txt', 'w') as file:
    #    file.write(n_events)

    #print(f'RUNNING: {base_out} - {type}')

    input_file = origin + f"complete_{type}_{base_out}_photons.pickle"
    photons = pd.read_pickle(input_file)
    #analizamos los leptones ya que sirven para los triggers.
    leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
    #print(photons)
    #sys.exit()

    
    if leptons.size == 0 or photons.size == 0:
        return
    #print(photons.shape[0])
    ### Aplying resolutions

    ## Z Origin
    #estamos dandole una forma normal a los datos
    #aplicamos la distribucion gaussiana sobre las filas
    #aplicamos el ruido de la siguiente forma: primero dadas las condiciones experimentales
    #extraemos en funcion del z el ruido que posee. Esto lo interpolamos como histogramas.
    #Despues con una funcion lambda, sumamos al z_origin este error experimental. Este error estara escalado con
    #una distribucion normal con media 0 y desviacion de 1
    #tener en cuenta que zorigin_res_func te devuelve el valor interpolado y que recibe como input un escalar real
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
    #print(photons.shape[0])
    #sys.exit()

    
    ## Overlapping
    ### Primero electrones
    # a) Descartar electrones que esten a deltaR < 0.4 de algun foton.
    leptons.loc[(leptons.pdg==11),'el_iso_ph'] = isolation(leptons[leptons.pdg==11],photons,'pt',same=False,dR=0.4)
    leptons = leptons[(leptons.pdg==13)|(leptons['el_iso_ph']==0)]

    ## Luego jets
    # b) Descartar jets que esten a deltaR = 0.4 de algun foton o a deltaR = 0.2 de un electron.
    jets['jet_iso_ph'] = isolation(jets,photons,'pt',same=False,dR=0.4)
    jets['jet_iso_e'] = isolation(jets, leptons[leptons.pdg==11], 'pt', same=False, dR=0.2)
    #tener en cuenta que se descartan, entonces seria la negacion de delta < 0.4 o delta < 0.2
    #lo cual implica que sea mayor a 0.4 y mayor a 0.2 lo cual se traduce en que ambos tengan jet_iso_ph = 0
    jets = jets[jets['jet_iso_e'] + jets['jet_iso_ph']==0]

    ## Electrones de nuevo
    # c) Descartar electrones que esten a deltaR = 0.4 de algun jet.
    #quizas para hacer mas practico el codigo no convendria separar los datframes de electrones y muones
    #para asi no estar seleccionando pdg = 11 y pdg = 13
    leptons.loc[(leptons.pdg == 11), 'el_iso_j'] = isolation(leptons[leptons.pdg == 11], jets, 'pt', same=False,
                                                              dR=0.4)
    leptons = leptons[(leptons.pdg == 13) | (leptons['el_iso_j'] == 0)]

    ## Finalmente, muones
    #si esta aisaldo sera cero, si da un valor no esta aislado
    #N   id      pt ... jet_iso_mu
    #0   0       1.5     57.34949
    #    1       2.0     0.000000
    #1   0       1.8     0.000000

    #Descartar jets que esten a deltaR = 0.01 de algun muon.
    jets['jet_iso_mu'] = isolation(jets, leptons[leptons.pdg == 13], 'pt', same=False, dR=0.01)
    #print("Jets antes del overlapping", jets)
    
    #nos quedamos solo con los que tienen conos iguales a cero (los que si estan aislados)
    jets = jets[jets['jet_iso_mu'] == 0]
    #print("Jets despues del overlapping", jets)

    #Descartar muones que esten a deltaR = 0.4 de algun jet o foton.
    leptons.loc[(leptons.pdg == 13), 'mu_iso_j'] = isolation(leptons[leptons.pdg == 13], jets, 'pt', same=False,
                                                                 dR=0.4)
    leptons.loc[(leptons.pdg == 13), 'mu_iso_ph'] = isolation(leptons[leptons.pdg == 13], photons, 'pt', same=False,
                                                                 dR=0.4)
    leptons = leptons[(leptons.pdg == 11) | ((leptons['mu_iso_j'] + leptons['mu_iso_ph']) == 0)]

    
    ##### De ahi leptones con pt > 27
    #esto elimina filas que no tengo pt mayor a 27 GeV
    leptons = leptons[leptons.pt > 27]
    #print(leptons)

    ### Invariant mass
    #El codigo     photons0 = photons.groupby(['N']).nth(0) genera lo siguiente, por ejemplo, para la fila 23
    #tenemos dos id el 0 y el 1, solo considerara el 0 (la particula con mayor momento pt)
    #inicialmente:
    #             E         pt       eta       phi      z_origin       rel_tof         MET  zo_smeared  rt_smeared      detected
    #23 0   202.464508  74.844223 -1.652243 -3.027883  0.000000e+00  0.000000e+00  116.806808   26.485956   -0.043635      True
    #   1    64.569824  23.534149 -1.667443  2.030808  5.572224e-07  3.916334e-10  116.806808    3.636897   -0.108982      True
   
    #Finalmente:
    #    E         pt       eta       phi      z_origin       rel_tof         MET  zo_smeared  rt_smeared      detected
    #23  202.464508  74.844223 -1.652243 -3.027883  0.000000e+00  0.000000e+00  116.806808   26.485956   -0.043635      True
    photons0 = photons.groupby(['N']).nth(0)
    #print(photons.head(24))
    #print("despues del groupby")
    #print(photons0.head(24))
    #sys.exit()
    
    photons0['px'] = photons0.pt * np.cos(photons0.phi)
    photons0['py'] = photons0.pt * np.sin(photons0.phi)
    photons0['pz'] = photons0.pt / np.tan(2 * np.arctan(np.exp(photons0.eta)))
    photons0 = photons0[['E', 'px', 'py', 'pz']]

    #estamos eliminando el multiindice y nos quedamos solo con el evento mas energetico
    # que es el indice N de los eventos
    leptons0 = leptons.groupby(['N']).nth(0)
    leptons0['px'] = leptons0.pt * np.cos(leptons0.phi)
    leptons0['py'] = leptons0.pt * np.sin(leptons0.phi)
    leptons0['pz'] = leptons0.pt / np.tan(2 * np.arctan(np.exp(leptons0.eta)))
    # m **2 = E - |vec(p)|
    leptons0['E'] = np.sqrt(leptons0.mass**2 + leptons0.pt**2 + leptons0.pz**2)
    #nos quedamos con el pdg para poder diferenciar
    leptons0 = leptons0[['E','px','py','pz','pdg']]

    #nos quedamos con la intercepcion de dos dataframes
    # gamma   l                                                                                 F
    # 0       0 este te interesa pues hubo al menos un foton y un lepton en el evento 0         0
    # 2       1 el evento 1 no aparece pues no hubo fotones                                     4
    # 4       4 sobrevive el evento 4
    # 7       6

    #Example of Join
    # DataFrame photons:
    #     E_ph  pt_ph  eta_ph
    # N                       
    # 1     10      5     0.1
    # 2     20     10     0.2
    # 3     30     15     0.3

    # DataFrame leptons:
    #     E_l  pt_l  eta_l
    # N                    
    # 1    25     8    0.2
    # 3    35    12    0.3
    # 4    45    18    0.4

    # DataFrame after join:
    #     E_ph  pt_ph  eta_ph  E_l  pt_l  eta_l
    # N                                         
    # 1     10      5     0.1   25     8    0.2
    # 3     30     15     0.3   35    12    0.3

    #de que particula es la masa invariante?
    final_particles = photons0.join(leptons0,how='inner',lsuffix='_ph',rsuffix='_l')
    final_particles['M_eg'] = np.sqrt((final_particles.E_ph + final_particles.E_l) ** 2 -
                    ((final_particles.px_ph + final_particles.px_l) ** 2 +
                     (final_particles.py_ph + final_particles.py_l) ** 2 +
                         (final_particles.pz_ph + final_particles.pz_l) ** 2))
    #quedate con los eventos que es un muon o si tiene fotones cumple con |meg - m_Z| < 15 GeV
    final_particles = final_particles[(final_particles.pdg == 13) | (np.abs(final_particles.M_eg - m_Z) > 15)]

    #final_particles.index.get_level_values(0):= esto nos da los indices del primer nivel de indexado de
    #el dataframe final_particles
    #print(final_particles.head(24))
    #print(final_particles.index.get_level_values(0))
    #the show it print give you:
    #Int64Index([  1,   3,   4,   6,   7,   8,  12,  14,  16,  17,
    #        ...
    #       476, 479, 480, 487, 489, 492, 493, 494, 495, 497],
    #      dtype='int64', name='N', length=250)
    #list(final_particles.index.get_level_values(0))) := convierte en una lista el objeto anterior
    #photons.index.get_level_values(0).isin(...) : = chequea que indices del df photons se presentan tambien
    # en el df final_particles
    #photons[...] : = finalmente selecciona las filas de photons donde la condicion especificada es verdad
    #sys.exit()
    photons = photons[photons.index.get_level_values(0).isin(
            list(final_particles.index.get_level_values(0)))]

    ### CLaasifying in channels
    #The following code do this:
    # DataFrame 'photons':
    #    N  E_ph  pt_ph  eta_ph
    # 0  1    10      5    0.10
    # 1  1    20     10    0.20
    # 2  2    15      7    0.15
    # 3  2    25     12    0.25
    # 4  3    30     15    0.30
    # 5  3    35     20    0.35
    # 6  3    40     25    0.40

    # Resulting Series 'ph_num':
    # N
    # 1    2
    # 2    2
    # 3    3
    # dtype: int64

    ph_num = photons.groupby(['N']).size()
    #print(ph_num[ph_num == 1].index)
    #sys.exit()
    
    #divide el dataframe en el que tiene una particula y mas de dos
    #ph_num[ph_num == 1] con este codigo obtenemos un subconjunto donde la cantidad de fotones en el evento es 1
    #ph_num[ph_num == 1].index de alli nos quedamos solo con una lista de indices
    #photons.loc[...] con esto seleccionamos las filas que coinciden con los indices de la lista anterior
    dfs = {'1': photons.loc[ph_num[ph_num == 1].index], '2+': photons.loc[ph_num[ph_num > 1].index]}

    #print(scale)
    #with open(destiny + f'bin_matrices-{base_out}-{type}.txt', 'w') as file:
    #    file.write(scale)

    for channel, phs in dfs.items():
        ## Keeping the most energetic
        # Esto ya no se realizo antes?
        #print("before gruopby")
        #print(phs)
        phs = phs.groupby(['N']).nth(0)
        #print("after gruopby")
        #print(phs)
        #sys.exit()
    
        ## Filtering Ecell, zorigin and reltof
        phs = phs[(Ecell_factor * phs['E']) > 10]
        phs = phs[phs['zo_smeared'] < 2000]
        phs = phs[(0 < phs['rt_smeared']) & (phs['rt_smeared'] < 12)]
        ## Classifying in bins
        #digitize recibe un numero y luego, dependindo del bin que le demos, en este caso z_bins
        #entonces si el numero por ejemplo esta en 0.1 y el bineado inidical es de 0 a 0.2,
        #este numero correspondera al bin 1, por ello le restamos 1 para que quede desde 0 en adelante por la
        #sintaxis de python.
        phs['z_binned'] = np.digitize(phs['zo_smeared'], z_bins) - 1
        #print(phs)
        #sys.exit()
        phs['t_binned'] = np.digitize(phs['rt_smeared'], t_bins[channel]) - 1
        phs['met_binned'] = np.digitize(phs['MET'], met_bins) - 1
        #print(phs[phs['z_binned'] == 5])
        #con en el print de abajo estamos creando una lista con varias listas, las filas representan
        #los eventos y las columnas z_binned, t_binned y met_binned
        #[[0 1 2]
        #[0 0 1]
        #[0 1 2]
        #[0 0 2]

        #print(phs[['z_binned','t_binned','met_binned']].values)
        #sys.exit()

        #This code make the following, suppose you have the data
        # [0 0 0]
        # [0 1 0]
        # [0 1 1]
        # [0 2 2]
        # [1 0 1]
        # [0 1 0]
        # [1 1 1]
        # [2 0 1]
        # [2 1 2]

        #Then after the unique code, you only will have

        #Unique combinations of values(ixs):
        # [0 0 0]
        # [0 1 0]
        # [0 1 1]
        # [0 2 2]
        # [1 0 1]
        # [1 1 1]
        # [2 0 1]
        # [2 1 2]

        # Frequencies of each unique combination(tallies):
        # [1 2 1 1 1 1 1 1]

        #axis = 0 implica que la unicidad se debe cumplir en las filas (comapara si las filas son iguales)
        ixs, tallies = np.unique(phs[['z_binned','t_binned','met_binned']].values,
                        return_counts=True, axis=0)

        #print("Unique combinations of values:")
        #print(ixs)
        #print()

        #print("Frequencies of each unique combination:")
        #print(tallies)
        #sys.exit()
        #print(zip(ixs, tallies))
        #If ixs contains [[0, 0, 0], [0, 1, 0], [1, 0, 1]] and tallies contains [2, 3, 1], 
        #the zip function combines them as ([0, 0, 0], 2), ([0, 1, 0], 3), and ([1, 0, 1], 1).
        #print(bin_matrix.keys())
        #sys.exit()
        #print(ixs, tallies)
        #i = 0
        for ix, tally in zip(ixs, tallies):
            #recordar que por la construccion de bin_matrix, esta tendra las mismas keys de t_bins:
            #dict_keys(['1', '2+']) esto debido a que se construye a traves de un loop por los items de t_bins
            z, t, met = ix
            #print("For i: ",i)
            #print()
            #print(tally)
            #print("the ix is:")
            #print(ix)
            #bin_matrix[channel] accede al key de la matriz
            #[z][t][met] hace referencia a las 3 dimensiones
            #el met es la dimension mas interna, la del t es la del medio z la de afuera y channel es el
            #key del diccionario que puede ser 1 o 2+ dependiendo del canal
            #si imaginamos el bin matrix como un punto en R3 con color, lo podemos ver asi:
            #tenemos z, t, met = [0, 1, 0] por ejemplo
            #ahora para categorizar la frecuencia de este punto, que en ejemplo anterior es 3, entonces lo ponemos
            #de un color rojo intenso, si fuese 1 seria un rojo menos intenso.
            #El diccionario tiene internamente objetos con la siguiente caracteristica:
            #matrices[z][t][met]. Si por ejemplo seleccionamos matrices[0][0][0] podemos interpretarlo asi.
            #por un lado la sub-seleccion minmatriz[0][0] podria ser la fila y la columna, en este caso
            #podria ser el primer elemento de la fila y columna de una matrix. Finalmente al agregar otro cero
            #matrices[0][0][0] este podria hacer analogia al color que puede ir cambiando si es 1,2,3 etc.
            #de esta forma, estamos llenando nuestro grid de puntos y le estamos asignando un valor que es tally*scale
            # De que servia scale?
            bin_matrix[channel][z][t][met] += tally * scale
            #i += 1
            #print(scale)
        #sys.exit()
        #np.save(destiny + f'bin_matrices-{base_out}-{type}-ch{channel}.npy', bin_matrix[channel])
    
    #bin_matrix = {k: v.tolist() for k, v in bin_matrix.items()}

    with open(destiny + f'bin_matrices-{base_out}-{type}.json', 'w') as file:
        json.dump(bin_matrix, file)
    #print(bin_matrix)
    #os.system(f'echo {bin_matrix}')
    #print('Matrix saved!')

    #with open(destiny + f'bin_matrices-{base_out}.json', 'w') as file:
    #    json.dump(bin_matrix, file)
    
    return


# For bin classification
#milimteros
z_bins = [0,50,100,200,300,2000.1]
#nanosegundos
t_bins = {'1': [0,0.2,0.4,0.6,0.8,1.0,1.5,12.1], '2+': [0,0.2,0.4,0.6,0.8,1.0,12.1]}
met_bins = [0, 30, 50, np.inf]

origin = f"/Collider/scripts_2208/data/clean/"
#origin = "/Collider/2023_LLHN_CONCYTEC/"
destiny = f"./data/matrices_15/"
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


print(bases)
sys.exit("Salimos")

if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, bases)