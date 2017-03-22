import peewee
import datetime
from Database import DatabaseModel

DEFAULT_DEVICE = 42


class Devices(DatabaseModel):
    type_id = peewee.IntegerField()
    owner_id = peewee.IntegerField()
    display_name = peewee.CharField()
    uuid = peewee.CharField()
    creation_data = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    last_activity_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
