import uuid
from utilities.HttpManager import HttpManager, CylonManager

DEFAULT_ROBOT = "Test"
DEFAULT_TOKEN = "c.k9ESFrVN5RRMohA9drUlQRc5VINAUgdJUXKd1HK8aVveAWB6snK6wMvMN2zImZ8GlJIeqtcrxPofkUXePQdyWMqcnkPRYO5x6TYOEBgbVjiUnhBdczmh9TeEdCAfiR0pysSGkOwyjYKtn5gI"
CYLON_URL = "https://joulie-cylon.herokuapp.com"
cylon = CylonManager()


#
# Testing post of the HttpManage
#
# def test_get():
#     result = HttpManager.Get(CYLON_URL)
#
#     assert result.status_code == 200
#
#
# #
# # Testing Cylon robots
# #
# def test_robots():
#     name = str(uuid.uuid4())
#
#     result = cylon.GetRobot(name)
#     assert result.status_code == 404
#
#     result = cylon.AddRobot(name)
#     assert result.status_code == 200
#
#     result = cylon.GetRobot(name)
#     assert result.status_code == 200
#
#     result = cylon.RemoveRobot(name)
#     assert result.status_code == 200
#
#     result = cylon.GetRobot(name)
#     assert result.status_code == 404
#
#
# #
# # Testing Cylon nest devices
# #
# def test_nestDevices():
#     name = str(uuid.uuid4())
#
#     result = cylon.GetDevice(DEFAULT_ROBOT, name)
#     assert result.status_code == 404
#
#     result = cylon.AddNestDevice(DEFAULT_ROBOT, name, DEFAULT_TOKEN)
#     assert result.status_code == 200
#
#     result = cylon.GetDevice(DEFAULT_ROBOT, name)
#     assert result.status_code == 200
#
#     result = cylon.RemoveNestDevice(DEFAULT_ROBOT, name, DEFAULT_TOKEN)
#     assert result.status_code == 200
#     assert result.text.find("device removed") != -1
#
#     result = cylon.GetDevice(DEFAULT_ROBOT, name)
#     assert result.status_code == 404
