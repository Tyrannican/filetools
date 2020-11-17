"""File Task Manager for performing tasks on files

Allows for the creation of Tasks to be performed on a selection of files.
Each task contains a callback function and a list of patterns for files.
Any file that meets the pattern will execute the callback fn

Examples:
    def read_file(path):
        with open(path) as fd:
            return fd.read()

    ftm = FileTaskManager('.')
    ftm.schedule(callback=read_file, patterhs=['*.py', '*.txt'])
    ftm.run()

Authors:
    Jonathan Grizou (https://github.com/jgrizou)
    Graham Keenan (https://github.com/tyrannican)
"""

# System imports
import time
import threading
from pathlib import Path
from typing import Callable, List

# Filetoosl improts
from .filehelpers import list_files

class FileTaskManager(threading.Thread):
    """Class for managing Tasks to perform on files in a given directory

    Args:
        watch_path (str): Path to watch
        screening_sleep_time (int, optional): Time between each task execution

    Inherits:
        threading.Thread
    """

    def __init__(self, watch_path: str, screening_sleep_time: int = 30):
        # Set as a Daemon and set up the lock
        threading.Thread.__init__(self)
        self.daemon = True
        self.interrupted = threading.Lock()

        # Set up path to watch over
        self.watch_path = Path(watch_path).resolve()

        # List for holding all executable tasks
        self.tasks = []

        # Wait time between each iteration
        self.screening_sleep_time = screening_sleep_time

    def stop(self):
        """Stop the Task manager
        """

        self.interrupted.release()

    def run(self):
        """Begin running the task manager
        """

        # Obtain the lock
        self.interrupted.acquire()

        # Loop for as long as the lock is held
        while not self.interrupted.acquire(False):
            # Iterate through all tasks
            for task in self.tasks:
                # Get all files that match the task's patterns
                files = list_files(self.watch_path, patterns=task['patterns'])

                # Cal lthe callback fn on each file
                for file in files:
                    task['callback'](file)

            # Wait before next tieration
            time.sleep(self.screening_sleep_time)

    def schedule(self, callback: Callable, patterns: List[str]):
        """Schedules a new task by adding it to the task list

        Args:
            callback (Callable): Callback function to call upon.
            patterns (List[str]): Patterns to match on the files.
        """

        # Add new task to list
        self.task.append({
            'callback': callback,
            'patterns': patterns,
        })
