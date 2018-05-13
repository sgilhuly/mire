from app import app
from app.room import Room

class Player():
	def __init__(self, name, room):
		self.name = name
		self.room = room
