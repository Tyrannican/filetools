from filetools import FileTaskManager


def printit(f):

    print(f.abspath)

    videofile = f.duplicate()
    videofile.change_filename('video.avi')
    videofile.write('stuff')


def ignore(f):
    videofile = f.duplicate()
    videofile.change_filename('video.avi')
    return videofile.exists

man = FileTaskManager('.', 1)
man.schedule(printit, ['*.json'], ignore)
man.start()

import time
while man.is_alive():
    time.sleep(10)

man.join()
