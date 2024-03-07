#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import env, put, run
from os.path import exists


# Define the list of web servers
env.hosts = ['100.25.45.246', '18.204.11.210']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    # Check if the archive file exists
    if not exists(archive_path):
        return False
    try:
        # Extract the filename from the archive path
        filename = archive_path.split('/')[-1]
        # Define the path where the archive will be extracted
        name = '/data/web_static/releases/' + \
            "{}".format(filename.split('.')[0])
        # Define the temporary path for the archive
        tmpName = "/tmpName/" + filename
        # Upload the archive to the temporary path on the server
        put(archive_path, "/tmpName/")
        # Create the directory for the extracted files
        run("mkdir -p {}/".format(name))
        # Extract the archive to the specified directory
        run("tar -xzf {} -C {}/".format(tmpName, name))
        # Remove the temporary archive file
        run("rm {}".format(tmpName))
        # Move the contents of the extracted directory to the parent directory
        run("mv {}/web_static/* {}/".format(name, name))
        # Remove the empty web_static directory
        run("rm -rf {}/web_static".format(name))
        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")
        # Create a new symbolic link to the extracted directory
        run("ln -s {}/ /data/web_static/current".format(name))
        return True
    except Exception:
        return False
