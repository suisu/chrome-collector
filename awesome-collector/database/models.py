#awesome-collector/database/models.py

from .db import db
import datetime

class Fragment(db.Document):
    date_modified = db.DateTimeField(default=datetime.datetime.utcnow)
    url = db.StringField(required=False)
    fields = db.DictField(required=False)
