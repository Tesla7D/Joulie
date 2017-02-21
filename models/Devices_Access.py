import peewee
import datetime
import Database


class Devices_Access(peewee.Model):
    user_id = peewee.IntegerField()
    device_id = peewee.IntegerField()
    access_level = peewee.IntegerField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = Database.database()
