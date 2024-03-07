#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime


env.hosts = ['100.25.45.246', '18.204.11.210']


def do_pack():
    """
    Compresses the contents of the web_static folder into a .tgz archive.

    Returns:
            str: The path to the generated archive
            if successful, None otherwise.
    """
    try:
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        local("sudo mkdir -p versions")
        local("sudo tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploys a compressed archive to the web server.

    Args:
        archive_path (str): The path to the compressed archive.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + \
            os.path.splitext(filename)[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Move the contents of the folder /data/web_static/releases/
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))

        # Delete the symbolic link /data/web_static/current from the web server
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the symbolic link /data/web_static/current
        # from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current on
        # the web server, linked to the new version of your code
        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
