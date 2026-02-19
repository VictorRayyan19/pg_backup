from preflight.main_checks import main_checks_and_load_conf
from core.archive_db import archive_db
from utils.scp_utils import scp_backup_to_target


# ! Note to do: add scp


if __name__ == "__main__":
    try:
        conf_dict = main_checks_and_load_conf("config.yaml")
        print("Preflight checks passed. Starting backup...")

    except Exception as e:
        print(f"Preflight checks failed: {e}")
        exit(1)

    try:
        if conf_dict is None:
            raise ValueError("Configuration dictionary is None. Cannot proceed with backup.")
        backup_file = archive_db(conf_dict)
        scp_backup_to_target(backup_file, conf_dict)

    except Exception as e:
        print(f"Error during backup: {e}")
        exit(1)