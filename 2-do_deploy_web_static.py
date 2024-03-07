#!/usr/bin/python3
from fabric.api import env, put, run
import os

env.hosts = ['100.25.45.246', '18.204.11.210']


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive
        # filename without extension> on the web server
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + \
                  os.path.splitext(filename)[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        # from the web server
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        # on the web server
        run('ln -s {} /data/web_static/current'.format(folder_name))

        return True
    except Exception:
        return False
