# FileHelper - Easy File Enumeration

FileHelper is designed to easily allow simple file manipulations and enumerations with minimal boilerplate code.

## Installation

You can install FileHelper from [PyPi](https://pypi.org/project/filehelper/)

```
pip install filehelper
```

## Usage

The main benefit of `FileHelper` is the ease of enumeration over files/folders

```python

import filehelper

# Find all python files in the current directory
py_files = filehelper.list_files('.', patterns['*.py'])

# Find all text and json files in the current directory and subdirectories
txt_files = filehelper.list_files('.', patterns=['*.txt', '*.json'], recursive=True)

# List all folders in the home directory
folders = filehelper.list_folders('/home')

# List all folders in a user's directory
folders = filehelper.list_folders('/home/user', recursive=True)

```

## Authors

* [Jonathan Grizou](https://github.com/jgrizou)

* [Graham Keenan](https://github.com/tyrannican)

All of the work and vision was developed by Jonathan Grizou.

Graham Keenan updated the code to Python3 and removed the dependency on `os` and replace with `pathlib`

Codebase is currently maintained by Graham Keenan