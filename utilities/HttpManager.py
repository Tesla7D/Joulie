import requests


#
# Manager that can handle HTTP connections
#
class HttpManager(object):

    def Post(self, url, data=None, json=None, headers=None):
        if json != None:
            if headers != None:
                return requests.post(url, json=json, headers=headers)

            return requests.post(url, json=json)

        if headers != None:
            return requests.post(url, data=data, headers=headers)

        return requests.post(url, data=data)

    def Get(self, url, data=None, json=None, headers=None):
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
    cylon_create_device = "api/robots/{}/commands/create_device"
    cylon_remove_device = "api/robots/{}/commands/remove_device"
    cylon_add_robot = "api/commands/create_robot"
    cylon_remove_robot = "api/commands/remove_robot"

    def __init__(self):
         i = 0

    def AddDevice(self, name, data=None, json=None, headers=None):
        url = self.cylon_url + "/" + self.cylon_create_device.format(name)

        return super(CylonManager, self).Post(url, data, json, headers)

    def RemoveDevice(self, name, data):
        url = self.cylon_url + "/" + self.cylon_remove_device.format(name)

        return requests.post(url, data=data)

    def AddRobot(self, data):
        url = self.cylon_url + "/" + self.cylon_add_robot

        return requests.post(url, data=data)

    def RemoveRobot(self, data):
        url = self.cylon_url + "/" + self.cylon_remove_robot

        return requests.post(url, data=data)
