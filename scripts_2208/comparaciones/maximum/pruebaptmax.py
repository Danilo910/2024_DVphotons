import numpy as np

# Initialize an empty dictionary
pt_dict = {}

# Example values to add (you should replace these with your actual calculations)
R1 = 1.1
R2 = 2.2
eta1 = 0.3
eta2 = 0.4
zsimpl_value = 2.0
z_atlas_value = 2.5
pt = 25  # Replace with your actual pt calculation

# Calculate deltaz
deltaz = np.abs((zsimpl_value - z_atlas_value) / z_atlas_value) * 100

# Add the new entry to the dictionary
if pt not in pt_dict:
    pt_dict[pt] = []

pt_dict[pt].append([R1, R2, eta1, eta2, zsimpl_value, z_atlas_value])

# Print the dictionary
print("Updated dictionary:")
for pt, values in pt_dict.items():
    print(f"pt: {pt}, values: {values}")
