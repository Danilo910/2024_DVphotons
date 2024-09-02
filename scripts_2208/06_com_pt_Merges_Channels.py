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


def plot_normalized_histogram(binado, df1, df2, column_name, title1, title2, xlabel, ylabel, destiny, output_file):
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
    bins = binado
    
    #np.savetxt(f"{origin}/comparison_{alpha}_{type}_electron.txt", df1[column_name].values)
    #np.savetxt(f"{origin}/comparison_{alpha}_{type}_muon.txt", df2[column_name].values)


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

def merge_particles(data_dict, particle_type):
    merged_dict = {}
    
    # Assuming alphas are 4, 5, and 6 as per your example
    alphas = [4, 5, 6]
    types = ['TTH', 'WH', 'ZH']

    for alpha in alphas:
        # List to hold DataFrames of the same alpha for merging
        print("alpha:", alpha)
        dfs = []
        
        for type in types:
            if alpha in data_dict[type]:
                dfs.append(data_dict[type][alpha][particle_type])
                #print("dfs: ", dfs)
        
        # Concatenate all DataFrames in the list
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            merged_dict[alpha] = merged_df
            print("merged_df: ", merged_df)
    
    #print("merge_dict: ", merged_dict)
    return merged_dict

def isolate_photons(df_photons, df_leptons, delta_r_max=0.2, pt_min=0.1, pt_ratio_max=0.065):

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
    df_isolated_photons = pd.DataFrame(columns=['N', 'id', 'E', 'pt', 'eta', 'phi', 'z_origin', 'rel_tof', 'MET'])

    # Get unique event indices
    events = df_photons.index.get_level_values('N').unique()

    for event in events:
        # Check if the event has both photons and leptons
        if event in df_photons.index.get_level_values('N') and event in df_leptons.index.get_level_values('N'):
            # Extract photons and leptons in the event
            photons = df_photons.loc[event]
            leptons = df_leptons.loc[event]
            

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

            # Determine if there are no leptons within the ΔR max condition
            no_leptons_within_cone = np.all(delta_r > delta_r_max, axis=1)

            # Apply the ΔR max condition
            within_cone = (delta_r < delta_r_max)

            # Apply the pT min condition to the leptons
            lepton_pt_filtered = np.where(lepton_pt > pt_min, lepton_pt, 0)

            # Calculate the sum of pT of leptons within the cone for each photon
            sum_pt_within_cone = np.sum(lepton_pt_filtered * within_cone, axis=1)

            # Calculate the isolation ratio for each photon
            isolation_ratio = sum_pt_within_cone / photon_pt

                                    # Use filter to find values less than 0.065
            values_below_threshold = list(filter(lambda x: x < 0.065 and x > 0, isolation_ratio))

            if values_below_threshold:
                print("Values less than 0.065:", values_below_threshold)

            # Determine if each photon is isolated based on the isolation ratio or if there are no leptons nearby
            isolated_photon_mask = (isolation_ratio < pt_ratio_max) | no_leptons_within_cone

            # Print statements for all variables
            not_isolated_photon_mask = ~isolated_photon_mask
            
            """
            print("photonsdataframe")
            print(photons)
            print("electronsdataframe")
            print(leptons)
            print("delta_phi:")
            print(delta_phi)
            print("delta_eta:")
            print(delta_eta)
            print("delta_r:")
            print(delta_r)
            print("no_leptons_within_cone:")
            print(no_leptons_within_cone)
            print("within_cone:")
            print(within_cone)
            print("lepton_pt_filtered:")
            print(lepton_pt_filtered)
            print("sum_pt_within_cone:")
            print(sum_pt_within_cone)
            print("isolation_ratio:")
            print(isolation_ratio)
            print("isolated_photon_mask:")
            print(isolated_photon_mask)
            """
            

            # Filter and store the isolated photons with the event number (N) and photon id
            if any(not_isolated_photon_mask):
                # Filter isolated photons
                not_isolated_photons = photons[not_isolated_photon_mask].copy()
                # Add the event number (N) as a column
                #print("N: ", event)
                #isolated_photons['N'] = event
                # Add the photon id as a column
                #isolated_photons['id'] = isolated_photons.index
                index_list = not_isolated_photons.index.tolist()
                #print("id: ", index_list)

                for index_event in index_list:
                    df_photons = df_photons.drop((event, index_event))
                # Elimina los que no estan aislados
                #df_photons = df_photons
                #df_isolated_photons = pd.concat([df_isolated_photons, isolated_photons[['N', 'id', 'E', 'pt', 'eta', 'phi', 'z_origin', 'rel_tof', 'MET']]])
                #print("isolated_photon:")
                #print(isolated_photons)

    return df_photons

# Initialize the nested dictionary
data_dict = {
    'ZH': {4: None, 5: None, 6: None},
    'TTH': {4: None, 5: None, 6: None},
    'WH': {4: None, 5: None, 6: None},
}


# List of alphas and event types
alphas = [4, 5, 6]
event_types = ['ZH', 'WH', 'TTH']

dataframes_electrons = []
dataframes_muons = []

#origin = "/Collider/scripts_2208/data/clean/compare"
#Path(origin).mkdir(exist_ok=True, parents=True)

real_origin = "/Collider/scripts_2208/data/clean/"


# Define the strings
iso = "iso"
no_iso = "no_iso"

# Create a list containing both strings
modes = [iso, no_iso]

# Loop through each mode in the list
for mode in modes:
    # Perform actions with each mode
    print(f"Processing mode: {mode}")

    for alpha in alphas:
        print("Alpha: ", alpha)
        for type in event_types:
            print("event_type: ", type)
            #destiny = f"./data/simples_com_pt/{type}_{alpha}/"
            #Path(destiny).mkdir(exist_ok=True, parents=True)
            
            input_file = real_origin + f"full_op_{type}_M9_Alpha{alpha}_13_photons.pickle"
            print("input_file: " ,input_file)
            photons = pd.read_pickle(input_file)
            leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))

            electrons = leptons[leptons['pdg'] == 11].copy()
            electrons = reset_id_by_pt(electrons)


            # Create sub DataFrame for muons (id = 13)
            muons = leptons[leptons['pdg'] == 13].copy()
            muons = reset_id_by_pt(muons)

            if mode == "iso":
                #el primer argumento se aisla del segundo
                electrons = isolate_photons(electrons, photons)
                electrons = reset_id_by_pt(electrons)

            
            muons = muons.xs(0, level='id')  # Extract rows where id = 0
            
            electrons = electrons.xs(0, level='id')  # Extract rows where id = 0

            # Extract the 'pt' column
            pt_values_electron = electrons['pt'].values
            pt_values_electron_df = pd.DataFrame(pt_values_electron, columns=['pt'])

            # Print the pt values as a row
            #print(" ".join(map(str, pt_values_electron)))

            # Extract the 'pt' column
            pt_values_muon = muons['pt'].values
            pt_values_muon_df = pd.DataFrame(pt_values_muon, columns=['pt'])

            # Print the pt values as a row
            #print(" ".join(map(str, pt_values_muon)))

            #print("After")
            #print_initial_and_final_lines(electrons)

            #sys.exit("Salimos")

            data_dict[type][alpha] = {
                'muons': pt_values_muon_df,
                'electrons': pt_values_electron_df
            }
            
            # Normalize and plot the comparison with x-axis limited to 300
            #plot_normalized_histogram(type, alpha, electrons, muons, 'pt', f'Most_Energetic_Electrons_{alpha}', f'Most_Energetic_Muon_{alpha}',
            #                    'Transverse Momentum (pt)', 'Probability Density', destiny, f'comparison_histogram_{alpha}.png')

    #print(data_dict)
    indices = [0, 1, 2]

    # Merge for electrons and muons separately
    merged_electrons = merge_particles(data_dict, 'electrons')
    #sys.exit("Salimos")
    merged_muons = merge_particles(data_dict, 'muons')

    #print("Electron 4: ")
    #print(merged_electrons[4])

    #print("Electron 5: ")
    #print(merged_electrons[4])



    for alpha, data_dict_electron in merged_electrons.items():

        destiny_muon_vs_e = f"./data/merges_comp/{mode}/pt_muon_vs_e/{alpha}/"
        Path(destiny_muon_vs_e).mkdir(exist_ok=True, parents=True)

        bins = np.arange(0, 310, 10)

        plot_normalized_histogram(bins, data_dict_electron, merged_muons[alpha], 'pt', f'Most_Energetic_Electrons_{alpha}', f'Most_Energetic_Muon_{alpha}',
                                'Transverse Momentum (pt)', 'Probability Density', destiny_muon_vs_e, f'comparison_histogram_{alpha}.png')


    destiny_alpha_ij = f"./data/merges_comp/{mode}/pt_alpha_ij/"
    Path(destiny_alpha_ij).mkdir(exist_ok=True, parents=True)


    # Iterate over combinations of electron indices
    for idx1, idx2 in combinations(indices, 2):

        bins = np.arange(0, 310, 10)
        plot_normalized_histogram(bins,merged_electrons[idx1+4], merged_electrons[idx2+4], 'pt',
            f'Most Energetic Electrons_{idx1+4}', f'Most Energetic Electron_{idx2+4}', 
            'Transverse Momentum (pt)', 'Probability Density', destiny_alpha_ij, 
            f'comparison_e_{idx1+4}vs{idx2+4}.png'
        )


    for idx1, idx2 in combinations(indices, 2):

        bins = np.arange(0, 310, 10)
        plot_normalized_histogram(bins,merged_muons[idx1+4], merged_muons[idx2+4], 'pt',
            f'Most Energetic Muons{idx1+4}', f'Most Energetic Muon{idx2+4}', 
            'Transverse Momentum (pt)', 'Probability Density', destiny_alpha_ij, 
            f'comparison_mu_{idx1+4}vs{idx2+4}.png'
        )
        
    