import sys
import numpy as np
import re
import glob
import pandas as pd
from scipy.interpolate import interp1d
from my_funcs import isolation
from my_funcs import isolation_muon
from pathlib import Path
import json
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt

#import os

def print_first_and_last_10(df):
    """
    This function prints the first 10 and last 10 rows of a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to print the rows from.
    """
    print("First 30 rows:")
    print(df.head(30))
    #print("\nLast 10 rows:")
    #print(df.tail(10))


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
                        bounds_error=False, kind='zero')
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
                        bounds_error=False, kind='zero')



new_pt_values = np.linspace(min(mu_eff_pt.pt), max(mu_eff_pt.pt), 1000)  # 1000 points within the pt range


"""
# Interpolate efficiency values for these new pt values using mu_func
interpolated_pt_eff_values = mu_func(new_pt_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(new_pt_values, interpolated_pt_eff_values, label='Interpolated Efficiency ($p_T$)', color='blue')
plt.scatter(mu_eff_pt.pt, mu_eff_pt.eff, color='red', label='Original Data Points')  # Original data points
plt.xlabel('$p_T$ (GeV)')
plt.ylabel('Efficiency')
plt.title('Interpolation of Muon Efficiency vs $p_T$')
plt.legend()
plt.grid(True)
plt.xlim(min(mu_eff_pt.pt), max(mu_eff_pt.pt))  # Set x limits to min and max pt
plt.ylim(min(mu_eff_pt.eff) - 0.05, max(mu_eff_pt.eff) + 0.05)  # Adjust y-limits for clarity

# Save the plot as a PNG file
plt.savefig('./data/muon_pt_eff_interpolation.png')  # Save in the specified directory

plt.show()
#sys.exit("Salimos")

# Assuming you have already loaded zorigin_res DataFrame and defined zorigin_res_func
# Generate new_z values from 0 to 700
new_z_values = np.linspace(0, 700, 1000)  # 1000 points between 0 and 700

# Interpolate res values for these new_z values
interpolated_res_values = zorigin_res_func(new_z_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(new_z_values, interpolated_res_values, label='Interpolated $res$', color='blue')
plt.scatter(zorigin_res.zorigin, zorigin_res.res, color='red', label='Original Data Points')  # Original data points
plt.xlabel('$zorigin$')
plt.ylabel('$res$')
plt.title('Interpolation of $res$ vs $zorigin$ from 0 to 700')
plt.legend()
plt.grid(True)
plt.xlim(0, 700)  # Set x limits to 0 and 700
plt.ylim(min(zorigin_res.res) - 10, max(zorigin_res.res) + 10)  # Adjust y-limits for clarity

# Save the plot as a PNG file
plt.savefig('./data/zorigin_res_interpolation.png')  # Save in the specified directory

plt.show()



new_eta_values = np.linspace(min(el_eff_eta.BinLeft), max(el_eff_eta.BinLeft), 1000)  # 1000 points over the eta range

# Interpolate efficiency values for these new_eta values
interpolated_eta_eff_values = el_eta_func(new_eta_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(new_eta_values, interpolated_eta_eff_values, label='Interpolated Efficiency ($\eta$)', color='blue')
plt.scatter(el_eff_eta.BinLeft, el_eff_eta.Efficiency, color='red', label='Original Data Points')  # Original data points
plt.xlabel('$\eta$')
plt.ylabel('Efficiency')
plt.title('Interpolation of Efficiency vs $\eta$')
plt.legend()
plt.grid(True)
plt.xlim(min(el_eff_eta.BinLeft), max(el_eff_eta.BinLeft))  # Set x limits to min and max eta
plt.ylim(min(el_eff_eta.Efficiency) - 0.05, max(el_eff_eta.Efficiency) + 0.05)  # Adjust y-limits for clarity

# Save the plot as a PNG file
plt.savefig('./data/eta_eff_interpolation.png')  # Save in the specified directory

plt.show()


new_pt_values = np.linspace(min(el_eff_pt.BinLeft), max(el_eff_pt.BinLeft), 1000)  # 1000 points over the pt range

# Interpolate efficiency values for these new_pt values
interpolated_pt_eff_values = el_pt_func(new_pt_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(new_pt_values, interpolated_pt_eff_values, label='Interpolated Efficiency ($p_T$)', color='blue')
plt.scatter(el_eff_pt.BinLeft, el_eff_pt.Efficiency, color='red', label='Original Data Points')  # Original data points
plt.xlabel('$p_T$ (GeV)')
plt.ylabel('Efficiency')
plt.title('Interpolation of Efficiency vs $p_T$')
plt.legend()
plt.grid(True)
plt.xlim(min(el_eff_pt.BinLeft), max(el_eff_pt.BinLeft))  # Set x limits to min and max pt
plt.ylim(min(el_eff_pt.Efficiency) - 0.05, max(el_eff_pt.Efficiency) + 0.05)  # Adjust y-limits for clarity

# Save the plot as a PNG file
plt.savefig('./data/pt_eff_interpolation.png')  # Save in the specified directory

plt.show()



new_z_values = np.linspace(0, max(ph_eff_zo.zorigin), 1000)  # 1000 points over the zorigin range

# Interpolate efficiency values for these new z values
interpolated_eff_values = photon_eff_zo(new_z_values)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(new_z_values, interpolated_eff_values, label='Step-wise Interpolated Efficiency', color='blue')
plt.scatter(ph_eff_zo.zorigin, ph_eff_zo.eff, color='red', label='Original Data Points')  # Original data points
plt.xlabel('$zorigin$')
plt.ylabel('Efficiency')
plt.title('Step-wise Interpolation of Photon Efficiency vs $zorigin$')
plt.legend()
plt.grid(True)
plt.xlim(0, max(ph_eff_zo.zorigin))  # Set x limits based on zorigin data
plt.ylim(min(ph_eff_zo.eff) - 0.05, max(ph_eff_zo.eff) + 0.05)  # Adjust y-limits for clarity

# Save the plot as a PNG file
plt.savefig('./data/ph_eff_zo_step_interpolation.png')  # Save in the specified directory

plt.show()
"""

#sys.exit("Salimos")
## For photon's relative tof resolution
#p0_h = 1.962
#p1_h = 0.262

#p0_m = 3.650
#p1_m = 0.223

#ponemos los valores adecuados que aparecen en el paper
p0_h = 2.071
p1_h = 0.208

p0_m = 2.690
p1_m = 0.219

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
    
    #  en este caso queremos chancar sobre el antiguo output.
    out_file = input_file
    
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

    #photons['random_value'] = np.random.normal(0, 1, len(photons))
    #photons['zo_smeared'] = photons.apply(lambda row: np.abs(row['z_origin'] + zorigin_res_func(row['z_origin']) * row['random_value']), axis=1)
    #print(photons[['z_origin', 'zo_smeared', 'random_value']])


    #print("print min, max function zorigin_res: ")
    #print(zorigin_res.zorigin.min(), zorigin_res.zorigin.max())
    #print("print min, max function photons_z_origin: ")
    #print(photons[['z_origin']].min(), photons[['z_origin']].max())

    #sys.exit("Salimos")
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

    #hacemos prueba para ver si funciona bien la mascara
    #leptons['detected'] = leptons.apply(lambda row: 0.92 < row['eff_value'], axis=1)

    # Print the DataFrame with the new 'detected' column (some True, some False)
    #print("\nLeptons con columna 'detected' (True/False):")
    #print(leptons[['eff_value', 'detected']])  # Showing only the relevant columns for clarity

    #la sintaxis leptons.detected es lo mismo que leptons['detected']
    #estamos conservando todos los trues y elminando los falses
    leptons = leptons[leptons.detected]

    

    # Print the DataFrame after applying the mask (should contain only True values)
    #print("\nLeptons después de aplicar la máscara (solo 'True'):")
    #print(leptons[['eff_value', 'detected']])  # Show the 'eff_value' and 'detected' columns

    #sys.exit("Salimos")

    

    ## photons
    #seguimos un procedimiento similar al de leptons
    photons['detected'] = \
        photons.apply(lambda row: np.random.random_sample() < photon_eff_zo(row['zo_smeared']), axis=1)
    # print(df[['zo_smeared','detected']])

    #aca lo escribimos de la otra forma posible, es equivalente a photons = photons[photons.detected]
    photons = photons[photons['detected']]
   
    
    
    #Overlap

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

    #print("Type of leptons: ", leptons)
    #print("Type of photons: ", photons)
    #sys.exit("Salimos")
    ## Overlapping
    ### Primero electrones
    # a) Descartar electrones que esten a deltaR < 0.4 de algun foton.
    #leptons.loc[(leptons.pdg==11),'el_iso_ph'] = isolation(leptons[leptons.pdg==11],photons,'pt',same=False,dR=0.4)
    #el momento es usado como un centinela para indicar si la particula es removida o no, no hay algoritmo de isolation

    #Empezamos aislando muones de los jets

    print("Antes del corte muones")
    print_first_and_last_10(leptons)
    print("Antes del corte jets")
    print_first_and_last_10(jets)
    leptons.loc[(leptons.pdg == 13), 'mu_iso_j'] = isolation_muon(leptons[leptons.pdg == 13], jets, 'pt', same=False,
                                                                 dR=0.4)
    leptons = leptons[(leptons.pdg == 11) | (leptons['mu_iso_j'] == 0)]

    print("Despues del corte muones")
    print_first_and_last_10(leptons)
    print("Despues del corte jets")
    print_first_and_last_10(jets)

    sys.exit("Salimos")
    """
    leptons.loc[(leptons.pdg==11),'el_iso_ph'] = isolation(leptons[leptons.pdg==11],photons,'pt',same=False,dR=0.4)
    print_first_and_last_10(leptons)
    sys.exit("Salimos")
    leptons = leptons[(leptons.pdg==13)|(leptons['el_iso_ph']==0)]

    #print("estructura leptons, despues corte photons0: ", leptons)
    #print("estructura fotones, despues corte photons0: ", photons)
    #sys.exit("Salimos")
    
    ## Luego jets
    # b) Descartar jets que esten a deltaR = 0.4 de algun foton o a deltaR = 0.2 de un electron.
    jets['jet_iso_ph'] = isolation(jets,photons,'pt',same=False,dR=0.4)
    jets['jet_iso_e'] = isolation(jets, leptons[leptons.pdg==11], 'pt', same=False, dR=0.2)
    #tener en cuenta que se descartan, entonces seria la negacion de (delta1 < 0.4 y delta2< 0.2)
    #implica delta1>=0.4 o delta2>=0.2
    #ya que abmos tienen que estar aislados
    #esto se traduce en que ambos tengan jet_iso_ph = 0
    #basta que jet_iso_e =! 0 entonces ya se tiene una particula no aislada y por lo tanto no pasa el filtro
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
    #Hacer un analisis de jets y muones, puede que se reeconstruyan en paralelo
    #en otras palabras todos los jets son reeconstruidos como muones
    #si estan muy pegados, darle preferencia al muon
    #esto pues esta botando los jets que estan muy cerca a los muones
    #este codigo deberia ir al inicio pues es uno adicional y queremos que no cause ruido para los demas isolation
    jets['jet_iso_mu'] = isolation(jets, leptons[leptons.pdg == 13], 'pt', same=False, dR=0.01)
    #print("Jets antes del overlapping", jets)
    
    #nos quedamos solo con los que tienen conos iguales a cero (los que si estan aislados)
    jets = jets[jets['jet_iso_mu'] == 0]
    #print("Jets despues del overlapping", jets)

    #Descartar muones que esten a deltaR = 0.4 de algun jet o foton.
    #El codigo de abajo deberia eliminarse ya que lo estamos poniendo arriba, pero con la version mejorada
    leptons.loc[(leptons.pdg == 13), 'mu_iso_j'] = isolation(leptons[leptons.pdg == 13], jets, 'pt', same=False,
                                                                 dR=0.4)
    leptons.loc[(leptons.pdg == 13), 'mu_iso_ph'] = isolation(leptons[leptons.pdg == 13], photons, 'pt', same=False,
                                                                 dR=0.4)
   
    leptons = leptons[(leptons.pdg == 11) | ((leptons['mu_iso_j'] + leptons['mu_iso_ph']) == 0)]
    


    #final Isolation_1

    leptons = leptons[leptons.pt > 27]
    
    #emepezamos el codigo que involucra photons0

    
    #guardamos los fotones mas energeticos hasta el momento
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

    #de que particula es la masa invariante?
    final_particles = photons0.join(leptons0,how='inner',lsuffix='_ph',rsuffix='_l')
    final_particles['M_eg'] = np.sqrt((final_particles.E_ph + final_particles.E_l) ** 2 -
                    ((final_particles.px_ph + final_particles.px_l) ** 2 +
                     (final_particles.py_ph + final_particles.py_l) ** 2 +
                         (final_particles.pz_ph + final_particles.pz_l) ** 2))
    #quedate con los eventos que es un muon o si tiene fotones cumple con |meg - m_Z| < 15 GeV
    final_particles = final_particles[(final_particles.pdg == 13) | (np.abs(final_particles.M_eg - m_Z) > 15)]

    photons = photons[photons.index.get_level_values(0).isin(
            list(final_particles.index.get_level_values(0)))]

    
    #print("estructura fotones, despues corte photons0: ", photons)
    #sys.exit("Salimos")

   
    
    #escribimos lo que esta dentro del for que genera el binado en bins_after Delphes
    photons = photons[(Ecell_factor * photons['E']) > 10]
    photons = photons[photons['zo_smeared'] < 2000]
    photons = photons[(0 < photons['rt_smeared']) & (photons['rt_smeared'] < 12)]

    #most_energetic_photons = photons.xs(0, level='id')  # Extract rows where id = 0

    #Lo extramemos asi porque queremos mantener la estructura de multi indice
    most_energetic_photons = photons.loc[(slice(None), 0), :]

    print("leptons: " ,leptons)

    print("most_energetic_photons: " ,most_energetic_photons)
    
    
    df = pd.DataFrame(most_energetic_photons)
    df_jets = pd.DataFrame(jets)
    df_leps = pd.DataFrame(leptons)
    df_all_photons = pd.DataFrame(photons)
    
    df.to_pickle(out_file)

    #creamos otro pickle, pero cambiando el nombre de fotones a jets
    df_jets.to_pickle(out_file.replace('_photons','_jets'))

    #seguimos el mismo procedimiento para los leptones
    df_leps.to_pickle(out_file.replace('_photons', '_leptons'))

    df_all_photons.to_pickle(out_file.replace('_photons', '_mega'))
    """

    #sys.exit("Salimos")


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