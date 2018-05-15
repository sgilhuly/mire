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
		TYPE_SCOUTER: 'SCOUTER',
		TYPE_SENSER: 'SENSER',
		TYPE_SIGNALLER: 'SIGNALLER',
		TYPE_SIGNER: 'SIGNER',
		TYPE_SIMPLETON: 'SIMPLETON',
		TYPE_SNIFFER: 'SNIFFER',
		TYPE_SOUNDER: 'SOUNDER'
	}

	TYPE_DESCRIPTIONS = { 
		TYPE_SCOUTER: 'Faster and more energetic than the others. A scouter can move 200 spaces\ninstead of 100. Others may find this constant energy annoying.',
		TYPE_SENSER: 'In tune with an innate location sense. A senser always knows their exact grid\nlocation. This sense makes up for a permanent blindness.',
		TYPE_SIGNALLER: 'Just a person with a compass.',
		TYPE_SIGNER: 'Posesses a magical marking skill. A signer can leave up to 5 magic signs, each\nwith a short message.',
		TYPE_SIMPLETON: 'Just a person.',
		TYPE_SNIFFER: 'A dog. A sniffer has a powerful sense of smell that can tell when the exit is\nclose. Can be heard from further away by barking, but can not speak.',
		TYPE_SOUNDER: 'Has a fine sense of hearing. A sounder can sing in any direction, and tell how\nfar away the nearest wall is. Can also find dead ends by listening for echoes.'
	}

	TYPE_HELP = {
		TYPE_SCOUTER: 'You have 200 max steps instead of 100.\nYou also speak in all-caps.',
		TYPE_SENSER: 'Not implemented, so you have no powers yet.',
		TYPE_SIGNALLER: 'Not implemented, so you have no powers yet.',
		TYPE_SIGNER: 'Not implemented, so you have no powers yet.',
		TYPE_SIMPLETON: 'You are an ordinary person.\nYou have neither special abilities nor distinguishing features.',
		TYPE_SNIFFER: 'You are a dog.\nYou can smell when you are getting closer to the exit.\nYou cannot speak, but your barks can be heard from further away.\nYou can point if you want to indicate a direction.',
		TYPE_SOUNDER: 'sing <direction>: Sing in a direction and listen for echoes.\nSinging tells you how far away a wall is.\nSinging also lets you know if your voice can reach back to you.\nIf a strong echo is present, you are singing into a closed chamber.'
	}

	EXHAUSTION_MILESTONES = {
		75: "You are still feeling great and ready for anything this maze will throw at you!",
		50: "You are beginning to feel tired",
		25: "You are exhausted",
		10: "Your body tires. Every step is a great effort",
		0: 'You have taken your last laborious step, and collapse.'
	}

	def __init__(self, name):
		self.name = name
		self.room = None
		self.type = Player.TYPE_NONE
		self.type_confirmed = False
		self.steps_left = 100

	def describe_class(self):
		try:
			return '{}\n\n{}'.format(self.TYPE_NAMES[self.type], self.TYPE_DESCRIPTIONS[self.type])
		except KeyError:
			return '(Type 1 - 7 to select a class)'

	def passed_exhaustion_milestone(self):
		return self.steps_left in self.EXHAUSTION_MILESTONES.keys()

	def get_exhaustion(self):
		sorted_keys = [*self.EXHAUSTION_MILESTONES.keys()]
		sorted_keys.sort()
		
		for k in sorted_keys:
			if self.steps_left <= k:
				return self.EXHAUSTION_MILESTONES[k]

	def help_class(self):
		try:
			return '%s\n\n%s' % (self.TYPE_NAMES[self.type], self.TYPE_HELP[self.type])
		except KeyError:
			return 'You have no class.'

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

