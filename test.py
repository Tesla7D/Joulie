import socketio
import eventlet
import eventlet.wsgi
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace, SocketIONamespace
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)


def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)

socketIO = SocketIO('localhost', 3000, SocketIONamespace)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

# Listen
socketIO.on('aaa_response', on_aaa_response)
socketIO.on('aaa', on_aaa_response)
socketIO.on('chat message', on_aaa_response)
socketIO.on('chat message_response', on_aaa_response)
socketIO.emit('chat message', "Test")
socketIO.emit('chat message', "Test2")

@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')


@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    sio.emit('chat message', data, namespace='/chat')


@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    while True:
        i = 0
    # deploy as an eventlet WSGI server
    #eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
