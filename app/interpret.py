from functools import wraps

from flask_socketio import join_room, leave_room, send

from app import app

app.game.commands = {}

# Attach this to a function to make the aliases available to the interpreter
def command(aliases):
	def command_decorator(func):
		@wraps(func)
		def func_wrapper(player, args):
			return func(player, args)
		for c in aliases:
			app.game.commands[c] = func_wrapper
		return func_wrapper
	return command_decorator

@command(['say'])
def command_say(player, args):
	send('%s says "%s"' % (player, ' '.join(args[1:])), room="chat", broadcast=True)

@command(['jump'])
def command_jump(player, args):
	send('%s jumps up and down.' % player, room="chat", broadcast=True)

@command(['go', 'n', 's', 'e', 'w', 'north', 'south', 'east', 'west'])
def command_go(player, args):
	send('You try to walk somewhere, but your legs are not yet implemented.')

@command(['help', 'what'])
def command_help(player, args):
	send('Here is a list of things you can do:\nsay <something>: Say something to the room\njump: Do some jumps')
