#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import models
import os


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = 'reviews'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        text = ""
        place_id = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """ Initialize review """
        super().__init__(*args, **kwargs)

    def place(self):
        """ Return the place """
        place = models.storage.all(Place)
        for key, value in place.items():
            if value.id == self.place_id:
                return value
        return None
