import os
import yaml


# ! Note: the path variable will be provided by the main_checks.py
#  that will also take the accountability for the path expantion


# Checks if a certain directory exists, and that it is a dir before starting the script.
def check_directory_exists(directory: str) -> None:
    does_dir_exists = os.path.isdir(directory)
    if not does_dir_exists:
        raise FileNotFoundError(f"Directory {directory} does not exist.") # !: This exception should be handeled
    
    

# Checks if a certain file exists before starting the script.
def check_file_exists(file_path: str) -> None:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.") # !: This exception should be handeled