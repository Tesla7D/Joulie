import peewee
import datetime
from Database import DatabaseModel

DEFAULT_USER = 2


class Users(DatabaseModel):
    group_id = peewee.IntegerField()
    uuid = peewee.CharField()
    user_id = peewee.CharField()
    cylon_url = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    last_activity_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
