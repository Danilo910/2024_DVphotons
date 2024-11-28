import pandas as pd
import matplotlib.pyplot as plt
import os

# Directories
base_dir_wanilo = "/Collider/llpatlas/scripts_2208/crisvswd"
base_dir_cristian = "/Collider/llpatlas/scripts_2208/crisvswd"

# Prefixes for the comparison
categories = ["TTH", "WH", "ZH"]
observables = ["before_overlapping", "after_overlapping"]

# Function to load data
def load_data(base_dir, prefix, observable, particle):
    file_path = os.path.join(base_dir, f"{particle}_filtered_Wanilo_{observable}_{prefix}.pkl")
    return pd.read_pickle(file_path)

# Function to create plots
def compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables):
    for observable in observables:
        for category in categories:
            # Load muons and electrons data for Wanilo and Cristian
            muons_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"muons_filtered_Wanilo_{observable}_{category}.pkl"))
            electrons_wanilo = pd.read_pickle(os.path.join(base_dir_wanilo, f"electrons_filtered_Wanilo_{observable}_{category}.pkl"))
            
            muons_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"muons_filtered_Cristian_{category}.pkl"))
            electrons_cristian = pd.read_pickle(os.path.join(base_dir_cristian, f"electrons_filtered_Cristian_{category}.pkl"))

            # Plot configuration
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))
            fig.suptitle(f"{category.upper()} ({observable.replace('_', ' ').capitalize()}) - pt Distribution", fontsize=16)

            # Muons pt distribution
            axes[0].hist(muons_wanilo["pt"], bins=30, color='blue', alpha=0.5, label="Wanilo")
            axes[0].hist(muons_cristian["pt"], bins=30, color='red', alpha=0.5, label="Cristian")
            axes[0].set_title("Muons")
            axes[0].set_xlabel("pt (GeV)")
            axes[0].set_ylabel("Frequency")
            axes[0].legend()

            # Electrons pt distribution
            axes[1].hist(electrons_wanilo["pt"], bins=30, color='blue', alpha=0.5, label="Wanilo")
            axes[1].hist(electrons_cristian["pt"], bins=30, color='red', alpha=0.5, label="Cristian")
            axes[1].set_title("Electrons")
            axes[1].set_xlabel("pt (GeV)")
            axes[1].set_ylabel("Frequency")
            axes[1].legend()

            # Save plot
            output_file = os.path.join(base_dir_wanilo, f"{category}_{observable}_comparison_pt.png")
            plt.savefig(output_file)
            plt.close()
            print(f"Saved plot for {category} ({observable}) to {output_file}")

# Run the comparison
compare_distributions(base_dir_wanilo, base_dir_cristian, categories, observables)
