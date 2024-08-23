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

def plot_histogram(df, column_name, title, xlabel, ylabel, destiny, output_file):
    """
    Plots and saves a histogram for a specified column in the DataFrame.

    Parameters:
    df (DataFrame): The DataFrame containing the data.
    column_name (str): The name of the column to plot.
    title (str): The title of the histogram.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    destiny (str): The directory where the histogram image will be saved.
    output_file (str): The name of the output file.
    """
    # Define bins based on the column name
    if column_name == 'z_origin':
        bins = np.arange(0, 1100, 100)  # Bins from 0 to 1000 with steps of 100
    elif column_name == 'rel_tof':
        bins = np.arange(0, 6.3, 0.3)  # Bins from 0 to 6 with steps of 0.3
    else:
        bins = 30  # Default number of bins
    
    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df[column_name], bins=bins, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}/{output_file}")
    
    # Optionally, display the plot
    plt.show()

def plot_z_origin_histogram(df, particle_type, destiny):
    """
    Plots and saves a histogram of the z_origin for the most energetic photon (id = 0).

    Parameters:
    df (DataFrame): The DataFrame containing the photon data.
    destiny (str): The directory where the histogram image will be saved.
    """
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0
    plot_histogram(most_energetic_photons, 'z_origin', f'Histogram of z_origin for Most Energetic {particle_type.capitalize()} ',
                   'z_origin', 'Frequency', destiny, f'z_origin_histogram_{particle_type}.png')

def plot_rel_tof_histogram(df, particle_type, destiny):
    """
    Plots and saves a histogram of the rel_tof for the most energetic photon (id = 0).

    Parameters:
    df (DataFrame): The DataFrame containing the photon data.
    destiny (str): The directory where the histogram image will be saved.
    """
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0
    plot_histogram(most_energetic_photons, 'rel_tof', f'Histogram of rel_tof for Most Energetic {particle_type.capitalize()}',
                   'rel_tof', 'Frequency', destiny, f'rel_tof_histogram_{particle_type}.png')

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

    # Define bins from 0 to 300 with intervals of 10
    bins = np.arange(0, 310, 10)

    # Create the histogram of 'pt' (transverse momentum)
    plt.figure(figsize=(10, 6))
    plt.hist(most_energetic_particles['pt'], bins=bins, color='blue', edgecolor='black')
    plt.title(f'Histogram of Most Energetic {particle_type.capitalize()} Transverse Momentum (pt)')
    plt.xlabel('Transverse Momentum (pt)')
    plt.ylabel('Frequency')

    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}_most_energetic_{particle_type}_pt_histogram.png")

    # Optionally, display the plot
    plt.show()

def plot_met_histogram(df, alpha_type, destiny):
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


    bins = np.arange(0, 310, 10)

    # Create the histogram of 'MET' (Missing Transverse Energy)
    plt.figure(figsize=(10, 6))
    plt.hist(most_energetic_photons['MET'], bins=bins, color='green', edgecolor='black')
    plt.title(f'Histogram of MET for event {alpha_type.capitalize()}')
    plt.xlabel('MET (Missing Transverse Energy)')
    plt.ylabel('Frequency')

    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}most_energetic_photon_met_histogram{alpha_type.capitalize()}.png")

    # Optionally, display the plot
    plt.show()

# Function to load and print initial and final lines of a pickle file
def print_initial_and_final_lines(pickle_file):
    # Load the pickle file into a DataFrame
    df = pd.read_pickle(os.path.join(origin, pickle_file))
    
    # Print the first 5 rows
    print(f"Initial lines of {pickle_file}:")
    print(df.head())
    
    # Print the last 5 rows
    print(f"\nFinal lines of {pickle_file}:")
    print(df.tail())
    print("\n" + "="*80 + "\n")

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

# Origin directory where the mega archives are stored
origin = "/Collider/scripts_2208/data/clean/"
destiny = f"./data/finales_simples/"
Path(destiny).mkdir(exist_ok=True, parents=True)

# List of mega pickle files
#megaphoton = origin + f"megaphoton_4.pickle"
#megalepton = origin + f"megaleptons_4.pickle"

#print_initial_and_final_lines(megaphoton)
#print_initial_and_final_lines(megalepton)

#sys.exit("Salimos")

# Loop through each mega file and print its initial and final lines
#for file in mega_files:
#    print_initial_and_final_lines(file)
for alpha in [4, 5, 6]:
    input_file = origin + f"megaphoton_{alpha}.pickle"
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photon', 'leptons'))
    jets = pd.read_pickle(input_file.replace('photon', 'jets'))

    # Rest photons
    photons = reset_id_by_pt(photons)

    #Reset Jets
    jets = reset_id_by_pt(jets)


    # Create sub DataFrame for electrons (id = 11)
    electrons = leptons[leptons['pdg'] == 11].copy()
    electrons = reset_id_by_pt(electrons)


    # Create sub DataFrame for muons (id = 13)
    muons = leptons[leptons['pdg'] == 13].copy()
    muons = reset_id_by_pt(muons)


    electron_alpha_type = f'electrons_{alpha}'
    muon_alpha_type = f'muon_{alpha}'
    photon_alpha_type = f'photon_{alpha}'
    alpha_s = str(alpha)

    # Plot for electrons
    plot_most_energetic_histogram(electrons, electron_alpha_type, destiny)

    # Plot for muons
    plot_most_energetic_histogram(muons, muon_alpha_type, destiny)

    # Plot for photons
    plot_most_energetic_histogram(photons, photon_alpha_type, destiny)

    # Plot the MET histogram for the most energetic photons
    plot_met_histogram(photons, alpha_s, destiny)

    # Plot z_origin histogram
    plot_z_origin_histogram(photons, photon_alpha_type, destiny)

    # Plot rel_tof histogram
    plot_rel_tof_histogram(photons, photon_alpha_type, destiny)