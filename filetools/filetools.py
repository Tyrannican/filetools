import os


def ensure_dir(file):
    if not os.path.exists(file.dirname):
        os.makedirs(file.dirname)


def is_subdir(path, directory):
    path = os.path.realpath(path)
    directory = os.path.realpath(directory)
    relative = os.path.relpath(path, directory)
    if relative.startswith(os.pardir):
        return False
    else:
        return True


class File(object):
    def __init__(self, filepath, refpath):
        self.refpath = os.path.abspath(refpath)
        if os.path.isabs(filepath):
            self.path = os.path.normpath(filepath)
        else:
            self.path = os.path.join(self.refpath, filepath)

    @property
    def abspathfromref(self):
        return os.path.join(os.sep, self.relpath)

    @property
    def absdirnamefromref(self):
        return os.path.join(os.sep, self.reldirname)

    @property
    def abspath(self):
        return os.path.abspath(self.path)

    @property
    def relpath(self):
        return os.path.relpath(self.path, self.refpath)

    @property
    def reldirname(self):
        return os.path.relpath(self.dirname, self.refpath)

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def filebasename(self):
        return os.path.splitext(self.filename)[0]

    @property
    def extension(self):
        return os.path.splitext(self.filename)[1][1:]

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def dirname(self):
        return os.path.dirname(self.path)

    @property
    def modified(self):
        return os.path.getmtime(self.path)

    @property
    def created(self):
        return os.path.getctime(self.path)

    def change_filename(self, newfilename):
        self.path = os.path.join(self.dirname, newfilename)

    def change_filebasename(self, newbasename):
        self.path = os.path.join(self.dirname, newbasename + os.extsep + self.extension)

    def change_ext(self, newext):
        self.path = os.path.join(self.dirname, self.filebasename + os.extsep + newext)

    def change_refpath(self, newrefpath):
        self.path = os.path.normpath(os.path.join(newrefpath, self.relpath))
        self.refpath = os.path.normpath(newrefpath)

    def is_older(self, file):
        return self.modified < file.modified

    def duplicate(self, newrefpath=None):
        file_copy = File(self.path, self.refpath)
        if newrefpath:
            file_copy.change_refpath(newrefpath)
        return file_copy

    def read(self):
        with open(self.path) as f:
            data = f.read()
        return data

    def write(self, data):
        ensure_dir(self)
        with open(self.path, 'w') as f:
            f.write(data)

    def append(self, data):
        ensure_dir(self)
        with open(self.path, 'a') as f:
            f.write(data)
