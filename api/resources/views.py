from flask import request,redirect, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..utils import db
from model.url import Url, is_valid_url
from api.schema import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extension.extension import cache, limiter




blp =  Blueprint('Url', 'url', description='Operation on Shortening Url')

'''
    1. Build Api first
    2. Test it
    3. Integrate
'''

#   to get the url from the client and return a value (shortened Url)
@blp.route('/url_shortener')
class ShortenUrl(MethodView):
    @jwt_required()
    @blp.arguments(PlainUrlSchema)
    @blp.response(201,ScissorsSchema)
    def post(self,url_data):

        current_user = get_jwt_identity()

        # #   Validating the Url
        if not is_valid_url(url_data['org_url']):
            abort(400, message='Invalid Url')

        #   checking if url exist in the user's db (reason for the 'user_id=current_user' )
        url = Url.query.filter_by(org_url=url_data['org_url'], user_id=current_user).first()
        if url and url.short_url== url_data['short_url']:
            abort(400, message='This Url and  short url already exist')
        
        url = Url.query.filter_by(short_url=url_data['short_url'], user_id=current_user).first()
        if url :
            abort(400, message='Short url already exist')



        new_link = Url(
            org_url = url_data['org_url'],
            short_url = url_data['short_url'],
            user_id = current_user
        )
        #   logic for customizing short url
        if url_data['short_url']:
            new_link.short_url = url_data['short_url']
            new_link.qr_code = new_link.generateqr()
         
        
        new_link.save()
        response = {
            'org_url': new_link.org_url,
            'short_url': f'{request.host_url}{new_link.short_url}'
        }
        return response, 201
    
    '''getting the urls of a specific logged in user'''
    @jwt_required()
    @blp.response(200,ScissorsSchema(many=True))
    @cache.cached(timeout=3600)
    def get(self):
        current_user = get_jwt_identity()
        _urls = Url.query.filter_by(user_id=current_user).all()
        response = []
        for url in _urls:
            response.append({
                'org_url': url.org_url,
                'short_url': f'{request.host_url}{url.short_url}',
                'clicks': url.clicks,
                # 'qr_code': url.qr_code
            })
        return response, 201
    
"""Redirect to the original url"""    
@blp.route("/<short_url>")
class RedirectUrl(MethodView):
    @jwt_required()
    @blp.response(302)
    @cache.cached(timeout=3600)
    @limiter.limit("10/minute")  # Allow 10 requests per minute
    def get(self, short_url):
        new_link = Url.query.filter_by(short_url=short_url).first()
        if new_link:
            new_link.clicks += 1
            db.session.commit()
            return redirect(new_link.org_url)
        else:
            abort(404, message="Url not found")

"""Get the QR code for a short url"""
@blp.route("/<short_url>/qr_code")
@jwt_required()
@cache.cached(timeout=3600) # Cache for 1 hour (3600 seconds)
@limiter.limit("10/minute")  # Allow 10 requests per minute
def qr_code(short_url):
    link = Url.query.filter_by(short_url=short_url).first_or_404()
    response = make_response(link.qr_code)
    response.headers.set("Content-Type", "image/jpeg")
    return response
    

    
@blp.route('/link_history')
class LinkHistory(MethodView):
    '''getting the urls of a specific user'''
    @jwt_required()
    @blp.response(200,ScissorsSchema(many=True))
    @cache.cached(timeout=3600)
    def get(self):
        current_user = get_jwt_identity()
        urls = Url.query.filter_by(user_id=current_user).all()

        if not urls:
            abort(404, message='Oops! No Url history found')
        return urls

