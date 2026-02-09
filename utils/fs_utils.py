import os
import yaml

def create_directory_if_not_exists(directory: str) -> None:
    """
    Creates a directory if it does not exist.
    """
    try:
        if not os.path.exists(directory):
         os.makedirs(directory)
    except Exception as e:
        raise OSError(f"Failed to create directory {directory}: {e}")
    
def load_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in {file_path}: {e}")
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {file_path}, got {type(data).__name__}")
    return data