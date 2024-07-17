import numpy as np
import os

def read_data(file_path):
    # Print the current working directory to verify the script's location
    print("Current working directory:", os.getcwd())
    
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

def find_and_write_extremes(x_values, y_values, output_file):
    # Find maximum and minimum y values and their corresponding x values
    max_y_index = np.argmax(y_values)
    min_y_index = np.argmin(y_values)
    
    max_x = x_values[max_y_index]
    max_y = y_values[max_y_index]
    
    min_x = x_values[min_y_index]
    min_y = y_values[min_y_index]
    
    # Write the results to a text file
    with open(output_file, 'w') as file:
        file.write(f"Maximum y value:\n")
        file.write(f"x: {max_x}, y: {max_y}\n")
        file.write(f"\nMinimum y value:\n")
        file.write(f"x: {min_x}, y: {min_y}\n")

# Example usage
file_path = 'eta_histo_no_pt.txt'  # Use the filename directly
output_file = 'output.txt'

x_values, y_values = read_data(file_path)
find_and_write_extremes(x_values, y_values, output_file)

print(f"Results have been written to {output_file}")
