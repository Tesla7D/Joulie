import datetime
from models import Users, User_Groups

class DatabaseManager(object):
    def __init__(self):
        i = 0

    def CreateUser(self):
        user = Users.Users(group_id=2, email="test", nickname="nick ick", last_activity_date=datetime.datetime.utcnow())
        user.save()

    def GetUser(self):
        result = ""

        for user in Users.Users:
            result += user.nickname

        return result

    def AddUserGroup(self):
        group = User_Groups.User_Groups(group_name="peewee")
        group.save()

    def AddDevice(self):
        return ""
