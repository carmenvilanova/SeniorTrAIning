import gdown
import pandas as pd
import os
import shutil

def download_file_from_cloud(url: str, base_path: str):
    """
    Downloads a file from a given URL (Google Drive) and saves it two levels up in the directory hierarchy.

    Parameters:
    - url (str): The download URL of the file.
    - base_path (str): The destination folder where the file will be stored.

    Steps:
    1. Download the file while preserving its original name.
    2. Move the file to the specified directory.
    3. Load the file as a DataFrame (if it's a CSV).
    4. Display the first few rows of the DataFrame.

    Exception Handling:
    - If the download fails, an error message is displayed.
    - If the file does not exist after downloading, an error message is shown.
    """
    try:
        print("Downloading file...")
        file_downloaded = gdown.download(url, None, quiet=False)  # Download while keeping the original name

        if file_downloaded and os.path.exists(file_downloaded):
            # Construct the new path while preserving the original filename
            dest_path = os.path.join(base_path, os.path.basename(file_downloaded))

            # Move the file to the target location
            shutil.move(file_downloaded, dest_path)

            print(f"File saved at: {dest_path}")

            # Load the CSV file into a DataFrame
            df = pd.read_csv(dest_path)
            print("File successfully loaded. First rows:")
        else:
            print("Error: The file could not be downloaded.")
    except Exception as e:
        print(f"Error during execution: {e}")


def opening_dataframes(file_ids: dict, base_path: str):
    """
    This function takes a dictionary of file IDs (keys as file names) and a base directory path,
    and loads the corresponding CSV files into pandas DataFrames.

    Args:
    file_ids (dict): A dictionary where keys are the names of the CSV files (without extension),
                      and values are the file IDs or any other identifier.
    base_path (str): The path to the directory where the CSV files are located.

    Returns:
    dict: A dictionary where keys are the same as in the `file_ids` input,
          and values are pandas DataFrames containing the data from the corresponding CSV files.
    """

    # Create a dictionary to store DataFrames
    dfs = {}

    # Loop through all the keys in the file_ids dictionary
    for key in file_ids.keys():
        # Construct the expected file name based on the key (e.g., 'dim_people.csv')
        file_name = f"{key}.csv"
        file_path = os.path.join(base_path, file_name)

        # Check if the file exists in the specified directory
        if os.path.exists(file_path):
            print(f"Loading {file_name}...")
            # Load the CSV file into a DataFrame and store it in the dictionary
            dfs[key] = pd.read_csv(file_path)
        else:
            # Print a message if the file does not exist in the directory
            print(f"{file_name} not found in the directory!")

    # Return the dictionary of DataFrames
    return dfs
