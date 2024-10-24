import sys
import os
import pandas as pd
import glob
import ROOT
import numpy as np
from multiprocessing import Pool


def main(input_file):

    #recordar que el input es .root
    #estamos cambiando el .root por _photons.pickle y el nombre lo guardamos como string en outfile
    out_file = input_file.replace('.root','_photons.pickle')
    #out_file = out_file.replace(origin, destiny)

    # Create chain of root trees
    chain = ROOT.TChain("Delphes")
    chain.Add(input_file)

    # Create object of class ExRootTreeReader
    treeReader = ROOT.ExRootTreeReader(chain)
    numberOfEntries = treeReader.GetEntries()
    print(input_file)
    #print(numberOfEntries)
    #print("\n")
    #sys.exit("Salimos")
    
    met = treeReader.UseBranch("MissingET")
    branchPhoton = treeReader.UseBranch("Photon")
    branchJet = treeReader.UseBranch("Jet")
    branchElectron = treeReader.UseBranch("Electron")
    branchMuon = treeReader.UseBranch("Muon")

    # Loop over all events
    photons = []
    jets = []
    leptons = []

    
    #print(f"Number of Entries: {numberOfEntries}") #Commented by JJP
    #entry sera el numero de eventos (en nuestro caso son 500 eventos de 0 a 499 seria el iterador)
    contador_jets_un_muon = 0
    todos_los_jets = 0
    for entry in range(numberOfEntries):
        # Load selected branches with data from specified event
        if(entry%5000 == 0):
            print("Estamos en el evento: ",entry)
        #con este codigo desbloqueamos la informacion de todos los branch (por ejemplo treeReader.UseBranch("Photon"))
        treeReader.ReadEntry(entry)
        #esta es la forma de extraer el MET del evento
        miss = met[0].MET
        #print(entry0)

        counter = 0
        #print(branchPhoton, branchElectron, branchMuon)
        #ahora con la informacion desbloqueada podemos, por cada evento correr sobre los fotones
        """
        for ph in branchPhoton:
        # Print the element
            print(ph)
            
            # Increment the counter
            counter += 1
            
            # Check if the counter has reached 4
            if counter == 4:
                # If it has, exit the loop
                break
        """

        for jet in branchJet:
            #Condiciones para jets
            #print("Entramos al jet")
            #Write_jet = True
            if jet.PT > 25:
                #Formula del rapidity en base a los atributos que si tenemos
                y = np.log((jet.PT * np.sinh(jet.Eta) + np.sqrt(jet.Mass**2 +
                    (jet.PT * np.cosh(jet.Eta))**2)) / (np.sqrt(jet.Mass**2 + jet.PT**2)))
                if abs(y) < 4.4: 
                    
                    jets.append({"N": entry, "pt": jet.PT, "eta": jet.Eta, 'phi': jet.Phi})
                    
                    ConstList = 0

                    #print("Constituyentes del jet")
                    #print(jet.Constituents.GetEntries())
                    
                    if jet.Constituents.GetEntries() == 1:

                        obj = jet.Constituents.At(0)                        
                        strings=str(jet.Constituents.At(0))
                        #print(strings)
                        if strings == "Name: Muon Title: ":
                            #print("Tenemos un muon")
                            #print("El jet esta hecho por un muon")
                            #Write_jet = False
                            contador_jets_un_muon = contador_jets_un_muon + 1
                    
                    #if(Write_jet):
                        #print("El evento esta hecho por mas particulas y no solo un muon")
                    #    jets.append({"N": entry, "pt": jet.PT, "eta": jet.Eta, 'phi': jet.Phi})
                
        for ph in branchPhoton:
            #print(ph)
            
            #print(ph.PT, ph.Eta)
            #condiciones experimentales del detector
            if ph.PT > 10 and (abs(ph.Eta) < 1.37 or 1.52 < abs(ph.Eta) < 2.37):
                #print(ph.Eta)
                #entry nos da el numero del evento (de 0 a 499 en nuestro caso)
                photons.append({"N": entry, "E":ph.E, "pt":ph.PT, "eta":ph.Eta, 'phi': ph.Phi,
                                'z_origin': ph.ZOrigin, 'rel_tof': ph.RelativeT,'MET': miss})
        
        #sys.exit("Salimos")

    
        for e in branchElectron:
            #if e.PT > 10 and (abs(e.Eta) < 1.37 or 1.52 < abs(e.Eta) < 2.47):
            leptons.append({"N": entry, 'pdg': 11, "pt":e.PT,
                            "eta":e.Eta, 'phi': e.Phi, 'mass': 0.000511})

        for mu in branchMuon:
            #if mu.PT > 10 and abs(mu.Eta) < 2.7:
            leptons.append({"N": entry, 'pdg': 13, "pt": mu.PT,
                            "eta": mu.Eta, 'phi': mu.Phi, 'mass': 0.10566})
        

    #print("Estamos en el run: ", input_file)
    #print("Cantidad de jets hechos por un muon en el respectio run: ", contador_jets_un_muon)

    
    #sys.exit("Salimos")
    #input_file.close()
    chain.Clear()

    #definimos los dataframes
    df = pd.DataFrame(photons)
    df_jets = pd.DataFrame(jets)
    df_leps = pd.DataFrame(leptons)

    #si los fotones o los leptones no tiene filas (registros) entonces la funcion acaba alli
    if (df.shape[0] == 0) or (df_leps.shape[0] == 0):
        print(df.shape,df_leps.shape)
        return
    #si los jets no poseen filas,de todas formas inicializa los jets con esa estructura de columnas.
    #esto es util si deseamos llenar mas adelante el dataframe de los jets
    if df_jets.shape[0] == 0:
        df_jets = pd.DataFrame(columns=["N", "pt", "eta", 'phi','M', 'MET'])
        #print(df_jets)
    
    #print("Antes de ordenar")
    #print(df)
    #si es que N ya esta ordenado, ordenar el pt no cambiaria este orden, solo daria dentro del mismo grupo de N
    #por ejemplo en el evento 3 del mayor a menor valor en el pt
    #hacemos la prioridad de N ordenandolos y mantenemos ese orden, si solo ordenamos en pt, esto desordenaria todo
    #ya que no distinguiria el evento y lo ordenaria solo por pt
    df = df.sort_values(by=['N', 'pt'], ascending=[True, False])
    #print("antes de g")
    #print(df)
    #sys.exit()

    #The following code will do this:
    #   N  pt
    #0  1  10
    #1  1  20
    #2  2  30
    #3  2  40
    #4  2  50

       #N  pt  g
    #0  1  10  0
    #1  1  20  1
    #2  2  30  0
    #3  2  40  1
    #4  2  50  2

    #como se observa el N tiene dos repeticiones (dos fotones uno menos energetico y otro mas), entonces
    #g tendra el primer foton (mas energetico) con un indice 0 y el segundo con indice 1. Si hubiera otro, tendria el 
    #indice 2 en g.

    #creamos una columna nueva como vemos anteriormente
    g = df.groupby('N', as_index=False).cumcount()
    # en realidad hasta este momento no hemos creado una columna hasta que no aplicamos el codigo que viene abajo
   
    #ahora creamos otra columna con el nombre de id
    df['id'] = g
    
    #print("despues de g")
    #print(df)
    #sys.exit()
    
    #hacemos un multi_indice
    df = df.set_index(['N', 'id'])

    # la data ahora se vera asi
    #        pt  g
    #N id        
    #1 1     10  0
    #  2     20  1
    #2 1     30  0
    #  2     40  1
    #  3     50  2

    #print(f'{100 * df.index.unique(0).size / numberOfEntries:2f} %') #Commented by JJP
    df.to_pickle(out_file)

    df_jets = df_jets.sort_values(by=['N', 'pt'], ascending=[True, False])
    g = df_jets.groupby('N', as_index=False).cumcount()
    df_jets['id'] = g
    df_jets = df_jets.set_index(['N', 'id'])
    #creamos otro pickle, pero cambiando el nombre de fotones a jets
    df_jets.to_pickle(out_file.replace('_photons','_jets'))

    #seguimos el mismo procedimiento para los leptones
    df_leps = df_leps.sort_values(by=['N', 'pt'], ascending=[True, False])
    g = df_leps.groupby('N', as_index=False).cumcount()
    df_leps['id'] = g
    df_leps = df_leps.set_index(['N', 'id'])
    df_leps.to_pickle(out_file.replace('_photons', '_leptons'))
    #print(df) #Commented by JJP
    
    return


#Commented by JJP
#print('ROOT FIRST ATTEMPT:',ROOT.gSystem.Load("libDelphes"))
#print('DELPHES CLASSES   :',ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"'))
#print('EXRROT TREE READER:',ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"'))
ROOT.gSystem.Load("libDelphes")
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')


for mode_atlas in ["", "zsimp"]:
    print("Mode_atlas: ",mode_atlas)
    origin = f"/Collider/scripts_2208/data/clean{mode_atlas}/"
    destiny = f"/Collider/scripts_2208/data/clean{mode_atlas}/"
    #destiny = f"/Collider/2023_LLHN_CONCYTEC/"

    types = ['ZH', "WH", "TTH"]
    tevs = [13]
    allcases = []

    if(mode_atlas == ""):
        for typex in types[:]:
            for tevx in tevs[:]:
                for file_inx in sorted(glob.glob(origin + f"full_op_{typex}*{tevx}.root"))[:]:
                    allcases.append(file_inx)
    else:
        for typex in types[:]:
            for tevx in tevs[:]:
                for file_inx in sorted(glob.glob(origin + f"{mode_atlas}_full_op_{typex}*{tevx}.root"))[:]:
                    allcases.append(file_inx)

    print("allcases: ", allcases)
    #sys.exit("SALIMOS")
    #estamos pasandole .root como input_file
    
    if __name__ == '__main__':
        #print(allcases) #Commented by JJP
        with Pool(1) as pool:
            pool.map(main, allcases)