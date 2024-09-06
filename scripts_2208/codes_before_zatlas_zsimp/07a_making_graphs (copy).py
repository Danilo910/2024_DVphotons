import sys
import matplotlib.pyplot as plt
import glob
import re
import json
import numpy as np
import os

#M9 A4 M9 A5 M9 A6 
#file_path = "/data/matrices_15/bin_matrices-M3_Alpha1_13-WH.json"

#if os.access(file_path, os.R_OK):
#    print("File is readable by Python.")
#else:
#    print("File is not readable by Python.")


destiny = f"./data/"

deltas = ['15']
met_labels = ['BKG', 'CR', 'SR']
vround = np.vectorize(round)
colores = {'60':'r','50':'g','40':'b','30':'m'}
k_factors = {'ZH':1.491,'WH':1.253,'TTH':1.15}
new_mode = 0o666
process_label = ['ZH', 'WH', 'TTH']

#origin = f"./data/matrices_15"
#for alpha in ['1','2','3']:
#    for process in process_label:
#        file_path = origin + f"/bin_matrices-M3_Alpha{alpha}_13-{process}.json"
        #print(file_path)
#        os.chmod(file_path, new_mode)


for delta in deltas[:]:
    origin = f"./data/matrices_{delta}/"
    fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(20, 30))
    plt.subplots_adjust(left=None, bottom=0.05, right=None, top=0.95, wspace=None, hspace=0.3)
#adaptar el codigo para que corra en vez de las masas en los alpha
    #print(origin)
    
    for alpha in ['4','5','6']:
        burrito = []
        #estamos buscando los input file, como resultado, tendremos para alpha = 1 una lista de elementos
        #['./data/matrices_15/bin_matrices-M3_Alpha1_13-ZH.json', 
        #'./data/matrices_15/bin_matrices-M3_Alpha1_13-WH.json', './data/matrices_15/bin_matrices-M3_Alpha1_13-TTH.json']
        input_files = list(reversed(sorted(glob.glob(origin + f"bin_*M9_Alpha{alpha}_*.json"))))
        #input_files = list(reversed(sorted(glob.glob(origin + f"bin_matrices-M3_Alpha{alpha}_*.json"))))
        #print(input_files)

        for input_file in input_files:
            #seleccion WH, ZH o TTH
            process = re.search(f'/.*_13-(.*).json', input_file).group(1)
            #print(process)
            with open(input_file, 'r') as file:
                cofre = json.load(file)
            #estamos haciendo un loop sobre cada key y matriz en ese key para editarlo y convertirlo
            # en un np.asarray. K_factors es un diccionario que agrega un determinado peso para cada proceso.
            cofre = {key: k_factors[process]*np.asarray(matrix) for key, matrix in cofre.items()}
            #print(cofre)
            #sys.exit()
            #print(cofre)
            # suponer que inicialmente se tiene
            #cofre = {
            #   'key1': [7, 8, 9],
            #   'key3': [10, 11, 12]
            #}
            #en el primer loop burrito seria lo mismo, luego suponer que se cambia
            #cofre = {
                #'key1': [7, 8, 9],
                #'key3': [10, 11, 12]
            #}
            # luego burrito sera 
            #burrito = {
            #    'key1': [1, 2, 3] + [7, 8, 9],  # Sum of existing and new values for 'key1'
            #    'key2': [4, 5, 6],               # Existing values for 'key2'
            #    'key3': [10, 11, 12]             # New values for 'key3'
            #}
            if burrito == []:
                burrito = cofre
            else:
                #por que estamos sumando en las matrices de los eventos?
                #sumamos todos los procesos porque simulamos lo que veriamos como tal en simulador
                #en este no se distingue si vine de ZH, WH O TTH
                burrito = {key: burrito[key] + cofre[key] for key in cofre.keys()}
            #print(burrito)
        #sys.exit()
        norm = sum([x[:,:,-1].sum() for x in burrito.values()])
        #estamos normalizando la data
        burrito = {key: value[:,:,-1]/norm for key, value in burrito.items()}
        #print(sum([x.sum() for x in burrito.values()]))
        #sys.exit()
        ymax_p = []
        ymin_p = []

        for key, matrix in burrito.items():
            nbins = np.array(range(matrix.shape[1] + 1)) + 0.5
            #este codigo realiza lo siguiente, por ejemplo si tenemos
            #burrito = {
            #    'matrix1': np.array([[1, 2, 3], [4, 5, 6]]),
            #    'matrix2': np.array([[7, 8, 9], [10, 11, 12], [13, 14, 15]])
            #}
            #luego nos devolvera np.array(range(3 + 1)) + 0.5 -> np.array([0.5, 1.5, 2.5, 3.5])
            #esto nos viene a dar los bins que estan espaciados correctamente
            #
            ix = int(key[0]) - 1
            ir = 0
            #print(nbins)
            #print(matrix[ir][:,-1])
            #sys.exit()
            #axs representa un arreglo de todos los subplots
            #un subplot solo un grafico de un conjunto de graficos que se muestran en un solo archivo
            #i = 0
            for row in axs:
                #print(i)
                #print(row)
                #i = i +1
                #ix es el iterador en la columna, caso 1 y caso 2fotones en este caso
                row[ix].hist(nbins[:-1],
                             bins=nbins, weights=matrix[ir], histtype='step', label=f'Alpha {alpha}')
                row[ix].set_yscale('log')
                row[ix].set_xticks(np.array(range(matrix.shape[1])) + 1)
                row[ix].set_title(f'Dataset {key} ph - bin z {ir + 1}')
                row[ix].legend()
                row[ix].secondary_yaxis("right")
                ymax_p.append(row[ix].get_ylim()[1])
                ymin_p.append(row[ix].get_ylim()[0])
                ir += 1
    ymax = max(ymax_p)
    ymin = min(ymin_p)
    plt.setp(axs, ylim=(ymin,ymax))
    plt.suptitle(f'Mass 9 - Delta {delta}')
    #plt.show()
    fig.savefig(destiny + f'validation_graphs-Delta{delta}.png')
    plt.close()