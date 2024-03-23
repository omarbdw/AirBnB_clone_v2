#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
import models
import os


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False)
)


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenities = relationship(
        'Amenity',
        secondary='place_amenity',
        viewonly=False)
    reviews = relationship('Review', backref='place')
else:
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    @property
    def reviews(self):
        """Getter attribute that returns the list of Review instances
        with place_id equals to the current Place.id"""
        review_list = []
        for review in models.storage.all(Review).values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """Getter attribute that returns the list of Amenity instances
        based on the attribute amenity_ids that contains all Amenity.id"""
        amenity_list = []
        for amenity in models.storage.all(Amenity).values():
            if amenity.id in self.amenity_ids:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, obj):
        """Setter attribute that handles append method for adding an Amenity.id
        to
        the attribute amenity_ids"""
        if isinstance(obj, Amenity):
            self.amenity_ids.append(obj.id)
