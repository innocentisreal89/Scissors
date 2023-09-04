import os
from decouple import config  # we'll use config package in this decouple to read the secret key in the .env file
from datetime import timedelta

#   the path to our datatbase
base_dir = os.path.dirname(os.path.realpath(__file__))

# uri =config('DATABASE_URL')
# if uri.startswith('posgres://'):
#     uri = uri.replace('postgres://', 'postgresql://', 1)
    
class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=20)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Url Shortener"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        'info': {
            'title': 'Scissors',
            'version': '1.0',
            'description': 'Url Shortner API',
        },
        'servers': [
            {'url': 'http://localhost:5000', 'description': 'Development server'},
        ],
    }


class DevConfig(Config):
    DEBUG = config('DEBUG', True, cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite3')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' 

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("://", "ql://", 1)               
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = config('DEBUG', False, cast=bool)
    
   


#this config_dict is created so dat we can easily read/hold these classes
config_dict = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}