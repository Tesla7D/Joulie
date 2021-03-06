from models import Users, Devices, Rules, Energy_Logs, Devices_Access
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

    def GetUsers(self):
        users = Users.select()

        return users

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

    def AddDevice(self, owner_id, display_name, uuid, creation_data, type_id=2):
        device = Devices(type_id=type_id, owner_id=owner_id, display_name=display_name, uuid=uuid, creation_data=creation_data)
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

    def GetDevices(self, owner_id=None):
        if owner_id:
            return Devices.select().where(Devices.owner_id == owner_id)

        return Devices.select()


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

    #
    # RULES
    #

    def GetRule(self, id=None, uuid=None):
        try:
            if id:
                return Rules.get(Rules.id == id)
            if uuid:
                return Rules.get(Rules.uuid == uuid)
        except DoesNotExist:
            return None

        raise AttributeError("No parameters specified. Nothing was done")

    def GetRules(self, owner_id=None, device_id=None):
        if owner_id:
            try:
                return Rules.select().where(Rules.owner_id == owner_id)
            except DoesNotExist:
                return None
        elif device_id:
            try:
                return Rules.select().where(Rules.device_id == device_id)
            except DoesNotExist:
                return None
        else:
            return Rules.select()

    def AddRule(self, run_time, run_repeat, state, owner_id, device_id, uuid):
        rule = Rules(type_id=2, device_id=device_id, owner_id=owner_id, state=state, run_time=run_time, run_repeat=run_repeat, uuid=uuid)
        rule.save()

        return True

    def DeleteRule(self, id=None, uuid=None):
        rule = self.GetRule(id, uuid)
        if rule:
            rule.delete_instance()

        return True
    #
    # ENERGY LOGS
    #

    def AddEnergyLog(self, device_id, value, metadata=None):
        energyLog = Energy_Logs(type_id=2, device_id=device_id, energy_value=value, metadata=metadata)
        energyLog.save()

        return True

    def GetEnergyLogs(self, device_id):
        return Energy_Logs.select().where(Energy_Logs.device_id == device_id)

    #
    # DEVICE ACCESS
    #

    def GetDeviceAccess(self, device, user):
        try:
            return Devices_Access.get((Devices_Access.user == user) & (Devices_Access.device == device))
        except DoesNotExist:
            return None

    def GetSharedDevices(self, user):
        try:
            return Devices_Access.select().where(Devices_Access.user == user)
        except DoesNotExist:
            return None

    def AddDeviceAccess(self, device, user, level=2):
        if self.GetDeviceAccess(device, user):
            return False

        deviceAccess = Devices_Access(device=device, user=user, access_level=level)
        result = deviceAccess.save(force_insert=True)

        return result == 1

    def DeleteDeviceAccess(self, device, user):
        deviceAccess = self.GetDeviceAccess(device, user)
        if not deviceAccess:
            return False

        deviceAccess.delete_instance()
        return True
