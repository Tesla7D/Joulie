import requests


#
# Manager that can handle HTTP connections
#
class HttpManager(object):

    @staticmethod
    def Post(url, data=None, json=None, headers=None):
        print "Doing POST to [{}]".format(url)

        if json != None:
            if headers != None:
                return requests.post(url, json=json, headers=headers)

            return requests.post(url, json=json)

        if headers != None:
            return requests.post(url, data=data, headers=headers)

        return requests.post(url, data=data)

    @staticmethod
    def Get(url, data=None, json=None, headers=None):
        print "Doing GET to [{}]".format(url)

        if json != None:
            if headers != None:
                return requests.get(url, json=json, headers=headers)

            return requests.get(url, json=json)

        if headers != None:
            return requests.get(url, data=data, headers=headers)

        return requests.get(url, data=data)


#
# Manager that performs actions on Cylon side
#
class CylonManager(HttpManager):

    cylon_url = "https://joulie-cylon.herokuapp.com"
    cylon_robot = "api/robots/{}"
    cylon_device = "devices/{}"
    cylon_commands = "commands/{}"
    cylon_create_device = "commands/create_device"
    cylon_remove_device = "commands/remove_device"
    cylon_add_robot = "api/commands/create_robot"
    cylon_remove_robot = "api/commands/remove_robot"

    def __init__(self):
         i = 0

    def AddDevice(self, robot, data, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_create_device

        return HttpManager.Post(url, data=data)

    def GetDevice(self, robot, name, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_device.format(name)

        return HttpManager.Get(url)

    def RemoveDevice(self, robot, name, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_remove_device
        data = {'opts': {'name': name}}

        return HttpManager.Post(url, json=data)

    def AddNestDevice(self, robot, name, token, json=None):
        url = self.cylon_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_create_device

        if json != None:
            data = json
        else:
            data = {'opts': {'device_name': name,
                             'conn_name': 'nest',
                             'connection': 'nest',
                             'adaptor': 'nest',
                             'accessToken': token,
                             'driver': 'nest-thermostat',
                             'deviceId': 'sPmk4pq4eGMa7nT5eiYy5G66DVALDY-J'
                             }}

        return HttpManager.Post(url, json=data)

    def RemoveNestDevice(self, robot, name, token):
        url = self.cylon_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_remove_device
        data = {'opts': {'name': name,
                         'deviceId': 'sPmk4pq4eGMa7nT5eiYy5G66DVALDY-J'
                         }}

        return HttpManager.Post(url, json=data)

    def GetRobot(self, name, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + self.cylon_robot.format(name)

        return HttpManager.Get(url)

    def AddRobot(self, name, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + self.cylon_add_robot

        data = {'opts': {'name': name}}
        return HttpManager.Post(url, json=data)

    def RemoveRobot(self, name, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + self.cylon_remove_robot

        data = {'opts': {'name': name}}
        return HttpManager.Post(url, json=data)

    def RunCommand(self, robot, device, command, data, c_url="https://joulie-cylon.herokuapp.com"):
        url = c_url + "/" + \
              self.cylon_robot.format(robot) + "/" + \
              self.cylon_device.format(device) + "/" + \
              self.cylon_commands.format(command)

        return HttpManager.Post(url, json=data)
