import peewee
import Database

DEFAULT_ACCESS_LEVEL = 2
BASIC_ACCESS_LEVEL = 32


class Access_Levels(peewee.Model):
    level_name = peewee.CharField()

    class Meta:
        database = Database.database()
