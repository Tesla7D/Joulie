import peewee
import datetime
import Database

DEFAULT_DEVICE = 42


class Devices(peewee.Model):
    type_id = peewee.IntegerField()
    device_name = peewee.CharField()
    owner_id = peewee.IntegerField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    last_activity_date = peewee.DateTimeField()

    class Meta:
        database = Database.database()
