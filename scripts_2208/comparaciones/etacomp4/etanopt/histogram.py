import matplotlib.pyplot as plt
import os
import numpy as np

# Read the data from the file
file_path = 'eta_histo.txt'

# Initialize lists to store x and y values
x_values = []
y_values = []

with open(file_path, 'r') as file:
    for line in file:
        # Split each line into two parts and convert to float
        parts = line.split()
        if len(parts) == 2:
            x = np.abs(float(parts[0]))
            y = float(parts[1])
            x_values.append(x)
            y_values.append(y)

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, alpha=0.7, label='Data Points', color='blue')
plt.xlabel('delta z atlas')
plt.ylabel('Error porcentual deltaz atlas vs deltaz simple')
plt.title('Scatter Plot of X and Y Values')
plt.legend()

# Save the plot to a PNG file
output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scatter_plot.png')
plt.savefig(output_file)

print(f"Scatter plot saved as 'scatter_plot.png' in {os.path.dirname(os.path.abspath(__file__))}")
