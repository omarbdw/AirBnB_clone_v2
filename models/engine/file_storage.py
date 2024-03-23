#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            return {key: obj for key, obj in FileStorage.__objects.items()
                    if obj.__class__.__name__ == cls}
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = '{}.{}'.format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        for key, val in FileStorage.__objects.items():
            temp[key] = val.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        ''' delete obj from __objects if it is inside '''
        if obj:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            del FileStorage.__objects[key]

    def close(self):
        """ Deserialize JSON file to objects before leaving """
        self.reload()

    def get(self, cls, id):
        """ get object by class and id """
        key = '{}.{}'.format(cls, id)
        return self.__objects.get(key)

    def count(self, cls=None):
        """ count objects in storage """
        if cls:
            return len(self.all(cls))
        return len(self.all())

    def get_all(self, cls):
        """ get all objects by class """
        return self.all(cls)

    def get_all_by_user(self, user_id):
        """ get all objects by user """
        return self.all('Place')

    def get_all_by_city(self, city_id):
        """ get all objects by city """
        return self.all('Place')

    def get_all_by_state(self, state_id):
        """ get all objects by state """
        return self.all('City')

    def get_all_by_amenity(self, amenity_id):
        """ get all objects by amenity """
        return self.all('Place')

    def get_all_by_place(self, place_id):
        """ get all objects by place """
        return self.all('Review')

    def get_all_by_review(self, review_id):
        """ get all objects by review """
        return self.all('User')
