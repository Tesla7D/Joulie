import uuid
from utilities.HttpManager import HttpManager, CylonManager

cylon_url = "https://joulie-cylon.herokuapp.com"
cylon = CylonManager()


#
# Testing post of the HttpManage
#
def test_post():

    result = HttpManager.Get(cylon_url)

    assert result.status_code == 200


#
# Testing Cylon robots
#
def test_robots():
    name = str(uuid.uuid4())

    result = cylon.GetRobot(name)
    assert result.status_code == 404

    result = cylon.AddRobot(name)
    assert result.status_code == 200

    result = cylon.GetRobot(name)
    assert result.status_code == 200

    result = cylon.RemoveRobot(name)
    assert result.status_code == 200

    result = cylon.GetRobot(name)
    assert result.status_code == 404