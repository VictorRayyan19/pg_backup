import os
from datetime import datetime


def get_format_extension(format_name: str) -> str:
    format_mapping = {
        "c": ".dump",
        "t": ".tar",
        "p": ".sql",
        "d": ""
    }
    ext = format_mapping.get(format_name)
    if ext is None:
        formats = ", ".join(format_mapping.keys())
        raise ValueError(f"Unsupported backup format: {format_name}. "
                         f"Supported formats are: {formats}.")
    return ext


""" This function creates the backup file name based on the
 current timestamp and the backup format specified in the 
 configuration."""

def create_backup_object_name(source_conf_dict: dict[str, str]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = source_conf_dict["backup_dir"]
    backup_format = source_conf_dict["backup_format"]
    extension = get_format_extension(backup_format)
    filename = f"backup_file_{timestamp}{extension}"
    backup_file = os.path.expanduser(os.path.join(backup_dir, filename))
    return backup_file
