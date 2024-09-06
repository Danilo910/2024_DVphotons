import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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

def plot_histogram_z_and_t(type, df, column_name, title, xlabel, ylabel, destiny, output_file):
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
        bins = np.arange(0, 310, 10)
        np.savetxt(f"{destiniy_txt}/z_origin_{alpha}_{type}.txt", df[column_name])
    elif column_name == 'rel_tof':
        bins = np.arange(0, 3.1, 0.1)
        np.savetxt(f"{destiniy_txt}/rel_tof_{alpha}_{type}.txt", df[column_name])
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

def plot_z_origin_histogram(df, particle_type, type, destiny):
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0
    plot_histogram_z_and_t(type, most_energetic_photons, 'z_origin', f'Histogram of z_origin for Most Energetic {particle_type.capitalize()}',
                   'z_origin', 'Frequency', destiny, f'z_origin_histogram_{particle_type}.png')

def plot_rel_tof_histogram(df, particle_type, type, destiny):
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0
    plot_histogram_z_and_t(type, most_energetic_photons, 'rel_tof', f'Histogram of rel_tof for Most Energetic {particle_type.capitalize()}',
                   'rel_tof', 'Frequency', destiny, f'rel_tof_histogram_{particle_type}.png')

def plot_most_energetic_histogram(df, particle_type, type, destiny):
    plt.figure(figsize=(10, 6))
    most_energetic_particles = df.xs(0, level='id')  # Extract rows where id = 0
    if 'photon' in particle_type.lower():
        bins = np.arange(0, 210, 10)
    else:
        bins = np.arange(0, 310, 10)
   
    particle = particle_type.split('_')[0]
    np.savetxt(f"{destiniy_txt}/PT_{particle}_{alpha}_{type}.txt", most_energetic_particles['pt'])
    plt.hist(most_energetic_particles['pt'], bins=bins, color='blue', edgecolor='black')
    plt.title(f'Histogram of Most Energetic {particle_type.capitalize()} Transverse Momentum (pt)')
    plt.xlabel('Transverse Momentum (pt)')
    plt.ylabel('Frequency')
    plt.savefig(f"{destiny}/most_energetic_{particle_type}_pt_histogram.png")
    plt.show()

def plot_met_histogram(df, alpha, type, destiny):
    plt.figure(figsize=(10, 6))
    most_energetic_photons = df.xs(0, level='id')  # Extract rows where id = 0
    bins = np.arange(0, 310, 10)
    plt.hist(most_energetic_photons['MET'], bins=bins, color='green', edgecolor='black')
    np.savetxt(f"{destiniy_txt}/MET_{alpha}_{type}.txt", most_energetic_photons['MET'])
    plt.title(f'Histogram of MET for event {alpha.capitalize()}')
    plt.xlabel('MET (Missing Transverse Energy)')
    plt.ylabel('Frequency')
    plt.savefig(f"{destiny}/most_energetic_photon_met_histogram_{alpha.capitalize()}.png")
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


# Define the strings
iso = "iso"
no_iso = "no_iso"

# Create a list containing both strings
modes = [iso, no_iso]

# List of alphas and event types
alphas = [4, 5, 6]
event_types = ['ZH', 'WH', 'TTH']


# Loop through each mode in the list
for mode in modes:
    # Perform actions with each mode
    print(f"Processing mode: {mode}")
    # You can add any additional operations here
    for alpha in [4, 5, 6]:

        print("Alpha: ", alpha)
    
        for type in ['ZH', 'WH', 'TTH']:

            destiny = f"./data/simples_{mode}/{type}_{alpha}/"
            Path(destiny).mkdir(exist_ok=True, parents=True)

            destiniy_txt = f"/Collider/scripts_2208/data/clean/simples_{mode}"
            Path(destiniy_txt).mkdir(exist_ok=True, parents=True)

            print("Type: ", type)
            
            input_file = origin + f"full_op_{type}_M9_Alpha{alpha}_13_photons.pickle"
            photons = pd.read_pickle(input_file)
            leptons = pd.read_pickle(input_file.replace('photons', 'leptons'))

            electrons = leptons[leptons['pdg'] == 11].copy()
            electrons = reset_id_by_pt(electrons)

            # Apply isolation algorithm
            if mode == "iso":
                photons = isolate_photons(photons, electrons)
                photons = reset_id_by_pt(photons)

                electrons = isolate_photons(electrons, photons)
                electrons = reset_id_by_pt(electrons)


            # Create sub DataFrame for muons (id = 13)
            muons = leptons[leptons['pdg'] == 13].copy()
            muons = reset_id_by_pt(muons)

            alpha_s = str(alpha)
            photon_alpha_type = f'photon_{alpha}'
            electron_alpha_type = f'electron_{alpha}'
            muon_alpha_type = f'muon_{alpha}'

            # Plot histograms
            plot_met_histogram(photons, alpha_s, type, destiny)

            plot_most_energetic_histogram(electrons, electron_alpha_type, type, destiny)
            plot_most_energetic_histogram(muons, muon_alpha_type, type, destiny)
            plot_most_energetic_histogram(photons, photon_alpha_type, type, destiny)

            plot_z_origin_histogram(photons, photon_alpha_type, type, destiny)
            plot_rel_tof_histogram(photons, photon_alpha_type, type, destiny)
        
