import random

from app import app
from app.braid import Maze, generate_braid_maze
from app.room import Room

class Game():
	def __init__(self):
		self.active_connections = {}
		self.rooms = {}
		self.start_room = None
		self.end_room = None

	def random_room(self):
		return random.choice(self.rooms.values())

app.game = Game()
maze = generate_braid_maze(20, 20)
maze.render_text()

rooms = [[None for x in range(maze.width)] for y in range(maze.height)]
for y in range(maze.height):
	for x in range(maze.width):
		room = Room('x%dy%d' % (x, y), x, y)
		rooms[y][x] = room
		if x > 0 and not maze.is_wall_left(x, y):
			room.connect(rooms[y][x - 1], 'w')
		if y > 0 and not maze.is_wall_up(x, y):
			room.connect(rooms[y - 1][x], 'n')

app.game.start_room = rooms[2][2]
app.game.end_room = rooms[maze.height - 3][maze.width - 3]