from __future__ import print_function

from flask import render_template, request
from flask_socketio import join_room, leave_room, send

from app import app, socketio

class Connection():
	def __init__(self):
		self.player = None

@socketio.on('connect')
def handle_connect():
	print('%s has connected' % (request.sid))
	send('A cloaked figure emerges from the mist.\nHe beckons you closer, whispering:\n\n"Welcome to MIRE, traveller. What is your name?"')
	app.game.active_connections[request.sid] = Connection()

@socketio.on('disconnect')
def handle_disconnect():
	print('%s has disconnected' % (request.sid))
	del app.game.active_connections[request.sid]

@socketio.on('message')
def handle_message(message):
	print('%s: %s' % (request.sid, message))
	# Maybe the connection was ignored due to inactivity
	try:
		conn = app.game.active_connections[request.sid]
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
	args = message.split(' ')
	print(app.game.commands)

	if not args:
		send('You pause for a moment and think.')

	if not args[0] in app.game.commands:
		send('"%s" is unrecognized.' % args[0])

	else:
		app.game.commands[args[0]](conn.player, args)
