from flask_socketio import join_room, leave_room, send

from app import app
from app.room import Room

# Character classes
# Signaller: knows direction to exit (has a compass)
# Sounder: knows distance to wall, if direction leads to dead end (echoes)
# Scouter: has higher move limit, speaks in all caps
# Senser: knows grid coordinates, blind
# Sniffer: knows logarithmic distance to exit (smell strength), can't speak (is a dog)
# Signer: can leave a few messages
# Simpleton: No abilities

class Player():
	TYPE_NONE = 0
	TYPE_SCOUTER = 1
	TYPE_SENSER = 2
	TYPE_SIGNALLER = 3
	TYPE_SIGNER = 4
	TYPE_SIMPLETON = 5
	TYPE_SNIFFER = 6
	TYPE_SOUNDER = 7

	TYPE_NAMES = {
		1: 'SCOUTER',
		2: 'SENSER',
		3: 'SIGNALLER',
		4: 'SIGNER',
		5: 'SIMPLETON',
		6: 'SNIFFER',
		7: 'SOUNDER'
	}

	def __init__(self, name):
		self.name = name
		self.room = None
		self.type = Player.TYPE_NONE
		self.type_confirmed = False
		self.steps_left = 100

	def describe_class(self):
		if self.type == Player.TYPE_SCOUTER:
			return 'SCOUTER\n\nFaster and more energetic than the others. A scouter can move 200 spaces\ninstead of 100. Others may find this constant energy annoying.'
		elif self.type == Player.TYPE_SENSER:
			return 'SENSER\n\nIn tune with an innate location sense. A senser always knows their exact grid\nlocation. This sense makes up for a permanent blindness.'
		elif self.type == Player.TYPE_SIGNALLER:
			return 'SIGNALLER\n\nJust a person with a compass.'
		elif self.type == Player.TYPE_SIGNER:
			return 'SIGNER\n\nPosesses a magical marking skill. A signer can leave up to 5 magic signs, each\nwith a short message.'
		elif self.type == Player.TYPE_SIMPLETON:
			return 'SIMPLETON\n\nJust a person.'
		elif self.type == Player.TYPE_SNIFFER:
			return 'SNIFFER\n\nA dog. A sniffer has a powerful sense of smell that can tell when the exit is\nclose. Can be heard from further away by barking, but can not speak.'
		elif self.type == Player.TYPE_SOUNDER:
			return 'SOUNDER\n\nHas a fine sense of hearing. A sounder can sing in any direction, and tell how\nfar away the nearest wall is. Can also find dead ends by listening for echoes.'
		else:
			return '(Type 1 - 7 to select a class)'

	def exit_room(self, room, message):
		leave_room(room.name)
		send(message, room=room.name, broadcast=True)
		room.players.discard(self)
		self.room = None

	def enter_room(self, room, message):
		send(message, room=room.name, broadcast=True)
		join_room(room.name)
		room.players.add(self)
		self.room = room
