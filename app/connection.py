from flask import render_template, request
from flask_socketio import join_room, leave_room, send

from app import app, socketio

class Connection():
	def __init__(self):
		self.player = None

def get_connection():
	return app.game.active_connections[request.sid]

@socketio.on('connect')
def handle_connect():
	send('A cloaked figure emerges from the mist.\nHe beckons you closer, whispering:\n\n"Welcome to MIRE, traveller. What is your name?"')
	app.game.active_connections[request.sid] = Connection()

@socketio.on('message')
def handle_message(message):
	# Maybe the connection was ignored due to inactivity
	try:
		conn = get_connection()
	except KeyError:
		send('\nYour connection is invalid, please refresh the page.')
		return

	send('> %s' % message)

	# Login, or create a player
	if not conn.player:
		conn.player = message
		send('Okay, you are named "%s".' % conn.player)
		join_room('chat')
		return

	# Decide what the player's action was
	send('%s: %s' % (conn.player, message), room='chat', broadcast=True)
