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



# class GetUrlSchema(Schema):
#     id = fields.Integer()
#     user_id = fields.Integer()
#     org_url = fields.String()
#     short_url = fields.String()
#     clicks = fields.Integer()
#     date_created = fields.String()

#     @post_dump(pass_many=True)
#     def add_host_url(self, data, many, **kwargs):
#         host_url = request.host_url  # Get the host URL from the request
#         if many:
#             # If serializing multiple objects, update each object's short_url field
#             for obj in data:
#                 obj['short_url'] = host_url + obj['short_url']
#         else:
#             # If serializing a single object, update its short_url field
#             data['short_url'] = host_url + data['short_url']
#         return data
