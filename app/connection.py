from __future__ import print_function

from flask import render_template, request
from flask_socketio import join_room, leave_room, send

from app import app, socketio
from app.player import Player

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
	message = message.strip()
	print('%s: %s' % (request.sid, message))
	# Maybe the connection was ignored due to inactivity
	try:
		conn = app.game.active_connections[request.sid]
	except KeyError:
		send('\nYour connection is invalid, please refresh the page.')
		return

	send('\n> %s\n' % message)

	# Check if character details need to be filled out
	if not conn.player:
		if not 4 <= len(message) <= 20:
			send('The figure acts as if he didn\'t hear you right, and gestures as if to say:\n"Choose a name between 4 and 20 characters long."')
			return
		conn.player = Player(message)
		conn.player.conn = conn
		send('"Welcome, %s. Before you lies a great maze.\nYou connection to this world is tenuous, and you will have only 100 steps to\nreach the goal. You may need to rely on others to complete your jounery.\n\nNow, may I ask what your profession is?"' % conn.player.name)
		send('\n(Type 1 - 7 to select one of the following)\n  1 - SCOUTER\n  2 - SENSER\n  3 - SIGNALLER\n  4 - SIGNER\n  5 - SIMPLETON\n  6 - SNIFFER\n  7 - SOUNDER')
		return

	args = message.split(' ')

	if not conn.player.type_confirmed:

		if conn.player.type == Player.TYPE_NONE:

			#Assign a player class if it is in the list of classes
			if int(args[0]) in Player.TYPE_NAMES.keys():
				conn.player.type = int(args[0])
				send(conn.player.describe_class())
				send('\n"Is this an accurate description of yourself?" (yes/no)')
			return

		else:
			if args[0] == 'yes' or args[0] == 'y':
				conn.player.type_confirmed = True
				send('The figure bows. "Your goal lies near the south east corner of the maze."\n\nYou experience the sensation of jolting awake, though your eyes remain open.\n(Type "help" for general commands, or "help class" for class details.)')
				conn.player.enter_room(app.game.start_room, '%s appears.' % conn.player.name)
				if conn.player.type == Player.TYPE_SCOUTER:
					conn.player.steps_left *= 2
				return
			elif args[0] == 'no' or args[0] == 'n':
				conn.player.type = Player.TYPE_NONE
				send('(Type 1 - 7 to select one of the following)\n  1 - SCOUTER\n  2 - SENSER\n  3 - SIGNALLER\n  4 - SIGNER\n  5 - SIMPLETON\n  6 - SNIFFER\n  7 - SOUNDER')
				return
			else:
				send('"Well, yes or no?"')
				return

	# Decide what the player's action was
	if not args:
		send('You pause for a moment and think.')

	if not args[0] in app.game.commands:
		send('"%s" is unrecognized.' % args[0])

	else:
		app.game.commands[args[0]](conn.player, *args[1:])
