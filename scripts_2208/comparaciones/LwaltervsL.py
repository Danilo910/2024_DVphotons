# Use the name of your text file
file_name = 'betactauvsL.txt'

# Open the file and read the lines
with open(file_name, 'r') as file:
    lines = file.readlines()

# Count the number of lines with more than a 5% error
count = 0
for line in lines:
    value = float(line.strip())
    if value > 0.10:  # Assuming 0.05 represents the 5% threshold
        count += 1

print(f"Number of lines with more than a 8% error (beta*c*tau vs L): {count}")

