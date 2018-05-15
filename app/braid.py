from __future__ import print_function

import random

class Maze():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.walls_left = [[False for x in range(width + 1)] for y in range(height)]
		self.walls_up = [[False for x in range(width)] for y in range(height + 1)]

	def create_bounds(self):
		for y in range(self.height):
			self.walls_left[y][0] = True
			self.walls_left[y][self.width] = True
		for x in range(self.width):
			self.walls_up[0][x] = True
			self.walls_up[self.height][x] = True

	def render_text(self):
		print('')
		for y in range(self.height + 1):
			# Walls facing up
			for x in range(self.width):
				print('#', end='')
				if self.is_wall_up(x, y):
					print('#', end='')
				else:
					print(' ', end='')
			print('#')

			# Walls facing left
			if y < self.height:
				for _ in range(1):
					for x in range(self.width + 1):
						if self.is_wall_left(x, y):
							print('#', end='')
						else:
							print(' ', end='')
						if x < self.width:
							print(' ', end='')
					print('')
		print('')

	def is_wall_up(self, x, y):
		return self.walls_up[y][x]

	def is_wall_down(self, x, y):
		return self.walls_up[y + 1][x]

	def is_wall_left(self, x, y):
		return self.walls_left[y][x]

	def is_wall_right(self, x, y):
		return self.walls_left[y][x + 1]

	def is_wall_up_c(self, c):
		return self.is_wall_up(c[0], c[1])

	def is_wall_down_c(self, c):
		return self.is_wall_down(c[0], c[1])

	def is_wall_left_c(self, c):
		return self.is_wall_left(c[0], c[1])

	def is_wall_right_c(self, c):
		return self.is_wall_right(c[0], c[1])

	def get_walls(self, x, y):
		return (self.is_wall_up(x, y), self.is_wall_left(x, y), self.is_wall_down(x, y), self.is_wall_right(x, y))

	def get_walls_c(self, c):
		return (self.is_wall_up_c(c), self.is_wall_left_c(c), self.is_wall_down_c(c), self.is_wall_right_c(c))

	def get_neighbours(self, x, y):
		neighbours = []
		if y > 0 and not self.is_wall_up(x, y):
			neighbours.append((x, y - 1))
		if y + 1 < self.height and not self.is_wall_down(x, y):
			neighbours.append((x, y + 1))
		if x > 0 and not self.is_wall_left(x, y):
			neighbours.append((x - 1, y))
		if x + 1 < self.width and not self.is_wall_right(x, y):
			neighbours.append((x + 1, y))
		return neighbours

	def get_neighbours_c(self, c):
		return self.get_neighbours(c[0], c[1])

	def fully_connected(self):
		# Recursively follow paths that are unvisited, counting cells
		queue = [(0, 0)]
		visited = set(queue)
		count = 1

		while len(queue) > 0:
			cell = queue[0]
			queue = queue[1:]

			for n in self.get_neighbours_c(cell):
				if n not in visited:
					queue.append(n)
					visited.add(n)
					count += 1

			if count > self.width * self.height:
				print('INFINITE RECURSION DETECTED')
				return false

		return count == self.width * self.height

	def test_add_wall(self, is_up, c, full_check=False):
		if is_up:
			if self.walls_up[c[1]][c[0]]:
				return True
			c2 = (c[0], c[1] - 1)
			self.walls_up[c[1]][c[0]] = True
		else:
			if self.walls_left[c[1]][c[0]]:
				return True
			c2 = (c[0] - 1, c[1])
			self.walls_left[c[1]][c[0]] = True

		violated = self.get_walls_c(c).count(False) < 2 or self.get_walls_c(c2).count(False) < 2
		if full_check:
			violated = violated or not self.fully_connected()

		if violated:
			if is_up:
				self.walls_up[c[1]][c[0]] = False
			else:
				self.walls_left[c[1]][c[0]] = False
			return False
		return True

def generate_braid_maze(width=10, height=10):
	maze = Maze(width, height)
	maze.create_bounds()

	# Remove all pole walls
	all_poles = set() # Poles are above and left of these cells
	pole_options = []
	for y in range(1, maze.height):
		for x in range(1, maze.width):
			all_poles.add((x, y))
			if x + 1 < maze.width and y + 1 < maze.height:
				pole_options.append((x, y))
	random.shuffle(pole_options)

	# Quick, cheap pole removal, I think this creates a nicer texture
	for pole in pole_options:
		if pole in all_poles:
			if random.random() < 0.5:
				if maze.test_add_wall(True, pole):
					all_poles.discard(pole)
					all_poles.discard((pole[0] + 1, pole[1]))
			else:
				if maze.test_add_wall(False, pole):
					all_poles.discard(pole)
					all_poles.discard((pole[0], pole[1] + 1))

	# Populate a list of all walls that can be added
	wall_options = [] # Tuples of (wall is up?, (x, y)
	for y in range(maze.height):
		for x in range(maze.width):
			if y > 0:
				wall_options.append((True, (x, y)))
			if x > 0:
				wall_options.append((False, (x, y)))
	random.shuffle(wall_options)

	# Add each wall that does not violate the maze principle
	for wall in wall_options:
		if random.random() < 0.7: # Leave some corridors open
			maze.test_add_wall(wall[0], wall[1], full_check=True)

	return maze

if __name__ == '__main__':
	generate_braid_maze(20, 20)