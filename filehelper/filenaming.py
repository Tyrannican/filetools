"""General filenaming utilities

Provides helper functions for naming files.

Authors:
    Jonathan Grizou (https://github.com/jgrizou)
    Graham Keenan (https://github.com/tyrannican)

"""

import time
import uuid
from typing import Optional

def generate_timestamped_name(
    extension: str = '',
    fname: Optional[str] = None,
    fmt: str = '%d_%m_%Y_%Hh%Mm%Ss'
) -> str:
    """Generates a filename with the current time stammped

    Args:
        extension (str, optional): File extension (e.g. `.txt`).
        Defaults to ''.

        fname (Optional[str], optional): Name of the file. Defaults to None.

        fmt (str, optional): Time format. Defaults to '%d_%m_%Y_%Hh%Mm%Ss'.

    Returns:
        str: Timestammped filename
    """

    # Return Name plus timestamp if given
    if fname is not None:
        return f'{fname}_{time.strftime(fmt)}{extension}'

    # Return just the timestamp
    return f'{time.strftime(fmt)}{extension}'

def generate_random_name(extension: str = '') -> str:
    """Generate a random filename using UUIDv4

    Args:
        extension (str, optional): File extension (e.g. `.txt`). Defaults to ''.

    Returns:
        str: Random filename
    """
    return f'{str(uuid.uuid4())}{extension}'

def generate_n_digit_name(
    number: int, n_digit: int = 4, extension: str = ''
) -> str:
    """Generate a filename with N digits (e.g. 0004)

    Args:
        number (int): Number for the name
        n_digit (int, optional): Padding. Defaults to 4.
        extension (str, optional): File extension (e.g. `.txt`). Defaults to ''.

    Returns:
        str: N-digit name
    """

    return f'{str(number).zfill(n_digit)}{extension}'
