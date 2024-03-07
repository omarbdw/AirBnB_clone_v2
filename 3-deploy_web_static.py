#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy


env.hosts = ['<IP web-01>', '<IP web-02>']


def deploy():
	"""
	Creates and distributes an archive to web servers
	"""
	archive_path = do_pack()
	if not archive_path:
		return False
	return do_deploy(archive_path)
 