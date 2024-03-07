#!/usr/bin/python3

"""
Distributes an archive to my web servers,
"""

from fabric.api import *
# Importing fabric API for remote operations
from datetime import datetime
# Importing datetime module for timestamp
import os
# Importing os module for file operations

env.hosts = ['100.25.45.246', '18.204.11.210']
# Setting the host IP addresses
env.user = 'ubuntu'
# Setting the username for remote operations


def deploy():
    ''' Full deployment'''
    archive_path = do_pack()
# Calling the do_pack function to create an archive
    if not archive_path:
        return False
    return do_deploy(archive_path)
# Calling the do_deploy function to deploy the archive


def do_pack():
    '''
    Generates a tgz archive from the web_static folder
    '''
    try:
        local('mkdir -p versions')
# Creating a directory to store the archive
        datetime_format = '%Y%m%d%H%M%S'
# Setting the format for the timestamp
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        # Creating the archive path with timestamp
        # Creating the archive using tar command
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {}'.format(archive_path))
        print('Size: {}'.format(os.path.getsize(archive_path)))
        # Printing the path and size of the archive
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    '''
    Deploy archive to web server
    '''
    if not os.path.exists(archive_path):
        # Checking if the archive exists
        return False
    # Extracting the file name from the archive path
    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/'
    # Setting the path for releases
    # Creating the path for the release folder
    releases_path = file_path + file_name[:-4]
    try:
        # Uploading the archive to the remote server
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(releases_path))
        # Creating the release folder
        # Extracting the archive to the release folder
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        # Removing the archive from the temporary folder
        run('rm /tmp/{}'.format(file_name))
        # Moving the contents of web_static folder to the release folder
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        # Removing the web_static folder from the release folder
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')  # Removing the current symlink
        # Creating a new symlink to the latest release
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')  # Printing a success message
        return True
    except Exception:
        return False
