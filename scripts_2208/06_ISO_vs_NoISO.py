import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to determine the bins based on the observable in the file name
def get_bins_for_observable(observable):
    """
    Returns the appropriate bins for the histogram based on the observable.
    """
    if observable == 'z_origin':
        return np.arange(0, 310, 10)
    elif observable == 'rel_tof':
        return np.arange(0, 3.1, 0.1)
    elif observable == 'PT_photon':
        return np.arange(0, 210, 10)
    elif observable in ['PT_electron', 'PT_muon']:
        return np.arange(0, 210, 10)
    elif observable == 'MET':
        return np.arange(0, 310, 10)
    elif observable == 'deltaR':
        return np.arange(0, 6, 0.1)
    else:
        return 30  # Default number of bins if none of the above


# Define the strings
simples = "simples"
deltaR = "deltaR"
ph_vs_phdeltaR = "ph_vs_phdeltaR"

# Create a list containing both strings
#observables = [simples, deltaR, ph_vs_phdeltaR]
observables = [ph_vs_phdeltaR]

# Define the directories
for observable in observables:
    iso_dir = f"/Collider/scripts_2208/data/clean/{observable}_iso"
    no_iso_dir = f"/Collider/scripts_2208/data/clean/{observable}_no_iso"
    destiny = f"./data/{observable}_iso_vs_no_iso"

    print("iso_dir", iso_dir)
    print("no_iso_dir", no_iso_dir)
    
    # Create the destination directory if it doesn't exist
    os.makedirs(destiny, exist_ok=True)

    # Get the list of files in both directories
    iso_files = set(os.listdir(iso_dir))
    no_iso_files = set(os.listdir(no_iso_dir))

    # Find common files between the two directories
    common_files = iso_files.intersection(no_iso_files)

    print("common_files", common_files)
    
    # Loop through each common file and compare
    for file_name in common_files:
        # Read the data from the ISO directory
        iso_path = os.path.join(iso_dir, file_name)
        no_iso_path = os.path.join(no_iso_dir, file_name)

        # Extract the observable name from the file name (e.g., "MET" from "MET_4_TTH.txt")
        observable = file_name.split('_')[0]

        # Get the appropriate bins for the observable
        bins = get_bins_for_observable(observable)

        # Assuming the files are TXT, read them into DataFrames (or numpy arrays)
        iso_data = pd.read_csv(iso_path, header=None).values.flatten()
        no_iso_data = pd.read_csv(no_iso_path, header=None).values.flatten()

        #print("iso_data", iso_data)
        #print("no_iso_data", no_iso_data)

        
        # Plotting the data as histograms
        plt.figure(figsize=(10, 6))
        
        # Plot the ISO data
        plt.hist(iso_data, bins=bins, alpha=0.7, label='ISO', color='blue', edgecolor='black')
        
        # Plot the No ISO data
        plt.hist(no_iso_data, bins=bins, alpha=0.7, label='No ISO', color='red', edgecolor='black')
        
        # Adding title and labels
        plt.title(f'Comparison for {observable}')
        plt.xlabel(observable)
        plt.ylabel('Frequency')
        plt.legend()
        
        # Save the plot as a PNG file
        save_path = os.path.join(destiny, f'comparison_{file_name}.png')
        plt.savefig(save_path)

        # Optionally, show the plot
        # plt.show()

        # Close the plot to free memory
        plt.close()
        