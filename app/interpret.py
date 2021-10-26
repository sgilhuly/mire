import math
from functools import wraps

from flask_socketio import join_room, leave_room, send

from app import app
from app.player import Player
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
	if player.type == Player.TYPE_SNIFFER:
		send('%s barks.' % player.name, room=player.room.name, broadcast=True)
	else:
		text = ' '.join(args[1:])
		if player.type == Player.TYPE_SCOUTER:
			text = text.upper()
		send('%s says "%s".' % (player.name, text), room=player.room.name, broadcast=True)

@command('shout')
def command_shout(player, *args):
	if player.type == Player.TYPE_SNIFFER:
		room_message = '%s barks loudly!' % player.name
		far_message = 'You hear barks coming from the %s.'
		message_distance = 6
	else:
		text = ' '.join(args[1:])
		if player.type == Player.TYPE_SCOUTER:
			text = text.upper()
		room_message = '%s shouts "%s"!' % (player.name, text)
		far_message = 'You hear from the %%s "%s"!' % text
		message_distance = 4

	# Breadth first search the dungeon, sending the specified message
	send(room_message, room=player.room.name, broadcast=True)
	rooms_found = set([player.room])
	room_queue = [(player.room, 0)]
	while len(room_queue) > 0:
		(room, distance) = room_queue[0]
		room_queue = room_queue[1:]
		for (exit_dir, exit_room) in room.exits.items():
			if exit_room not in rooms_found:
				rooms_found.add(exit_room)
				if distance + 1 < message_distance:
					room_queue.append((exit_room, distance + 1))
				send(far_message % Room.direction_names[(exit_dir + 4) % 8], room=exit_room.name, broadcast=True)

@command('jump')
def command_jump(player, *args):
	send('%s jumps up and down.' % player.name, room=player.room.name, broadcast=True)

@command('look', 'l')
def command_look(player, *args):
	send('You are in featureless maze.')
	send(player.room.describe_exits())

@command('point')
def command_point(player, *args):
	if len(args) > 1 and args[1] in Room.direction_codes:
		dir_name = Room.direction_names[Room.direction_codes[args[1]]]
		send('%s points to the %s.' % (player.name, dir_name), room=player.room.name, broadcast=True)
		return
	send('Provide a direction to point in.')

@command('status', 'stats', 'stat')
def command_status(player, *args):
	send('%d steps left.' % player.steps_left)

@command('go', 'move', 'walk', 'n', 's', 'e', 'w', 'north', 'south', 'east', 'west', 'ne', 'nw', 'se', 'sw', 'northeast', 'northwest', 'southeast', 'southwest')
def command_go(player, *args):
	if player.steps_left <= 0:
		send('You are too tired to move.')
		return

	going = args[0]
	if not going in Room.direction_codes:
		going = args[1]
		if not going in Room.direction_codes:
			send('"%s" is not a valid direction.' % args[1])
			return

	dir_code = Room.direction_codes[going]
	if dir_code not in player.room.exits:
		send('You cannot go to the %s.' % Room.direction_names[dir_code])
		return

	new_room = player.room.exits[dir_code]
	old_room = player.room
	exit_message = '%s exits to the %s.' % (player.name, Room.direction_names[dir_code])
	enter_message = '%s enters from the %s.' % (player.name, Room.direction_names[(dir_code + 4) % 8])
	player.exit_room(old_room, exit_message)
	player.enter_room(new_room, enter_message)
	send('You move %s.' % Room.direction_names[dir_code])
	send(player.room.describe_exits())

	if player.type == Player.TYPE_SNIFFER:
		send('%d' % new_room.distance)
		if new_room.distance_log < old_room.distance_log:
			send('Oh boy, the smell is much stronger here!')
		elif new_room.distance_log > old_room.distance_log:
			send('The smell is stronger behind you, go back!')

	player.steps_left -= 1
	won = player.room == app.game.end_room
	if player.steps_left <= 0:
		send('You have taken your last laborious step, and collapse.')
		if won:
			send('However...')
	if won:
		send('\n\nBefore you is a column of light ready to take you out of the maze.\nYou have, at last, found the exit.\n\nYOU DID IT.')

@command('sing', 'sound')
def command_sing(player, *args):
	if player.type == Player.TYPE_SOUNDER and len(args) > 1:
		if args[1] in Room.direction_codes:
			sing_dir = Room.direction_codes[args[1]]
			room = player.room
			send('%s sings to the %s.' % (player.name, Room.direction_names[sing_dir]))
			wall_distance = 0
			while sing_dir in room.exits:
				wall_distance += 1
				room = room.exits[sing_dir]
			send('There is a wall %d spaces away.' % wall_distance)
			if wall_distance > 0:
				# Breadth first search the dungeon, counting the number of rooms
				rooms_found = set([player.room, player.room.exits[sing_dir]])
				room_queue = [(player.room.exits[sing_dir], 0)]
				while len(room_queue) > 0:
					(room, distance) = room_queue[0]
					room_queue = room_queue[1:]
					for (exit_dir, exit_room) in room.exits.items():
						if exit_room == player.room:
							send('You hear an echo from the %s.' % Room.direction_names[(exit_dir + 4) % 8])
						if exit_room not in rooms_found:
							rooms_found.add(exit_room)
							if distance + 1 < 10:
								room_queue.append((exit_room, distance + 1))
				if len(rooms_found) < 10:
					send('There is a strong echo.')
			return
	send('%s sings.' % player.name, room=player.room.name, broadcast=True)

@command('direction', 'dir', 'compass')
def command_compass(player, *args):
	if player.type != Player.TYPE_SIGNALLER:
		send('Alas, you do not have a compass.')
		return

	if player.room == app.game.end_room:
		send('Your compass is going crazy!')
		return

	x = app.game.end_room.x - player.room.x
	y = app.game.end_room.y - player.room.y
	# atan2 takes y then x, and goes cclockwise from 1,0
	# by giving x then y, we get clockwise from 0,1, the same way we count directions
	angle = (round(math.atan2(x, -y) * 180.0 / math.pi / 5) * 5) % 360
	if angle % 45 == 0:
		send('Your compass is reading due %s.' % Room.direction_names[angle / 45])
		return
	# Hard code this for now
	elif 0 < angle < 90:
		send('Your compass is reading %s degrees east of north.' % angle)
		return
	elif 90 < angle < 180:
		send('Your compass is reading %s degrees east of south.' % 180 - angle)
		return
	elif 180 < angle < 270:
		send('Your compass is reading %s degrees west of south.' % angle - 180)
		return
	else:
		send('Your compass is reading %s degrees west of north.' % 360 - angle)
		return

@command('help', 'what')
def command_help(player, *args):
	if len(args) > 1 and args[1] == 'class':
		send(player.help_class())
		return
	send('Here is a list of things you can do:\nsay <something>: Say something to the room\njump: Do some jumps\nlook: Look around\n<dir> / go <dir>: Move in a direction\nhelp class: Class details')
