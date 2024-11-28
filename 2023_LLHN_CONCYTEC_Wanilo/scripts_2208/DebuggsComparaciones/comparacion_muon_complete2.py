import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Directories
base_dir_wanilo = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"
base_dir_cristian = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"

# Prefixes for the comparison
categories = ["TTH", "WH", "ZH"]
observables = ["before_overlapping", "after_overlapping"]

# Function to calculate ΔR
def delta_r(eta1, phi1, eta2, phi2):
    delta_phi = np.abs(phi1 - phi2)
    delta_phi = np.where(delta_phi > np.pi, 2 * np.pi - delta_phi, delta_phi)
    return np.sqrt((eta1 - eta2) ** 2 + delta_phi ** 2)

# Function to load data
def load_data(base_dir, prefix, observable, particle):
    file_path = os.path.join(base_dir, f"{particle}_filtered_Wanilo_{observable}_{prefix}.pkl")
    return pd.read_pickle(file_path)

# Function to create plots
# Function to create plots with updated ΔR calculation for id=0
def compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables):
    for observable in observables:
        for category in categories:
            # Load data for Wanilo and Cristian
            muons_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"muons_filtered_Wanilo_{observable}_{category}.pkl"))
            electrons_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"electrons_filtered_Wanilo_{observable}_{category}.pkl"))
            jets_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"jets_filtered_Wanilo_{observable}_{category}.pkl"))
            photons_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"photons_filtered_Wanilo_{observable}_{category}.pkl"))

            muons_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"muons_filtered_Cristian_{category}.pkl"))
            electrons_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"electrons_filtered_Cristian_{category}.pkl"))
            jets_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"jets_filtered_Cristian_{category}.pkl"))
            photons_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"photons_filtered_Cristian_{category}.pkl"))

            # Particle pairs to compare ΔR
            particle_pairs = [
                ("Muon", muons_wanilo, muons_cristian),
                ("Electron", electrons_wanilo, electrons_cristian),
                ("Jet", jets_wanilo, jets_cristian),
                ("Photon", photons_wanilo, photons_cristian)
            ]

            # Filter for id=0 for each particle dataset
            for i, (particle1_name, particle1_wanilo, particle1_cristian) in enumerate(particle_pairs):
                for j, (particle2_name, particle2_wanilo, particle2_cristian) in enumerate(particle_pairs):
                    if i >= j:  # Avoid duplicate pairs (e.g., Muon-Muon)
                        continue

                    # Filter datasets for id=0
                    particle1_wanilo = particle1_wanilo.xs(0, level='id', drop_level=False)
                    particle2_wanilo = particle2_wanilo.xs(0, level='id', drop_level=False)

                    particle1_cristian = particle1_cristian.xs(0, level='id', drop_level=False)
                    particle2_cristian = particle2_cristian.xs(0, level='id', drop_level=False)

                    # Calculate ΔR for Wanilo dataset
                    if not particle1_wanilo.empty and not particle2_wanilo.empty:
                        delta_r_wanilo = delta_r(
                            particle1_wanilo["eta"],
                            particle1_wanilo["phi"],
                            particle2_wanilo["eta"],
                            particle2_wanilo["phi"],
                        )

                        plt.figure(figsize=(8, 6))
                        plt.hist(delta_r_wanilo, bins=30, color='blue', alpha=0.7,
                                 label=f"ΔR ({particle1_name} vs {particle2_name})")
                        plt.title(f"ΔR Between {particle1_name} and {particle2_name} (Wanilo) ({category} - {observable})")
                        plt.xlabel("ΔR")
                        plt.ylabel("Frequency")
                        plt.legend()

                        # Save plot
                        output_file = os.path.join(base_dir_wanilo,
                                                   f"{category}_{observable}_deltaR_{particle1_name}_{particle2_name}_wanilo.png")
                        plt.savefig(output_file)
                        plt.close()
                        print(f"Saved ΔR plot for {particle1_name} vs {particle2_name} (Wanilo) ({category} - {observable}) to {output_file}")

                    # Calculate ΔR for Cristian dataset
                    if not particle1_cristian.empty and not particle2_cristian.empty:
                        delta_r_cristian = delta_r(
                            particle1_cristian["eta"],
                            particle1_cristian["phi"],
                            particle2_cristian["eta"],
                            particle2_cristian["phi"],
                        )

                        plt.figure(figsize=(8, 6))
                        plt.hist(delta_r_cristian, bins=30, color='red', alpha=0.7,
                                 label=f"ΔR ({particle1_name} vs {particle2_name})")
                        plt.title(f"ΔR Between {particle1_name} and {particle2_name} (Cristian) ({category} - {observable})")
                        plt.xlabel("ΔR")
                        plt.ylabel("Frequency")
                        plt.legend()

                        # Save plot
                        output_file = os.path.join(base_dir_cristian,
                                                   f"{category}_{observable}_deltaR_{particle1_name}_{particle2_name}_cristian.png")
                        plt.savefig(output_file)
                        plt.close()
                        print(f"Saved ΔR plot for {particle1_name} vs {particle2_name} (Cristian) ({category} - {observable}) to {output_file}")

# Run the comparison
compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables)


