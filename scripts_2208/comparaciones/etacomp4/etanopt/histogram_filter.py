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
# Filter the x_values and y_values where x_values > 200
# Filter the x_values and y_values where x_values > 200
x_values = np.array(x_values)
y_values = np.array(y_values)

filtered_indices = np.where(x_values > 200)
filtered_x_values = x_values[filtered_indices]
filtered_y_values = y_values[filtered_indices]

# Create a scatter plot for filtered values
plt.figure(figsize=(10, 6))
plt.scatter(filtered_x_values, filtered_y_values, alpha=0.7, label='Data Points', color='blue')
plt.xlabel('delta z atlas')
plt.ylabel('Error porcentual deltaz atlas vs deltaz simple')
plt.title('Scatter Plot of X and Y Values (x > 200)')
plt.legend()

# Save the plot to a PNG file
output_file = 'filtered_scatter_plot.png'
plt.savefig(output_file)

print(f"Scatter plot saved as '{output_file}'")
