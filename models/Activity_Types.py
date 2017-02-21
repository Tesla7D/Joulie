import peewee
import Database

DEFAULT_ACTIVITY_TYPE = 2


class Activity_Types(peewee.Model):
    type_name = peewee.CharField()

    class Meta:
        database = Database.database()
