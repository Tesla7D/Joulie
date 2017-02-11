import os
import socketio
import eventlet.wsgi
import requests
from flask import Flask, render_template, request

from utilities import DatabaseManager

cylon_url = "https://joulie-cylon.herokuapp.com"
cylon_create_device = "api/robots/kyle/commands/create_device"
cylon_remove_device = "api/robots/kyle/commands/remove_device"

sio = socketio.Server()
app = Flask(__name__)

# db = DatabaseManager.DatabaseManager()
# db.CreateBook()
# print(db.GetBook())

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

@app.route('/device', methods=['POST'])
def addDevice():
    data = request.data
    response = requests.post(cylon_url + "\\" + cylon_create_device, data=data)

    return "device added"

@app.route('/device_test', methods=['POST'])
def addDeviceT():
    data = request.data
    return requests.post(cylon_url + "\\" + cylon_create_device, data=data)

@app.route('/device/<uuid:device_id>', methods=['DELETE'])
def removeDevice(device_id):
    data = request.data
    response = requests.post(cylon_url + "\\" + cylon_remove_device, data=data)

    return "device %" + str(device_id) + "% removed"

@app.route('/device_test', methods=['DELETE'])
def removeDeviceT():
    data = request.data
    return requests.post(cylon_url + "\\" + cylon_remove_device, data=data)

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