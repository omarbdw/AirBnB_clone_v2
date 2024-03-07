#!/usr/bin/python3
"""
Fabric script based on the file
2-do_deploy_web_static.py that creates and
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
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
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception:
        return False


def deploy():
    """ creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
