import peewee
import Database
import datetime


class Activity_Logs(peewee.Model):
    type_id = peewee.IntegerField()
    user_id = peewee.IntegerField()
    device_id = peewee.IntegerField()
    metadata = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = Database.database()
