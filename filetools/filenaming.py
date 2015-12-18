import os
import time
import uuid

from filetools import File
from filetools import list_files
from filetools import list_folders


def generate_timestamped_name(extension='', fname=None, fmt='%d_%m_%Y_%Hh%Mm%Ss'):
    if fname is not None:
        fmt = '{fname}_' + fmt
    return time.strftime(fmt).format(fname=fname) + extension


def generate_random_name(extension=''):
    return str(uuid.uuid4()) + extension


def generate_n_digit_name(number, n_digit=4, extension=''):
    return str(number).zfill(n_digit) + extension


def generate_incremental_filename(folderpath='.', extension='', n_digit=4):
    folderpath = os.path.abspath(folderpath)
    found_files = list_files(folderpath, '*' + extension, max_depth=0)

    current_max = -1
    for f in found_files:
        basename = File(f, folderpath).filebasename
        if basename.isdigit():
            count = int(basename)
            if count > current_max:
                current_max = count
    fname = generate_n_digit_name(current_max + 1, n_digit, extension)
    return os.path.join(folderpath, fname)


def generate_incremental_foldername(folderpath='.', n_digit=4):
    folderpath = os.path.abspath(folderpath)
    found_folders = list_folders(folderpath)

    current_max = -1
    for f in found_folders:
        basename = File(f, folderpath).filebasename
        if basename.isdigit():
            count = int(basename)
            if count > current_max:
                current_max = count
    fname = generate_n_digit_name(current_max + 1, n_digit)
    return os.path.join(folderpath, fname)
