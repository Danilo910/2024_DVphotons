import pandas as pd
import matplotlib.pyplot as plt
import os

# Directories
base_dir_wanilo = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"
base_dir_cristian = "/Collider/2023_LLHN_CONCYTEC/scripts_2208/crisvswd"

# Prefixes for the comparison
categories = ["TTH", "WH", "ZH"]
observables = ["before_overlapping", "after_overlapping"]
particles = ["muons", "electrons", "photons", "jets"]  # Include photons and jets

# Function to create plots
def compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables, particles):
    for observable in observables:
        for category in categories:
            for particle in particles:
                # Load data for Wanilo and Cristian
                file_wanilo = f"{particle}_filtered_Wanilo_{observable}_{category}.pkl"
                file_cristian = f"{particle}_filtered_Cristian_{category}.pkl"

                try:
                    data_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, file_wanilo))
                    data_cristian = pd.read_pickle(os.path.join(base_dir_cristian, file_cristian))
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                    continue

                # Plot pt distribution
                plt.figure(figsize=(8, 6))
                plt.title(f"{category.upper()} ({observable.replace('_', ' ').capitalize()}) - {particle.capitalize()} pt Distribution", fontsize=16)

                plt.hist(data_wanilo["pt"], bins=30, color='blue', alpha=0.5, label="Wanilo")
                plt.hist(data_cristian["pt"], bins=30, color='red', alpha=0.5, label="Cristian")
                plt.xlabel("pt (GeV)")
                plt.ylabel("Frequency")
                plt.legend()

                # Save pt plot
                output_file = os.path.join(base_dir_wanilo, f"{category}_{observable}_{particle}_comparison_pt.png")
                plt.savefig(output_file)
                plt.close()
                print(f"Saved plot for {category} ({observable}, {particle}) to {output_file}")

                # Additional observables for photons
                if particle == "photons":
                    for extra_obs in ["z_origin", "rel_tof"]:
                        plt.figure(figsize=(8, 6))
                        plt.title(f"{category.upper()} ({observable.replace('_', ' ').capitalize()}) - {particle.capitalize()} {extra_obs} Distribution", fontsize=16)

                        plt.hist(data_wanilo[extra_obs], bins=30, color='blue', alpha=0.5, label="Wanilo")
                        plt.hist(data_cristian[extra_obs], bins=30, color='red', alpha=0.5, label="Cristian")
                        plt.xlabel(extra_obs.replace('_', ' ').capitalize())
                        plt.ylabel("Frequency")
                        plt.legend()

                        # Save additional observable plot
                        output_file = os.path.join(base_dir_wanilo, f"{category}_{observable}_{particle}_comparison_{extra_obs}.png")
                        plt.savefig(output_file)
                        plt.close()
                        print(f"Saved plot for {category} ({observable}, {particle}, {extra_obs}) to {output_file}")

# Run the comparison
compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables, particles)




