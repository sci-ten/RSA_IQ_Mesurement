import glob
import os


def get_latest_file(dir,extension=None):
    if extension is not None:
        add='*.'+extension
    else:
        add='*'
    dir=os.path.join(dir,add)
    dir=dir.replace("\\","//")

    list_of_files = glob.glob(dir)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

