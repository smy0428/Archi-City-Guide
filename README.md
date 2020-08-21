# Archi Guide Full Stack Web Application

## About

The Archi Guide is an architecture-tour-guide site that facilitates the discovery and sharing of travel experiences. This site lets you list new architects, cities, discover them, and list architectural work designed by the architects in the cities. You can also find various useful information to make a better plan for your next trip. You can easily start to explore the architectural world by typing the name of a city or architect. 

The link is as follows:
https://archi-city-guide.herokuapp.com/


## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the project directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup in Postgres

With Postgres running, create a database:

```bash
createdb Archi_Guide
```

### Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server on Mac / Linux, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

To run the server on Windows, execute:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to run the application from `app.py` file. 


## Data Modeling

The schema for the database and helper methods to simplify API behavior are in models.py:

- There is an abstract base class 'BaseModel' which has been inherited from other three subclasses, they all share methods: insert, update, delete.
- There are three tables created: City, Architect, Architecture.
- The Architecture table has two foreign keys, one on the City table as city_id and the other one on the Architect table as architect_id.
- The City table is used to store the information about various cities. They will be sorted according to the country.
- The Architect table is used to store the information about various architects. They will be sorted according to the nationality.
- Each table has init, repr and format helper functions.


## Roles and Permissions

There are three roles for this application:

- public: 
    - City:          view & search
    - Architect:     view & search
    - Architecture:  view & search
- user: 
    - City:          view & search & add
    - Architect:     view & search & add
    - Architecture:  view & search & add
- owner: 
    - City:          view & search & add & edit & delete
    - Architect:     view & search & add & edit & delete
    - Architecture:  view & search & add & edit & delete


## API Reference

### Endpoints

`GET '/architects'`
- Fetches a list of architects
- Request arguments: None

`GET '/architects/<int: architect_id>'`
- Fetches an architect according to the id
- Request arguments: architect_id

`GET '/cities'`
- Fetches a list of cities
- Request arguments: None

`GET '/cities/<int: city_id>'`
- Fetches a city according to the id
- Request arguments: city_id

`GET '/architectures'`
- Fetches a list of architectures
- Request arguments: None

`GET '/architectures/<int: architecture_id>'`
- Fetches an architecture according to the id
- Request arguments: architecture_id

`GET/POST '/architects'`
- Add a new architect in the database
- Request arguments: 
```
{
    name: string, 
    awards: list(string),
    gender: string,
    birthday: data,
    birthplace: string,
    nationality: string,
    image_link: string,
    website: string,
    has_quote: boolean,
    quote: string
}
```

`GET/POST '/cities'`
- Add a new city in the database
- Request arguments: 
```
{
    name: string,
    transports: list(string),
    country: string,
    image_link: string,
    has_more_info: boolean,
    info: string
}
```

`GET/POST '/architectures'`
- Add a new architecture in the database
- Request arguments: 
```
{
    name: string,
    completed_year: integer,
    address: string,
    latitude: float,
    longitude: float,
    image_link: string,
    has_more_info: boolean,
    info: string,
    other_image_link_1: string,
    other_image_link_2: string,
    other_image_link_3: string
}
```

`GET/POST '/architects/<int:architect_id>'`
- Update an architect in the database based on the architect_id
- Request arguments (optional): 
```
{
    name: string, 
    awards: list(string),
    gender: string,
    birthday: data,
    birthplace: string,
    nationality: string,
    image_link: string,
    website: string,
    has_quote: boolean,
    quote: string
}
```

`GET/POST '/cities/<int:city_id>'`
- Update an city in the database based on the city_id
- Request arguments (optional): 
```
{
    name: string,
    transports: list(string),
    country: string,
    image_link: string,
    has_more_info: boolean,
    info: string
}
```

`GET/POST'/architectures/<int:architecture_id>'`
- Update an architecture in the database based on the architecture_id
- Request arguments (optional): 
```
{
    name: string,
    completed_year: integer,
    address: string,
    latitude: float,
    longitude: float,
    image_link: string,
    has_more_info: boolean,
    info: string,
    other_image_link_1: string,
    other_image_link_2: string,
    other_image_link_3: string
}
```

`DELETE '/architects/<int:architect_id>'`
- Delete an architect from the database based on the architect_id
- Request arguments: architect_id

`DELETE '/cities/<int:city_id>'`
- Delete an city from the database based on the city_id
- Request arguments: city_id

`DELETE '/cities/<int:architecture_id>'`
- Delete an architecture from the database based on the architecture_id
- Request arguments: architecture_id

`POST '/architects/search'`
- Searches architects from the database based on the search term and fetches a list of related architects
- Request arguments: search term

`POST '/cities/search'`
- Searches cities from the database based on the search term and fetches a list of related cities
- Request arguments: search term

`POST '/architectures/search'`
- Searches architecture from the database based on the search term and fetches a list of related architecture
- Request arguments: search term


### Error Handling

Errors are handled by errorhandler and render with file in template/errors.


## Testing

### Test API locally using command line tool

- Tokens 'TOKEN_USER' and 'TOKEN_OWNER' need in environment update if expired.
- To run the tests locally, run
```
dropdb archi_guide_test
createdb archi_guide_test
python3 test_app.py
```
