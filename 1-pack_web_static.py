#!/usr/bin/python3
"""
This module contains a Fabric script that generates a .tgz
archive from the contents of the web_static folder.
"""
from fabric.api import local
from datetime import datetime


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
