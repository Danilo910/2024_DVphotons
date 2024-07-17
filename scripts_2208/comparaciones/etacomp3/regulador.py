# Read the entire file
with open('etayz.txt', 'r') as file:
    lines = file.readlines()

# Prepare an empty list to store the modified lines
modified_lines = []

# Process each line
for line in lines:
    # Remove any surrounding whitespace or newline characters
    line = line.strip()
    
    # Split the line based on commas
    values = line.split(',')
    
    # Convert each value to float
    float_values = [float(value) for value in values]
    
    # Insert 0 between the second-last and last elements
    float_values.insert(-1, 0.0)
    
    # Convert float values to strings
    str_values = [str(value) for value in float_values]
    
    # Join the values into a single string without commas
    result_string = ' '.join(str_values)
    
    # Append the result to the modified_lines list
    modified_lines.append(result_string)

# Write the modified lines to a new file
with open('output_file.txt', 'w') as output_file:
    for line in modified_lines:
        output_file.write(line + '\n')

print("Modified lines have been saved to 'output_file.txt'")
