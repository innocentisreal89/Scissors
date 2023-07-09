import unittest
from app import create_app,config_dict
from db import db
from model.user import User
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token



