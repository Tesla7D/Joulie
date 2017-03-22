import os
import socketio
import eventlet.wsgi
import json
import threading
import uuid
from models.Database import *
from utilities.HttpManager import *
from utilities.DatabaseManager import *
from utilities.AuthO import requires_auth, GetUserId, GetUserInfo
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


def cylon_check():
  threading.Timer(300, cylon_check).start()
  print "Calling Cylon..."
  response = requests.get(cylon_url)

cylon_check()

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
    """Serve the client-side application."""
    return render_template('index.html')

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
    data = request.get_json()
    head = request.headers

    user_info = GetUserInfo(head)

    return user_info.text

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

    url = cylon_url
    if (data and
        'url' in data and
        data['url']):
        url = data['url']
    guid = str(uuid.uuid4())
    if user:
        if not user.uuid:
            user.uuid = guid
            cylon.AddRobot(guid, c_url=url)
        if not user.cylon_url:
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


#
# Device
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

    data = db.GetDevices(user.id)
    return json.dumps(data)

@app.route('/device', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def addDevice(robot):
    print "Running addDevice"
    data = request.get_json(force=True)
    head = request.headers

    display_name = data['display_name'] if data['display_name'] else None
    if not display_name:
        abort(500)

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(500)

    c_url = user.cylon_url
    robot = user.uuid
    guid = uuid.uuid4()
    data['name'] = guid

    response = cylon.AddDevice(robot, data, c_url=c_url)
    #url = c_url + "/" + cylon_create_device.format(str(robot))
    #response = requests.post(url, data=data)

    if response.status_code == 200:
       db.AddDevice(user_id, display_name, guid, str(data))

    return response.text

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

@app.route('/robot_test/<string:robot>/device', methods=['POST'])
def addDevice_test(robot):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_create_device.format(str(robot))

    response = requests.post(url, data=data)
    return response.text

@app.route('/robot_test/<string:robot>/device/<string:device>', methods=['DELETE'])
def removeDevice_test(robot, device):
    return cylon.RemoveDevice(robot, device)


#
# Robot
#
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

@app.route('/robot_test/<string:name>', methods=['POST'])
def addRobot_test(name):
    return cylon.AddRobot(name)

@app.route('/robot_test/<string:name>', methods=['DELETE'])
def removeRobot_test(name):
    return cylon.RemoveRobot(name)


#
# Run Command
#
@app.route('/device/<string:device>/<string:command>', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def deviceCommand(device, command):
    print "Running deviceCommand"
    data = request.get_json()
    head = request.headers

    user_id = GetUserId(head)
    user = db.GetUser(user_id=user_id)
    if not user:
        abort(500)

    c_url = user.cylon_url
    robot = user.uuid

    result = cylon.RunCommand(robot, device, command, data, c_url=c_url)
    return result.text

@app.route('/robot_test/<string:robot>/device/<string:device>/<string:command>', methods=['POST'])
def deviceCommand_test(robot, device, command):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_command.format(str(robot), str(device), str(command))

    response = requests.post(url, json=data)
    return response.text


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