import os
import pathlib

def refine_path(path):
    return str(pathlib.Path(path))


def check_and_create(dirname):
    if os.path.isdir(dirname):
        return True
    else:
        try:
            os.mkdir(dirname)
            return True
        except FileNotFoundError:
            check_and_create(os.path.dirname(dirname))
            os.mkdir(dirname)
            return True
        except Exception as e:
            raise e
