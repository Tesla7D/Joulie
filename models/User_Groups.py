import peewee
import Database


class User_Groups(peewee.Model):
    group_name = peewee.CharField()

    class Meta:
        database = Database.database()
