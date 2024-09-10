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

def calculate_delta_r(df_photons, df_leptons):
    """
    Calculates the minimum ΔR between the most energetic photon and all electrons in each event.

    Parameters:
    df_photons (DataFrame): The DataFrame containing photon data.
    df_leptons (DataFrame): The DataFrame containing lepton data.

    Returns:
    min_delta_r_values (list): A list of minimum ΔR values for each event.
    """
    min_delta_r_values = []

    # Get unique event indices
    events = df_photons.index.get_level_values('N').unique()

    for event in events:
    # Check if the event has both a photon and an electron
        if event in df_photons.index.get_level_values('N') and event in df_leptons.index.get_level_values('N'):
            # Initialize the minimum ΔR as a large number
            min_delta_r = float('inf')

            # Extract photons and electrons in the event
            photons = df_photons.loc[event]
            electrons = df_leptons.loc[event]

            #print("Event", event)

            #print("photonsdataframe")
            #print(photons)
            #print("electronsdataframe")
            #print(electrons)

            # Loop through all photons in the event
            for _, photon in photons.iterrows():
                # Loop through all electrons in the event
                for _, electron in electrons.iterrows():
                    # Calculate Δphi and Δeta
                    delta_phi = photon['phi'] - electron['phi']
                    delta_eta = photon['eta'] - electron['eta']
                    
                    # Calculate ΔR
                    delta_r = np.sqrt(delta_phi**2 + delta_eta**2)
                    #print("delta_r", delta_r)
                    # Update the minimum ΔR if the current one is smaller and not zero or very small
                    if delta_r < min_delta_r and delta_r > 1e-15:
                        min_delta_r = delta_r
                    #print("min_delta_r", min_delta_r)

            # Append the minimum ΔR for this event to the list
            min_delta_r_values.append(min_delta_r)
    
    return min_delta_r_values

def plot_delta_r_histogram(delta_r_values, alpha, destiny):
    """
    Plots and saves a histogram of ΔR values.

    Parameters:
    delta_r_values (list): A list of ΔR values to plot.
    destiny (str): The directory where the histogram image will be saved.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(delta_r_values, bins=30, color='blue', edgecolor='black')
    plt.title(f'Histogram of ΔR between Most Energetic Photon and Electron {alpha.capitalize()}')
    plt.xlabel('ΔR')
    plt.ylabel('Frequency')
    
    # Save the histogram as a PNG file
    plt.savefig(f"{destiny}/delta_r_histogram_{alpha}.png")
    
    # Optionally, display the plot
    plt.show()

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

origin = "/Collider/scripts_2208/data/clean/"
destiny = f"./data/deltaR_tracks/"
Path(destiny).mkdir(exist_ok=True, parents=True)


for alpha in [4, 5, 6]:

    print("Alpha: ", alpha)
    input_file = origin + f"megaphoton_{alpha}.pickle"

    
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photon', 'leptons'))


    # Create sub DataFrame for electrons (id = 11)
    electrons = leptons[leptons['pdg'] == 11].copy()

    electrons = reset_id_by_pt(electrons)

    #print(electrons)
    #sys.exit("Salimos")
    alpha_s = str(alpha)
    # Example usage:
   

    # Calculate ΔR values
    delta_r_values = calculate_delta_r(photons, electrons)

    # Plot ΔR histogram
    plot_delta_r_histogram(delta_r_values, alpha_s, destiny)
