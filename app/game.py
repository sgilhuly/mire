import random

from app import app

class Game():
	def __init__(self):
		self.active_connections = {}
		self.rooms = {}

	def random_room(self):
		return random.choice(self.rooms.values())

app.game = Game()