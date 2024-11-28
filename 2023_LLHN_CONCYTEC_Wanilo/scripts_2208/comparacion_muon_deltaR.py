import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Directories
base_dir_wanilo = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"
categories = ["TTH", "WH", "ZH"]
observables = ["before_overlapping", "after_overlapping"]

# Function to calculate DeltaR
def calculate_delta_r(eta1, phi1, eta2, phi2):
    """
    Calculate DeltaR between two particles using their eta and phi coordinates.
    DeltaR = sqrt((Delta eta)^2 + (Delta phi)^2)
    """
    delta_eta = eta1 - eta2
    delta_phi = np.abs(phi1 - phi2)
    # Ensure phi is wrapped within [-pi, pi]
    delta_phi = np.where(delta_phi > np.pi, 2 * np.pi - delta_phi, delta_phi)
    return np.sqrt(delta_eta**2 + delta_phi**2)

# Function to process particles and generate DeltaR plots
def process_delta_r(base_dir, categories, observables):
    plot_files = []  # To store paths of saved plots

    for observable in observables:
        for category in categories:
            # Load particle data
            try:
                photons = pd.read_pickle(os.path.join(base_dir, f"photons_filtered_Wanilo_{observable}_{category}.pkl"))
                muons = pd.read_pickle(os.path.join(base_dir, f"muons_filtered_Wanilo_{observable}_{category}.pkl"))
                electrons = pd.read_pickle(os.path.join(base_dir, f"electrons_filtered_Wanilo_{observable}_{category}.pkl"))
                jets = pd.read_pickle(os.path.join(base_dir, f"jets_filtered_Wanilo_{observable}_{category}.pkl"))
            except FileNotFoundError:
                continue

            # Group by 'N' and select the first particle in each group (nth(0))
            photons0 = photons.groupby(['N']).nth(0)
            muons0 = muons.groupby(['N']).nth(0)
            electrons0 = electrons.groupby(['N']).nth(0)
            jets0 = jets.groupby(['N']).nth(0)

            # Pairings for DeltaR calculation
            pairings = [
                ("muon0", muons0, "photon0", photons0),
                ("electron0", electrons0, "muon0", muons0),
                ("electron0", electrons0, "photon0", photons0),
                ("jet0", jets0, "muon0", muons0),
                ("jet0", jets0, "electron0", electrons0),
                ("jet0", jets0, "photon0", photons0)
            ]

            for name1, data1, name2, data2 in pairings:
                # Merge data based on index and drop rows with missing values
                combined = pd.merge(data1, data2, left_index=True, right_index=True, suffixes=(f"_{name1}", f"_{name2}"))
                if combined.empty:
                    continue

                # Calculate DeltaR
                combined["DeltaR"] = calculate_delta_r(
                    combined[f"eta_{name1}"], combined[f"phi_{name1}"],
                    combined[f"eta_{name2}"], combined[f"phi_{name2}"]
                )

                # Generate and save the DeltaR plot
                plt.figure(figsize=(8, 6))
                plt.hist(combined["DeltaR"], bins=30, color='blue', alpha=0.7)
                plt.title(f"{category.upper()} ({observable.replace('_', ' ').capitalize()}) - $\Delta R$ Distribution: {name1} with {name2}", fontsize=16)
                plt.xlabel("$\Delta R$")
                plt.ylabel("Frequency")
                plt.tight_layout()

                # Save the plot as .png
                output_file = os.path.join(base_dir, f"{category}_{observable}_{name1}_with_{name2}_DeltaR.png")
                plt.savefig(output_file)
                plt.close()

                # Track saved plots
                plot_files.append(output_file)

    # Print paths of all saved plots after processing
    for plot_file in plot_files:
        print(f"Saved plot: {plot_file}")

# Run the DeltaR plot generation
process_delta_r(base_dir_wanilo, categories, observables)






