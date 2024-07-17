import numpy as np
import matplotlib.pyplot as plt

# Step 1: Read the data from the file
filename = 'dist_n990016.txt'
data = []
with open(filename, 'r') as file:
    data = file.readlines()
data = [float(line.strip()) for line in data]

# Step 2: Create a histogram with logarithmic x-axis
plt.figure(figsize=(10, 6))
plt.hist(data, bins=50, log=True)  # Using log scale for the histogram and specifying the number of bins

# Step 3: Set logarithmic scale for the x-axis
plt.xscale('log')

# Step 4: Add labels and title
plt.xlabel('Value (log scale)')
plt.ylabel('Frequency')
plt.title('Distribution of Points')

output_filename = 'distribution_plot.png'  # Specify the output file name and format
plt.savefig(output_filename)

# Step 5: Display the plot
plt.show()
