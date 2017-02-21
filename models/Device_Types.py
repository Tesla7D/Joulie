import peewee
import Database

DEFAULT_DEVICE_TYPE = 2


class Device_Types(peewee.Model):
    type_name = peewee.CharField()

    class Meta:
        database = Database.database()
