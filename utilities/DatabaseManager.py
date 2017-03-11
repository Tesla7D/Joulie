import datetime
from models import Users, User_Groups
from peewee import DoesNotExist

class DatabaseManager(object):
    def __init__(self):
        i = 0

    def AddUser(self, user_id, cylon_url, uuid):
        user = Users(group_id=2, user_id=user_id, cylon_url=cylon_url, uuid=uuid)
        user.save()

        return True

    def GetUser(self, id = None, uuid = None, user_id = None):
        try:
            if id:
                return Users.get(id == id)
            if uuid:
                return Users.get(Users.uuid == uuid)
            if user_id:
                return Users.get(Users.user_id == user_id)
        except DoesNotExist:
            return None

        raise AttributeError("No parameters specified. Nothing was done")

    def DeleteUser(self, id = None, uuid = None, user_id = None):
        user = self.GetUser(id=id, uuid=uuid, user_id=user_id)
        user.delete_instance()

        return True

    def UpdateUser(self, id, user_id = None, cylon_url = None, uuid = None, last_activity_date = None, group_id = None):
        user = self.GetUser(id=id)

        if user_id:
            user.user_id = user_id
        if cylon_url:
            user.cylon_url = cylon_url
        if uuid:
            user.uuid = uuid
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
