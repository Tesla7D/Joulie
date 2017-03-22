import peewee
import datetime
import Database
from models import Users, Devices


class Devices_Access(peewee.Model):
    user = peewee.ForeignKeyField(Users)
    device = peewee.ForeignKeyField(Devices)
    access_level = peewee.IntegerField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = Database.database()
        primary_key = peewee.CompositeKey('user', 'device')
