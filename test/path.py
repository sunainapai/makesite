import os
import tempfile
import shutil


def temppath(*paths):
    return os.path.join(tempfile.gettempdir(), *paths)


def move(src, dst):
    if os.path.isfile(dst):
        os.remove(dst)
    elif os.path.isdir(dst):
        shutil.rmtree(dst)
    if os.path.exists(src):
        os.rename(src, dst)
