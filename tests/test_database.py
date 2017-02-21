import uuid
import datetime
import random
from models import *
from peewee import DoesNotExist


#
#   Testing User_Groups model
#
def test_userGroups():
    name = str(uuid.uuid4())
    userGroup = User_Groups(group_name=name)

    # Make sure that we can save the group
    result = userGroup.save()
    assert result == 1

    # Make sure that we can get the data back
    result = User_Groups.get(User_Groups.id == userGroup.id)
    assert userGroup.__eq__(result)

    # Updating the model and trying to get it back
    userGroup = result
    new_name = str(uuid.uuid4())
    userGroup.group_name = new_name
    userGroup.save()
    result = User_Groups.get(User_Groups.id == userGroup.id)
    assert userGroup.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on trying to get the record back
    try:
        result = User_Groups.get(User_Groups.id == userGroup.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Users model
#
def test_users():
    email = str(uuid.uuid4())
    nickname = str(uuid.uuid4())
    user = Users(group_id=DEFAULT_USER_GROUP, email=email, nickname=nickname, last_activity_date=datetime.datetime.utcnow())

    # Make sure that we can save the group
    result = user.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Users.get(Users.id == user.id)
    assert user.__eq__(result)

    # Updating the model and trying to get it back
    user = result
    new_email = str(uuid.uuid4())
    new_nickname = str(uuid.uuid4())
    user.email = new_email
    user.nickname = new_nickname
    user.last_activity_date = datetime.datetime.utcnow()
    user.save()
    result = Users.get(Users.id == user.id)
    assert user.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on getting the record back
    try:
        result = Users.get(Users.id == user.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Device_Types model
#
def test_deviceTypes():
    name = str(uuid.uuid4())
    deviceType = Device_Types(type_name=name)

    # Make sure that we can save the group
    result = deviceType.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Device_Types.get(Device_Types.id == deviceType.id)
    assert deviceType.__eq__(result)

    # Updating the model and trying to get it back
    deviceType = result
    new_name = str(uuid.uuid4())
    deviceType.type_name = new_name
    deviceType.save()
    result = Device_Types.get(Device_Types.id == deviceType.id)
    assert deviceType.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on trying to get the record back
    try:
        result = Device_Types.get(Device_Types.id == deviceType.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Device model
#
def test_devices():
    name = str(uuid.uuid4())
    device = Devices(type_id=DEFAULT_DEVICE_TYPE, device_name=name, owner_id=DEFAULT_USER, last_activity_date=datetime.datetime.utcnow())

    # Make sure that we can save the group
    result = device.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Devices.get(Devices.id == device.id)
    assert device.__eq__(result)

    # Updating the model and trying to get it back
    device = result
    new_name = str(uuid.uuid4())
    device.email = new_name
    device.last_activity_date = datetime.datetime.utcnow()
    device.save()
    result = Devices.get(Devices.id == device.id)
    assert device.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on getting the record back
    try:
        result = Devices.get(Devices.id == device.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Access_Levels model
#
def test_accessLevels():
    name = str(uuid.uuid4())
    accessLevel = Access_Levels(level_name=name)

    # Make sure that we can save the group
    result = accessLevel.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Access_Levels.get(Access_Levels.id == accessLevel.id)
    assert accessLevel.__eq__(result)

    # Updating the model and trying to get it back
    accessLevel = result
    new_name = str(uuid.uuid4())
    accessLevel.level_name = new_name
    accessLevel.save()
    result = Access_Levels.get(Access_Levels.id == accessLevel.id)
    assert accessLevel.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on trying to get the record back
    try:
        result = Access_Levels.get(Access_Levels.id == accessLevel.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Activity_Types model
#
def test_activityTypes():
    name = str(uuid.uuid4())
    activityType = Activity_Types(type_name=name)

    # Make sure that we can save the group
    result = activityType.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Activity_Types.get(Activity_Types.id == activityType.id)
    assert activityType.__eq__(result)

    # Updating the model and trying to get it back
    activityType = result
    new_name = str(uuid.uuid4())
    activityType.type_name = new_name
    activityType.save()
    result = Activity_Types.get(Activity_Types.id == activityType.id)
    assert activityType.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on trying to get the record back
    try:
        result = Activity_Types.get(Activity_Types.id == activityType.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Energy_Types model
#
def test_energyTypes():
    name = str(uuid.uuid4())
    energyType = Energy_Types(type_name=name)

    # Make sure that we can save the group
    result = energyType.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Energy_Types.get(Energy_Types.id == energyType.id)
    assert energyType.__eq__(result)

    # Updating the model and trying to get it back
    energyType = result
    new_name = str(uuid.uuid4())
    energyType.type_name = new_name
    energyType.save()
    result = Energy_Types.get(Energy_Types.id == energyType.id)
    assert energyType.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on trying to get the record back
    try:
        result = Energy_Types.get(Energy_Types.id == energyType.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Device_Access model
#
def test_deviceAccess():
    deviceAccess = Devices_Access(user_id=DEFAULT_USER, device_id=DEFAULT_DEVICE, access_level=DEFAULT_ACCESS_LEVEL)

    # Make sure that we can save the group
    result = deviceAccess.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Devices_Access.get(Devices_Access.id == deviceAccess.id)
    assert deviceAccess.__eq__(result)

    # Updating the model and trying to get it back
    deviceAccess = result
    deviceAccess.access_level = BASIC_ACCESS_LEVEL
    deviceAccess.save()
    result = Devices_Access.get(Devices_Access.id == deviceAccess.id)
    assert deviceAccess.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on getting the record back
    try:
        result = Devices_Access.get(Devices_Access.id == deviceAccess.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Activity_Logs model
#
def test_activityLogs():
    metadata = str(uuid.uuid4())
    activityLog = Activity_Logs(type_id=DEFAULT_ACTIVITY_TYPE, user_id=DEFAULT_USER, device_id=DEFAULT_DEVICE, metadata=metadata)

    # Make sure that we can save the group
    result = activityLog.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Activity_Logs.get(Activity_Logs.id == activityLog.id)
    assert activityLog.__eq__(result)

    # Updating the model and trying to get it back
    activityLog = result
    new_metadata = str(uuid.uuid4())
    activityLog.metadata = new_metadata
    activityLog.save()
    result = Activity_Logs.get(Activity_Logs.id == activityLog.id)
    assert activityLog.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on getting the record back
    try:
        result = Activity_Logs.get(Activity_Logs.id == activityLog.id)
        assert False
    except DoesNotExist:
        assert True


#
#   Testing Energy_Logs model
#
def test_activityLogs():
    metadata = str(uuid.uuid4())
    value = random.uniform(0.0, 100000.0)
    energyLog = Energy_Logs(type_id=DEFAULT_ACTIVITY_TYPE, device_id=DEFAULT_DEVICE, energy_value=value, metadata=metadata)

    # Make sure that we can save the group
    result = energyLog.save()
    assert result == 1

    # Make sure that we can get the data back
    result = Energy_Logs.get(Energy_Logs.id == energyLog.id)
    assert energyLog.__eq__(result)

    # Updating the model and trying to get it back
    energyLog = result
    new_metadata = str(uuid.uuid4())
    new_value = random.uniform(0.0, 100000.0)
    energyLog.metadata = new_metadata
    energyLog.value = new_value
    energyLog.save()
    result = Energy_Logs.get(Energy_Logs.id == energyLog.id)
    assert energyLog.__eq__(result)

    # Trying to delete record
    result = result.delete_instance()
    assert result == 1

    # Now we should fail on getting the record back
    try:
        result = Energy_Logs.get(Energy_Logs.id == energyLog.id)
        assert False
    except DoesNotExist:
        assert True
