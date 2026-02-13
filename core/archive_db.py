
import os
import subprocess
import datetime
from preflight.main_checks import main_checks_and_load_conf

def archive_db(conf_dict) -> None:
    backup_file = os.path.expanduser(f"{conf_dict['backup_dir']}/backup_file_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.dump")
    cmd = [
        "/usr/bin/pg_dump",
        "-U", conf_dict["pg_user"],
        "-h", conf_dict["host"],
        "-p", str(conf_dict["port"]),
        "-d", conf_dict["database_name"],
        "-F", conf_dict["backup_format"],
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