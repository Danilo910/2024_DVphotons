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
            # Extract the most energetic photon (id = 0) as a DataFrame row
            photon = df_photons.loc[[(event, 0)]].iloc[0]
            # Extract the most energetic electron (id = 0) as a DataFrame row
            # Initialize the minimum ΔR as a large number
            min_delta_r = float('inf')
            
            #print("Event", event)
            # Loop through all electrons in the event
            electrons = df_leptons.loc[event]

            #print("photonsdataframe")
            #print(photon)
            #print("electronsdataframe")
            #print(electrons)

            #sys.exit("Salimos")
            for _, electron in electrons.iterrows():
                # Calculate Δphi and Δeta
                delta_phi = photon['phi'] - electron['phi']
                delta_eta = photon['eta'] - electron['eta']
                
                # Calculate ΔR
                delta_r = np.sqrt(delta_phi**2 + delta_eta**2)
                #print("delta_r", delta_r)

                # Update the minimum ΔR if the current one is smaller
                if delta_r < min_delta_r:
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

origin = "/Collider/scripts_2208/data/clean/"
destiny = f"./data/basics_graphs_merge_alpha_deltaR/"
Path(destiny).mkdir(exist_ok=True, parents=True)


for alpha in [4, 5, 6]:

    input_file = origin + f"megaphoton_{alpha}.pickle"

    
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photon', 'leptons'))


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

    #print(electrons)
    #sys.exit("Salimos")
    alpha_s = str(alpha)
    # Example usage:
   

    # Calculate ΔR values
    delta_r_values = calculate_delta_r(photons, electrons)

    # Plot ΔR histogram
    plot_delta_r_histogram(delta_r_values, alpha_s, destiny)
