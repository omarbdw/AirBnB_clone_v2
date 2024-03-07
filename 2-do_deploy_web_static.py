#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists


env.hosts = ['100.25.45.246', '18.204.11.210']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Uncompress the archive to /data/web_static/releases/<filename>/
        run('mkdir -p /data/web_static/releases/{}'.format(filename))
        run('tar -xzf /tmp/{}.tgz'.format(filename))
        run('-C /data/web_static/releases/{}'.format(filename))

        # Delete the archive from the web server
        run('rm /tmp/{}.tgz'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s /data/web_static/releases/{} '.format(filename) +
            '/data/web_static/current'.format(filename))

        return True
    except Exception:
        return False
