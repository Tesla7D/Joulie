import datetime
from models import Users, User_Groups

class DatabaseManager(object):
    def __init__(self):
        i = 0

    def AddUser(self, email, nickname, uuid):
        user = Users(group_id=2, email=email, nickname=nickname, last_activity_date=datetime.datetime.utcnow())
        user.save()

        return True

    def GetUser(self, id = None, uuid = None, nickname = None):
        if id:
            return Users.get(id == id)
        if uuid:
            return Users.get(id == uuid)
        if nickname:
            return Users.get(Users.nickname == nickname)

        raise AttributeError("No parameters specified. Nothing was done")

    def DeleteUser(self, id = None, uuid = None):
        user = self.GetUser(id=id, uuid=uuid)
        user.delete_instance()

        return True

    def UpdateUser(self, id, email = None, nickname = None, uuid = None, last_activity_date = None, group_id = None):
        user = self.GetUser(id=id)

        if email:
            user.email = email
        if nickname:
            user.nickname = nickname
        if last_activity_date:
            user.last_activity_date = last_activity_date
        if group_id:
            user.group_id = group_id

        user.save()
        return True

    def CreateUser(self):
        user = Users(group_id=2, email="test", nickname="nick ick", last_activity_date=datetime.datetime.utcnow())
        user.save()



    def AddUserGroup(self):
        group = User_Groups(group_name="peewee")
        group.save()

    def AddDevice(self):
        return ""
