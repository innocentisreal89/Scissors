import unittest
from app import create_app,config_dict
from db import db
from model.url import Url
from model.user import User
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token

# Note: to have a pass on all of this please comment the # qr.add_data(f'{request.host_url}{self.short_url}') in the Url Model.

class UrlTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        user = User(
            username="izzy",
            email="innocentisreal8@gmail.com",
            password=sha256.hash("password")
        )
        user.save()
        new_link = Url(
            org_url="https://www.wikipedia.com",
            # short_url="",
            user_id='innocentisreal8@gmail.com'
        )
        new_link.save()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_create_short_link(self):
        with self.app.test_request_context():
            # test for creating a short link: user can choose to customize the short url or not
            data = {
                "org_url": "https://www.kaagle.com",
                "short_url": "israel"
            }

            # create JWT token for authorization
            token = create_access_token(identity='innocentisreal8@gmail.com')

            # set headers with JWT token
            headers = {
                "Authorization": f"Bearer {token}"
            }

            response = self.client.post("/url_shortener", json=data, headers=headers)

            self.assertEqual(response.status_code, 201)
            self.assertIn("short_url", response.json)
            """ To have a passed on this, please comment the # qr.add_data(f'{request.host_url}{self.short_url}') in the 
                Url Model.
            """
    


    def test_user_link_history(self):
        # test for getting user link history
        token = create_access_token(identity='innocentisreal8@gmail.com')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get("/link_history", headers=headers)
        self.assertEqual(response.status_code, 200)
