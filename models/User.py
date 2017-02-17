import peewee
import datetime
import Database


class Users(peewee.Model):
    group_id = peewee.IntegerField()
    email = peewee.CharField()
    nickname = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    last_activity_date = peewee.DateTimeField()

    class Meta:
        database = Database.database()
