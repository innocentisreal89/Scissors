import unittest
from app import create_app,config_dict
from db import db
from model.user import User
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token


# Note: to have a pass on all of this please comment the # qr.add_data(f'{request.host_url}{self.short_url}') in the Url Model.



class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config= config_dict["test"])
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        user = User(
            username="jay23",
            email="oddystitches@gmail.com",
            password=sha256.hash("password")
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_user_registration(self):
        # test for user registration
        data = {
            "username": "jay234",
            "email": "oddystitches8@gmail.com",
            "password": "password"
        }
        response = self.client.post("/register", json=data)
        user = User.query.filter_by(email=data["email"]).first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])

    def test_user_login(self):
        # test for user login
        data = {
            "email": "oddystitches@gmail.com",
            "password": "password"
        }
        response = self.client.post("/login", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)

    def test_get_a_user(self):
        # test for getting a user
        # create JWT token for authorization
        token = create_access_token(identity='oddystitches@gmail.com')

        # set headers with JWT token
        headers = {
            "Authorization": f"Bearer {token}"
            }
        response = self.client.get("/users", headers=headers)
        self.assertEqual(response.status_code, 200)
        
