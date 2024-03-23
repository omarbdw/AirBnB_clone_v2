#!/usr/bin/python3
"""
Instantiates a storage object.
"""
from os import getenv
import models


if getenv("HBNB_TYPE_STORAGE") == "db":
    models.storage = models.engine.db_storage.DBStorage()
else:
    models.storage = models.engine.file_storage.FileStorage()
models.storage.reload()
