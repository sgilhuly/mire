from app import app

class Room():
	direction_codes = {
		'n': 0,
		'north': 0,
		'ne': 1,
		'northeast': 1,
		'e': 2,
		'east': 2,
		'se': 3,
		'southeast': 3,
		's': 4,
		'south': 4,
		'sw': 5,
		'southwest': 5,
		'w': 6,
		'west': 6,
		'nw': 7,
		'northwest': 7
	}

	direction_names = {
		0: 'north',
		1: 'northeast',
		2: 'east',
		3: 'southeast',
		4: 'south',
		5: 'southwest',
		6: 'west',
		7: 'northwest'
	}

	def __init__(self, name, x, y):
		app.game.rooms[name] = self
		self.exits = {}
		self.name = name
		self.x = x
		self.y = y
		self.players = set()

	def connect(self, other, direction, connect_other=True):
		# Convert string directions to number
		if isinstance(direction, str):
			direction = Room.direction_codes[direction]
		self.exits[direction] = other
		if connect_other:
			other.exits[(direction + 4) % 8] = self
		return self

	def describe_exits(self):
		exits_sorted = sorted(self.exits.items())
		exits_named = [Room.direction_names[k] for (k, v) in exits_sorted]
		if len(exits_named) == 0:
			return 'There are no exits!'
		if len(exits_named) == 1:
			return 'Exits are to the %s.' % exits_named[0]
		else:
			# Join the direction names, and insert an oxford comma if there are at least three exits
			return 'Exits are to the %s%s and %s.' % (', '.join(exits_named[:-1]), ',' if len(exits_named) >= 3 else '', exits_named[-1])

# x2y0 = Room('x2y0')

# x0y1 = Room('x0y1')
# x1y1 = Room('x1y1').connect(x0y1, 'w').connect(x2y0, 'ne')
# x2y1 = Room('x2y1').connect(x1y1, 'w').connect(x2y0, 'n')

# x0y2 = Room('x0y2').connect(x0y1, 'n')
# x3y2 = Room('x3y2').connect(x2y1, 'nw')

# x1y3 = Room('x1y3').connect(x0y2, 'nw')
# x2y3 = Room('x2y3').connect(x1y3, 'w')
# x3y3 = Room('x3y3').connect(x2y3, 'w').connect(x3y2, 'n')

# x1y4 = Room('x1y4').connect(x1y3, 'n').connect(x2y3, 'ne')
