from app import app

class Game():
	def __init__(self):
		self.active_connections = {}

app.game = Game()