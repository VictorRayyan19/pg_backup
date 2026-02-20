
import subprocess
import logging
from preflight.env_checks import find_pg_dump_in_safe_paths
from utils.backup_extention_format import create_backup_object_name

logger = logging.getLogger(__name__)

""" This finction is the core functionality of the app as it runs the
pg_dump the secure way
"""
def archive_db(conf_dict: dict[str, dict[str, str]]) -> str:
    # dictionary for source configuration
    source_conf_dict = conf_dict["source"];

    # dictionary for the target configuration.
    # need to be used in the future
    target_conf_dict = conf_dict["target"]

    backup_file = create_backup_object_name(source_conf_dict)
    secure_pg_dump_path = find_pg_dump_in_safe_paths() 
    cmd = [
        secure_pg_dump_path,
        "-U", source_conf_dict["pg_user"],
        "-h", source_conf_dict["host"],
        "-p", str(source_conf_dict["port"]),
        "-d", source_conf_dict["database_name"],
        "-F", source_conf_dict["backup_format"],
        "-f", backup_file
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True
        )
        logging.info(f"Backup successful to local storage: {backup_file}")
        return backup_file
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(f"Backup failed: {e.stderr.decode()}")
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during backup: {e}")
