from os.path import expanduser, join, isdir
from os import mkdir
from uuid import uuid4
from pathlib import Path

HOME = expanduser("~")
DEFAULT_LOCATION = join(HOME, ".tzfwrapper")

def create_cache():
    """Creates the cache folder in the user home."""
    if not isdir(DEFAULT_LOCATION):
        mkdir(DEFAULT_LOCATION)

def create_record():
    """Creates a unique folder"""
    id_ = str(uuid4())
    folder_path = join(DEFAULT_LOCATION, id_)
    mkdir(folder_path)
    return id_
    
def clear_cache():
    """Clears out the cache folder"""
    Path(DEFAULT_LOCATION).rmdir()
    create_cache()