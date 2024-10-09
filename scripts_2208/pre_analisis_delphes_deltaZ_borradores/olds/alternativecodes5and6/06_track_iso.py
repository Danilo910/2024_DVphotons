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

#originales: delta_r_max=0.2, pt_min=0.1, los editamos para ver mejor los prints
def isolate_photons(df_photons, df_leptons, delta_r_max=3, pt_min=15, pt_ratio_max=1.4):
    """
    Isolates photons using the Mini-cone algorithm and returns a DataFrame of isolated photons.

    Parameters:
    df_photons (DataFrame): The DataFrame containing photon data.
    df_leptons (DataFrame): The DataFrame containing lepton (e.g., electron) data.
    delta_r_max (float): The maximum ΔR to consider for isolation (cone size).
    pt_min (float): The minimum pT threshold for leptons to be considered in the isolation.
    pt_ratio_max (float): The maximum allowable ratio of the sum of lepton pT to photon pT.

    Returns:
    isolated_photons (DataFrame): A DataFrame containing only the isolated photons.
    """
    df_isolated_photons = pd.DataFrame(columns=['E', 'pt', 'eta', 'phi', 'z_origin', 'rel_tof', 'MET'])

    df_isolated_photons.index = pd.MultiIndex.from_tuples([], names=['N', 'id'])

    # Get unique event indices
    events = df_photons.index.get_level_values('N').unique()

    for event in events:
        # Check if the event has both photons and leptons
        if event in df_photons.index.get_level_values('N') and event in df_leptons.index.get_level_values('N'):
            # Extract photons and leptons in the event
            photons = df_photons.loc[event]
            leptons = df_leptons.loc[event]

            print("photonsdataframe")
            print(photons)
            print("electronsdataframe")
            print(leptons)


            # Extract phi, eta, and pt values as numpy arrays
            photon_phi = photons['phi'].values
            photon_eta = photons['eta'].values
            photon_pt = photons['pt'].values
            lepton_phi = leptons['phi'].values
            lepton_eta = leptons['eta'].values
            lepton_pt = leptons['pt'].values
            
            # Calculate Δphi and Δη using numpy broadcasting (outer subtraction)
            delta_phi = np.subtract.outer(photon_phi, lepton_phi)
            delta_eta = np.subtract.outer(photon_eta, lepton_eta)
        for event in events:
        # Check if the event has both photons and leptons
            if event in df_photons.index.get_level_values('N') and event in df_leptons.index.get_level_values('N'):
                # Extract photons and leptons in the event
                photons = df_photons.loc[event]
                leptons = df_leptons.loc[event]

                print("photonsdataframe")
                print(photons)
                print("electronsdataframe")
                print(leptons)


                # Extract phi, eta, and pt values as numpy arrays
                photon_phi = photons['phi'].values
                photon_eta = photons['eta'].values
                photon_pt = photons['pt'].values
                lepton_phi = leptons['phi'].values
                lepton_eta = leptons['eta'].values
                lepton_pt = leptons['pt'].values
                
                # Calculate Δphi and Δη using numpy broadcasting (outer subtraction)
                delta_phi = np.subtract.outer(photon_phi, lepton_phi)
                delta_eta = np.subtract.outer(photon_eta, lepton_eta)
            
                # Calculate ΔR for all photon-lepton pairs
                delta_r = np.sqrt(delta_phi**2 + delta_eta**2)

                print("deltar:")
                print(delta_r)

                # Apply the ΔR max condition
                within_cone = (delta_r < delta_r_max)

                print("deltar max condition:")
                print(within_cone)
                
                # Apply the pT min condition to the leptons
                lepton_pt_filtered = np.where(lepton_pt > pt_min, lepton_pt, 0)

                print("lepton_pt_filtered:")
                print(lepton_pt_filtered)
                
                # Calculate the sum of pT of leptons within the cone for each photon
                sum_pt_within_cone = np.sum(lepton_pt_filtered * within_cone, axis=1)
                print("sum_pt_within_cone:")
                print(sum_pt_within_cone)

                # Calculate the isolation ratio for each photon
                isolation_ratio = sum_pt_within_cone / photon_pt

                print("isolation_ratio")
                print(isolation_ratio)
                
                # Determine if each photon is isolated based on the isolation ratio
                isolated_photon_mask = (isolation_ratio < pt_ratio_max) & (sum_pt_within_cone > 0)

                print("isolated_photon_mask")
                print(isolated_photon_mask)

                # Store the indices of isolated photons
                #isolated_photon_indices.extend(photons[isolated_photon_mask].index.tolist())

                all_false = not any(isolated_photon_mask)

                #print("all false", all_false)
                # Store the result in a variable
                if all_false:
                    result = "All conditions are False"
                    print(result)
                else:
                    # Select isolated photons and retain their multi-index, considering the current event
                    isolated_photon = photons.loc[isolated_photon_mask]
                    # Ensure the multi-index is preserved
                    isolated_photon.index = pd.MultiIndex.from_tuples([(event, idx) for idx in isolated_photon.index], names=['N', 'id'])
                    # Append isolated photons to the result DataFrame with correct multi-index
                    df_isolated_photons = pd.concat([df_isolated_photons, isolated_photon])
                    print("isolated_photon")
                    print(isolated_photon)
                    print(df_isolated_photons)
            else:
                # If no leptons are present, consider all photons in this event as isolated
                isolated_photon = df_photons.loc[event]
                # Append all photons to the result DataFrame as they are considered isolated
                df_isolated_photons = pd.concat([df_isolated_photons, isolated_photon])

    # Return the DataFrame of isolated photons
    isolated_photons = df_photons.loc[isolated_photon_indices]

    

    return isolated_photons

def calculate_delta_r(df_photons, df_leptons):
    """
    Calculates the minimum ΔR between each photon and all electrons in each event,
    and stores the minimum ΔR for each photon.

    Parameters:
    df_photons (DataFrame): The DataFrame containing photon data.
    df_leptons (DataFrame): The DataFrame containing lepton data.

    Returns:
    min_delta_r_values (numpy array): An array of minimum ΔR values for each photon in each event.
    """
    min_delta_r_values = np.array([])

    # Get unique event indices
    events = df_photons.index.get_level_values('N').unique()

    for event in events:

        #print("Evento: ", event)
        # Check if the event has both photons and electrons
        if event in df_photons.index.get_level_values('N') and event in df_leptons.index.get_level_values('N'):
            # Extract photons and electrons in the event
            photons = df_photons.loc[event]
            electrons = df_leptons.loc[event]

            #print("photonsdataframe")
            #print(photons)
            #print("electronsdataframe")
            #print(electrons)
            
            # Extract phi and eta values as numpy arrays
            photon_phi = photons['phi'].values
            photon_eta = photons['eta'].values
            lepton_phi = electrons['phi'].values
            lepton_eta = electrons['eta'].values
            
            # Calculate Δphi and Δη using numpy broadcasting (outer subtraction)
            delta_phi = np.subtract.outer(photon_phi, lepton_phi)
            delta_eta = np.subtract.outer(photon_eta, lepton_eta)
        
            
            # Calculate ΔR for all photon-electron pairs
            delta_r = np.sqrt(delta_phi**2 + delta_eta**2)
            
            #print("deltar antes de corte:")
            #print(delta_r)


            # Ignore ΔR values that are too small
            #mandamos a infinito los que tienen cero para que asi nunca puedan ser seleccionados
            delta_r = np.where(delta_r > 1e-15, delta_r, np.inf)
            
            #print("deltar despues de corte: ")
            #print(delta_r)
            
            # Find the minimum ΔR for each photon
            min_delta_r_per_photon = np.min(delta_r, axis=1)

            #print("min_delta_r_per_photon")
            #print(min_delta_r_per_photon)

            #print("min_delta_r_per_photon: ", min_delta_r_per_photon)
            
            # Append the minimum ΔR for each photon in this event to the result array
            min_delta_r_values = np.append(min_delta_r_values, min_delta_r_per_photon)

    return min_delta_r_values

def plot_delta_r_histogram(delta_r_values, alpha, destiny):
    """
    Plots and saves a histogram of ΔR values.

    Parameters:
    delta_r_values (list): A list of ΔR values to plot.
    destiny (str): The directory where the histogram image will be saved.
    """
    plt.figure(figsize=(10, 6))

    bins = np.arange(0, 0.1, 0.01)  # Bins from 0 to 1000 with steps of 100

    plt.hist(delta_r_values, bins=bins, color='blue', edgecolor='black')
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
destiny = f"./data/final_deltaR/"
Path(destiny).mkdir(exist_ok=True, parents=True)


for alpha in [4, 5, 6]:

    print("Alpha: ", alpha)
    input_file = origin + f"megaphoton_{alpha}.pickle"

    
    photons = pd.read_pickle(input_file)
    leptons = pd.read_pickle(input_file.replace('photon', 'leptons'))

    #Reset id photons
    photons = reset_id_by_pt(photons)

    # Create sub DataFrame for electrons (id = 11)
    electrons = leptons[leptons['pdg'] == 11].copy()

    electrons = reset_id_by_pt(electrons)
    
    isolated_photons = isolate_photons(photons, electrons)

    #print(electrons)
    sys.exit("Salimos")
    alpha_s = str(alpha)
    # Example usage:
   

    # Calculate ΔR values
    delta_r_values = calculate_delta_r(photons, electrons)

    # Plot ΔR histogram
    plot_delta_r_histogram(delta_r_values, alpha_s, destiny)
