#!/usr/bin/python3
"""
Generates a .tgz archive from the contents
of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    '''
    Generates a tgz archive from the web_static folder
    '''
    try:
        # Create a directory to store the archive
        local('mkdir -p versions')

        # Define the format for the archive name
        # using the current date and time
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))

        # Create the archive using the tar command
        local('tar -cvzf {} web_static'.format(archive_path))

        # Print the path and size of the packed archive
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
    except Exception:
        return None
