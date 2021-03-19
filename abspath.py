# relpath.py
# Tawfeeq Mannan
# Last updated 2021/03/19

import sys
import os


def absolute_path(relativePath):
    # get absolute path to resource, whether stored in local folder or TEMP
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)
