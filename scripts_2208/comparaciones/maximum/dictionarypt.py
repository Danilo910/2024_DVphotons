# Example data
pt_values = [10, 20, 30, 10, 20]  # Sample pt values
zsimpl_values = [1.0, 2.0, 3.0, 1.1, 2.1]  # Sample zsimpl values
z_atlas_values = [1.5, 2.5, 3.5, 1.6, 2.6]  # Sample z_atlas values
deltaz_values = [0.5, 0.5, 0.5, 0.5, 0.5]  # Sample deltaz values

# Initialize an empty dictionary
pt_dict = {}

# Iterate over the data
for pt, zsimpl, z_atlas, deltaz in zip(pt_values, zsimpl_values, z_atlas_values, deltaz_values):
    if pt not in pt_dict:
        pt_dict[pt] = []
    pt_dict[pt].append([zsimpl, z_atlas, deltaz])

# Print the resulting dictionary
for pt, values in pt_dict.items():
    print(f"pt: {pt}, values: {values}")
