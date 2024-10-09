import sys
import matplotlib.pyplot as plt
import glob
import re
import json
import numpy as np

#plt.switch_backend('agg')  # Use the 'agg' backend
#plt.ion()  # Turn on interactive mode

#este solo analiza un grupo de matrices .json, el 07a si analiza dos grupos que se diferencian por el delta
#correccion: antes origin = f"./data/matrices/"
#            ahora origin = f"./data/matrices_15/"
origin = f"./data/matrices_15/"
destiny = f"./cases/"

met_labels = ['BKG', 'CR', 'SR']
#round es una funcion inherente de python, es como print
#round normalmente solo actua sobre integers, con eso acutara sobre vectores
vround = np.vectorize(round)

colores = {'60':'r','50':'g','40':'b','30':'m'}
fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(20, 30))
plt.subplots_adjust(left=None, bottom=0.05, right=None, top=0.95, wspace=None, hspace=0.3)

print("antes del for")
#plt.show()

for input_file in list(reversed(sorted(glob.glob(origin + f"bin_*.json"))))[:]:

    ymax_p = []
    ymin_p = []
    print("despues del for")
    base_out = re.search(f'/.*bin_matrices-(.+)\.json', input_file).group(1)
    print(base_out)

    with open(input_file, 'r') as file:
        burrito = json.load(file)

    burrito = {key: np.asarray(matrix) for key, matrix in burrito.items()}

    for key, matrix in burrito.items():
        nbins = np.array(range(matrix.shape[1] + 1)) + 0.5
        ix = int(key[0]) - 1 #columna de los graficos
        ir = 0 #row de la matriz
        #print(matrix[ir][:,-1])
        #sys.exit()
        for row in axs:
            row[ix].hist(nbins[:-1],
                         bins=nbins, weights=matrix[ir][:,-1], histtype='step',
                         stacked=False, label=base_out, color=colores[re.search(f'MN(.+)_ML', base_out).group(1)])
            row[ix].set_yscale('log')
            row[ix].set_xticks(np.array(range(matrix.shape[1])) + 1)
            row[ix].set_title(f'Dataset {key} ph - bin z {ir + 1}')
            row[ix].legend()
            row[ix].secondary_yaxis("right")
            ymax_p.append(row[ix].get_ylim()[1])
            ymin_p.append(row[ix].get_ylim()[0])
            ir += 1
#al final se deberia programar para hallar el maximo y minimo 10**-2 y el 2*10**6

plt.setp(axs, ylim=(10**-2, 2*10**6))
#plt.suptitle(f'{base_out} GeV\n{events} events')
#plt.show()
fig.savefig(destiny + f'validation_graphs.png')
plt.close()
