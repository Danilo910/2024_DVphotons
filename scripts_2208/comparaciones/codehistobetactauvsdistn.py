import matplotlib.pyplot as plt

# Read the data from the text file
file_path = 'datahisto_distnvsLwalter.txt'
with open(file_path, 'r') as file:
    data = [line.strip().split() for line in file]

# Convert data to float
data = [[float(val) for val in row] for row in data]

# Separate data into three lists based on z value ranges
z1 = [(x, y) for x, y in data if 1e-10 <= x < 1e-5 and y <= 1000]
z2 = [(x, y) for x, y in data if 1e-5 <= x < 1 and y <= 1000]
z3 = [(x, y) for x, y in data if x >= 1 and y <= 1000]
outliers = [(x, y) for x, y in data if y > 1000]

# Plot the three scatter plots with logarithmic scale for x-axis
plt.figure(figsize=(12, 6))

# Plot for z between 1e-10 and 1e-5
plt.subplot(1, 3, 1)
plt.scatter(*zip(*z1), color='blue', marker='o', alpha=0.7)
plt.xlabel('Beta Ctau')
plt.ylabel('Percentual Error')
plt.title('Beta Ctau: 1e-10 to 1e-5')
plt.xscale('log')

# Plot for z between 1e-5 and 1
plt.subplot(1, 3, 2)
plt.scatter(*zip(*z2), color='green', marker='o', alpha=0.7)
plt.xlabel('Beta Ctau')
plt.ylabel('Percentual Error')
plt.title('Beta Ctau: 1e-5 to 1')
plt.xscale('log')

# Plot for z greater than 1
plt.subplot(1, 3, 3)
plt.scatter(*zip(*z3), color='red', marker='o', alpha=0.7)
plt.xlabel('Beta Ctau')
plt.ylabel('Percentual Error')
plt.title('Beta Ctau: > 1')
plt.xscale('log')

# Save the plots as PNG files
output_file_path1 = 'scatter_plots_logscale_xaxis.png'
output_file_path2 = 'outliers_scatter_plot.png'
plt.savefig(output_file_path1)

# Close the plot to prevent it from being displayed on the screen
plt.close()

# Create a separate scatter plot for outliers
plt.figure(figsize=(8, 6))
plt.scatter(*zip(*outliers), color='black', marker='x', alpha=0.7)
plt.xlabel('Beta Ctau')
plt.ylabel('Percentual Error')
plt.title('Outliers (Percentual Error > 1000)')
plt.xscale('log')

# Save the outliers scatter plot as a PNG file
plt.savefig(output_file_path2)

# Close the plot to prevent it from being displayed on the screen
plt.close()








