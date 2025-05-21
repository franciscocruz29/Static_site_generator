import os
import shutil
from typing import NoReturn


def copy_files_recursive(source_dir_path: str, dest_dir_path: str) -> NoReturn:
    """
    Recursively copies the contents of a source directory to a destination directory.

    If the destination directory does not exist, it is created. All files and subdirectories
    from the source are copied into the destination. Each copied path is logged to stdout.

    Args:
        source_dir_path (str): The path to the source directory to copy from.
        dest_dir_path (str): The path to the destination directory to copy to.
    """
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
