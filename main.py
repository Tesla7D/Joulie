import socketio
import eventlet.wsgi
import os
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

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
    return "device added"

@app.route('/device/<uuid:device_id>', methods=['DELETE'])
def removeDevice(device_id):
    return "device %" + str(device_id) + "% removed"

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
