
import os
import subprocess
import datetime
from preflight.main_checks import main_checks_and_load_conf
from utils.backup_extention_format import get_format_extension

""" This function creates the backup file name based on the
 current timestamp and the backup format specified in the 
 configuration."""

def create_backup_object_name(conf_dict: dict[str, dict[str, str]]) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = conf_dict["source"]["backup_dir"]
    backup_format = conf_dict["source"]["backup_format"]
    extension = get_format_extension(backup_format)
    filename = f"backup_file_{timestamp}{extension}"
    backup_file = os.path.expanduser(os.path.join(backup_dir, filename))
    return backup_file
""" This finction is the core functionality of the app as it runs the
pg_dump the secure way
"""
def archive_db(conf_dict: dict[str, dict[str, str]]) -> None:
    backup_file = create_backup_object_name(conf_dict)
    cmd = [
        "/usr/bin/pg_dump",
        "-U", conf_dict["source"]["pg_user"],
        "-h", conf_dict["source"]["host"],
        "-p", str(conf_dict["source"]["port"]),
        "-d", conf_dict["source"]["database_name"],
        "-F", conf_dict["source"]["backup_format"],
        "-f", backup_file
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True
        )
        print(f"Backup successful: {backup_file}")
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(f"Backup failed: {e.stderr.decode()}")
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during backup: {e}")
