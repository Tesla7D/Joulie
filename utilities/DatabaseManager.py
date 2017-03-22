from models import Users, Devices
from peewee import DoesNotExist

class DatabaseManager(object):
    def __init__(self):
        i = 0

    #
    # USER
    #

    def AddUser(self, user_id, cylon_url, uuid):
        user = Users(group_id=2, user_id=user_id, cylon_url=cylon_url, uuid=uuid)
        user.save()

        return True

    def GetUser(self, id = None, uuid = None, user_id = None):
        try:
            if id:
                return Users.get(Users.id == id)
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

    #
    # DEVICES
    #

    def AddDevice(self, owner_id, display_name, uuid, creation_data):
        device = Devices(type_id=2, owner_id=owner_id, display_name=display_name, uuid=uuid, creation_data=creation_data)
        device.save()

        return True

    def GetDevice(self, id=None, uuid=None):
        try:
            if id:
                return Devices.get(Devices.id == id)
            if uuid:
                return Devices.get(Devices.uuid == uuid)
        except DoesNotExist:
            return None

        raise AttributeError("No parameters specified. Nothing was done")

    def GetDevices(self, owner_id):
        devices = Devices.select().where(Devices.owner_id == owner_id)
        data = []
        counter = 0

        for device in devices:
            device_data = {'display_name': device.display_name,
                           'uuid': device.uuid,
                           'owner_user_id': 0,
                           'type': device.type_id,
                           'creation_date': str(device.creation_date),
                           'last_activity_date': str(device.last_activity_date)}
            data.append(device_data)
            counter += 1

        return data


    def DeleteDevice(self, id = None, uuid = None):
        user = self.GetDevice(id=id, uuid=uuid)
        user.delete_instance()

        return True

    def UpdateDevice(self, id, type_id = None, owner_id=None, display_name=None, uuid=None, creation_data=None, last_activity_date = None):
        device = self.GetDevice(id=id)

        if type_id:
            device.type_id = type_id
        if owner_id:
            device.owner_id = owner_id
        if uuid:
            device.uuid = uuid
        if creation_data:
            device.creation_date = creation_data
        if last_activity_date:
            device.last_activity_date = last_activity_date
        if display_name:
            device.display_name = display_name

        device.save()
        return True
