from sqlalchemy import (
    Column, String,
    Integer, Float,
    Date, Boolean
)
from flask_sqlalchemy import SQLAlchemy
import os


# ---------------------------------------------------------------------------#
# App Config.
# ---------------------------------------------------------------------------#


database_path = os.environ.get('DATABASE_URL')
if database_path is None:
    database_name = "Archi_Guide"
    # database_name = 'archi_guide_test'
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)


db = SQLAlchemy()


'''
setup_db binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# ---------------------------------------------------------------------------#
# Base Model. (OOP)
# ---------------------------------------------------------------------------#

class BaseModel(db.Model):
    '''
    __abstract__ causes declarative to skip the production of a table or mapper
    for the class entirely. A class can be added within a hierarchy in the same
    way as mixin (see Mixin and Custom Base Classes), allowing subclasses to
    extend just from the special class.
    '''
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# ---------------------------------------------------------------------------#
# Architect Model.
# ---------------------------------------------------------------------------#

class Architect(BaseModel):
    __tablename__ = 'architects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    awards = Column(db.ARRAY(String))
    gender = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    birthplace = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    website = Column(String)
    has_quote = Column(Boolean, nullable=False)
    quote = Column(String)
    architectures = db.relationship(
        'Architecture', backref='architect', lazy=False
    )
    '''
    Architecture class has not been created.
    use strings to refer to classes that are not created yet.

    Declarative initializer allows string arguments to be passed
    to relationship(). These string arguments are converted into
    callables that evaluate the string as Python code, using the
    Declarative class-registry as a namespace. This allows the
    lookup of related classes to be automatic via their string
    name, and removes the need for related classes to be imported
    into the local module space before the dependent classes have
    been declared.

    It is still required that the modules in which these related
    classes appear are imported anywhere in the application at
    some point before the related mappings are actually used, else
    a lookup error will be raised when the relationship() attempts
    to resolve the string reference to the related class.
    '''

    def __init__(
        self, name, gender, birthday, birthplace, nationality,
        image_link, website, has_quote, quote, awards
    ):
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.birthplace = birthplace
        self.nationality = nationality
        self.image_link = image_link
        self.website = website
        self.has_quote = has_quote
        self.quote = quote
        self.awards = awards

    def __repr__(self):
        return f'<Architect No.{self.id} is {self.name}.>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'birthday': self.birthday
        }


# ---------------------------------------------------------------------------#
# City Model.
# ---------------------------------------------------------------------------#

class City(BaseModel):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    transports = Column(db.ARRAY(String))
    country = Column(String, nullable=False)
    image_link = Column(String, nullable=False)
    has_more_info = Column(Boolean, nullable=False)
    info = Column(String)
    architectures = db.relationship('Architecture', backref='city', lazy=False)

    def __init__(
        self, name, transports, country, image_link, has_more_info, info
    ):
        self.name = name
        self.transports = transports
        self.country = country
        self.image_link = image_link
        self.has_more_info = has_more_info
        self.info = info

    def __repr__(self):
        return f'<City No.{self.id} is {self.name}.>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'image_link': self.image_link,
            'has_more_info': self.has_more_info,
            'info': self.info
        }


# ---------------------------------------------------------------------------#
# Architecture Model.
# ---------------------------------------------------------------------------#

class Architecture(BaseModel):
    __tablename__ = 'architectures'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    completed_year = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_link = Column(String, nullable=False)
    has_more_info = Column(Boolean, nullable=False)
    info = Column(String)
    other_image_link_1 = Column(String)
    other_image_link_2 = Column(String)
    other_image_link_3 = Column(String)

    '''
    ForeignKey takes a single target column
    a column object or a column name as a string
    eg: db.ForeignKey(other_class.__tablename__.id)
    '''
    architect_id = Column(
        Integer, db.ForeignKey('architects.id'), nullable=False
    )
    city_id = Column(
        Integer, db.ForeignKey('cities.id'), nullable=False
    )

    def __init__(
        self, name, completed_year, address, latitude, longitude,
        image_link, architect_id, city_id, has_more_info, info,
        other_image_link_1, other_image_link_2, other_image_link_3
    ):

        self.name = name
        self.completed_year = completed_year
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.image_link = image_link
        self.architect_id = architect_id
        self.city_id = city_id
        self.has_more_info = has_more_info
        self.info = info
        self.other_image_link_1 = other_image_link_1
        self.other_image_link_2 = other_image_link_2
        self.other_image_link_3 = other_image_link_2

    def __repr__(self):
        return f'<Architecture No.{self.id} is {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'completed_year': self.completed_year,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_link': self.image_link,
            'architect_name': self.architect.name,
            'architect_id': self.architect.id,
            'city_name': self.city.name,
            'city_id': self.city.id,
            'has_more_info': self.has_more_info,
            'info': self.info
        }

    def format_images(self):
        links = []

        if self.other_image_link_1:
            links.append(self.other_image_link_1)
        if self.other_image_link_2:
            links.append(self.other_image_link_2)
        if self.other_image_link_3:
            links.append(self.other_image_link_3)

        return links
