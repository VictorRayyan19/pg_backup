import logging
import os
import subprocess

logger = logging.getLogger(__name__)

def scp_backup_to_target(backup_path: str, conf_dict: dict[str, dict[str, str]]) -> None:
    target_conf = conf_dict["target"]
    is_dir = os.path.isdir(backup_path)
    scp_cmd = [
        "scp",
        "-r" if is_dir else "",
        "-i", target_conf["ssh_keys"],
        "-P", str(target_conf["port"]),
        backup_path,
        f"{target_conf['user']}@{target_conf['host']}:{target_conf['path']}"
    ]
    scp_cmd = [part for part in scp_cmd if part]
    
    try:
        result = subprocess.run(
            scp_cmd,
            capture_output=True,
            check=True
        )
        logger.info("Backup successfully transferred to target: %s", target_conf["host"])
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(f"SCP transfer failed: {e.stderr.decode()}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during SCP transfer: {e}")