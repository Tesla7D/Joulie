import peewee
import Database
import datetime


class Energy_Logs(peewee.Model):
    type_id = peewee.IntegerField()
    device_id = peewee.IntegerField()
    energy_value = peewee.FloatField()
    metadata = peewee.CharField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        database = Database.database()
