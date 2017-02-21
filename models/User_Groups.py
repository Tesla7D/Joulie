import peewee
import Database

DEFAULT_USER_GROUP = 2


class User_Groups(peewee.Model):
    group_name = peewee.CharField()

    class Meta:
        database = Database.database()
