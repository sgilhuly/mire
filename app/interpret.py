from functools import wraps

from flask_socketio import join_room, leave_room, send

from app import app
from app.room import Room

app.game.commands = {}

# Attach this to a function to make the aliases available to the interpreter
def command(*aliases):
	def command_decorator(func):
		@wraps(func)
		def func_wrapper(player, *args):
			return func(player, *args)
		for c in aliases:
			app.game.commands[c] = func_wrapper
		return func_wrapper
	return command_decorator

@command('say')
def command_say(player, *args):
	send('%s says "%s"' % (player.name, ' '.join(args[1:])), room="chat", broadcast=True)

@command('jump')
def command_jump(player, *args):
	send('%s jumps up and down.' % player.name, room="chat", broadcast=True)

@command('look', 'l')
def command_look(player, *args):
	send('You are in a room named %s' % player.room.name)
	send(player.room.describe_exits())

@command('go', 'n', 's', 'e', 'w', 'north', 'south', 'east', 'west', 'ne', 'nw', 'se', 'sw', 'northeast', 'northwest', 'southeast', 'southwest')
def command_go(player, *args):
	going = args[0]
	print('args %s'%args)
	if not going in Room.direction_codes:
		going = args[1]
		if not going in Room.direction_codes:
			send('"%s" is not a valid direction.' % args[1])
			return

	dir_code = Room.direction_codes[going]
	if dir_code not in player.room.exits:
		send('You cannot go to the %s.' % Room.direction_names[dir_code])
		return

	player.room = player.room.exits[dir_code]
	send('You are now in %s.' % player.room.name)
	send(player.room.describe_exits())

@command('help', 'what')
def command_help(player, *args):
	send('Here is a list of things you can do:\nsay <something>: Say something to the room\njump: Do some jumps\nlook: Look around\n<dir> / go <dir>: Move in a direction')
