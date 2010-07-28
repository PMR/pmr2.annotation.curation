import os.path
from pmr2.annotation.curation import browser

def getPath(filename):
    return os.path.join(os.path.dirname(browser.__file__), filename)

