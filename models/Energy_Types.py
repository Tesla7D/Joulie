import peewee
import Database

DEFAULT_ENERGY_TYPE = 2


class Energy_Types(peewee.Model):
    type_name = peewee.CharField()

    class Meta:
        database = Database.database()
