import datetime
from db import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2040))
    new_url = db.Column(db.String(5), unique=True)
    clcks = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<URL {self.new_url}>'