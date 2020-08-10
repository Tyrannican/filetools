"""Filehandling tools for filesystem enumeration and file creation.

This module enables the user to enumerate over folders and files in a given
filepath with minimal boilerplate code. File creation and writing is also
supported.

Examples:
    import filetools

    files = filetools.list_files('.', patterns=['*.py', '*.json'])
    folders = filetools.list_folders('.')

Authors:
    Jonathan Grizou (https://github.com/jgrizou)

    Graham Keenan (https:/github.com/tyrannican)
"""

# System imports
from pathlib import Path
from typing import List, Union

def ensure_dir(dirname: str):
    """Ensures a directory exists

    Args:
        dirname (str): Name of the directory
    """

    # Create path object
    path = Path(dirname)

    # Create if it doesn't already exist
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def list_files(
    path: str = '.', patterns: List[str] = ['*'], recursive: bool = False
) -> List[str]:
    """List all files in a given directory that match the given glob patterns.

    Args:
        path (str, optional): Path to search. Defaults to '.'.

        patterns (List[str], optional): Glob patterns to match for.
        Defaults to ['*'].

        recursive (bool): Recursively search all subdirectories

    Returns:
        List[str]: All files in a given directory
    """

    # Construct path pbject
    path = Path(path)

    # Get all files and folders
    files = []

    # Populate files with files that match each glob pattern
    for pattern in patterns:
        files.extend([f.absolute() for f in path.glob(pattern) if f.is_file()])

    # Not a recursive search, just return
    if not recursive:
        return files

    # For every folder, get all files within recursively
    folders = [f.absolute() for f in path.iterdir() if f.is_dir()]
    for folder in folders:
        files.extend(list_files(folder, recursive=recursive))

    # Return all files
    return files


def list_folders(path: str = '.', recursive: bool = False) -> List[str]:
    """Gets all folders and subfolders in a directory

    Args:
        path (str, optional): Path to search. Defaults to '.'.

    Returns:
        List[str]: All folders and subfolders
    """

    # Construct path object
    path = Path(path)

    # Get all folders in path
    folders = [f.absolute() for f in path.iterdir() if f.is_dir()]

    # Not a s=recursive search, just return
    if not recursive:
        return folders

    # Get all subfolders
    for folder in folders:
        folders.extend(list_folders(folder, recursive=recursive))

    # Return folders
    return folders

class File:
    """Custom file object
    Args:
        filepath (str): Path of the file
    """

    def __init__(self, filepath: str):
        # Make the path absolute
        self.path = Path(filepath).resolve()

    @property
    def exists(self) -> bool:
        """Checks if the file exists

        Returns:
            bool: Exists or not
        """

        return self.path.exists()

    @property
    def filebasename(self) -> str:
        """Get the name of the file without extension

        Returns:
            str: Name of the file without extension
        """

        return self.path.name.split('.')[0]

    @property
    def extension(self) -> str:
        """Get the extension of the file

        Returns:
            str: Extension of the file
        """
        return self.path.suffix

    @property
    def filename(self) -> str:
        """Get teh name of the file with extension

        Returns:
            str: Name of the file with extension
        """

        return self.path.name

    @property
    def dirname(self) -> Path:
        """Get the parent directory of the file

        Returns:
            Path: Parent directory
        """
        return self.path.parent

    @property
    def modified(self) -> float:
        """Gets the last tiome the file was modified

        Returns:
            float: Last modified time
        """

        return self.path.stat().st_mtime

    @property
    def created(self) -> float:
        """Get the time when the file was created

        Returns:
            float: Creation time
        """

        return self.path.stat().st_ctime

    def change_filename(self, filename: str):
        """Change the name of the file

        Args:
            filename (str): New filename
        """
        self.path = self.path.parent / filename

    def change_filebasename(self, basename: str):
        """Change the basename of the file

        Args:
            basename (str): New basename
        """

        self.path = self.path.parent / f'{basename}{self.path.suffix}'

    def change_ext(self, ext: str):
        """Change the extension of the file

        Args:
            ext (str): New file extension
        """

        self.path = self.dirname / f'{self.filebasename}.{ext}'

    def is_older(self, file) -> bool:
        """Checks if the current file is older than another file

        Args:
            file (File): Comparison file

        Returns:
            bool: Current file is older or not
        """

        return self.modified < file.modified

    def read(self, rb: bool = False) -> Union[str, bytes]:
        """Reads a file's contents.
        Reads bytes if `rb` flag is set

        Args:
            rb (bool, optional): Read bytes. Defaults to False.

        Returns:
            Union[str, bytes]: File contents, etiher string or bytes
        """

        return self.path.read_text() if not rb else self.path.read_bytes()

    def write(self, data: Union[str, bytes], wb: bool = False):
        """Writes data to a file.
        Writes bytes if `wb` flag is set

        Args:
            data (Union[str, bytes]): Data to write either string or bytes
            wb (bool, optional): Write bytes. Defaults to False.
        """

        ensure_dir(self.dirname)
        self.path.write_text(data) if not wb else self.path.write_bytes(data)

    def append(self, data: Union[str, bytes], ab: bool = False):
        """Append data to a file.
        Appends bytes if `ab` flag is set

        Args:
            data (Union[str, bytes]): Data to append to file
            ab (bool, optional): Append bytes. Defaults to False.
        """

        ensure_dir(self.dirname)
        write_mode = 'a' if not ab else 'ab'

        with open(self.path, write_mode) as fd:
            fd.write(data)
