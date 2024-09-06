import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Function to merge data and create plots
def merge_and_plot(mode, alpha):
    # Directory where txt files are stored
    origin = f"/Collider/scripts_2208/data/clean/deltaR_{mode}"
    
    # Initialize an empty DataFrame to hold merged data
    merged_data = pd.DataFrame()
    
    # Dictionary to hold data for each event type separately
    data_dict = {}

    # Read and merge the data for each event type
    for event_type in ['ZH', 'WH', 'TTH']:
        file_path = f"{origin}/deltaR_Alpha{alpha}_{event_type}.txt"
        data = np.loadtxt(file_path)
        df = pd.DataFrame(data, columns=["deltaR"])
        
        # Store the data for individual plotting
        data_dict[event_type] = df

        #print("event_type: ")
        #print(event_type)
        #print("data_dict")
        #print(data_dict)
        
        # Merge the data
        merged_data = pd.concat([merged_data, df], ignore_index=True)


    # Save the merged plot in the specified directory
    destiny = f"./data/deltaR_merge/{mode}_{alpha}/"
    Path(destiny).mkdir(exist_ok=True, parents=True)


    # Create the first plot: All data merged
    bins = np.arange(0, 6, 0.1)
    plt.figure(figsize=(10, 6))
    plt.hist(merged_data['deltaR'], bins=bins, alpha=0.7, label=f"Alpha {alpha}")
    plt.title(f"deltaR Histogram for Alpha {alpha} (All Merged)")
    plt.xlabel("deltaR")
    plt.ylabel("Frequency")
    plt.legend()
    
   
    plt.savefig(f"{destiny}/deltaR_histogram_alpha{alpha}_merged.png")
    plt.close()

    # Create the second plot: Differentiating by event type
    plt.figure(figsize=(10, 6))
    for event_type, df in data_dict.items():
        plt.hist(df['deltaR'], bins=bins, alpha=0.5, label=event_type, histtype='stepfilled')
    
    plt.title(f"deltaR Histogram for Alpha {alpha} (Differentiated by Type)")
    plt.xlabel("deltaR")
    plt.ylabel("Frequency")
    plt.legend()
    
    # Save the differentiated plot in the specified directory
    plt.savefig(f"{destiny}/deltaR_histogram_alpha{alpha}_differentiated.png")
    plt.close()

# Define the strings
iso = "iso"
no_iso = "no_iso"

# Create a list containing both strings
modes = [iso, no_iso]


# Loop through each mode in the list
for mode in modes:
    # Perform actions with each mode
    print(f"Processing mode: {mode}")
    # Run the analysis for each alpha value
    for alpha in [4, 5, 6]:
        print(f"alpha: {alpha}")
        merge_and_plot(mode, alpha)