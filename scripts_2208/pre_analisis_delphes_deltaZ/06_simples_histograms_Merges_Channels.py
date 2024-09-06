import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

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
    else:
        return 30  # Default number of bins if none of the above

def merge_and_plot_observable(observable, alphas, event_types, origin, mode):
    """
    Merges and plots data for a given observable across different alphas and event types.

    Parameters:
    observable (str): The observable to merge and plot (e.g., 'MET', 'PT_electron', 'rel_tof', 'z_origin').
    alphas (list): The list of alphas to process (e.g., [4, 5, 6]).
    event_types (list): The list of event types to process (e.g., ['ZH', 'WH', 'TTH']).
    origin (str): The directory where the txt files are stored.
    """
    for alpha in alphas:
        merged_data = pd.DataFrame()
        data_dict = {}

        for event_type in event_types:
            file_path = f"{origin}/{observable}_{alpha}_{event_type}.txt"
            data = np.loadtxt(file_path)
            df = pd.DataFrame(data, columns=[observable])
            
            # Store data for this event type
            data_dict[event_type] = df

            # Merge data across event types
            merged_data = pd.concat([merged_data, df], ignore_index=True)

        # Determine the bins based on the observable
        bins = get_bins_for_observable(observable)
        
        #Definimos el destino donde queremos que esten las imagenes (iso y no iso)

        destiny = f"./data/Merge_simples_{mode}/{observable}/"
        Path(destiny).mkdir(exist_ok=True, parents=True)


        # Plotting merged data for the current observable and alpha
        plt.figure(figsize=(10, 6))
        plt.hist(merged_data[observable], bins=bins, alpha=0.7, label=f"{observable} for Alpha {alpha}")
        plt.title(f"{observable} Histogram for Alpha {alpha} (Merged across Event Types)")
        plt.xlabel(observable)
        plt.ylabel("Frequency")
        plt.legend()

        plt.savefig(f"{destiny}/{mode}_{observable}_histogram_alpha{alpha}_merged.png")
        plt.close()

        # Create the second plot: Differentiating by event type
        plt.figure(figsize=(10, 6))
        for event_type, df in data_dict.items():
            plt.hist(df[observable], bins=bins, alpha=0.5, label=event_type, histtype='stepfilled')

        plt.title(f"{observable} Histogram for Alpha {alpha} (Differentiated by Type)")
        plt.xlabel(observable)
        plt.ylabel("Frequency")
        plt.legend()

        # Save the differentiated plot
        plt.savefig(f"{destiny}/{observable}_histogram_alpha{alpha}_differentiated.png")
        plt.close()

def merge_and_plot_for_all_observables(mode):

    origin = f"/Collider/scripts_2208/data/clean/simples_{mode}"
    alphas = [4, 5, 6]
    event_types = ['ZH', 'WH', 'TTH']

    # List of observables
    observables = ['MET', 'PT_electron', 'PT_muon', 'PT_photon', 'rel_tof', 'z_origin']

    # Merge and plot for each observable
    for observable in observables:
        merge_and_plot_observable(observable, alphas, event_types, origin, mode)


# Define the strings
iso = "iso"
no_iso = "no_iso"

# Create a list containing both strings
modes = [iso, no_iso]

# Run the full merging and plotting process
for mode in modes:
    # Perform actions with each mode
    print(f"Processing mode: {mode}")

    merge_and_plot_for_all_observables(mode)

