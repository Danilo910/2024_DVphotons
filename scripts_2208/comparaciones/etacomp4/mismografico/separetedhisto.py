import matplotlib.pyplot as plt
import os
import numpy as np

def read_data(file_path):
    x_values = []
    y_values = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 2:
                x = np.abs(float(parts[0]))
                y = float(parts[1])
                if x > 1:
                    x_values.append(x)
                    y_values.append(y)
    return x_values, y_values

def create_scatter_plot(x_values, y_values, label, color, output_file):
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, alpha=0.7, label=label, color=color)
    plt.xlabel('delta z atlas')
    plt.ylabel('Error porcentual deltaz atlas vs deltaz simple')
    plt.title(f'Scatter Plot of {label} (Log Scale)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.savefig(output_file)
    print(f"Scatter plot saved as '{output_file}'")

# Read the data from both files
file_path_no_pt = 'eta_histo_no_pt.txt'
file_path_pt = 'eta_histo_pt.txt'

x_values_no_pt, y_values_no_pt = read_data(file_path_no_pt)
x_values_pt, y_values_pt = read_data(file_path_pt)

# Create and save the scatter plot for eta_histo_no_pt.txt
output_file_no_pt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot_no_pt.png')
create_scatter_plot(x_values_no_pt, y_values_no_pt, 'No PT Data Points', 'red', output_file_no_pt)

# Create and save the scatter plot for eta_histo_pt.txt
output_file_pt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot_pt.png')
create_scatter_plot(x_values_pt, y_values_pt, 'PT Data Points', 'blue', output_file_pt)

