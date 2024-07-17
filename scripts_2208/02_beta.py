import re
import json
import numpy as np
from pathlib import Path
#import sys
#print(sys.version)
import pandas as pd
from my_funcs import my_arctan
import sys
import glob
from multiprocessing import Pool

import time

# Record the start time
start_time = time.time()

def main(paremeters):

    #Estas variables generaban histogramas de debugueo, actualmente eso esta en un branch de github
    z_prompts=[]
    z_origin = []
    pts = []
    pzs = []
    tofs = []
    tofs_b = []
    tofs_e = []
    p_tofs = []
    rel_tofs = []
    nus = []
    tns = []
    tphs = []
    trs = []
    tzs = []
    counter = 0
    dicts = []

    #estamos pasando la tupla de este tipo:
    #['/Collider/scripts_2208/data/clean/recollection_photons-ZH_M3_Alpha1_13-1.json'], 'ZH_M3_Alpha1_13']
    files, base_out = paremeters
    for file_in in files[:]:

        #print(file_in) #Commented by JJP
        #el try
        try:
            del data
        except UnboundLocalError:
            file_in
    
        with open(file_in, 'r') as file:
            data = json.load(file)
        #imprimomos la cantidad de keys en el diccionario (por que solo salen 2?)
        #print(len(data.keys())) #Commented by JJP
        #print(list(data.keys()))
        #sys.exit("salimos")
        #los keys son el numero de eventos.con list podemos hacer un debugging y correr solo los primeros diez
        i = 0
        for event in list(data.keys())[:]:
            #print(event)
            #if (int(event) % 500) == 0:
                #print(f'RUNNING: {base_out} - ATLAS - Event {event}') #Commented by JJP
            #por que no se usan comillas en este caso?
            #no se usan pues event es una variable que esta en el for y hace referencia al data.keys()
            print(event)
            i = i + 1
            holder = data[event]
            #print(holder)
            params = holder['params']
            #print(params) 
            
            # Defining scaler according to parameters units
            if params[0] == 'GEV':
                p_scaler = 1  # GeV to GeV
            elif params[0] == 'MEV':
                p_scaler = 1 / 1000  # MeV to GeV
            else:
                #print(params[0])
                continue

            if params[1] == 'MM':
                d_scaler = 1  # mm to mm
            elif params[1] == 'CM':
                d_scaler = 10  # cm to mm
            else:
                #print(params[1])
                continue
            
            # Adjusting detector boundaries
            r_detec = ATLASdet_radius * 1000  # m to mm
            z_detec = ATLASdet_semilength * 1000

            # Define our holder for pairs:

            ix = 1
            i = 1
            file_path = '/Collider/limon/scripts_2208/outputwd.txt'

            # Open the file in write mode
            with open(file_path, 'w') as file:
                pass  # No need to write anything initially

            
            for photon in holder['a']:
                
                info = dict()
                info['Event'] = int(event) 
                # id px,py,pz,E,m,vertex from where it comes
                # esto venia de antes, ahora solo extraemos el ultimo
                vertex = str(photon[-1])
                
                pid = photon[0]
                px, py, pz = [p_scaler*ix for ix in photon[1:4]]
                x, y, z, ctau= [d_scaler*ix for ix in holder['v'][vertex][0:4]]
                mass_ph = photon[-2] * p_scaler
                r = np.sqrt(x ** 2 + y ** 2)
                # Calculating transverse momentum
                pt = np.sqrt(px ** 2 + py ** 2)
                Et = np.sqrt(mass_ph ** 2 + pt ** 2)
                E = np.sqrt(mass_ph ** 2 + pt ** 2 + pz ** 2)

                # print(mass_ph)
                info['pid'] = pid
                info['r'] = r / r_detec
                info['z'] = z / z_detec
                info['px'] = px
                info['py'] = py
                info['pt'] = pt
                info['pz'] = pz
                info['ET'] = Et
                info['E'] = E
                ix += 1
                
                #print(px)
                
                #se puede salir fuera del circulo y fuera de z
                if pt < 10.0:
                    continue
                elif r >= (r_detec) or abs(z) >= (z_detec):
                     continue

                #print(vertex)
                # Calculating the z_origin of each photon
                v_z = np.array([0, 0, 1])  # point in the z axis
                d_z = np.array([0, 0, 1])  # z axis vector

                v_ph = np.array([x, y, z]) # point in the trayectorie of the photon
                d_ph = np.array([px, py, pz]) # vector of the trayectorie

                n = np.cross(d_z, d_ph)

                n_ph = np.cross(d_ph, n)

                c_z = v_z + (((v_ph - v_z) @ n_ph) / (d_z @ n_ph)) * d_z
		
		
                # Calculating the time of flight
                try:
                    # TIme of the neutralino
                    #aqui buscamos que tenga el mismo vertice que el foton?
                    # el vertice del que entra el neutrino pesado es el mismo del que sale el foton
                    #vertex_n es el vertice donde se origina el neutrino pesado, el outg (de donde sale)
                    #por eso es el try porque si sale un error es que el neutrino viene de un foton
                    #print(vertex)
                    #Pregunta Jones: se podria hacer un codigo para que la particula decaiga en dos fotones
                    vertex_n = str(holder['n5'][vertex][-1])
                    #print(vertex_n)
                    mass_n = holder['n5'][vertex][-2] * p_scaler
                    
                    # print(mass_n)
                    pdg_n, px_n, py_n, pz_n, E_n = [p_scaler*ix for ix in holder['n5'][vertex][0:5]]
                    
                    x_n, y_n, z_n = [d_scaler*ix for ix in holder['v'][vertex_n][0:3]]
                    
                    
                    #print(pdg_n)
                    # print(vertex_n)
                    #Hallamos la distancia entre su vertice de origen y su vertice de decaimiento 
                    #(en el cual se origina el foton delayed)
                    dist_n = np.sqrt((x - x_n) ** 2 + (y - y_n) ** 2 + (z - z_n) ** 2)
                    p_n = np.sqrt(px_n ** 2 + py_n ** 2 + pz_n ** 2)
                    #if(pdg_n == 9900016):
                    #    print(dist_n)
                    L = np.sqrt( x** 2 + y**2 + z**2)
                    beta_n = p_n/E_n

                    #print(beta_n)

                    L_walter = beta_n*ctau

                    L_walter_sin_beta = ctau

                    #difference = abs(L - L_walter)
                    #print("the difference is: ", difference)

                    #difference = abs(dist_n - L_walter)
                    #print("the difference is: ", difference)
                    difference = abs((L - L_walter)/L)
                    
                    #print(L_walter, difference)
                    #differences.append(difference)
                    #with open(file_path, 'a') as file:  # Open in append mode to add content
                    #    file.write(str(difference) + '\n')
                    
                    #print(p_conversion/mass_conversion)
                    prev_n = (p_n * p_conversion) / (mass_n * mass_conversion)
                    
                    #usar formula relativista vector (p) = gamma.m.vector(v)
                    
                    v_n = (prev_n / np.sqrt(1 + (prev_n / c_speed) ** 2)) * 1000  # m/s to mm/s
                    # Dividimos la distancia entre la rapidez del NP
                    
                    t_n = dist_n / v_n  # s
                    
                    t_n = t_n * (10 ** 9)  # ns

                    #print(t_n)
                    #print(t_n)
                    tns.append(t_n)
                    #print(t_n)
                    #print(z)
                    ic = 0
                    
                except KeyError:
                    #si el foton no viene del neutrino pesado entonces en prompt
                    t_n = 0.0
                    #x= y = z = r = 0.0
                    ic = 1
                    z_prompts.append(z)
                    #print(z)
                #print(t_n)
                # Now, time of the photon
                #aqui considerar que el vector (p) nos da la direccion en la que se mueve la particula
                #y esta lo hace con modulo de velocidad c y despues lo descompones en sus tres componentes
                vx = (c_speed * px / np.linalg.norm(d_ph)) * 1000  # mm/s
                vy = (c_speed * py / np.linalg.norm(d_ph)) * 1000  # mm/s
                vz = (c_speed * pz / np.linalg.norm(d_ph)) * 1000  # mm/s
                

                tr = (-(x * vx + y * vy) + np.sqrt(
                    (x * vx + y * vy) ** 2 + (vx ** 2 + vy ** 2) * (r_detec ** 2 - r ** 2))) / (
                         (vx ** 2 + vy ** 2))
                #r_detec equivale a rcms
                if tr < 0:
                    tr = (-(x * vx + y * vy) - np.sqrt(
                        (x * vx + y * vy) ** 2 + (vx ** 2 + vy ** 2) * ((r_detec) ** 2 - r ** 2))) / (
                             (vx ** 2 + vy ** 2))

                tz = (np.sign(vz) * z_detec - z) / vz

                # Now we see which is the impact time
                if tr < tz:
                    # rf = r_detec
                    rf = r_detec
                    #todo queda en funcion de tr pues ese es el tiempo real de colision
                    zf = z + vz * tr
                    #lo estamos regresando a GeV?
                    t_ph = tr * (10 ** 9)

                    x_final = x + vx * tr
                    y_final = y + vy * tr

                elif tz < tr:
                    #estamos encontrando el radio en donde sale del detector al salir por el eje z
                    rf = np.sqrt((y + vy * tz) ** 2 + (x + vx * tz) ** 2)
                    zf = np.sign(vz) * z_detec
                    t_ph = tz * (10 ** 9)

                    x_final = x + vx * tz
                    y_final = y + vy * tz

                else:
                    rf = r_detec
                    zf = np.sign(vz) * z_detec
                    t_ph = tz * (10 ** 9)

                    x_final = x + vx * tz
                    y_final = y + vy * tz
                
                #print("tz, rf, r_detec, zf, t_ph, x_final, y_final: ", tz, rf, r_detec, zf, t_ph, x_final, y_final)

                #print(t_n)
                tof = t_ph + t_n
                
                prompt_tof = (10**9)*np.sqrt(rf**2+zf**2)/(c_speed*1000)
                rel_tof = tof - prompt_tof

                #print("prompt_tof, rel_tof: ",prompt_tof, rel_tof)
                phi = my_arctan(y_final, x_final)

                theta = np.arctan2(rf, zf)
                nu = -np.log(np.tan(theta / 2))

                counter += 1

                z_origin.append(c_z[-1])
                pts.append(pt)
                pzs.append(pz)
                tofs.append(tof)
                if abs(nu) < abs(-np.log(np.tan(np.arctan2(r_detec, z_detec) / 2))):
                    tofs_b.append(tof)
                else:
                    tofs_e.append(tof)
                p_tofs.append(prompt_tof)
                rel_tofs.append(rel_tof)
                nus.append(nu)
                #print(t_n)
                tphs.append(t_ph)
                trs.append(tr * (10 ** 9))
                tzs.append(tz * (10 ** 9))

                info['eta']=nu
                info['phi']=phi
                #estamos extrayendo la ultima coordenada del punto
                info['z_origin'] = abs(c_z[-1])
                info['rel_tof'] = rel_tof

                dicts.append(info)

    #print("the total number of times that the difference was bigger than 5%:  ", i)
    #print(differences)
    sys.exit("Salimos del codigo")
    #print(f'Detected photons in ATLAS: {counter}') #Commented by JJP

    dicts = pd.DataFrame(dicts)
    #print(dicts) #Commented by JJP

    #pickle te permite usar los data_frame de una forma mas rapida
    dicts.to_pickle(destiny_info+f'photon_df-{base_out}.pickle')
    #print('df saved!') #Commented by JJP
    
    return

#unidades metros
ATLASdet_radius= 1.5
# la mitada de la longitud en z del detector
ATLASdet_semilength = 3.512

mass_conversion = 1.78266192*10**(-27)	#GeV to kg
p_conversion = 5.344286*10**(-19)	#GeV to kg.m/s
c_speed = 299792458	#m/s

types = ["ZH","WH","TTH"]
tevs = [13]
destiny_info = '/Collider/scripts_2208/data/clean/'

allcases = []
for type in types[:]:
    for tev in tevs[:]:
        # Este codigo a lo que originalmente tiene la sintaxis recollection_photons_ZH_M3_Alpha2_13.json
        # la reduce a ZH_M3_Alpha2_13
        mwpairs = set(re.search(f'({type}.+)\-', x).group(1) for x in
                      glob.glob(f'/Collider/scripts_2208/data/clean/recollection_photons-{type}*{tev}-*.json'))
        #print('Type: {}, TEV: {}, MWPairs: {}'.format(type, tev, mwpairs))
        for base_out in sorted(list(mwpairs))[:]:
            allcases.append(
                [sorted(glob.glob(f'/Collider/scripts_2208/data/clean/recollection_photons-{base_out}-*.json')),base_out]
            )
#cuando trabajemos con mas data tendremos una mayor cantidad de archivos json
if __name__ == '__main__':
    with Pool(1) as pool:
        pool.map(main, allcases)


# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds")