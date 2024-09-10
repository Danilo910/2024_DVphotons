import json
import numpy as np
from pathlib import Path
import gc
import glob
import re
from multiprocessing import Pool
import sys
import time

start_time = time.time()


def main(parameters):
    # Programming Parameters
    # Parameters es un vector que posee distintas componentes con la estructura
    #['/Collider/scripts_2208/data/raw/run_ZH_M3_Alpha2_13.hepmc', 'ZH']
    file_in, type = parameters

    #print(file_in)
    #print(type)
    #sys.exit("Salimos")
    # Extract label
    # Este codigo a lo que originalmente tiene la sintaxis run_ZH_M3_Alpha2_13.hepmc
    #la reduce a ZH_M3_Alpha2_13
    base_out = re.search(f'({type}.+)\.', file_in).group(1)
    # Name of output file
    #Todos los diccionarios terminaran en json
    file_out = destiny + f'recollection_photons-{base_out}.json'

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
    
    # Action
    # Open the hepmc
    df = open(file_in, "r")

    # Reading unnecesary lines
    #Con este codigo nos estamos salteando las dos primeras lineas del hepmc que tienen basura
    while it < 2:
        df.readline()
        it += 1

    # Initializing values
    data = dict()
    num = 0
    p_scaler = None
    d_scaler = None
    #selection2 = set() 
    for sentence in df:
        #while i<(limit+20):
        #sentence = df.readline()
        # print(sentence)
        line = sentence.split() # Divide the wtring in whitespaces
        #como en nuestro caso corte_inf es cero, solo correra una vez
        if num <= corte_inf:
            #'v': dict(),   # 'v' key associated with an empty dictionary
            #'a': [],       # 'a' key associated with an empty list
            #'n5': dict()   # 'n5' key associated with an empty dictionary
            holder = {'v': dict(), 'a': [], 'n5': dict()}
            #si el primer elemento del vector line es la letra E, continua
            #cada hepmc puede tener varios eventos, aqui estamos recogiendo hasta el corte_inf (por ejemplo 500)
            if line[0] == 'E':
                if (num % 500) == 0:
                    print(f'RUNNING: {base_out} ' + f'Event {num}')
                    print(0)
                num += 1
            nfile = it_start + 1
            #con este continue regresamos a la siguiente iteracion del while sin leer lo de abajo
            continue
        elif line[0] == 'E':
            # num = int(line[1])
            if num > 0:  # Selection of relevant particles/vertices in the last event
                selection = set() # Vertices that interact with a heavy neutrino
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
                for vertex in selection:
                    # select only the vertices that have a heavy neutrino or a photon interacting
                    #aqui el vertex tiene la misma estructura in_vertex : .... outvertex
                    data[num - 1]['v'][vertex] = holder['v'][vertex]
            #print("the data is:")        
            #print(data)
            #sys.exit("Exiting the script...")
            holder = {'v': dict(), 'a': [], 'n5': dict()}
            i += 1
            if (num % 500) == 0:
                print(f'RUNNING: {base_out} ' + f'Event {num}')
                print(len(data))
            if num == nfile * batch:
                with open(file_out.replace('.json', f'-{nfile}.json'), 'w') as file:
                    json.dump(data, file)
                    #estamos guardando en json diferentes por cada batch
                print(f'Saved til {num - 1} in {file_out.replace(".json", f"-{nfile}.json")}')
                del data
                gc.collect()

                data = dict()
                holder = {'v': dict(), 'a': [], 'n5': dict()}
                nfile += 1
            if num == corte_sup:
                final_part_active = False
                break
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
        for vertex in selection:
            # select only the vertices that have a neutralino as incoming
            data[num - 1]['v'][vertex] = holder['v'][vertex]

        with open(file_out.replace('.json', f'-{nfile}.json'), 'w') as file:
            json.dump(data, file)

        #print(f'FINAL {base_out}: Saved til {num - 1} in {file_out.replace(".json", f"-{nfile}.json")}\n')
    
    #print("selection: ")
    #print(selection2)
    return

# Particle Parameters
#son neutrinos pesados
#identificador de la naturaleza de la particula
neutralinos = [9900016, 9900014, 9900012, 1000023]
neutrinos = [12, 14, 16, 1000022]

destiny = "/Collider/scripts_2208/data/clean/"
#destiny = "/home/cristian/"
types = ["ZH","WH","TTH"]
tevs = [13]

#aqui creamos el directorio especificado en destiny
Path(destiny).mkdir(exist_ok=True, parents=True)

allcases = []
#Hacemos un loop en typex, tevx, y file_inx: si es ZH,WH O TTH, distinta energia y run_{typex}*{tevx}.hepmc siendo el distinto archivo
for typex in types[:]:
    for tevx in tevs[:]:
    #glob sirve para buscar un patron de strings en el directorio dado, nos da la lista de directorios que coinciden con el patron
    #sorted lo ordena en orden alfabetico
    #En nuestro caso tenemos run_TTH_M3_Alpha1_13.hepmc  run_TTH_M3_Alpha3_13.hepmc  run_WH_M3_Alpha2_13.hepmc  				       run_ZH_M3_Alpha1_13.hepmc   run_ZH_M3_Alpha3_13.hepmc   run_TTH_M3_Alpha2_13.hepmc  				       run_WH_M3_Alpha1_13.hepmc   run_WH_M3_Alpha3_13.hepmc  run_ZH_M3_Alpha2_13.hepmc 
    #si por ejemplo estamos en el caso ZH y tevx = 13
    #Entonces el resultado seria el siguiente vector:
    #['/Collider/scripts_2208/data/raw/run_ZH_M3_Alpha1_13.hepmc',
    # '/Collider/scripts_2208/data/raw/run_ZH_M3_Alpha2_13.hepmc',
    # '/Collider/scripts_2208/data/raw/run_ZH_M3_Alpha3_13.hepmc']
        for file_inx in sorted(glob.glob(f"/Collider/scripts_2208/data/raw/run_{typex}*{tevx}.hepmc"))[:]:
            allcases.append([file_inx, typex])

#print(allcases[-1])
#sys.exit("Salimos")
main(allcases[-1])
#este pool es como un foor, estamos haciendo main(allcases[i])
#if __name__ == '__main__':
#    with Pool(1) as pool:
#        pool.map(main, allcases[-1])


# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")