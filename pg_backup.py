from preflight.main_checks import main_checks_and_load_conf
from core.archive_db import archive_db



if __name__ == "__main__":
    try:
        conf_dict = main_checks_and_load_conf("config.yaml")
        print("Preflight checks passed. Starting backup...")

    except Exception as e:
        print(f"Preflight checks failed: {e}")
        exit(1)

    try:
        archive_db(conf_dict)
    except Exception as e:
        print(f"{e}")
        exit(1)