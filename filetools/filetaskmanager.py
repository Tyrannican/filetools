import os
import time
import fnmatch
import threading

from filetools import File
from filetools import list_files

class FileTaskManager(threading.Thread):

    def __init__(self, ref_path, screening_sleep_time=30):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interrupted = threading.Lock()

        self.ref_path = ref_path
        self.tasks = []

        self.screening_sleep_time = screening_sleep_time

    def stop(self):
        self.interrupted.release()

    def run(self):
        self.interrupted.acquire()
        while not self.interrupted.acquire(False):
            for (dirpath, dirnames, filenames) in os.walk(self.ref_path):
                for filename in filenames:
                    for task in self.tasks:
                        for pattern in task['patterns']:
                            if fnmatch.fnmatch(filename, pattern):
                                filedir = os.path.abspath(dirpath)
                                filepath = os.path.join(filedir, filename)
                                matched_file = File(filepath, self.ref_path)
                                if not task['ignore_function'](matched_file):
                                    task['callback'](matched_file)
            time.sleep(self.screening_sleep_time)

    def schedule(self, callback, patterns, ignore_function):
        task = {}
        task['callback'] = callback
        task['patterns'] = patterns
        task['ignore_function'] = ignore_function
        self.tasks.append(task)
