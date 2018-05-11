from app import app

class Game():
	def __init__(self):
		self.active_connections = {}
		self.rooms = {}

app.game = Game()