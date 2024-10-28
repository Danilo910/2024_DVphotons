import os
import numpy as np
import matplotlib.pyplot as plt
import sys

def create_mass_mapping(directory):
    mass_mapping = {}
    processed_indices = set()  # To track processed main indices

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if filename.startswith("param_card.ScalarLLP") and filename.endswith(".dat"):
            # Extract the main index, e.g., "1" from "param_card.ScalarLLP.1.1.dat"
            index_str = filename.split('.')[2]
            index = float(index_str)
            
            # Skip if this index has already been processed
            if index in processed_indices:
                continue
            processed_indices.add(index)
            
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                in_mass_block = False
                dark_photon_mass = None
                scalar_mass = None
                print("file_path")
                print(file_path)
                # Start reading the file
                for line in f:
                    # Detect the start of the "Block mass" section
                    if line.strip() == "Block mass":
                        in_mass_block = True
                        continue  # Move to the next line after "Block mass"

                    # Only process lines within the "Block mass" section
                    if in_mass_block:
                        if "9900022" in line:  # Dark photon mass
                            try:
                                dark_photon_mass = float(line.split()[1])
                                print("dark_photon_mass")
                                print(dark_photon_mass)
                            except ValueError:
                                print(f"Error parsing dark photon mass in {filename}")
                        
                        elif "9900035" in line:  # Scalar mass
                            try:
                                scalar_mass = float(line.split()[1])
                                print("scalar_mass")
                                print(scalar_mass)
                            except ValueError:
                                print(f"Error parsing scalar mass in {filename}")
                    
                        # Stop reading further once both masses are found
                        if dark_photon_mass is not None and scalar_mass is not None:
                            break  # Exit the loop after finding both masses

                # Add masses to the dictionary if both were found
                if dark_photon_mass is not None and scalar_mass is not None:
                    mass_mapping[index] = (scalar_mass, dark_photon_mass)

    return mass_mapping


def generate_alpha_mapping(directory):
    alpha_mapping = {}
    
    # Iterar sobre cada archivo en el directorio
    for filename in sorted(os.listdir(directory)):
        if filename.startswith("param_card.ScalarLLP") and filename.endswith(".dat"):
            # Extraer el índice principal (main index) y el subíndice (sub index) del nombre del archivo
            main_index = float(filename.split('.')[2])  # Primer número, e.g., 1, 2, 3
            sub_index = int(filename.split('.')[3])  # Segundo número, e.g., 1, 2, ..., 10
            
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                in_darksector_block = False
                gD_value = None
                
                # Leer el archivo línea por línea
                for line in f:
                    # Detectar el inicio del bloque "Block darksector"
                    if line.strip() == "Block darksector":
                        in_darksector_block = True
                        continue
                    
                    # Dentro del bloque "Block darksector", buscar la línea con "gD"
                    if in_darksector_block and "gD" in line:
                        try:
                            # Extraer el valor de gD
                            gD_value = float(line.split()[1])
                        except ValueError:
                            print(f"Error parsing gD in {filename}")
                        break  # Salir del bucle una vez que encontramos el valor de gD
            
            # Almacenar el valor de gD en el diccionario alpha_mapping
            if gD_value is not None:
                # Asegurarse de que la clave para main_index exista en el diccionario
                if main_index not in alpha_mapping:
                    alpha_mapping[main_index] = {}
                
                # Asignar el valor de gD al subíndice correspondiente para este main_index
                alpha_mapping[main_index][sub_index] = gD_value

    return alpha_mapping


def lambda_max(m_phi, BR, m_h=125.1, Gamma_SM=4.07e-3, epsilon=1e-6, alpha=0.01, beta=0.5):
    """
    Calculate the maximum coupling constant lambda_max for Higgs decay.
    
    Parameters:
    - m_phi (float): Mass of the scalar particle in GeV.
    - BR (float or np.array): Branching ratio(s) of Higgs decay into new particles.
    - m_h (float): Mass of the Higgs boson in GeV (default: 125.1 GeV).
    - Gamma_SM (float): Decay width of the Higgs boson into SM particles (default: 4.07e-3 GeV).
    - epsilon (float): Small offset to avoid division by zero when BR is close to 1 (default: 1e-6).
    - alpha (float): Softening factor for the denominator when BR > 1, controls continuity.
    - beta (float): Scaling factor to control additional divergence near BR > 1.
    
    Returns:
    - float or np.array: The calculated lambda_max for each BR value.
    """
    # Ensure BR is a numpy array for element-wise operations
    BR = np.asarray(BR)
    
    # Compute the denominator term (m_h^2 - 4 * m_phi^2)^(1/4)
    mass_diff_term = (m_h**2 - 4 * m_phi**2)**0.25
    
    # Initialize sqrt_term as an array of zeros with the same shape as BR
    sqrt_term = np.zeros_like(BR, dtype=float)
    
    # Case 1: For 0 < BR < 1, use the original formula
    mask_normal = (BR > 0) & (BR < 1)
    sqrt_term[mask_normal] = np.sqrt(Gamma_SM * BR[mask_normal] / (1 - BR[mask_normal]))

    # Case 2: For BR > 1, use the modified denominator and apply the scaling function
    mask_modified = BR > 1
    smooth_denominator = np.maximum(1 - BR[mask_modified], epsilon) + alpha * BR[mask_modified]**2
    scaled_sqrt_term = np.sqrt(Gamma_SM * BR[mask_modified] / smooth_denominator)
    scaling_factor = 1 + beta * (BR[mask_modified]**2 / (1 + BR[mask_modified]))
    sqrt_term[mask_modified] = scaled_sqrt_term * scaling_factor
    
    # Calculate lambda_max for each BR value
    lambda_max_value = (4 * np.sqrt(np.pi) * m_h / mass_diff_term) * sqrt_term
    
    return lambda_max_value



# Directory where the param_card files are stored
#hay que adecuar los directorios para que sean los correctos
directory = '/Collider/limon/param_cards-DarkPh'
mass_mapping = create_mass_mapping(directory)
print("mass_mapping")
print(mass_mapping)


alpha_mapping = generate_alpha_mapping(directory)
print("alpha_mapping")
print(alpha_mapping)


# Directory containing the data files
data_dir = './data/'



lambda_max_vector = np.array([])


# Loop through all files in the directory that match the pattern
for filename in os.listdir(data_dir):
    if filename.startswith("datapoints_") and filename.endswith(".dat"):
        file_path = os.path.join(data_dir, filename)
        
        # Load the data, skipping the first row (header)
        data = np.genfromtxt(file_path, delimiter=',', skip_header=1)

        if data.shape[0] == 0:
            print(f"No data found in {file_path}")
            continue

        # Extract columns
        mass_index = data[:, 0]
        alpha_indices = data[:, 1].astype(int)  # Convert to int for mapping lookup
        y_values = data[:, 2]
        
        # Convert alpha indices to actual alpha values using the alpha_mapping dictionary
        x_values = np.array([alpha_mapping[index][idx] for index, idx in zip(mass_index, alpha_indices)])
        
        # Get unique mass indices in the file to construct the legend
        unique_mass_indices = np.unique(mass_index)
        
        signal_region = filename.replace("datapoints_15GeV-", "").replace(".dat", "")
        print("signal region:", signal_region)

        
        # Create the plot
        plt.figure(figsize=(10, 6))
        
        for index in unique_mass_indices:
            # Filter data for this specific mass index
            mask = mass_index == index
            x_vals = x_values[mask]
            y_vals = y_values[mask]
            
            # Sort x_vals and y_vals by x_vals to ensure continuity
            sorted_indices = np.argsort(x_vals)
            x_vals = x_vals[sorted_indices]
            y_vals = y_vals[sorted_indices]
            
            print("y_vals")
            print(y_vals)
            
            # Retrieve masses for the legend
            scalar_mass, dark_photon_mass = mass_mapping.get(index, ("Unknown", "Unknown"))
            
            #lambda_max_vector = lambda_max(scalar_mass, y_vals)

            #print("lambda_max")
            #print(lambda_max_vector)

            label = f"Scalar Mass: {scalar_mass} GeV, Dark Photon Mass: {dark_photon_mass} GeV"
            
            # Plot
            plt.plot(x_vals, y_vals, marker='o', linestyle='-', label=label)

        
        
        # Add labels and title
        plt.xlabel(r'$\alpha$ (custom scale)')
        plt.ylabel('Branching Ratio (BR)')
        plt.title(f'BR vs Alpha for {signal_region}')
        plt.legend()
        
        # Save the plot with a filename that includes the signal region
        plot_name = f"BRmaxvsAlpha_ScalarHiggs_{signal_region}.png"
        plt.savefig(plot_name)
        plt.close()

        print(f"Saved plot as {plot_name}")
        
        