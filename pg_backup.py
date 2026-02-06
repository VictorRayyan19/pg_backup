import subprocess
import os
import datetime
import yaml

def load_config(config_path: str) -> dict:
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file {config_path} not found: {e}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {config_path}: {e}")

def check_backup_dir_exists(backup_dir: str) -> None:
    if not os.path.exists(os.path.expanduser(backup_dir)):
        raise FileNotFoundError(f"Backup directory {backup_dir} does not exist.")

def archive_and_apply_config(config: dict) -> None:
    check_backup_dir_exists(config["backup_dir"])
    archive_db(
        config["database_name"],
        config["backup_dir"],
        config["pg_user"],
        config["port"],
        config["host"],
        config["backup_format"]
    )


def archive_db(database_name: str, backup_dir: str, pg_user: str, port: int, host: str, backup_format: str,) -> None:
    backup_file = os.path.expanduser(f"{backup_dir}/backup_file_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.dump")
    cmd = [
        "pg_dump",
        "-U", pg_user,
        "-h", host,
        "-p", str(port),
        "-d", database_name,
        "-F", backup_format,
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
        config = load_config("config.yaml")
        archive_and_apply_config(config)
        print("Backup process completed.")
    except (FileNotFoundError, subprocess.SubprocessError, ValueError) as e:
        print(f"Error : {e}")