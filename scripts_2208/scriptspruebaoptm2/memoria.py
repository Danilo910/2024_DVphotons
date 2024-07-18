from pathlib import Path
import json
import sys
import glob
import re
import pandas as pd
from multiprocessing import Pool
import numpy as np
from my_funcs import my_arctan
import os
import time

# Record the start time
start_time = time.time()

def main(parameters):
    
    global t_n
    #De los dataframes, en base al evento y al id, seleccionamos un registro y sacamos datos.
    
    #parameters, nuevamente, son el nombre del archivo y el tipo


    file_in, type = parameters
    
    #Extraemos el baseout y ponemos el nombre del archivo de salida (complete...hepmc)
    base_out = re.search(f'({type}.+)\.', file_in).group(1)
    file_out = destiny + f'full_ctb_{base_out}.hepmc'

    #print(f'\nRUNNING: {base_out}') #Commented by JJP
    '''    
    #Antes del comando set_index tenemos un index generico (0,1,2,...)
    #Luego de hacer el set index seteamos las variables de Event y pid como un multiindex
    #El nombre de cada registro estara basado en el numero de su evento y el id del foton
    #Notamos que la etiqueta 0,1,2,3,etc de la primera columna original desaparece porque la estamos sobreescribiendo con el index de las columnas especificas evento e id
    #NO PUEDO USAR ESTO
    #new_observs = new_observs.set_index(['Event','pid'])
    #print(new_observs)
    '''

    #importante para emular codigo de Cristian
    it = 0 # Iterator for unnecessary lines
    i = 0
    limit = 2

    it_start = 0
    #queremos que el codigo se corra de 5000 eventos en 5000 eventos, eso es el batch
    batch = 5000
    #este codigo ya no se usa debido a que se a automatizado este procedimiento
    corte_inf = it_start * batch
    corte_sup = corte_inf + batch * 99999
    final_part_active = True

    ######
    
    #Abrimos los hepmc. Uno para leer y otro para escribir
    df = open(file_in, 'r')
    hepmc = open(file_in, 'w')
    new_hepmc = open(file_out, 'w')

    event = -1
    sentences = ''
    #Leemos linea por linea del hepmc
    #Cuando se abre un archivo, el for lo interpreta como readline
    while it < 2:
        df.readline()
        it += 1

    # Initializing values
    data = dict()
    #selectiond = dict()
    num = 0
    p_scaler = None
    d_scaler = None
    holder = {'v': dict(), 'a': [], 'n5': dict()}
    selectiond = dict()
    selection = set()
    repitioevento = False


    for sentence in df:
        #while i<(limit+20):
        #sentence = df.readline()
        # print(sentence)
        line = sentence.split() # Divide the wtring in whitespaces
        #como en nuestro caso corte_inf es cero, solo correra una vez
        
        
        if line[0] == 'E':
            # num = int(line[1])
            if(num > 0):
                
                #aqui se esta creando un label en el diccionario con valor num -1 que contiene todo lo que esta a la
                #derecha de la igualdad
                data[num - 1] = {'params': params, 'v': dict(), 'a': [], 'n5': holder['n5']}
                for n5_k, n5_v in holder['n5'].items(): # Extracting the initial and decaying vertex of the heavy neutrino
                    #print(n5_k , n5_v)
                    selection.add(n5_k) # decaying vertex
                    #debido a que hicimos list(info) entonces se tiene que dentro de n5 tenemos:
                    # label del vertice decay: lista con px,py,etc... verticesaliente
                    #como vemos el ultimo elemento es el verticesaliente
                    selection.add(n5_v[-1]) # initial vertex
                #print(selection)
                #sacamos info del foton venga del neutrino o no
                for photon in holder['a']:
                    # select only the photons that come from a n5 vertex
                    # add photons
                    outg_a = photon[-1]
                    data[num - 1]['a'].append(photon)
                    #en selection esta el vertice entrante del neutrino pesado y el saliente
                    selection.add(outg_a)
                #set se queda con valores unicos y por ello se borran los duplicados
                #selection2.update(selection)
                #print("num: ", num)
                #print("selection: ", list(selection))
                selectiond[num - 1] = list(selection)
                
                for vertex in selection:
                    # select only the vertices that have a heavy neutrino or a photon interacting
                    #aqui el vertex tiene la misma estructura in_vertex : .... outvertex
                    data[num - 1]['v'][vertex] = holder['v'][vertex]
                #print("the data is:")        
                #print(data)
                #sys.exit("Exiting the script...")
                selection = set()

                holder = {'v': dict(), 'a': [], 'n5': dict()}
            num += 1

        elif line[0] == 'U':
            params = line[1:]
            if params[0] == 'GEV':
                p_scaler = 1
            else:
                p_scaler = 1 / 1000
            if params[1] == 'MM':
                d_scaler = 1
            else:
                d_scaler = 10
            # print(p_scaler)
        elif line[0] == 'V':
            #estamos guardando el varcode en una variable
            outg = int(line[1])
            #el 8 es el numero de particulas que sale (revisar manual hepmc)
            #el asterisco al inicio hace que sea una sequence
            info = *[float(x) for x in line[3:6]], int(line[8])  # x,y,z,number of outgoing
            #estamos guardando la informacion relevante del vertice
            #la linea holder['v'] esta accediendo a un diccionario
            #como sabemos, en un diccionario si realizamos dic['camote'] = int(7.5)
            #estamos creando un label llamado camote con el valor int(7.5) dentro
            #de esta forma estamos agregando un label al diccionario v que esta dentro de holder con el valor de list(info)
            holder['v'][outg] = list(info)
            # print(outg)
        elif line[0] == 'P':
            pid = line[1]
            pdg = line[2]
            in_vertex = int(line[11])
            #cual es la diferencia entre outg y in_vertex
	        #outg es el vertice donde aparece o se origina (primer item del v) y el in_vertex es el item 11 del p
	        # in_vertex == 0 implica que la particula no decae
            if (abs(int(pdg)) == 22) and (in_vertex == 0):
                # id = int(line[1])
                # px, py, pz, E, m = [float(x) for x in line[3:8]]
                info = int(pid), *[float(x) for x in line[3:8]], outg  # id px,py,pz,E,m,vertex from where it comes
                holder['a'].append(list(info))
            elif abs(int(pdg)) in neutralinos:
                info = *[float(x) for x in line[3:8]], outg  # px,py,pz,E,m,out_vertex
                 # en princip en el diccionario n5 se veria algo asi:
                # numero del vertice : info asociada al px,py,pz,E,m,out_vertex
                holder['n5'][in_vertex] = list(info)
                
    df.close()

     #mismo analisis para el evento final
    if final_part_active:
        # Event selection for the last event
        selection = set()
        data[num - 1] = {'params': params, 'v': dict(), 'a': [], 'n5': holder['n5']}
        for n5_k, n5_v in holder['n5'].items():
            # print(n5_k , n5_i)
            selection.add(n5_k)
            selection.add(n5_v[-1])
        for photon in holder['a']:
            # select only the photons that come from a n5 vertex
            outg_a = photon[-1]
            data[num - 1]['a'].append(photon)
            selection.add(outg_a)

        #selection2.update(selection)
        selectiond[num - 1] = list(selection)
        for vertex in selection:
            # select only the vertices that have a neutralino as incoming
            data[num - 1]['v'][vertex] = holder['v'][vertex]

    print(data[0])
    sys.exit("salimos")

    return

t_n = None
ATLASdet_radius= 1.5 #radio del detector de ATLAS
ATLASdet_semilength = 3.512 #Mitad de la longitud del radio de atlas (metros) (z_atlas)

# Adjusting detector boundaries
r_detec = ATLASdet_radius * 1000  # m to mm
z_detec = ATLASdet_semilength * 1000

mass_conversion = 1.78266192*10**(-27)	#GeV to kg
p_conversion = 5.344286*10**(-19)	#GeV to kg.m/s
c_speed = 299792458	#m/s

neutralinos = [9900016, 9900014, 9900012, 1000023]

destiny = "/Collider/scripts_2208/data/raw/"
types = ["ZH","WH","TTH"]
tevs = [13]

allcases = []
for typex in types[:]:
    for tevx in tevs[:]:
        #Nuevamente, abrimos los hepmc para reescribirlos
        for file_inx in sorted(glob.glob(f"/Collider/scripts_2208/data/raw/run_{typex}*{tevx}.hepmc"))[:]:
            allcases.append([file_inx, typex])

if __name__ == '__main__':
    with Pool(1) as pool:
        #print(allcases[-1:])
        pool.map(main, allcases)