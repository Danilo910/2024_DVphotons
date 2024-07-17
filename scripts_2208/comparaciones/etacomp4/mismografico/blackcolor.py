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
    return np.array(x_values), np.array(y_values)

# Read the data from both files
file_path_no_pt = 'eta_histo_no_pt.txt'
file_path_pt = 'eta_histo_pt.txt'

x_values_no_pt, y_values_no_pt = read_data(file_path_no_pt)
x_values_pt, y_values_pt = read_data(file_path_pt)

# Find common x values
common_x_values = np.intersect1d(x_values_no_pt, x_values_pt)

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot common points in black
for x in common_x_values:
    y_no_pt = y_values_no_pt[np.where(x_values_no_pt == x)]
    y_pt = y_values_pt[np.where(x_values_pt == x)]
    plt.scatter([x]*len(y_no_pt), y_no_pt, color='black', alpha=0.7)
    plt.scatter([x]*len(y_pt), y_pt, color='black', alpha=0.7)

# Plot non-common points with less intensity
for x, y in zip(x_values_no_pt, y_values_no_pt):
    if x not in common_x_values:
        plt.scatter(x, y, color='red', alpha=0.3)

for x, y in zip(x_values_pt, y_values_pt):
    if x not in common_x_values:
        plt.scatter(x, y, color='blue', alpha=0.3)

# Set log scale for both axes
plt.xscale('log')
plt.yscale('log')

# Set labels and title
plt.xlabel('delta z atlas')
plt.ylabel('Error porcentual deltaz atlas vs deltaz simple')
plt.title('Scatter Plot of X and Y Values (Log Scale)')

# Show legend
plt.legend(['Common Data Points', 'No PT Data Points', 'PT Data Points'])

# Save the plot to a PNG file
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot_highlighted.png')
plt.savefig(output_file)

print(f"Scatter plot saved as 'scatter_plot_highlighted.png' in {os.path.dirname(os.path.abspath(__file__))}")

