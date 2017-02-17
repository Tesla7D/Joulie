import datetime
from models import User

class DatabaseManager(object):
    def __init__(self):
        i = 0

    def CreateUser(self):
        user = User.Users(group_id=2, email="test", nickname="nick ick", last_activity_date=datetime.datetime.utcnow())
        user.save()

    def GetUser(self):
        result = ""

        for user in User.Users:
            result += user.nickname

        return result

    def AddDevice(self):
        return ""
