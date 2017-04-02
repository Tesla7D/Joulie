import os
import ngrok
import socketio
import eventlet.wsgi
import json
import threading
import uuid

from models.Database import database
from utilities.HttpManager import *
from utilities.DatabaseManager import *
from utilities.AuthO import handle_error, requires_auth, GetUserId, GetUserInfo
from utilities.Package import is_local
from flask import Flask, render_template, request, abort
from flask_cors import cross_origin

cylon_url = "https://joulie-cylon.herokuapp.com"
cylon_create_device = "api/robots/{}/commands/create_device"
cylon_remove_device = "api/robots/{}/commands/remove_device"
cylon_add_robot = "api/commands/create_robot"
cylon_remove_robot = "api/commands/remove_robot"
cylon_command = "api/robots/{}/devices/{}/commands/{}"

sio = socketio.Server()
app = Flask(__name__)
cylon = CylonManager()
db = DatabaseManager()
database = database()


def rules_check():
    threading.Timer(300, rules_check).start()


def cylon_check():
    threading.Timer(300, cylon_check).start()
    print "Calling Cylon..."
    response = requests.get(cylon_url)

# No need to run cylon check anymore
# cylon_check()

# db = DatabaseManager.DatabaseManager()
# db.AddUserGroup()
# db.CreateUser()
# print(db.GetUser())

# Heroku support: bind to PORT if defined, otherwise default to 5000.
if 'PORT' in os.environ:
    port = int(os.environ.get('PORT'))
    # use '0.0.0.0' to ensure your REST API is reachable from all your
    # network (and not only your computer).
    host = '0.0.0.0'
else:
    port = 8000
    host = '127.0.0.1'

#
# REST endpoints
#

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response

@app.route('/')
def index():
    # Serve the client-side application
    # return render_template('index.html')

    return handle_error('test', int('200'))

    #return 'true'


def currentNgrok():
    try:
        tunnels = ngrok.client.get_tunnels()

        for tunnel in tunnels:
            if str.startswith(str(tunnel.public_url), "https"):
                return str(tunnel.public_url)

        return None
    except Exception, e:
        print ("Got exception: " + str(e))
        return None

@app.route('/ngrok', methods=['GET'])
def getNgrok():
    ngrok = currentNgrok()
    if not ngrok:
        abort(503)

    return ngrok


@app.route('/data', methods=['GET'])
def getData():
    data = {
            "point1": {"timestamp": "201702121140", "value": "50"}
            , "point2": {"timestamp": "201702121150", "value": "20"}
            , "point3": {"timestamp": "201702121200", "value": "30"}
            , "point4": {"timestamp": "201702121210", "value": "40"}
            , "point5": {"timestamp": "201702121220", "value": "75"}
            }

    return json.dumps(data)


#
# User
#
@app.route('/user', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def getCurrentUser():
    print "Getting current user info"
    head = request.headers

    user_info = GetUserInfo(head)
    user_id = GetUserId(head, user_info)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(505)

    data = {'url': user.cylon_url}

    return json.dumps(data)

@app.route('/user/<string:user_id>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def getUser(user_id):
    return None

@app.route('/finduser/<string:email>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def findUser(email):
    return None

@app.route('/newuser', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def newUser():
    print "Running newUser"
    data = request.get_json()
    head = request.headers

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)

    url = None
    if (data and
        'url' in data and
        data['url']):
        url = data['url']
    guid = str(uuid.uuid4())

    if user:
        if not user.uuid:
            user.uuid = guid
            cylon.AddRobot(guid, c_url=url)
        if (not user.cylon_url and
            url):
            user.cylon_url = url

        user.save()
        return "User Updated"

    db.AddUser(user_id, url, guid)
    cylon.AddRobot(guid, c_url=url)
    return "User Added"

@app.route('/updateuser', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def updateUser():
    print "Running updateuser"
    data = request.get_json()
    head = request.headers

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)

    url = None
    guid = None
    if data:
        if ('url' in data and
            data['url']):

            url = data['url']
        if ('uuid' in data and
            data['uuid']):

            guid = data['uuid']

    if user:
        if guid:
            user.uuid = guid
            cylon.AddRobot(guid, c_url=url)
        if url:
            user.cylon_url = url

        user.save()
        return "User Updated"

    db.AddUser(user_id, url, guid)
    cylon.AddRobot(guid, c_url=url)
    return "User Added"


@app.route('/syncuser/<string:user_id>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def syncUser(user_id):
    print "Syncing user data"

    if is_local():
        abort(503)

    user = db.GetUser(user_id=user_id)
    if not user:
        abort(503)

    url = user.cylon_url + "/db/user/{}".format(user.user_id)
    data = {'uuid': user.uuid}
    HttpManager.Post(url, json=data)

    devices = db.GetDevices(user.id)
    for device in devices:
        url = user.cylon_url + "/db/device/{}".format(device.uuid)
        data = {'display_name': device.display_name,
                'auth_id': user_id,
                'creation_data': device.creation_data}
        HttpManager.Post(url, json=data)

    return 'Done'

@app.route('/db/user/<string:user_id>', methods=['POST'])
def dbUser(user_id):
    print "Running DB user"

    if not is_local():
        abort(503)

    data = request.get_json()
    guid = None
    if data:
        if ('uuid' in data and
            data['uuid']):

            guid = data['uuid']

    user = db.GetUser(user_id=user_id)
    if not user:
        db.AddUser(user_id, 'localhost', guid)
        return 'Added new user'

    if guid:
        user.uuid = guid

    user.save()
    return 'User updated'

#
# Device
#


@app.route('/db/device/<string:guid>', methods=['POST'])
def dbDevice(guid):
    print "Running DB device"

    if not is_local():
        abort(503)

    data = request.get_json()
    display_name = None
    owner = None
    creation_data = None
    if data:
        if ('display_name' in data and
            data['display_name']):

            display_name = data['display_name']

        if ('auth_id' in data and
            data['auth_id']):

            auth_id = data['auth_id']
            owner = db.GetUser(user_id=auth_id)

        if ('creation_data' in data and
            data['creation_data']):

            creation_data = data['creation_data']

    device = db.GetDevice(uuid=guid)
    if not device:
        if not owner:
            return 'Cannot add device: no owner'

        if not creation_data:
            return 'Cannot add device: no creation data'

        db.AddDevice(owner.id, display_name, guid, creation_data)
        return 'Added new device'

    if display_name:
        device.display_name = display_name
    if owner:
        device.owner_id = owner.id
    if creation_data:
        device.creation_data = creation_data

    device.save()
    return 'Device updated'


#
# Get info about device with specified uuid
#
@app.route('/device/<string:name>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def getDevice(name):
    print "Getting device"

    device = db.GetDevice(uuid=name)
    if not device:
        return None

    user = db.GetUser(id=device.owner_id)
    owner_user_id = user.user_id if user else ""

    data = {'display_name': device.display_name,
            'uuid': device.uuid,
            'owner_user_id': owner_user_id,
            'type': device.type_id,
            'creation_date': str(device.creation_date),
            'last_activity_date': str(device.last_activity_date)}
    return json.dumps(data)


#
# Gets information about all devices for current user
#
@app.route('/devices', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def getDevices():
    print "Getting multiple devices"
    head = request.headers

    user_info = GetUserInfo(head)
    user_id = GetUserId(head, user=user_info)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(505)

    devices = db.GetDevices(user.id)
    data = []
    counter = 0

    for device in devices:
        device_data = {'display_name': device.display_name,
                       'uuid': device.uuid,
                       'type': device.type_id,
                       'owned': 1,
                       'creation_date': str(device.creation_date),
                       'last_activity_date': str(device.last_activity_date)}
        data.append(device_data)
        counter += 1

    return json.dumps(data)

@app.route('/user/current/devices/reset', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def resetDevices():
    print "Resetting all devices"

    users = db.GetUser()
    for user in users:
        c_url = user.cylon_url
        robot = user.uuid
        if not c_url or not robot:
            continue

        devices = db.GetDevices(user.id)
        for device in devices:
            data = device.creation_data
            if not data:
                continue

            result = cylon.AddDevice(robot, data, c_url=c_url)
            if result.status_code != 200:
                print "Got error: " + result.text

    return "Done"

#
# Resets all devices for selected user
#


@app.route('/robot/<string:robot>/devices/reset', methods=['POST'])
@requires_auth
def resetUserDevicesLocal(robot):
    print "Resetting user devices"
    if not is_local():
        abort(503)

    data = request.get_json(force=True)
    result = cylon.AddDevice(robot, data)
    if result.status_code != 200:
        print "Got error: " + result.text

    return "Done"


@app.route('/user/<string:user_id>/devices/reset', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def resetUserDevices(user_id):
    print "Resetting user devices"
    if not is_local():
        user = db.GetUser(user_id=user_id)
        if not user:
            abort(500)

        c_url = user.cylon_url
        robot = user.uuid
        if not c_url or not robot:
            abort(500)

        url = c_url + "/devices/reset/" + robot
        devices = db.GetDevices(user_id)
        for device in devices:
            data = device.creation_data
            if not data:
                continue

            result = HttpManager.Post(url, json=data)
            if result.status_code != 200:
                print "Got error: " + result.text
    else:
        data = request.get_json(force=True)
        result = cylon.AddDevice(user_id, data)
        if result.status_code != 200:
            print "Got error: " + result.text

    return "Done"


@app.route('/robot/<string:robot>/device', methods=['POST'])
@requires_auth
def addDevice(robot, user=None, data=None):
    print "Running addDevice"
    if not data:
        data = request.get_json()

    # code for remote version
    if not is_local():
        if not user:
            head = request.headers

            user_id = GetUserId(head)
            user = db.GetUser(user_id=user_id)

        c_url = user.cylon_url
        if not c_url:
            abort(500)

        url = c_url + "/robot/{}/device".format(robot)
        response = HttpManager.Post(url, json=data)
        print "Got response from server-core. \nCode: {}\nMessage: {}".format(response.status_code, response.text)
        if response.status_code != 200:
            print "Got {} back instead of 200".format(response.status_code)
            abort(503)

        return response.text

    # code for local version
    guid = uuid.uuid4()
    data['name'] = guid
    response = cylon.AddDevice(robot, data)
    if not response:
        # no connection
        abort(404)

    print "Got response from cylon. \nCode: {}\nMessage: {}".format(response.status_code, response.text)
    if response.status_code != 200:
        print "Got {} back instead of 200".format(response.status_code)
        abort(503)

    return response.text


@app.route('/device', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def addUserDevice():
    print "Running user addDevice"
    if is_local():
        abort(503)

    data = request.get_json()
    head = request.headers

    display_name = data['display_name'] if 'display_name' in data else None
    if not display_name:
        print "No display name"
        abort(500)

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)
    if not user:
        print "No user found"
        abort(500)

    robot = user.uuid
    response = addDevice(robot, user, data)
    print "Got response from addDevice.\nMessage: {}".format(response)

    payload = response
    success = payload['success'] if 'success' in payload else None
    if success != "true":
        print "Success = {}".format(success)
        abort(500)

    result = payload['result'] if 'result' in payload else None
    name = result['name'] if (result and 'name' in result) else None
    if not name:
        abort(503)

    print "Adding device to db"
    db.AddDevice(user.id, display_name, name, str(data))

    return response

@app.route('/device/<string:device>', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def removeDevice(device):
    print "Running removeDevice"
    head = request.headers

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(500)

    c_url = user.cylon_url
    robot = user.uuid

    return cylon.RemoveDevice(robot, device, c_url=c_url)


#
# Robot
#
@app.route('/robots/reset', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def resetUserRobots():
    print "Resetting all robots"
    if is_local():
        abort(503)

    users = db.GetUsers()
    for user in users:
        result = resetUserRobot(None, user)

    return "Done"


@app.route('/robots/reset/<string:user_id>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def resetUserRobot(user_id, user=None):
    print "Resetting robot"

    if is_local():
        return 'false'

    # code for remote version
    if not user:
        user = db.GetUser(user_id=user_id)

    if not user:
        return 'false'

    c_url = user.cylon_url
    robot = user.uuid
    if not c_url or not robot:
        return 'false'

    return resetRobot(robot)


@app.route('/robot/<string:robot>/reset', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def resetRobot(robot):
    print "Resetting robot"

    # code for local version
    if is_local():
        print "Checking local robot"
        result = cylon.GetRobot(robot)
        if (result and
            result.status_code == 200):
            return "Already exists"

        print "Checked robot and got {} back".format(result.status_code)
        result = cylon.AddRobot(robot)
        if result.status_code != 200:
            print "Got error: " + result.text
            abort(result.status_code)

        return result.text

    # code for remote version
    user = db.GetUser(uuid=robot)
    if not user:
        abort(500)

    c_url = user.cylon_url
    if not c_url:
        abort(500)

    url = c_url + "/robot/{}/reset".format(robot)
    result = HttpManager.Post(url)
    return result.text


@app.route('/robot/<string:name>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def addRobot(name):
    print "Running addRobot"
    head = request.headers

    user_id = GetUserId(head)
    c_url = db.GetUser(user_id=user_id).cylon_url

    return cylon.AddRobot(name, c_url=c_url)

@app.route('/robot/<string:name>', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def removeRobot(name):
    print "Running removeRobot"
    head = request.headers

    user_id = GetUserId(head)
    c_url = db.GetUser(user_id=user_id).cylon_url

    return cylon.RemoveRobot(name, c_url=c_url)


#
# Run Command
#
@app.route('/robot/<string:robot>/device/<string:device>/<string:command>', methods=['POST'])
@requires_auth
def deviceCommandLocal(robot, device, command, user=None, data=None):
    print "Running deviceCommand"
    if not data:
        data = request.get_json()

    if not is_local():
        if not user:
            device_info = db.GetDevice(uuid=device)
            if not device_info:
                abort(503)

            owner_id = device_info.owner_id
            user = db.GetUser(id=owner_id)

        if not user:
            abort(500)

        c_url = user.cylon_url
        url = c_url + "/robot/{}/device/{}/{}".format(robot, device, command)
        result = HttpManager.Post(url, json=data)
        return handle_error(result.text, result.status_code)

    result = cylon.RunCommand(robot, device, command, data)
    if not result:
        abort(404)

    return handle_error(result.text, result.status_code)


@app.route('/device/<string:device>/<string:command>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deviceCommand(device, command):
    print "Running deviceCommand"
    data = request.get_json()

    if is_local():
        abort(503)

    # device_info = db.GetDevice(uuid=device)
    # if not device_info:
    #     abort(503)
    #
    # owner_id = device_info.owner_id
    # user = db.GetUser(id=owner_id)
    # if not user:
    #     abort(500)

    head = request.headers
    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(500)

    robot = user.uuid

    result = deviceCommandLocal(robot, device, command, user, data)
    return handle_error(result.data, result.status_code)


#
# Socket.io endpoints
#

@sio.on('connect', namespace='/chat')
@sio.on('connect', namespace='/api')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('disconnect', namespace='/chat')
@sio.on('disconnect', namespace='/api')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit('chat message', data, namespace='/chat')

@sio.on('data publish', namespace='/api')
def on_data(sid, data):
    print('got data ', data, " from ", sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', port)), app)
