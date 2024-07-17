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

# Read the data from both files
file_path_no_pt = 'eta_histo_no_pt.txt'
file_path_pt = 'eta_histo_pt.txt'

x_values_no_pt, y_values_no_pt = read_data(file_path_no_pt)
x_values_pt, y_values_pt = read_data(file_path_pt)

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot data from eta_histo_no_pt.txt
plt.scatter(x_values_no_pt, y_values_no_pt, alpha=0.5, label='No PT Data Points', color='red')

# Plot data from eta_histo_pt.txt
plt.scatter(x_values_pt, y_values_pt, alpha=0.5, label='PT Data Points', color='blue')

# Set log scale for both axes
plt.xscale('log')
plt.yscale('log')

# Set labels and title
plt.xlabel('delta z atlas')
plt.ylabel('Error porcentual deltaz atlas vs deltaz simple')
plt.title('Scatter Plot of X and Y Values (Log Scale)')

# Show legend
plt.legend()

# Save the plot to a PNG file
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot_combined.png')
plt.savefig(output_file)

print(f"Scatter plot saved as 'scatter_plot_combined.png' in {os.path.dirname(os.path.abspath(__file__))}")

