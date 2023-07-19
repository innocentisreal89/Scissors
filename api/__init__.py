from flask import Flask, jsonify
from flask_smorest import Api
from .config.config import config_dict
from model.url import Url
from model.user import User
from .utils import db
from api.extension.extension import cache, limiter, BLOCKLIST
from resources.views import blp as UrlBlueprint
from resources.user import blp as UserBlueprint
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager



def create_app(config=config_dict['dev']):

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    api = Api(app)

    
    cache.init_app(app)

    limiter.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The Token has Expired.", "error": "token_expired"}), 401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "description": "Signature verification failed.",
                "error": "invalid token"
            }), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "description": "Request does not contain an access token.",
                "error": "authorization_required"
            }), 401
        )




    api.register_blueprint(UrlBlueprint)
    api.register_blueprint(UserBlueprint)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'Url':Url,
            'User':User
          
        }
    

    
    return app
