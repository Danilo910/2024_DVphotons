import os
import numpy as np
import matplotlib.pyplot as plt

# Mapping of the index in column 1 to mass values for scalar and dark photon
mass_mapping = {
    1.0: (5, 10),  # 5 GeV scalar, 10 GeV dark photon
    2.0: (10, 15), # 10 GeV scalar, 15 GeV dark photon
    # Add more mappings if needed
}

# Directory containing the data files
data_dir = './data/'

# Load the alpha mapping from an external file
alpha_mapping_file = os.path.join(data_dir, 'alpha_mapping.dat')
alpha_mapping = {}

# Read the alpha_mapping file to create a dictionary
with open(alpha_mapping_file, 'r') as f:
    for line in f:
        integer_value, alpha_value = line.strip().split(',')
        alpha_mapping[int(integer_value)] = float(alpha_value)

# Loop through all files in the directory that match the pattern
for filename in os.listdir(data_dir):
    if filename.startswith("datapoints_") and filename.endswith(".dat"):
        file_path = os.path.join(data_dir, filename)
        
        # Load the data, skipping the first row (header)
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
        print("data: ", data)

        if data.shape[0] == 0:
            print(f"No data found in {file_path}")
            continue

        # Extract columns
        mass_index = data[:, 0]
        alpha_indices = data[:, 1].astype(int)  # Convert to int for mapping lookup
        y_values = data[:, 2]
        
        # Convert alpha indices to actual alpha values using the alpha_mapping dictionary
        x_values = np.array([alpha_mapping[idx] for idx in alpha_indices])
        
        # Get unique mass indices in the file to construct the legend
        unique_mass_indices = np.unique(mass_index)
        
        # Extract the signal region from the filename (assuming it's between two underscores and before ".dat")
        signal_region = filename.split('_')[-1].replace('.dat', '')

        print("signal_region", signal_region)
        

        # Create the plot
        plt.figure(figsize=(10, 6))
        
        for index in unique_mass_indices:
            # Filter data for this specific mass index
            mask = mass_index == index
            x_vals = x_values[mask]
            y_vals = y_values[mask]
            
            # Retrieve masses for the legend
            scalar_mass, dark_photon_mass = mass_mapping.get(index, ("Unknown", "Unknown"))
            label = f"Scalar Mass: {scalar_mass} GeV, Dark Photon Mass: {dark_photon_mass} GeV"
            
            # Plot
            plt.plot(x_vals, y_vals, marker='o', linestyle='-', label=label)
        
        # Add labels and title
        plt.xlabel(r'$\alpha$ (custom scale)')
        plt.ylabel('Branching Ratio (BR)')
        plt.title(f'BR vs Alpha for {filename}')
        plt.legend()
        
        # Save the plot with a filename that includes the signal region
        plot_name = f"BRmaxvsAlpha_Scalar{scalar_mass}_DarkPhoton{dark_photon_mass}_{signal_region}.png"
        plt.savefig(plot_name)
        plt.close()

        print(f"Saved plot as {plot_name}")
        