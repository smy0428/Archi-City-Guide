from flask import (
    abort, jsonify,
    flash, Response,
    make_response,
    render_template,
    make_response,
    redirect, url_for,
    session, Flask,
    request
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, db, Architect, City, Architecture
from auth import requires_auth, AuthError
from forms import ArchitectForm, CityForm, ArchitectureForm
import sys
import os
import json
import requests
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv
from functools import wraps


SECRET_KEY = os.urandom(28)
AUTH0_CLIENT_ID = 'AlHUXHQ9siAfCVG4lCLWyjI6DcK5ai53'
AUTH0_CALLBACK_URL = 'http://127.0.0.1:5000/callback'
AUTH0_DOMAIN = 'https://peter-coffee-shop.us.auth0.com'
AUTH0_AUDIENCE = 'archi_guide'
AUTHO_CLIENT_SECRET = os.environ.get(
    'CLIENT_SECRET',
    'N5EfgILViJR89Cap_2u3G7PqbjN2oCxdRvkPGZRC0WWpX2JwITMsHvmaOm1Efy_F'
)

LOGIN_LINK = (
    AUTH0_DOMAIN +
    '/authorize?audience=' +
    AUTH0_AUDIENCE +
    '&response_type=token&client_id=' +
    AUTH0_CLIENT_ID +
    '&redirect_uri=' +
    AUTH0_CALLBACK_URL
)

LOGOUT_LINK = (
    AUTH0_DOMAIN +
    '/v2/logout?client_id=' +
    AUTH0_CLIENT_ID
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app)
    CORS(app)

    oauth = OAuth(app)
    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTHO_CLIENT_SECRET,
        api_base_url=AUTH0_DOMAIN,
        access_token_url=AUTH0_DOMAIN + '/oauth/token',
        authorize_url=AUTH0_DOMAIN + '/authorize',
        client_kwargs={
            'scope': 'openid profile',
        },
    )

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE'
        )
        return response

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

    @app.route('/')
    def welcome():
        return render_template('pages/home.html')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(
            redirect_uri=url_for('callback', _external=True),
            audience=AUTH0_AUDIENCE)

    @app.route('/callback')
    def callback():

        # Handles response from token endpoint
        res = auth0.authorize_access_token()
        token = res.get('access_token')

        # Store the user information in flask session.
        session['jwt_payload'] = token

        flash('You have successfully logged in!')
        return redirect('/')

    def requires_auth_login(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt_payload' not in session:
                flash('You should log in first!')
                return redirect('/')
            return f(*args, **kwargs)
        return decorated

    @app.route('/dashboard')
    @requires_auth_login
    def dashboard():
        return render_template(
            'pages/dashboard.html',
            token=session['jwt_payload'])

    @app.route('/logout')
    @requires_auth_login
    def logout():
        # Clear session stored data
        session['jwt_payload'] = None
        session.clear()
        # Redirect user to logout endpoint
        params = {
            'returnTo': url_for('welcome', _external=True),
            'client_id': AUTH0_CLIENT_ID
        }
        flash('You have successfully logged out!')
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# ----------------------------------------------------------------------------#
# Architects.
# ----------------------------------------------------------------------------#

    @app.route('/architects', methods=['GET'])
    def get_architects():
        selections = Architect.query.distinct(Architect.nationality)
        if selections is None:
            abort(404)

        data = []
        for selection in selections:
            architects_data = []
            architects = Architect.query.filter_by(
                nationality=selection.nationality
            ).all()
            for architect in architects:
                architects_data.append(architect.format())
            data.append({
                'nationality_name': selection.nationality,
                'architects': architects_data
            })

        return render_template(
            'pages/architects.html',
            nationalities=data
        ), 200

    @app.route('/architects/<int:architect_id>', methods=['GET'])
    def get_architect(architect_id):
        architect = Architect.query.get(architect_id)

        if architect is None:
            abort(404)

        architecture_data = []
        for architecture in architect.architectures:
            architecture_data.append(architecture.format())

        architect_data = {
            'id': architect.id,
            'name': architect.name,
            'awards': architect.awards,
            'birthday': architect.birthday,
            'birthplace': architect.birthplace,
            'nationality': architect.nationality,
            'image_link': architect.image_link,
            'website': architect.website,
            'has_quote': architect.has_quote,
            'quote': architect.quote,
            'architectures': architecture_data,
            'architecture_count': len(architecture_data)
        }

        return render_template(
            '/pages/show_architect.html',
            architect=architect_data
        ), 200

    @app.route('/architects/search', methods=['POST'])
    def search_architects():
        search_term = request.form.get('search_term', '')
        search_architects = Architect.query.filter(
            Architect.name.ilike('%' + search_term + '%')).all()

        data = []
        for architect in search_architects:
            data.append({
                "id": architect.id,
                "name": architect.name
            })

        results = {
            "count": len(search_architects),
            "data": data
        }
        return render_template(
            'pages/search_architects.html',
            results=results,
            search_term=search_term
        ), 200

    @app.route('/architects/<int:architect_id>', methods=['DELETE'])
    @requires_auth('delete:architects')
    def delete_architect(jwt, architect_id):
        architect = Architect.query.get(architect_id)
        if architect is None:
            abort(404)

        name = architect.name
        try:
            architect.delete()
            flash('Architect ' + name + ' was successfully deleted!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Architect ' +
                name + ' could not be deleted.'
            )
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 200

    @app.route('/architects/create', methods=['GET'])
    @requires_auth('post:architects')
    def create_architect_form(jwt):
        form = ArchitectForm()
        return render_template('/forms/new_architect.html', form=form), 200

    @app.route('/architects/create', methods=['POST'])
    @requires_auth('post:architects')
    def create_architect(jwt):
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        birthplace = request.form.get('birthplace')
        nationality = request.form.get('nationality')
        image_link = request.form.get('image_link')
        website = request.form.get('website')
        if request.form.get('has_quote') == 'Yes':
            has_quote = True
        else:
            has_quote = False
        quote = request.form.get('quote')
        awards = request.form.getlist('awards')

        try:
            architect = Architect(
                name=name, gender=gender, birthday=birthday,
                birthplace=birthplace, nationality=nationality,
                image_link=image_link, website=website,
                has_quote=has_quote, quote=quote, awards=awards
            )
            architect.insert()
            flash('Architect ' + name + ' was successfully created!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Architect ' +
                name + ' could not be created.'
            )
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 201

    @app.route('/architects/<int:architect_id>/patch', methods=['GET'])
    @requires_auth('patch:architects')
    def update_architect_form(jwt, architect_id):
        form = ArchitectForm()
        architect = Architect.query.get(architect_id)

        if architect is None:
            abort(404)

        name = architect.name

        form.name.data = architect.name
        form.gender.data = architect.gender
        form.birthday.data = architect.birthday
        form.birthplace.data = architect.birthplace
        form.nationality.data = architect.nationality
        form.image_link.data = architect.image_link
        form.website.data = architect.website
        if architect.has_quote:
            form.has_quote.data = 'Yes'
        else:
            form.has_quote.data = 'No'
        form.quote.data = architect.quote
        form.awards.data = architect.awards

        return render_template(
            '/forms/edit_architect.html',
            form=form, architect=architect
        ), 200

    @app.route('/architects/<int:architect_id>/patch', methods=['POST'])
    @requires_auth('patch:architects')
    def update_architect(jwt, architect_id):
        architect = Architect.query.get(architect_id)

        if architect is None:
            abort(404)

        name = request.form.get('name')
        try:
            architect.name = request.form.get('name')
            architect.gender = request.form.get('gender')
            architect.birthday = request.form.get('birthday')
            architect.birthplace = request.form.get('birthplace')
            architect.nationality = request.form.get('nationality')
            architect.image_link = request.form.get('image_link')
            architect.website = request.form.get('website')
            if request.form.get('has_quote') == 'Yes':
                architect.has_quote = True
            else:
                architect.has_quote = False
            architect.quote = request.form.get('quote')
            architect.awards = request.form.getlist('awards')

            architect.update()
            flash('Architect ' + name + ' was successfully updated!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Architect ' +
                name + ' could not be updated.'
            )
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 202

# ---------------------------------------------------------------------------#
# Cities.
# ---------------------------------------------------------------------------#

    @app.route('/cities', methods=['GET'])
    def get_cities():
        selections = City.query.distinct(City.country)
        if selections is None:
            abort(404)

        data = []
        for selection in selections:
            cities_data = []
            cities = City.query.filter_by(country=selection.country).all()
            for city in cities:
                cities_data.append(city.format())
            data.append({
                'country_name': selection.country,
                'cities': cities_data
            })

        return render_template('pages/cities.html', countries=data), 200

    @app.route('/cities/<int:city_id>', methods=['GET'])
    def get_city(city_id):
        city = City.query.get(city_id)

        if city is None:
            abort(404)

        architecture_data = []
        for architecture in city.architectures:
            architecture_data.append(architecture.format())

        city_data = {
            'id': city.id,
            'name': city.name,
            'transports': city.transports,
            'country': city.country,
            'image_link': city.image_link,
            'has_more_info': city.has_more_info,
            'info': city.info,
            'architectures': architecture_data
        }

        return render_template(
            '/pages/show_city.html',
            city=city_data
        ), 200

    @app.route('/cities/search', methods=['POST'])
    def search_cities():
        search_term = request.form.get('search_term', '')
        search_cities = City.query.filter(
            City.name.ilike('%' + search_term + '%')
        ).all()

        data = []
        for city in search_cities:
            data.append({
                "id": city.id,
                "name": city.name
            })

        results = {
            "count": len(search_cities),
            "data": data
        }
        return render_template(
            'pages/search_cities.html',
            results=results,
            search_term=search_term
        ), 200

    @app.route('/cities/<int:city_id>', methods=['DELETE'])
    @requires_auth('delete:cities')
    def delete_city(jwt, city_id):
        city = City.query.get(city_id)
        if city is None:
            abort(404)

        name = city.name
        try:
            city.delete()
            flash('City ' + name + ' was successfully deleted!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. City ' + name + ' could not be deleted.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 200

    @app.route('/cities/create', methods=['GET'])
    @requires_auth('post:cities')
    def create_city_form(jwt):
        form = CityForm()
        return render_template('/forms/new_city.html', form=form), 200

    @app.route('/cities/create', methods=['POST'])
    @requires_auth('post:cities')
    def create_city(jwt):
        name = request.form.get('name')
        country = request.form.get('country')
        image_link = request.form.get('image_link')
        transports = request.form.getlist('transports')
        if request.form.get('has_more_info') == 'Yes':
            has_more_info = True
        else:
            has_more_info = False
        info = request.form.get('info')

        try:
            city = City(
                name=name, country=country, image_link=image_link,
                transports=transports, has_more_info=has_more_info, info=info
            )
            city.insert()
            flash('City ' + name + ' was successfully created!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. City ' + name + ' could not be created.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 201

    @app.route('/cities/<int:city_id>/patch', methods=['GET'])
    @requires_auth('patch:cities')
    def update_city_form(jwt, city_id):
        form = CityForm()
        city = City.query.get(city_id)

        if city is None:
            abort(404)

        form.name.data = city.name
        form.country.data = city.country
        form.image_link.data = city.image_link
        form.transports.data = city.transports
        if city.has_more_info:
            form.has_more_info.data = 'Yes'
        else:
            form.has_more_info.data = 'No'
        form.info.data = city.info

        return render_template(
            '/forms/edit_city.html',
            form=form, city=city
        ), 200

    @app.route('/cities/<int:city_id>/patch', methods=['POST'])
    @requires_auth('patch:cities')
    def update_city(jwt, city_id):
        city = City.query.get(city_id)

        if city is None:
            abort(404)

        name = request.form.get('name')
        try:
            city.name = request.form.get('name')
            city.country = request.form.get('country')
            city.image_link = request.form.get('image_link')
            city.transports = request.form.getlist('transports')
            if request.form.get('has_more_info') == 'Yes':
                city.has_more_info = True
            else:
                city.has_more_info = False
            city.info = request.form.get('info')

            city.update()
            flash('City ' + name + ' was successfully updated!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. City ' + name + ' could not be updated.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 202

# ---------------------------------------------------------------------------#
# Architectures.
# ---------------------------------------------------------------------------#

    @app.route('/architectures', methods=['GET'])
    def get_architectures():
        selections = Architecture.query.all()
        if selections is None:
            abort(404)

        architectures = [architecture.format() for architecture in selections]

        return render_template(
            'pages/architectures.html',
            architectures=architectures
        ), 200

    @app.route('/architectures/<int:architecture_id>', methods=['GET'])
    def get_architecture(architecture_id):
        architecture = Architecture.query.get(architecture_id)

        if architecture is None:
            abort(404)

        architecture_data = architecture.format()
        images_data = architecture.format_images()
        data = {
            'architecture': architecture_data,
            'images': images_data
        }

        return render_template('/pages/show_architecture.html', data=data), 200

    @app.route('/architectures/search', methods=['POST'])
    def search_architectures():
        search_term = request.form.get('search_term', '')
        search_architectures = Architecture.query.filter(
            Architecture.name.ilike('%' + search_term + '%')
        ).all()

        data = []
        for architecture in search_architectures:
            data.append({
                "id": architecture.id,
                "name": architecture.name
            })

        results = {
            "count": len(search_architectures),
            "data": data
        }
        return render_template(
            'pages/search_architectures.html',
            results=results,
            search_term=search_term
        ), 200

    @app.route('/architectures/<int:architecture_id>', methods=['DELETE'])
    @requires_auth('delete:architectures')
    def delete_architecture(jwt, architecture_id):
        architecture = Architecture.query.get(architecture_id)
        if architecture is None:
            abort(404)

        name = architecture.name
        try:
            architecture.delete()
            flash(name + ' was successfully deleted!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. ' + name + ' could not be deleted.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 200

    @app.route('/architectures/create', methods=['GET'])
    @requires_auth('post:architectures')
    def create_architecture_form(jwt):
        form = ArchitectureForm()
        return render_template('/forms/new_architecture.html', form=form), 200

    @app.route('/architectures/create', methods=['POST'])
    @requires_auth('post:architectures')
    def create_architecture(jwt):
        name = request.form.get('name')
        completed_year = request.form.get('completed_year')
        address = request.form.get('address')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        image_link = request.form.get('image_link')
        architect_id = request.form.get('architect_id')
        city_id = request.form.get('city_id')
        if request.form.get('has_more_info') == 'Yes':
            has_more_info = True
        else:
            has_more_info = False
        info = request.form.get('info')
        other_image_link_1 = request.form.get('other_image_link_1')
        other_image_link_2 = request.form.get('other_image_link_2')
        other_image_link_3 = request.form.get('other_image_link_3')

        try:
            architecture = Architecture(
                name=name, completed_year=completed_year, address=address,
                latitude=latitude, longitude=longitude, image_link=image_link,
                architect_id=architect_id, city_id=city_id,
                has_more_info=has_more_info, info=info,
                other_image_link_1=other_image_link_1,
                other_image_link_2=other_image_link_2,
                other_image_link_3=other_image_link_3
            )
            architecture.insert()
            flash(name + ' was successfully created!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. ' + name + ' could not be created.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 201

    @app.route('/architectures/<int:architecture_id>/patch', methods=['GET'])
    @requires_auth('patch:architectures')
    def update_architecture_form(jwt, architecture_id):
        form = ArchitectureForm()
        architecture = Architecture.query.get(architecture_id)

        if architecture is None:
            abort(404)

        form.name.data = architecture.name
        form.completed_year.data = architecture.completed_year
        form.address.data = architecture.address
        form.latitude.data = architecture.latitude
        form.longitude.data = architecture.longitude
        form.image_link.data = architecture.image_link
        form.architect_id.data = architecture.architect_id
        form.city_id.data = architecture.city_id
        if architecture.has_more_info:
            form.has_more_info.data = 'Yes'
        else:
            form.has_more_info.data = 'No'
        form.info.data = architecture.info
        form.other_image_link_1.data = architecture.other_image_link_1
        form.other_image_link_2.data = architecture.other_image_link_2
        form.other_image_link_3.data = architecture.other_image_link_3

        return render_template(
            '/forms/edit_architecture.html',
            form=form,
            architecture=architecture
        ), 200

    @app.route('/architectures/<int:architecture_id>/patch', methods=['POST'])
    @requires_auth('patch:architectures')
    def update_architecture(jwt, architecture_id):
        architecture = Architecture.query.get(architecture_id)

        if architecture is None:
            abort(404)

        name = request.form.get('name')
        try:
            architecture.name = request.form.get('name')
            architecture.completed_year = request.form.get('completed_year')
            architecture.address = request.form.get('address')
            architecture.latitude = request.form.get('latitude')
            architecture.longitude = request.form.get('longitude')
            architecture.image_link = request.form.get('image_link')
            architecture.architect_id = request.form.get('architect_id')
            architecture.city_id = request.form.get('city_id')
            if request.form.get('has_more_info') == 'Yes':
                architecture.has_more_info = True
            else:
                architecture.has_more_info = False
            architecture.info = request.form.get('info')

            architecture.other_image_link_1 = request.form.get(
                'other_image_link_1'
            )
            architecture.other_image_link_2 = request.form.get(
                'other_image_link_2'
            )
            architecture.other_image_link_3 = request.form.get(
                'other_image_link_3'
            )

            architecture.update()
            flash(name + ' was successfully updated!')
        except Exception:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. ' + name + ' could not be updated.')
            abort(422)
        finally:
            db.session.close()

        return render_template('pages/home.html'), 202

# ---------------------------------------------------------------------------#
# Error Handllers.
# ---------------------------------------------------------------------------#

    @app.errorhandler(400)
    def not_found_error(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def not_found_error(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(422)
    def not_found_error(error):
        return render_template('errors/422.html'), 422

    @app.errorhandler(AuthError)
    def auth_error(ex):
        return render_template('errors/401.html'), 401

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
