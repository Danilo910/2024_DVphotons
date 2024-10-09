import sys
import numpy as np
import re
import glob
import pandas as pd
from scipy.interpolate import interp1d
from my_funcs import isolation
from pathlib import Path
import json
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os  

# Origin directory where the files are stored
origin = "/Collider/scripts_2208/data/clean/"

# Get a list of all files in the directory
all_files = os.listdir(origin)

# Filter only the pickle files
pickle_files = [f for f in all_files if f.endswith('.pickle')]


# Separate the pickle files by type
photon_files_4 = [f for f in pickle_files if 'Alpha4_13_photons' in f]
photon_files_5 = [f for f in pickle_files if 'Alpha5_13_photons' in f]
photon_files_6 = [f for f in pickle_files if 'Alpha6_13_photons' in f]

lepton_files_4 = [f for f in pickle_files if 'Alpha4_13_leptons' in f]
lepton_files_5 = [f for f in pickle_files if 'Alpha5_13_leptons' in f]
lepton_files_6 = [f for f in pickle_files if 'Alpha6_13_leptons' in f]

jet_files_4 = [f for f in pickle_files if 'Alpha4_13_jets' in f]
jet_files_5 = [f for f in pickle_files if 'Alpha5_13_jets' in f]
jet_files_6 = [f for f in pickle_files if 'Alpha6_13_jets' in f]

print(photon_files_4)
print(jet_files_6)
#sys.exit("Salimos")

def merge_and_save(file_list, output_filename):
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through each file in the list and process them
    for file in file_list:
        # Read the pickle file into a DataFrame
        df = pd.read_pickle(os.path.join(origin, file))
        
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
    combined_df.to_pickle(os.path.join(origin, output_filename))

    print(f"{output_filename} saved successfully.")
"""
def merge_and_save(file_list, output_filename):
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through each file in the list and process them
    for file in file_list:
        # Read the pickle file into a DataFrame
        df = pd.read_pickle(os.path.join(origin, file))
        
        # Append the DataFrame to the list
        dataframes.append(df)
    
    # Concatenate all DataFrames in the list
    combined_df = pd.concat(dataframes)
    
    combined_df.to_pickle(os.path.join(origin, output_filename))

    print(f"{output_filename} saved successfully.")
"""
# Merge and save the pickle files for each type
merge_and_save(photon_files_4, "megaphoton_4.pickle")
merge_and_save(photon_files_5, "megaphoton_5.pickle")
merge_and_save(photon_files_6, "megaphoton_6.pickle")
merge_and_save(lepton_files_4, "megaleptons_4.pickle")
merge_and_save(lepton_files_5, "megaleptons_5.pickle")
merge_and_save(lepton_files_6, "megaleptons_6.pickle")
merge_and_save(jet_files_4, "megajets_4.pickle")
merge_and_save(jet_files_5, "megajets_5.pickle")
merge_and_save(jet_files_6, "megajets_6.pickle")
