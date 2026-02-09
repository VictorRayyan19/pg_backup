import errno
import subprocess


""" This module contains functions that check for the existence and permissions of the pg_dump command.
It checks if the pg_dump command is available in the system and if the user has permission to execute it. 
If any of these checks fail, it will raise an appropriate exception that should be handled"""


###########################################################
#!!!!!!!!!!!! TO DO !!!!!!!!!!!!#
# - Add more checks for pg_dump, such as using only the secure paths to the command, and checking for the version of pg_dump to ensure compatibility with the PostgreSQL server version.
# - Add logging instead of print statements for better error tracking and debugging.
# - Add unit tests for these functions to ensure they work as expected and handle edge cases properly

def check_pg_dump_exists_and_permitted() -> None:
    try:
        subprocess.run(
            ["pg_dump", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except OSError as e:
        if e.errno == errno.EACCES:
            raise PermissionError(
                "Permission denied when trying to execute pg_dump. Please check your permissions."
            )
        if e.errno == errno.ENOENT:
            raise FileNotFoundError(
                "pg_dump command not found. Please ensure PostgreSQL client tools are installed and pg_dump is in your PATH."
            )
        raise

    except subprocess.CalledProcessError as e:
        err_msg = (e.stderr or "").strip() or "Unknown error"
        raise subprocess.SubprocessError(f"Error executing pg_dump: {err_msg}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred while checking pg_dump: {e}")