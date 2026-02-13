import yaml
import os
from utils import fs_utils
from utils.fs_utils import create_directory_if_not_exists
from preflight.env_checks import check_pg_dump_exists_and_permitted

def main_checks_and_load_conf(config_file_path: str) -> dict[str, str] | None:
    """
    This function performs the main checks for the backup script needed resources to operate. 
    It checks if the backup directory exists and creates it if it does not, if the config file exists, 
    and if the config file has valid YAML syntax. 

    Fail:
    If any of these checks fail, it will raise an appropriate exception.

    Pass:
    If all checks pass, it will return the configuration dictionary.

    """
    try:
        # Check if pg_dump exists and is permitted
        check_pg_dump_exists_and_permitted()

        config_file_full_path = os.path.expanduser(config_file_path)

        # Check if the config file exists
        # This function will handle the case of the file not existing and will raise a FileNotFoundError if it does not exist
        # It also checks for the syntax of the file and will raise a ValueError if the syntax is invalid
        # And it will return yaml syntax errors if the file is not a valid yaml file
        conf_dict = fs_utils.load_yaml(config_file_full_path)

        # The file is only expanded once and no need to expand after it
        backup_dir_full_path = os.path.expanduser(conf_dict['backup_dir'])

        # Check if the backup directory exists and create it if it does not exist
        # May raise a PermissionError if the user does not have permission to create the directory
        create_directory_if_not_exists(backup_dir_full_path) 


        return (conf_dict)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error File Not Found: {e}") from e
    
    except ValueError as e:
        raise ValueError(f"Error Wrong Value: {e}") from e
    
    except PermissionError as e:
        raise PermissionError(f"Error Permission Denied: {e}") from e

    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e