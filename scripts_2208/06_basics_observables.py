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
import matplotlib.pyplot as plt
import os
#import os
# Function to print the content based on its type
def print_contents(label, data):
    print(f"\n{label}:")
    if isinstance(data, pd.DataFrame):
        print(data.head(10))  # Adjust the number of rows as needed
    elif isinstance(data, list):
        print(data[:100])  # Adjust the number of elements as needed
    elif isinstance(data, dict):
        for key, value in list(data.items())[:100]:  # Adjust the number of items as needed
            print(f"{key}: {value}")
    else:
        print(data)

def plot_most_energetic_histogram(df, particle_type, destiny):
    """
    Plots and saves a histogram of the most energetic particle (id = 0) for the given particle type.
    
    Parameters:
    df (DataFrame): The DataFrame containing the particle data.
    particle_type (str): The name of the particle type (e.g., 'electrons', 'muons', 'photons').
    destiny (str): The directory where the histogram image will be saved.
    """
    # Ensure the directory exists
    os.makedirs(destiny, exist_ok=True)

    # Filter to get the most energetic particle (id = 0) in each event
    most_energetic_particles = df.xs(0, level='id')  # Extract rows where id = 0

    # Create the histogram of 'pt' (transverse momentum)
    plt.figure(figsize=(10, 6))
    plt.hist(most_energetic_particles['pt'], bins=30, color='blue', edgecolor='black')
    plt.title(f'Histogram of Most Energetic {particle_type.capitalize()} Transverse Momentum (pt)')
    plt.xlabel('Transverse Momentum (pt)')
    plt.ylabel('Frequency')

    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}most_energetic_{particle_type}_pt_histogram.png")

    # Optionally, display the plot
    plt.show()

def plot_met_histogram(df, destiny):
    """
    Plots and saves a histogram of the MET for the most energetic photon (id = 0) in each event.

    Parameters:
    df (DataFrame): The DataFrame containing the photon data.
    destiny (str): The directory where the histogram image will be saved.
    """
    # Ensure the directory exists
    os.makedirs(destiny, exist_ok=True)

    # Filter to get the most energetic photon (id = 0) in each event
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0

    # Create the histogram of 'MET' (Missing Transverse Energy)
    plt.figure(figsize=(10, 6))
    plt.hist(most_energetic_photons['MET'], bins=30, color='green', edgecolor='black')
    plt.title('Histogram of MET for Most Energetic Photons')
    plt.xlabel('MET (Missing Transverse Energy)')
    plt.ylabel('Frequency')

    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}most_energetic_photon_met_histogram.png")

    # Optionally, display the plot
    plt.show()


def main(variables):

    type = variables[0]
    base_out = variables[1]
   
    input_file = origin + f"full_op_{type}_{base_out}_photons.pickle"
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photons', 'jets'))
   
    
    # Create sub DataFrame for electrons (id = 11)
    electrons = leptons[leptons['pdg'] == 11].copy()

    # Generate the 'new_id' column by resetting the id within each group
    electrons['new_id'] = electrons.groupby(level=0).cumcount()

    # Reset the index to turn the current 'id' level of the multi-index into a column
    electrons = electrons.reset_index(level='id')

    # Replace the 'id' in the index with 'new_id'
    electrons = electrons.set_index('new_id', append=True)

    # Rename the 'new_id' index level to 'id' to maintain the original naming
    electrons.index = electrons.index.rename('id', level='new_id')

    # Drop the 'id' column (not the multi-index)
    electrons = electrons.drop(columns=['id'])



    # Create sub DataFrame for muons (id = 13)
    muons = leptons[leptons['pdg'] == 13].copy()
    muons['new_id'] = muons.groupby(level=0).cumcount()  # Reset id within each group

    # Reset the index to turn the current 'id' level of the multi-index into a column
    muons = muons.reset_index(level='id')

    # Replace the 'id' in the index with 'new_id'
    muons = muons.set_index('new_id', append=True)

    # Rename the 'new_id' index level to 'id' to maintain the original naming
    muons.index = muons.index.rename('id', level='new_id')

    # Drop the 'id' column (not the multi-index)
    muons = muons.drop(columns=['id'])

    #print_contents("Photons", photons)
    #print_contents("Leptons", leptons)
    #print_contents("Jets", jets)
    #print_contents("Electrons", electrons)
    #print_contents("Muons", muons)
 
    # Plot for electrons
    plot_most_energetic_histogram(electrons, 'electrons', destiny)

    # Plot for muons
    plot_most_energetic_histogram(muons, 'muons', destiny)

    # Plot for photons
    plot_most_energetic_histogram(photons, 'photons', destiny)

    # Plot the MET histogram for the most energetic photons
    plot_met_histogram(photons, destiny)

    return



origin = f"/Collider/scripts_2208/data/clean/"
#origin = "/Collider/2023_LLHN_CONCYTEC/"
destiny = f"./data/basics_graphs/"
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