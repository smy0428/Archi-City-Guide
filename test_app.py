import unittest
from models import setup_db, db, Architect, City, Architecture
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
import os


# ---------------------------------------------------------------------------#
# Tokens need update if expired.
# ---------------------------------------------------------------------------#

token_user = os.environ['TOKEN_USER']
token_owner = os.environ['TOKEN_OWNER']

header_user = {'Authorization': 'Bearer ' + str(token_user)}
header_owner = {'Authorization': 'Bearer ' + str(token_owner)}

BEYOND_VALID_ID = 9999


# ---------------------------------------------------------------------------#
# This class represents Archi_Guide test case.
# ---------------------------------------------------------------------------#


class ArchiGuideTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "archi_guide_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)

        # everytime drop and create new tables
        db.drop_all()
        db.create_all()

        architect_1 = Architect(
            name='Peter Zumthor',
            awards=[],
            gender='Male',
            birthday='1943-04-26',
            birthplace='Basel',
            nationality='swiss',
            image_link='https://64.media.tumblr.com/43715c6c8aa5a49fd88189036e1b893a/tumblr_n92ujr2vCc1r267k8o1_500.png',
            website='https://en.wikipedia.org/wiki/Peter_Zumthor',
            has_quote=False,
            quote=''
        )
        architect_1.insert()

        city_1 = City(
            name='Vals',
            transports=[],
            country='Switzerland',
            image_link='https://en.wikipedia.org/wiki/Vals,_Switzerland#/media/File:Vals,_Switzerland.jpg',
            has_more_info=False,
            info=''
        )
        city_1.insert()

        architecture_1 = Architecture(
            name='Therme Vals',
            completed_year=1996,
            address='Poststrasse 560, 7132 Vals, Switzerland',
            latitude=46.64,
            longitude=9.18,
            architect_id=1,
            city_id=1,
            has_more_info=False,
            info='',
            image_link='https://vals.ch/files/uploads/fotos/erholung/dsc01587-2600x1735.jpg',
            other_image_link_1='https://vals.ch/files/uploads/fotos/erholung/therme/therme-vals_3-2048x1367.jpg',
            other_image_link_2='https://vals.ch/files/uploads/fotos/erholung/therme/therme-vals_4-2048x1368.jpg',
            other_image_link_3='https://vals.ch/files/uploads/fotos/erholung/therme/therme-vals_1-2048x1367.jpg'
        )
        architecture_1.insert()

        architect_2 = Architect(
            name='Louis Kahn',
            awards=[],
            gender='Male',
            birthday='1901-02-20',
            birthplace='Itze-Leib Schmuilowsky',
            nationality='american',
            image_link='https://en.wikipedia.org/wiki/Louis_Kahn#/media/File:Louis_Isadore_Kahn.jpg',
            website='https://en.wikipedia.org/wiki/Louis_Kahn',
            has_quote=False,
            quote=''
        )
        architect_2.insert()

        city_2 = City(
            name='Fort Worth',
            transports=[],
            country='United States',
            image_link='https://www.retirementliving.com/wp-content/uploads/2019/01/Fort-Worth-TX-Retirement-Living.jpg',
            has_more_info=False,
            info='',
        )
        city_2.insert()

        db.session.close()

        self.new_architect = {
            'name': 'Álvaro Siza',
            'awards': [],
            'gender': 'Male',
            'birthday': '1933-06-25',
            'birthplace': 'Matosinhos',
            'nationality': 'portuguese',
            'image_link': 'https://en.wikipedia.org/wiki/%C3%81lvaro_Siza_Vieira#/media/File:Siza_Vieira_na_Exponor.JPG',
            'website': 'https://www.sizavieira.pt/',
            'has_quote': 'No',
            'quote': ''
        }

        self.update_architect = {
            'name': 'Lina Bo Bardi',
            'awards': [],
            'gender': 'Female',
            'birthday': '1914-12-05',
            'birthplace': 'Rome',
            'nationality': 'brazilian',
            'image_link': 'https://www.casatigallery.com/wp-content/uploads/2019/10/Lina-Bo-Bardi-on-the-ship-Almirante-Jaceguay-on-her-way-to-Brasil-in-1946.jpg',
            'website': 'https://hgallery.com/lina-bo-bardi',
            'has_quote': 'No',
            'quote': ''
        }

        self.new_city = {
            'name': 'Bregenz',
            'transports': [],
            'country': 'Switzerland',
            'image_link': 'https://en.wikipedia.org/wiki/Bregenz#/media/File:Bregenz_pano_1.jpg',
            'has_more_info': 'No',
            'info': ''
        }

        self.bad_city = {
            'name': 'Bregenz',
            'transports': [],
            # 'country': 'Switzerland',
            'image_link': 'https://en.wikipedia.org/wiki/Bregenz#/media/File:Bregenz_pano_1.jpg',
            'has_more_info': 'No',
            'info': ''
        }

        self.update_city = {
            'name': 'Lisbon',
            'transports': [],
            'country': 'Portugal',
            'image_link': 'http://amazingplacespics.com/wp-content/uploads/2017/03/beautiful-lisbon-in-portugal.jpg',
            'has_more_info': 'No',
            'info': ''
        }

        self.new_architecture = {
            'name': 'Kimbell Art Museum',
            'completed_year': 1972,
            'address':
                '3333 Camp Bowie Blvd, Fort Worth, TX 76107, United States',
            'latitude': 32.75,
            'longitude': -97.36,
            'architect_id': 2,
            'city_id': 2,
            'has_more_info': 'No',
            'info': '',
            'image_link': 'https://www.kimbellart.org/sites/default/files/styles/hero_image/public/2018-12/visit_Hero.jpg?itok=A33MGydP',
            'other_image_link_1': 'https://www.artguide.pro/wp-content/uploads/job-manager-uploads/main_image/2017/05/KAM_gallery_crop-copy1-800x800.jpg',
            'other_image_link_2': 'https://www.kimbellart.org/sites/default/files/styles/hero_image/public/2018-12/Kahn_Hero.jpg?itok=ORCz4gKJ',
            'other_image_link_3': 'https://www.kimbellart.org/art-architecture/architecture/kahn-building'
        }

        self.update_architecture = {
            'name': 'Kimbell Art Museum',
            'completed_year': 1972,
            'address':
                '3333 Camp Bowie Blvd, Fort Worth, TX 76107, United States',
            'latitude': 32.75,
            'longitude': -97.36,
            'architect_id': 2,
            'city_id': 2,
            'has_more_info': 'No',
            'info': '',
            'image_link': 'https://www.kimbellart.org/sites/default/files/styles/hero_image/public/2018-12/visit_Hero.jpg?itok=A33MGydP',
            'other_image_link_1': 'https://www.artguide.pro/wp-content/uploads/job-manager-uploads/main_image/2017/05/KAM_gallery_crop-copy1-800x800.jpg',
            'other_image_link_2': 'https://www.kimbellart.org/sites/default/files/styles/hero_image/public/2018-12/Kahn_Hero.jpg?itok=ORCz4gKJ',
            'other_image_link_3': 'https://www.kimbellart.org/art-architecture/architecture/kahn-building'
        }

    def tearDown(self):
        db.session.commit()
        pass

# ---------------------------------------------------------------------------#
# READ.
# ---------------------------------------------------------------------------#

    def test_get_architects(self):
        res = self.client.get('/architects')
        self.assertEqual(res.status_code, 200)

    def test_get_an_architect(self):
        res = self.client.get('/architects/1')
        self.assertEqual(res.status_code, 200)

    def test_error_404_get_an_architect_unvalid_id(self):
        res = self.client.get('/architects/{BEYOND_VALID_ID}')
        self.assertEqual(res.status_code, 404)

    def test_get_cities(self):
        res = self.client.get('/cities')
        self.assertEqual(res.status_code, 200)

    def test_get_an_city(self):
        res = self.client.get('/cities/1')
        self.assertEqual(res.status_code, 200)

    def test_error_404_get_an_city_unvalid_id(self):
        res = self.client.get('/cities/{BEYOND_VALID_ID}')
        self.assertEqual(res.status_code, 404)

    def test_get_architectures(self):
        res = self.client.get('/architectures')
        self.assertEqual(res.status_code, 200)

    def test_get_an_architecture(self):
        res = self.client.get('/architectures/1')
        self.assertEqual(res.status_code, 200)

# ---------------------------------------------------------------------------#
# SEARCH.
# ---------------------------------------------------------------------------#

    def test_search_architects(self):
        architect = Architect.query.get(1)
        search_term = architect.name
        res = self.client.post('/architects/search', data=search_term)
        self.assertEqual(res.status_code, 200)

    def test_search_cities(self):
        city = City.query.get(1)
        search_term = city.name
        res = self.client.post('/cities/search', data=search_term)
        self.assertEqual(res.status_code, 200)

    def test_search_architectures(self):
        architecture = Architecture.query.get(1)
        search_term = architecture.name
        res = self.client.post('/architectures/search', data=search_term)
        self.assertEqual(res.status_code, 200)

# ---------------------------------------------------------------------------#
# CREATE.
# ---------------------------------------------------------------------------#

    def test_post_architects_form(self):
        res = self.client.get('/architects/create', headers=header_user)
        self.assertEqual(res.status_code, 200)

    def test_post_architects(self):
        res = self.client.post(
            '/architects', data=self.new_architect, headers=header_user
        )
        self.assertEqual(res.status_code, 201)

    def test_error_401_post_architects_unauthorized(self):
        res = self.client.post('/architects', data=self.new_architect)
        self.assertEqual(res.status_code, 401)

    def test_post_cities_form(self):
        res = self.client.get('/cities/create', headers=header_user)
        self.assertEqual(res.status_code, 200)

    def test_post_cities(self):
        res = self.client.post(
            '/cities', data=self.new_city, headers=header_user
        )
        self.assertEqual(res.status_code, 201)

    def test_error_422_post_cities_incomplete_info(self):
        res = self.client.post(
            '/cities', data=self.bad_city, headers=header_user
        )
        self.assertEqual(res.status_code, 422)

    def test_post_architectures(self):
        res = self.client.get('/architectures/create', headers=header_user)
        self.assertEqual(res.status_code, 200)

    def test_post_architectures(self):
        res = self.client.post(
            '/architectures',
            data=self.new_architecture,
            headers=header_user
        )
        self.assertEqual(res.status_code, 201)

    def test_error_401_post_architectures_form_unauthorized(self):
        res = self.client.get('/architectures/create')
        self.assertEqual(res.status_code, 401)

# ---------------------------------------------------------------------------#
# Delete.
# ---------------------------------------------------------------------------#

    def test_delete_architects(self):
        res = self.client.delete('/architects/2', headers=header_owner)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(None, Architect.query.get(2))

    def test_error_404_delete_architects_unvalid_id(self):
        res = self.client.delete(
            '/architects/{BEYOND_VALID_ID}', headers=header_owner
        )
        self.assertEqual(res.status_code, 404)
        self.assertTrue(Architect.query.get(2))

    def test_delete_cities(self):
        res = self.client.delete('/cities/2', headers=header_owner)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(None, City.query.get(2))

    def test_delete_architectures(self):
        res = self.client.delete('/architectures/1', headers=header_owner)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(None, Architecture.query.get(1))

    def test_error_401_delete_architectures_unauthorized(self):
        res = self.client.delete('/architectures/1', headers=header_user)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(Architecture.query.get(1))

# ---------------------------------------------------------------------------#
# UPDATE.
# ---------------------------------------------------------------------------#

    def test_update_architects_form(self):
        res = self.client.get('/architects/1/patch', headers=header_owner)
        self.assertEqual(res.status_code, 200)

    def test_update_architects(self):
        res = self.client.post(
            '/architects/1/patch',
            data=self.update_architect,
            headers=header_owner
        )
        self.assertEqual(res.status_code, 202)
        self.assertEqual(
            self.update_architect['gender'], Architect.query.get(1).gender
        )

    def test_error_401_update_architects_unauthorized(self):
        res = self.client.post(
            '/architects/1/patch',
            data=self.update_architect,
            headers=header_user
        )
        self.assertEqual(res.status_code, 401)

    def test_update_cities_form(self):
        res = self.client.get('/cities/1/patch', headers=header_owner)
        self.assertEqual(res.status_code, 200)

    def test_update_cities(self):
        res = self.client.post(
            '/cities/1/patch', data=self.update_city, headers=header_owner
        )
        self.assertEqual(res.status_code, 202)
        self.assertEqual(self.update_city['name'], City.query.get(1).name)

    def test_error_422_update_cities_incomplete_info(self):
        res = self.client.post(
            '/cities/1/patch', data=self.bad_city, headers=header_owner
        )
        self.assertEqual(res.status_code, 422)

    def test_update_architectures_form(self):
        res = self.client.get('/architectures/1/patch', headers=header_owner)
        self.assertEqual(res.status_code, 200)

    def test_update_architectures(self):
        res = self.client.post(
            '/architectures/1/patch',
            data=self.update_architecture,
            headers=header_owner
        )
        self.assertEqual(res.status_code, 202)
        self.assertEqual(
            self.update_architecture['name'],
            Architecture.query.get(1).name
        )

    def test_error_401_update_form_architectures_unauthorized(self):
        res = self.client.get('/architectures/1/patch', headers=header_user)
        self.assertEqual(res.status_code, 401)


# ---------------------------------------------------------------------------#
# Make the tests conveniently executable.
# ---------------------------------------------------------------------------#


if __name__ == "__main__":
    unittest.main()
