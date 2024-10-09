import glob
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from math import floor, ceil
import scipy.ndimage
import sys

#En este codigo no estamos haciendo los graficos, pero si dando los puntos para que mathematica lo haga.
#En python se necesita puntos que esten igual espaciados, pero hay eventos con cero por lo cual se elimina y
#para mathematica esto no genera problemas.
#K factors son explicados en la pagina 11 del paper bounding dimension 5 ecuacion 17
k_factors = {'ZH':1.491,'WH':1.253,'TTH':1.15}

deltas = ['1','15']

#tenemos los eventos maximos para asi calcular el S = Luminosity*sigmaXH*BR(higgs - > N4 N5 ) Br(N4 -> nu gamma)
#de esta forma obtenemos BR(H -> N4 N5) considerando Br(N4 -> nu gamma) = 1. El S se encuentra en el paper 2023 Atlas

#nosotros tenemos los eventos y senales detectadas, pero experimentalmente hay una cantidad observada predicha por el ruido
#esos seran nuestros bound limits
#se puede usar el sigma yel events up para hallar BR(higgs - > N4 N5 ) debido a que S = Luminosity * Sigmaup 
# Los events_up se extrapolan a partir de los sigmas_up (ver paper alli explican la parte estadistica)
events_up = {6.84578:['1'],3.84578:['2+'],6.84844:['1','2+']}
sigmas_up = {0.042:['1'],0.022:['2+'],0.041:['1','2+']}

for delta in deltas[1:]:
    #print(delta)
    origin = f"./data/matrices_{delta}/"
    destiny = f"./data/"
    names = list(sorted(glob.glob(origin + f"bin_*.json")))
    #for n_up, channels in events_up.items():
    #print(names)

    for s_up, channels in sigmas_up.items():
        print(channels)
        ## Opening the files and assigning mass and alpha as tag
        values=[]
        for name in names[:]:
            #sacamos el indice de la masa
            mass = float(re.search(f'/.*M(\d+,?\d+|\d+)_', name).group(1).replace(',','.'))
            #sacamos el indice del alpha
            alpha = float(re.search(f'/.*Alpha(\d+,?\d+|\d+)_', name).group(1).replace(',','.'))
            #print(alpha)
            #sacamos el tipo de proceso
            proccess = re.search(f'/.*_13-(.*).json', name).group(1)
            #print(mass, alpha)
            with open(name, 'r') as file:
                info = json.load(file)
            #Sacamos solo la info que nos interesa que corresponde al canal que sea 1, 2+ o ambos
            #estamos haciendo un for en los canales y estamos sacando el ultimo bin de z, ultimo bin
            #de t y ulimo bin de met
            info = [np.asarray(info[ch])[-1,-1,-1] for ch in channels]
            print("info")
            print(info)
            #sys.exit()
            #esto vino de stackoverflow
            #lista con dos elementos, el primero es un tuple con mass y alpha y 
            #el segundo es el proceso y la suma de info sera en el caso que haya mas de un canal (1 y 2+)
            #en ese caso si sumara dos elementos, normalmente no sumara nada
            values.append([(mass,alpha),(proccess,sum(info))])
        
        #print("values")
        #print(values)
        # Example list of tuples
        #values = [
        #    ((1.5, 0.2), ('A', 10)),
        #    ((2.0, 0.3), ('B', 15)),
        #    ((3.2, 0.1), ('C', 20))
        #]

        # Loop over each tuple in values and print it
        #for value in values:
        #   print(value)
        
        #output 1:

        #((1.5, 0.2), ('A', 10))
        #((2.0, 0.3), ('B', 15))
        #((3.2, 0.1), ('C', 20))
        
        #Por otro lado, si hacemos

        #for value in values:
        #points.setdefault(value[0], []).append(value[-1])

        # Print the points dictionary
        #print(points)

        #output 2
        #{(1.5, 0.2): [('A', 10), ('C', 20)], (2.0, 0.3): [('B', 15)]}


        # Grouping them by same mass and alpha

        points = {}

        for value in values:
            #print(value)
            #lo que hacce este codigo es setear value[0] como key y realiza un append del ultimo elemento del tuple
            #recordar que el for value en un tuple recorre cada dos elementos del tuple
            points.setdefault(value[0], []).append(value[-1])

        """
        #print("Points")
        #print(points)

        #Para la data que tenemos realiza esto:
        #values
        #se esta haciendo un loop en cada linea y seleccionando el primer y ultimo elemento de esta
        #[[(9.0, 4.0), ('TTH', 24.28868992183456)], 
        #[(9.0, 4.0), ('WH', 10.269876)], 
        #[(9.0, 4.0), ('ZH', 0.0)], 
        #[(9.0, 5.0), ('TTH', 74.55709909174936)], 
        #[(9.0, 5.0), ('WH', 10.372179999999998)], 
        #[(9.0, 5.0), ('ZH', 2.8329312)], 
        #[(9.0, 6.0), ('TTH', 0.0)], 
        #[(9.0, 6.0), ('WH', 0.0)], 
        #[(9.0, 6.0), ('ZH', 0.0)]]
        #Points
        #{(9.0, 4.0): [('TTH', 24.28868992183456), ('WH', 10.269876), ('ZH', 0.0)], 
        #(9.0, 5.0): [('TTH', 74.55709909174936), ('WH', 10.372179999999998), ('ZH', 2.8329312)], 
        #(9.0, 6.0): [('TTH', 0.0), ('WH', 0.0), ('ZH', 0.0)]}

        

        #pre_params = [set(i for i,j in points.keys()), set(j for i,j in points.keys())]
        #masses, alphas = [sorted(list(x)) for x in pre_params]
        #print(masses, alphas)
        
        # Keeping only the ones that have three elements
        #len(val) == 3 es circular, simplemente hay que considerar los tres procesos, pero esto por default ya se da
        #val representa lo siguiente: [('TTH', 24.28868992183456), ('WH', 10.269876), ('ZH', 0.0)] es una lista de tuples
        #luego dentro de esta lista de tuples se esta haciendo un for donde proc toma el valor de cada elemento
        #dentro de cada elemento hay dos elementos y estos se seleccionan con proc[0] y proc[1]
        points = {key: [k_factors[proc[0]]*proc[1] for proc in val] for key, val in points.items() if len(val) == 3}
        #points = {key: val for key, val in points.items()}# if key[0] >2 and key[1] < 8}

        #print(points)
        #sys.exit()
        # Sum all the channels
        points = {key: sum(val) for key, val in points.items()}

        # Get the branching ratio
        #not_points = [key for key, val in points.items() if val == 0]
        #points = {key: 100 * n_up/(val/0.2) for key, val in points.items() if val > 0 }#and key[0]%1==0 and key[1]%1==0}
        #asumimos 0.2 porque para validar el paper ATLAS 2023, esto corresponde al BR( N4 -> nu gamma)
        #que normalmente se toma como uno.
        points = {key: 100 * s_up/(val/(139 * 0.2)) for key, val in points.items() if val > 0 }#and key[0]%1==0 and key[1]%1==0}
        data = [[*key,val] for key, val in points.items()]

        pd.DataFrame(data).to_csv(destiny + f'datapoints_{delta}GeV-{"_".join(channels)}-Sigma.dat',index=False)
        print(data)
        """
#sys.exit()
#
# print(f'points considered: {len(points)}')
# print(f'points not considered: {len(not_points)}')
#
# zoom = 1
# x,y = np.meshgrid(masses,alphas)
# z = np.full((len(alphas),len(masses)),max(points.values()))#max(points.values()))
# print(len(masses),len(alphas),z.shape)
#
# for xi, mass in enumerate(masses):
#     for yi, alpha in enumerate(alphas):
#         if (mass, alpha) in points:
#             val = points[(mass, alpha)]
#             #if val <= 500.:
#             if val > 0.:
#                 z[yi, xi] = val
#
# #print(z[9,1])
# #z = 10.**scipy.ndimage.zoom(np.log10(z),zoom)
# #print(z)
# color_min = floor(np.log10(min([x for x in points.values() if x > 0])))
# color_max = ceil(np.log10(max(points.values())))
#
# levels = 10. ** np.arange(color_min,color_max+1)
# #levels = 10. ** np.array([-1,0,1,2,5,19])
# plt.contourf(x,y,z,levels=levels,locator=ticker.LogLocator())
# plt.colorbar()
#
# not_px = [zoom*x for x,y in not_points]
# not_py = [zoom*y for x,y in not_points]
# px = [zoom*x for x,y in points.keys()]
# py = [zoom*y for x,y in points.keys()]
#
# #plt.scatter(px, py, color='pink')
# #plt.scatter(not_px, not_py, color='orange')
#
# plt.xlabel('MASS')
# plt.ylabel('ALPHA')
# plt.xlim(1,10)
# plt.ylim(1,10)
# plt.show()
