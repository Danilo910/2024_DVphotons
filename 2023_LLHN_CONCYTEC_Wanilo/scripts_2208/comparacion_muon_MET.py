import pandas as pd
import matplotlib.pyplot as plt
import os

# Directories
base_dir_wanilo = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"
base_dir_cristian = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"

# Prefixes for the comparison
categories = ["TTH", "WH", "ZH"]
observables = ["before_overlapping", "after_overlapping"]

# Function to load photons0 and calculate MET
def process_photons0(base_dir, categories, observables):
    for observable in observables:
        for category in categories:
            # Load photons data
            file_photons = f"photons_filtered_Wanilo_{observable}_{category}.pkl"
            try:
                photons = pd.read_pickle(os.path.join(base_dir, file_photons))
            except FileNotFoundError as e:
                print(f"File not found: {e}")
                continue

            # Create photons0
            photons0 = photons.groupby(['N']).nth(0)  # Select only the first photon in each group

            print("photons0")
            print(photons0)
            # Plot MET distribution
            plt.figure(figsize=(8, 6))
            plt.title(f"{category.upper()} ({observable.replace('_', ' ').capitalize()}) - Photons0 MET Distribution", fontsize=16)

            plt.hist(photons0["MET"], bins=30, color='purple', alpha=0.7, label="MET")
            plt.xlabel("MET (GeV)")
            plt.ylabel("Frequency")
            plt.legend()

            # Save MET plot
            output_file = os.path.join(base_dir, f"{category}_{observable}_photons0_MET_distribution.png")
            plt.savefig(output_file)
            plt.close()
            print(f"Saved MET plot for {category} ({observable}) to {output_file}")

# Run the processing for photons0
process_photons0(base_dir_wanilo, categories, observables)



