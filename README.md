# Joulie
Server Core

[![Build Status](https://travis-ci.org/Tesla7D/Joulie.svg?branch=master)](https://travis-ci.org/Tesla7D/Joulie)

## Endpoint usage
All endpoints require authentication.

You can use robot_test instead of robot if you want to ignore it. **Try not to use it**
### Robots
You can specify robot name as any string, but please try to use uuid
* Adding robot
  * Do POST to https://joulie-core.herokuapp.com/robot/ \<string:name\>
  * No json required, name will be used as a robot name
* Remove robot
  * Do DELETE to https://joulie-core.herokuapp.com/robot/ \<string:name\>
  * No json required, name will be used to find and delete robot

### Devices
* Get Device info
  * Do GET to https://joulie-core.herokuapp.com/device/ \<string:name\>
  * Use 'name' to specify device name
* Get all devices for current user
  * Do GET to https://joulie-core.herokuapp.com/devices
* Adding device
  * Do POST to https://joulie-core.herokuapp.com/device
  * Include a json that is required to add a device - it will be simply forwarder to cylon
* Remove device
  * Do DELETE to https://joulie-core.herokuapp.com/device \<uuid:device\>
  * No json required, device will be used to find and delete device

### Run command
* Run command
    * Do POST to https://joulie-core.herokuapp.com/device/ \<string:device\>/\<string:command\>
    * Device is used to construct a path to the device
    * Command is the command you would like to run on the device
    * Included json will be simply forwarder to cylon

### Users
* New user
  * Do POST to https://joulie-core.herokuapp.com/newuser
  * Authentication token is required here
  * I can include json to specify cylon_url: {"url": "http://localhost:8000"}
* Update user
  * Do POST to https://joulie-core.herokuapp.com/updateuser
  * Authentication token is required here
  * I can include json to specify cylon_url: {"url": "http://localhost:8000"}
* Get current user
  * Do GET to https://joulie-core.herokuapp.com/user
  * Authentication token is required here
  
