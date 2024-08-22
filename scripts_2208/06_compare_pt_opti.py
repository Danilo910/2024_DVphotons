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
from itertools import combinations


def plot_normalized_histogram(df1, df2, column_name, title1, title2, xlabel, ylabel, destiny, output_file):
    """
    Plots and saves a normalized histogram for comparison, with x-axis limited to a specified range.

    Parameters:
    df1 (DataFrame): The DataFrame containing the first dataset.
    df2 (DataFrame): The DataFrame containing the second dataset.
    column_name (str): The name of the column to plot.
    title1 (str): The title of the first histogram.
    title2 (str): The title of the second histogram.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    destiny (str): The directory where the histogram image will be saved.
    output_file (str): The name of the output file.
    """
    plt.figure(figsize=(10, 6))
    
    # Define bins from 0 to 300 with intervals of 10
    bins = np.arange(0, 310, 10)
    
    # Plot first histogram
    plt.hist(df1[column_name], bins=bins, color='blue', edgecolor='black', alpha=0.5, density=True, label=title1)
    
    # Plot second histogram
    plt.hist(df2[column_name], bins=bins, color='red', edgecolor='black', alpha=0.5, density=True, label=title2)
    
    # Set the x-axis limit to 300
    plt.xlim(0, 300)
    
    plt.title(f'Comparison of {title1} and {title2}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    
    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}/{output_file}")
    
    # Optionally, display the plot
    plt.show()

def print_initial_and_final_lines(df):
    """
    Prints the first 10 and last 10 lines of a DataFrame.

    Parameters:
    df (DataFrame): The DataFrame to print.
    """
    print("Initial 10 lines of the DataFrame:")
    print(df.head(10))
    print("\n" + "="*80 + "\n")
    print("Final 10 lines of the DataFrame:")
    print(df.tail(11))

def reset_id_by_pt(electrons):
    """
    Sorts the DataFrame by 'pt' within each 'N', then assigns a new 'id' starting from 0 for each group.

    Parameters:
    electrons (DataFrame): The input DataFrame with a multi-index ('N', 'id').

    Returns:
    electrons (DataFrame): The DataFrame with a new multi-index ('N', 'id') sorted by 'pt'.
    """
    # Reset index to treat 'N' and 'id' as columns
    electrons = electrons.reset_index()

    electrons = electrons.drop(columns=['id'])

    #print_initial_and_final_lines(electrons)

    #sys.exit("Salimos")

    # Sort the DataFrame by 'N' and 'pt'
    electrons = electrons.sort_values(by=['N', 'pt'], ascending=[True, False])

    g = electrons.groupby('N', as_index=False).cumcount()

    electrons['id'] = g

    electrons = electrons.set_index(['N', 'id'])

    return electrons
    #print_initial_and_final_lines(electrons)

    #sys.exit("Salimos")

# Origin directory where the mega archives are stored
origin = "/Collider/scripts_2208/data/clean/"
destiny = f"./data/graphs_compare_pt_opt/"
Path(destiny).mkdir(exist_ok=True, parents=True)

dataframes_electrons = []
dataframes_muons = []

for alpha in [4, 5, 6]:

    input_file = origin + f"megaphoton_{alpha}.pickle"
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photon', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photon', 'jets'))

    # Create sub DataFrame for electrons (id = 11)
    electrons = leptons[leptons['pdg'] == 11].copy()
    electrons = reset_id_by_pt(electrons)

    
    # Create sub DataFrame for muons (id = 13)
    muons = leptons[leptons['pdg'] == 13].copy()
    muons = reset_id_by_pt(muons)


    #print("Before")
    #print_initial_and_final_lines(electrons)


    muons = muons.xs(0, level='id')  # Extract rows where id = 0
    
    electrons = electrons.xs(0, level='id')  # Extract rows where id = 0

    #print("After")
    #print_initial_and_final_lines(electrons)

    dataframes_muons.append(muons)
    dataframes_electrons.append(electrons)
    
    # Normalize and plot the comparison with x-axis limited to 300
    plot_normalized_histogram(electrons, muons, 'pt', f'Most Energetic Electrons_{alpha}', f'Most Energetic Muon_{alpha}', 
                          'Transverse Momentum (pt)', 'Probability Density', destiny, f'comparison_histogram_{alpha}.png')


# Define las combinaciones de índices para las comparaciones
indices = [0, 1, 2]

# Itera sobre las combinaciones de índices de los electrones
for idx1, idx2 in combinations(indices, 2):
    plot_normalized_histogram(
        dataframes_electrons[idx1], dataframes_electrons[idx2], 'pt',
        f'Most Energetic Electrons_{idx1+4}', f'Most Energetic Electron_{idx2+4}', 
        'Transverse Momentum (pt)', 'Probability Density', destiny, 
        f'comparison_e_{idx1+4}vs{idx2+4}.png'
    )

# Itera sobre las combinaciones de índices de los muones
for idx1, idx2 in combinations(indices, 2):
    plot_normalized_histogram(
        dataframes_muons[idx1], dataframes_muons[idx2], 'pt',
        f'Most Energetic Muons_{idx1+4}', f'Most Energetic Muon_{idx2+4}', 
        'Transverse Momentum (pt)', 'Probability Density', destiny, 
        f'comparison_m_{idx1+4}vs{idx2+4}.png'
    )
