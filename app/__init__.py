from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
socketio = SocketIO(app)

from app import connection, db, game, player, views