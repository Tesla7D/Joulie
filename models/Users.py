import peewee
import datetime
import Database

DEFAULT_USER = 2


class Users(peewee.Model):
    group_id = peewee.IntegerField()
    uuid = peewee.CharField()
    user_id = peewee.CharField()
    cylon_url = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    last_activity_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = Database.database()
