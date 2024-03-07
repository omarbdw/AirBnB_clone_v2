#!/usr/bin/python3
"""
Distributes an archive to my web servers,
"""
from fabric.api import *
from datetime import datetime
import os


# Import necessary modules

# Define the list of web servers
env.hosts = ['100.25.45.246', '18.204.11.210']
env.user = 'ubuntu'

# Function to generate a tgz archive


def do_pack():
    '''
    Generates a tgz archive from the web_static folder
    '''
    try:
        # Create a versions directory if it doesn't exist
        local('mkdir -p versions')

        # Define the format for the archive name
        # using current date and time
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))

        # Create the tgz archive
        local('tar -cvzf {} web_static'.format(archive_path))

        # Print the path and size of the created archive
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
    except Exception:
        return None

# Function to deploy the archive to the web server


def do_deploy(archive_path):
    '''
    Deploy archive to web server
    '''
    # Check if the archive exists
    if not os.path.exists(archive_path):
        return False

    # Extract the file name from the archive path
    file_name = archive_path.split('/')[1]

    # Define the file path and releases path on the web server
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]

    try:
        # Upload the archive to the /tmp/
        # directory on the web server
        put(archive_path, '/tmp/')

        # Create the releases directory
        run('mkdir -p {}'.format(releases_path))

        # Extract the archive to the releases directory
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))

        # Remove the archive from the /tmp/ directory
        run('rm /tmp/{}'.format(file_name))

        # Move the contents of the web_static
        # folder to the releases directory
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(releases_path))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the latest release
        run('ln -s {} /data/web_static/current'.format(releases_path))

        # Print a success message
        print('New version deployed!')

        return True
    except Exception:
        return False
