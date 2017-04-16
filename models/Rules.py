import peewee
import datetime
from Database import DatabaseModel

DEFAULT_TYPE = 2


class Rules(DatabaseModel):
    type_id = peewee.IntegerField()
    device_id = peewee.IntegerField()
    owner_id = peewee.IntegerField()
    state = peewee.IntegerField()
    run_time = peewee.IntegerField()
    run_repeat = peewee.IntegerField()
    creation_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    modify_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
    sync_date = peewee.DateTimeField(default=datetime.datetime.utcnow)
