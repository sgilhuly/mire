from app import app



class Room():
	def __init__(self, name):
		app.rooms[name] = self
		self