from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,create_refresh_token,get_jwt
from model.user import User
from schema import *
from datetime import timedelta
from extension import cache, limiter, BLOCKLIST


blp =  Blueprint('User', 'user', description='Operation on User')

'''
    1. Build Api first
    2. Test it
    3. Integrate
'''

#   to get register a user
@blp.route('/register')
class RegisterUser(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self,user_data):
        user = User.query.filter_by(username=user_data['username']).first()
        if user:
            abort(400, message=f'User with {user} already exist')

        user = User(
            username = user_data['username'].lower(),
            email = user_data['email'].lower(),
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        user.save()
        return {"message": "User Created Successfully!"}, 201
    
@blp.route('/login')
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @cache.cached(timeout=3600)
    @limiter.limit("10 per minute")
    def post(self,user_data):
        current_user = User.query.filter_by(email=user_data['email'].lower()).first()
            
        if current_user and pbkdf2_sha256.verify(user_data["password"], current_user.password):
            access_token = create_access_token(identity=current_user.email, fresh=True)
            refresh_token = create_refresh_token(identity=current_user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            abort(401, message="Invalid credentials.")


#Creating a refresh token so user will not have to re-login again
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.doc(description='Get an Access Token')
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, expires_delta=timedelta(hours=2))

        return {"access_token": new_token}

#Logout Function
# @blp.route("/logout")
# class Logout(MethodView):
#     @jwt_required()
#     @blp.doc(description='Logout')
#     def post(self):
#         jti = get_jwt()['jti']
#         BLOCKLIST.add(jti)
#         return {"message": "Successfully logged out"}


@blp.route("/logout", methods=["DELETE"])
@blp.doc(
    description="Logout a user", summary="Logout a user by revoking their access token"
)
@jwt_required()
def revoke_auth():
    jti = get_jwt()["jti"]
    current_user = get_jwt_identity()
    cached_data = cache.get(current_user)
    if cached_data:
        cache.delete(current_user)
    BLOCKLIST.add(jti)
    return {'message':"Successfully logged out"}
    
       
# Getting User details
@blp.route('/users')
class UserDetails(MethodView):
    @blp.response(200,UserSchema)
    @jwt_required()
    @cache.cached(timeout=3600)
    @limiter.limit("10 per minute")
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        return user

