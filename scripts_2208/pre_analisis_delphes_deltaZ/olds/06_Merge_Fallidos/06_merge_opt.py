import os
import pandas as pd

# Origin directory where the files are stored
origin = "/Collider/scripts_2208/data/clean/"

# Function to filter files by type, alpha value, and ensure they are .pickle files
def filter_files(file_list, alpha, data_type):
    return [f for f in file_list if f.endswith('.pickle') and f'Alpha{alpha}_13_{data_type}' in f]

# Function to merge and save the files
def merge_and_save(file_list, output_filename, origin_dir):
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through each file in the list and process them
    for file in file_list:
        # Read the pickle file into a DataFrame
        df = pd.read_pickle(os.path.join(origin_dir, file))
        
        # Append the DataFrame to the list
        dataframes.append(df)
    
    # Concatenate all DataFrames in the list
    combined_df = pd.concat(dataframes)
    
    # Reset the 'id' values to be sequential within each 'N'
    combined_df = combined_df.reset_index()
    
    # Sort the DataFrame by 'N' first and then by the original 'id'
    combined_df = combined_df.sort_values(by=['N', 'id'])
    
    # Create new sequential 'id' values within each 'N' group
    combined_df['id'] = combined_df.groupby('N').cumcount()
    
    # Set the index back to ['N', 'id']
    combined_df = combined_df.set_index(['N', 'id'])
    
    # Sort the resulting DataFrame by 'N' and 'id'
    combined_df = combined_df.sort_index()
    
    # Save the combined DataFrame to a new pickle file
    combined_df.to_pickle(os.path.join(origin_dir, output_filename))

    print(f"{output_filename} saved successfully.")

# Get a list of all files in the directory
all_files = os.listdir(origin)

# Data types and corresponding output filenames
data_types = ['photons', 'leptons', 'jets']
alphas = [4, 5, 6]

# Loop through each combination of data type and alpha value
for data_type in data_types:
    for alpha in alphas:
        # Filter files for the current data type and alpha value
        files = filter_files(all_files, alpha, data_type)
        
        print(files)
        # Define the output filename
        output_filename = f"mega{data_type}_{alpha}.pickle"
        
        # Merge and save the files
        merge_and_save(files, output_filename, origin)


