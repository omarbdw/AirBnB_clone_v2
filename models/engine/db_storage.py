from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                getenv('HBNB_MYSQL_USER'), getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"), getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        Base.metadata.create_all(self.__engine)

        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def all(self, cls=None):
        from models import classes
        objects = {}
        if cls:
            query = self.__session.query(classes[cls]).all()
        else:
            query = []
            for cls in classes.values():
                query += self.__session.query(cls).all()
        for obj in query:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects[key] = obj
        return objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
