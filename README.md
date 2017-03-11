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
* Adding device
  * Do POST to https://joulie-core.herokuapp.com/robot/ \<uuid:robot\>/device
  * Robot is used to construct a path to specific robot
  * Include a json that is required to add a device - it will be simply forwarder to cylon
* Remove device
  * Do DELETE to https://joulie-core.herokuapp.com/robot/ \<uuid:robot\>/device\<uuid:device\>
  * Robot is used to construct a path to specific robot
  * No json required, device will be used to find and delete device

### Run command
* Run command
    * Do POST to https://joulie-core.herokuapp.com/robot/ \<string:robot\>/device/\<string:device\>/\<string:command\>
    * Robot and device are used to construct a path to the device
    * Command is the command you would like to run on the device
    * Included json will be simply forwarder to cylon

### Users
* New user
  * Do POST to https://joulie-core.herokuapp.com/newuser
  * Authentication token is required here
  * I can include json to specify cylon_url: {"url": "http://localhost:8000"}
  
