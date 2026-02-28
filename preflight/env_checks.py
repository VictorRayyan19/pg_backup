import os
import subprocess
import shutil
import stat
import logging


logger = logging.getLogger(__name__)

""" This module contains functions that check for the existence and permissions of the pg_dump command.
It checks if the pg_dump command is available in the system and if the user has permission to execute it. 
If any of these checks fail, it will raise an appropriate exception that should be handled"""

###########################################################
#!!!!!!!!!!!! TO DO !!!!!!!!!!!!#
# - Add logging instead of print statements for better error tracking and debugging.
# - Add unit tests for these functions to ensure they work as expected and handle 
# edge cases properly (may not be done as it is an file system check and may require mocking)

def find_pg_dump_in_safe_paths() -> str:
    safe_dirs = [
        "/usr/bin",
        "/usr/local/bin",
        "/bin",
        "/usr/sbin",
        "/usr/local/sbin",
    ]
    search_path = os.pathsep.join(safe_dirs)
    pg_dump_executable_path = shutil.which("pg_dump", mode=os.F_OK, path=search_path)

    if pg_dump_executable_path is None:
        trusted_dirs = ", ".join(safe_dirs)
        raise FileNotFoundError(
            f"pg_dump command not found in trusted directories: {trusted_dirs}. "
            "Please ensure PostgreSQL client tools are installed."
        )

    return pg_dump_executable_path


"""
This function checks if the pg_dump command exists in the system and if the user has permission to execute it.
It first calls the find_pg_dump_in_safe_paths function to locate the pg_dump executable in trusted directories. 
Then it checks the ownership and permissions of the pg_dump executable using the check_pg_dump_ownership function. 
Finally, it attempts to execute pg_dump with the --version flag to verify that it is working properly.
"""

def check_pg_dump_exists_and_permitted() -> str:
    # Finding the secure pg_dump executable from the safe paths
    pg_dump_executable_path = find_pg_dump_in_safe_paths()
    
    # Check for permissions and security of the found binary
    check_pg_dump_ownership(pg_dump_executable_path)
    
    try:
        result = subprocess.run(
            [pg_dump_executable_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        logging.info(f"pg_dump version: {result.stdout.strip()}")

    except PermissionError:
        raise PermissionError(f"pg_dump exists at {pg_dump_executable_path} but is not executable by this user")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"pg_dump failed to execute: {e.stderr.strip()}")

    return pg_dump_executable_path



""" This function checks the ownership and permissions of the pg_dump executable.
It checks if the pg_dump executable is a regular file, if it is owned by root, 
and if it is not world-writable. If any of these checks fail, it will raise a PermissionError."""

def check_pg_dump_ownership(pg_dump_path: str) -> None:
    st = os.stat(pg_dump_path)
    
    if not stat.S_ISREG(st.st_mode):
        raise PermissionError(f"pg_dump at {pg_dump_path} is not a regular file.")
    
    if st.st_uid != 0:
        raise PermissionError(f"pg_dump at {pg_dump_path} is not owned by root.")
    
    if st.st_mode & stat.S_IWOTH:
        raise PermissionError(f"pg_dump at {pg_dump_path} is world-writable.")
