
import subprocess
from preflight.env_checks import find_pg_dump_in_safe_paths
from utils.backup_extention_format import create_backup_object_name


""" This finction is the core functionality of the app as it runs the
pg_dump the secure way
"""
def archive_db(conf_dict: dict[str, dict[str, str]]) -> str:
    backup_file = create_backup_object_name(conf_dict)
    secure_pg_dump_path = find_pg_dump_in_safe_paths() 
    cmd = [
        secure_pg_dump_path,
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
        return backup_file
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(f"Backup failed: {e.stderr.decode()}")
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during backup: {e}")