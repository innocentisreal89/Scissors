from marshmallow import Schema, fields, post_dump
from flask import request
'username, email, password'

class PlainUserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserSchema(PlainUserSchema):
    username =fields.Str(required=True)
    email = fields.Str(required=True)

class PlainUrlSchema(Schema):
    org_url = fields.Str(required=True)
    short_url = fields.Str()

class ScissorsSchema(PlainUrlSchema):
    org_url = fields.Str(dump_only=True)
    short_url = fields.Str(dump_only=True)
    # qr_code = fields.Raw(dump_only=True)
    clicks = fields.Int(required=True,dump_only=True)

class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class UserUrls(UserSchema):
    urls = fields.Nested(ScissorsSchema(), many=True)


