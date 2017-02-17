import os
import socketio
import eventlet.wsgi
import requests
import json
import threading
from flask import Flask, render_template, request

from utilities import DatabaseManager

cylon_url = "https://joulie-cylon.herokuapp.com"
cylon_create_device = "api/robots/{}/commands/create_device"
cylon_remove_device = "api/robots/{}/commands/remove_device"
cylon_add_robot = "api/commands/create_robot"
cylon_remove_robot = "api/commands/remove_robot"

sio = socketio.Server()
app = Flask(__name__)

def cylon_check():
  threading.Timer(300, cylon_check).start()
  print "Calling Cylon..."
  response = requests.get(cylon_url)

cylon_check()

# db = DatabaseManager.DatabaseManager()
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

@app.route('/device', methods=['POST'])
def addDevice():
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_create_device.format("kyle")
    response = requests.post(url, data=data)

    return "device added"

@app.route('/device_test', methods=['POST'])
def addDeviceT():
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_create_device.format("kyle")

    response = requests.post(url, data=data)
    return response.text

@app.route('/device_test/<string:name>', methods=['POST'])
def addDeviceTParam(name):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_create_device.format(str(name))

    response = requests.post(url, json=data)
    return response.text

@app.route('/robot_test/<string:name>', methods=['POST'])
def addRobotT(name):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_add_robot

    response = requests.post(url, json=data)
    return response.text

@app.route('/robot_test/<string:name>', methods=['DELETE'])
def removeRobotT(name):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_remove_robot

    response = requests.post(url, json=data)
    return response.text

@app.route('/device/<uuid:device_id>', methods=['DELETE'])
def removeDevice(device_id):
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_remove_device.format("kyle")
    response = requests.post(url, json=data)

    return "device %" + str(device_id) + "% removed"

@app.route('/device_test', methods=['DELETE'])
def removeDeviceT():
    data = request.get_json(force=True)
    url = cylon_url + "/" + cylon_remove_device.format("kyle")

    response = requests.post(url, json=data)
    return response.text

@app.route('/user', methods=['POST'])
def addUser():
    return "logged in"

@app.route('/user/<uuid:user_id>', methods=['DELETE'])
def removeUser(user_id):
    return "user %" + str(user_id) + "% removed"

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