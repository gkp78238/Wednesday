from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    
    # Initialize SocketIO with the app
    socketio.init_app(app)

    # Register your blueprints and other setup here

    return app
