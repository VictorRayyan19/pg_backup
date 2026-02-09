import subprocess
import os
import datetime
import yaml
from preflight.main_checks import main_checks_and_load_conf


def load_config(config_path: str) -> dict:
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file {config_path} not found: {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {config_path}: {e}")


def archive_db(conf_dict) -> None:
    backup_file = os.path.expanduser(f"{conf_dict['backup_dir']}/backup_file_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.dump")
    cmd = [
        "pg_dump",
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


if __name__ == "__main__":
    try:
        main_checks_and_load_conf("config.yaml")
        print("Preflight checks passed. Starting backup...")
    except Exception as e:
        print(f"Preflight checks failed: {e}")
        exit(1)