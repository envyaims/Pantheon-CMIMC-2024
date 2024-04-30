import random as rand
import copy
from collections import deque
from math import ceil

random = rand.Random()
random.seed(69420)

class Planner:
	def verify(self, plan, pairs):
		def dfsComponent(x, y, n, roads, visRoads):
			if x < 0 or x >= n or y < 0 or y >= n:
				return
			if roads[x][y] != 1:
				return
			if visRoads[x][y] == 1:
				return
			visRoads[x][y] = 1
			dfsComponent(x - 1, y, n, roads, visRoads)
			dfsComponent(x + 1, y, n, roads, visRoads)
			dfsComponent(x, y - 1, n, roads, visRoads)
			dfsComponent(x, y + 1, n, roads, visRoads)

		p = len(pairs)

		visRoads = [[0] * self.n for i in range(self.n)]

		for pairNum in range(p):
			root = pairs[pairNum][0]
			if visRoads[root[0]][root[1]] == 1:
				continue

			dfsComponent(root[0], root[1], self.n, plan, visRoads)

			for pairNum2 in range(p):
				pt1 = pairs[pairNum2][0]
				pt2 = pairs[pairNum2][1]
				if visRoads[pt1[0]][pt1[1]] != visRoads[pt2[0]][pt2[1]]:
					return False
			if visRoads[root[0]][root[1]] == 0:
				return False

		return True

	def bresenham(self, array, x1, y1, x2, y2, modifier=0):
		dx = abs(x2 - x1)
		dy = abs(y2 - y1)
		sx = 1 if x1 < x2 else -1
		sy = 1 if y1 < y2 else -1
		if x1 == x2:
			sx = 0
		if sy == y2:
			sy = 0
		err = dx - dy

		count = 0
		self.currWidth -= modifier
		for i in range(int(self.currWidth / 2) - int(self.currWidth), ceil(self.currWidth / 2) + 1, 1):
			count += 1
			if (count >= 16):
				break
			for j in range(int(self.currWidth / 2) - int(self.currWidth), ceil(self.currWidth / 2) + 1, 1):
				if 0 <= y1 + i < self.n and 0 <= x1 + j < self.n:
					try:
						array[y1 + i][x1 + j] = 1
					except: pass

		count = 0
		while x1 != x2 or y1 != y2:
			count += 1
			if (count >= 30):
				break
			for i in range(int(self.currWidth / 2) - int(self.currWidth), ceil(self.currWidth / 2) + 1, 1):
				if 0 <= y1 + i < self.n:
					try:
						array[y1 + i][x1] = 1
					except: pass
				if 0 <= x1 + i < self.n:
					try:
						array[y1][x1 + i] = 1
					except: pass

			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x1 += sx
			if e2 < dx:
				err += dx
				y1 += sy

		for i in range(int(self.currWidth / 2) - int(self.currWidth), ceil(self.currWidth / 2) + 1, 1):
			for j in range(int(self.currWidth / 2) - int(self.currWidth), ceil(self.currWidth / 2) + 1, 1):
				if 0 <= y2 + i < self.n and 0 <= x2 + j < self.n:
					try:
						array[y2 + i][x2 + j] = 1
					except: pass
		self.currWidth += modifier
	
	def bresenham_util(self, x1, y1, x2, y2, modifier):
		dx = abs(x2 - x1)
		dy = abs(y2 - y1)
		sx = 1 if x1 < x2 else -1
		sy = 1 if y1 < y2 else -1
		if x1 == x2:
			sx = 0
		if sy == y2:
			sy = 0
		err = dx - dy

		count = 0

		if dx >= dy:  
			if 0 <= y1 + modifier < self.n:
				self.tryList.append(tuple([y1 + modifier, x1]))
			if modifier != 0:
				if 0 <= y1 - modifier < self.n:
					self.tryList.append(tuple([y1 - modifier, x1]))

			while x1 != x2 or y1 != y2:
				count += 1
				if (count >= 30):
					break

				if 0 <= x1 < self.n and 0 <= y1 < self.n:
					if 0 <= y1 + modifier < self.n:
						self.tryList.append(tuple([y1 + modifier, x1]))
					if modifier != 0:
						if 0 <= y1 - modifier < self.n:
							self.tryList.append(tuple([y1 - modifier, x1]))

					e2 = 2 * err
					if e2 > -dy:
						err -= dy
						x1 += sx
					if e2 < dx:
						err += dx
						y1 += sy

			if 0 <= y2 + modifier < self.n:
				self.tryList.append(tuple([y2 + modifier, x2]))
			if modifier != 0:
				if 0 <= y2 - modifier < self.n:
					self.tryList.append(tuple([y2 - modifier, x2]))
		else:
			if 0 <= x1 + modifier < self.n:
				self.tryList.append(tuple([y1, x1 + modifier]))
			if modifier != 0:
				if 0 <= x1 - modifier < self.n:
					self.tryList.append(tuple([y1, x1 - modifier]))

			while x1 != x2 or y1 != y2:
				count += 1
				if (count >= 30):
					break

				if 0 <= x1 < self.n and 0 <= y1 < self.n:
					if 0 <= x1 + modifier < self.n:
						self.tryList.append(tuple([y1, x1 + modifier]))
					if modifier != 0:
						if 0 <= x1 - modifier < self.n:
							self.tryList.append(tuple([y1, x1 - modifier]))

				e2 = 2 * err
				if e2 > -dy:
					err -= dy
					x1 += sx
				if e2 < dx:
					err += dx
					y1 += sy

			if 0 <= x2 + modifier < self.n:
				self.tryList.append(tuple([y2, x2 + modifier]))
			if modifier != 0:
				if 0 <= x2 - modifier < self.n:
					self.tryList.append(tuple([y2, x2 - modifier]))

	def mod_bresenham(self, array, x1, y1, x2, y2, currWidth):
		dx = abs(x2 - x1)
		dy = abs(y2 - y1)
		sx = 1 if x1 < x2 else -1
		sy = 1 if y1 < y2 else -1
		if x1 == x2:
			sx = 0
		if sy == y2:
			sy = 0
		err = dx - dy

		count = 0
		for i in range(int(currWidth / 2) - int(currWidth), ceil(currWidth / 2) + 1, 1):
			count += 1
			if (count >= 16):
				break
			for j in range(int(currWidth / 2) - int(currWidth), ceil(currWidth / 2) + 1, 1):
				if 0 <= y1 + i < self.n and 0 <= x1 + j < self.n:
					try:
						array[y1 + i][x1 + j] = 1
					except: pass

		count = 0
		while x1 != x2 or y1 != y2:
			count += 1
			if (count >= 30):
				break
			for i in range(int(currWidth / 2) - int(currWidth), ceil(currWidth / 2) + 1, 1):
				if 0 <= y1 + i < self.n:
					try:
						array[y1 + i][x1] = 1
					except: pass
				if 0 <= x1 + i < self.n:
					try:
						array[y1][x1 + i] = 1
					except: pass

			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x1 += sx
			if e2 < dx:
				err += dx
				y1 += sy

		for i in range(int(currWidth / 2) - int(currWidth), ceil(currWidth / 2) + 1, 1):
			for j in range(int(currWidth / 2) - int(currWidth), ceil(currWidth / 2) + 1, 1):
				if 0 <= y2 + i < self.n and 0 <= x2 + j < self.n:
					try:
						array[y2 + i][x2 + j] = 1
					except: pass

	def calculate_depth(self, newPlan, start_coords):

		self.BOUND_3 = 1
		self.BOUND_2 = 1
		self.BOUND_1 = 1
		rows = len(newPlan)
		cols = len(newPlan[0])

		depths = [[-1 for _ in range(cols)] for _ in range(rows)]
		queue = deque([(start_coords[0], start_coords[1], 0)])
		depths[start_coords[0]][start_coords[1]] = 0

		directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

		while queue:
			r, c, depth = queue.popleft()

			for dr, dc in directions:
				new_r, new_c = r + dr, c + dc
				if 0 <= new_r < rows and 0 <= new_c < cols and newPlan[new_r][new_c] == 1 and depths[new_r][new_c] == -1:
					depths[new_r][new_c] = depth + 1
					self.depthCounts[depth + 1] = self.depthCounts.get(depth + 1, 0) + 1
					if (self.depthCounts[depth + 1] - 2 > self.BOUND_3):
						self.BOUND_3 = self.depthCounts[depth + 1] - 2
					queue.append((new_r, new_c, depth + 1))
		return depths

	def setup(self, pairs, bd):
		self.C_MODIFIER = [7, 8, 6, 9, 5, 10, 11, 4, 12, 13, 3, 2, 15, 1, 0, 14]
		self.R_MODIFIER = [7, 8, 6, 9, 5, 10, 11, 4, 12, 13, 3, 2, 15, 1, 0, 14]

		self.tryList = deque()

		self.n = 16
		self.r = 0
		self.mode = True
		self.c = -1
		self.currWidth = 0
		self.depthCounts = {}
		self.pairs = pairs
		self.BOUND_3 = 3
		self.last = 0

		self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
		self.direction_index = 0
		self.steps = 1
		self.step_count = 0
		self.target_zero = []
		self.BOUND_2 = 2
		self.bresenham_order = []
		self.BOUND_1 = 1
		self.count = 0
		self.modifier = 16
		self.pairset = []
		for pair in self.pairs:
			self.pairset.append(pair[0])
			self.pairset.append(pair[1])
		self.bd = bd
		self.yeetProbability = 0.07  # probability of removing a road
		self.bestPlan = [[1] * self.n for _ in range(self.n)]
		self.sentPlan = []

		self.visited = [[False] * self.n for _ in range(self.n)]


		self.effective_coords = list()
		for pair in self.pairs:
			if abs(pair[0][1] - pair[1][1]) + abs(pair[0][0] - pair[1][0]) < 2:
				continue
			for coord in pair:
				self.effective_coords.append(coord)


		self.xsum = 0
		self.ysum = 0
		for coord in self.effective_coords:
			self.xsum += coord[0]
			self.ysum += coord[1]
		if len(self.effective_coords) != 0:
			self.xsum /= len(self.effective_coords)
			self.ysum /= len(self.effective_coords)
		self.available = [False for _ in range(len(self.effective_coords))]
		self.targets = [-1 for _ in range(len(self.effective_coords))]
		for i in range(len(self.effective_coords)):
			if not self.available[i]:
				continue
			this_scores = list()
			for j in range(len(self.effective_coords)):
				if i == j:
					continue
				if abs(self.effective_coords[i][0] - self.effective_coords[j][0]) + abs(self.effective_coords[i][1] - self.effective_coords[j][1]) < abs(self.effective_coords[i][0] - self.xsum) + abs(self.effective_coords[i][1] - self.ysum):
					this_scores.append(abs(self.effective_coords[i][0] - self.effective_coords[j][0]) + abs(self.effective_coords[i][1] - self.effective_coords[j][1]) < abs(self.effective_coords[i][0] - self.xsum) + abs(self.effective_coords[i][1] - self.ysum))
			for j in range(len(self.effective_coords)):
				if self.this_scores[j] == min(this_scores):
					self.available[j] = False
					self.xsum -= self.effective_coords[i][0] / len(self.effective_coords)
					self.ysum -= self.effective_coords[i][1] / len(self.effective_coords)
					self.targets[i] = j
					break
		
		self.cw = self.clockwise_order()
		max_distance = 0

		# Iterate over the clockwise pairs
		for i in range(len(self.cw)):
			# Calculate the distance between the current pair and its adjacent pair
			dist = self.distance(self.cw[i], self.cw[(i + 1) % len(self.cw)])
			# Update max_distance if the current distance is greater
			if dist > max_distance:
				max_distance = dist

		self.start_index = 0
		for i in range(len(self.cw)):
			dist = self.distance(self.cw[i], self.cw[(i + 1) % len(self.cw)])
			if dist == max_distance:
				self.start_index = (i + 1) % len(self.cw)
		
		for i in range(self.start_index):
			self.cw.rotate(-1)
		# print(self.cw)
		self.cw_backup = copy.deepcopy(self.cw)

		return
	
	def distance(self, pair1, pair2):
		return abs(pair2[0] - pair1[0]) + abs(pair2[1] - pair1[1])


	def how_is_my_program_not_tle_yet(self, arr):
		for i in range(0, self.n):
			for j in range(0, self.n):
				if arr[i][j] == 1:
					count = 0
					if i + 1 < self.n and (arr[i + 1][j] != 1):
						count += 1
					if i - 1 >= 0 and (arr[i - 1][j] != 1):
						count += 1
						if j - 1 >= 0 and (arr[i][j - 1] != 1):
							if i + 1 < self.n and (arr[i + 1][j] == 1):
								if arr[i + 1][j - 1] != 1:
									if i + 2 < self.n and arr[i + 2][j] != 1:
										arr[i][j] = 0
										arr[i + 1][j] = 0
					if j + 1 < self.n and (arr[i][j + 1] != 1):
						count += 1
					if j - 1 >= 0 and (arr[i][j - 1] != 1):
						count += 1
					condition = [i, j] not in self.pairset
					if (count >= 3 or ((i == 0 or i == self.n - 1 or j == 0 or j == self.n - 1) and count >= 2 and condition)):
						if (not condition): continue
						arr[i][j] = 0

		for i in range(self.n - 2, 0, -1):
			for j in range(self.n - 2, 0, -1):
				if arr[i][j] == 1:
					if i - 1 >= 0 and (arr[i - 1][j] != 1):
						count += 1
						if j + 1 < self.n and (arr[i][j + 1] != 1):
							if i + 1 < self.n and (arr[i + 1][j] == 1):
								if arr[i + 1][j + 1] != 1:
									if i + 2 < self.n and arr[i + 2][j] != 1:
										arr[i][j] = 0
										arr[i + 1][j] = 0
						continue
					count = 0
					try:
						if (arr[i + 1][j] != 1):
							count += 1
					except: pass
					try:
						if (arr[i - 1][j] != 1):
							count += 1
					except: pass
					try:
						if (arr[i][j + 1] != 1):
							count += 1
					except: pass
					try:
						if (arr[i][j - 1] != 1):
							count += 1
					except: pass
					condition = [i, j] not in self.pairset
					if (count >= 3 or ((i == 0 or i == self.n - 1 or j == 0 or j == self.n - 1) and count >= 2 and condition)):
						if (not condition): continue
						arr[i][j] = 0

					count = 0
					if i + 1 < self.n and (arr[i + 1][j] != 1):
						count += 1
					if i - 1 >= 0 and (arr[i - 1][j] != 1):
						count += 1
						if j - 1 >= 0 and (arr[i][j - 1] != 1):
							if i + 1 < self.n and (arr[i + 1][j] == 1):
								if arr[i + 1][j - 1] != 1:
									if i + 2 < self.n and arr[i + 2][j] != 1:
										arr[i][j] = 0
										arr[i + 1][j] = 0
					if j + 1 < self.n and (arr[i][j + 1] != 1):
						count += 1
					if j - 1 >= 0 and (arr[i][j - 1] != 1):
						count += 1
					condition = [i, j] not in self.pairset
					if (count >= 3 or ((i == 0 or i == self.n - 1 or j == 0 or j == self.n - 1) and count >= 2 and condition)):
						if (not condition): continue
						arr[i][j] = 0
					


	
	def clockwise_order(self):
		clockwise_pairs = deque()
		for x in range(16):
			if [x, 0] in self.effective_coords: clockwise_pairs.append((x, 0))
		for y in range(1, 16):
			if [15, y] in self.effective_coords: clockwise_pairs.append((15, y))
		for x in range(14, -1, -1):
			if [x, 15] in self.effective_coords: clockwise_pairs.append((x, 15))
		for y in range(14, 0, -1):
			if [0, y] in self.effective_coords: clockwise_pairs.append((0, y))
		return clockwise_pairs


	def task1(self, q, queryOutputs):
		self.count += 1
		l = len(queryOutputs)

		if l > 0 and queryOutputs[l - 1]:
			self.bestPlan = copy.deepcopy(self.sentPlan)

		if self.count <= 6:
			self.cw = copy.deepcopy(self.cw_backup)
			self.r = 1
			if l > 0 and queryOutputs[l - 1]:
				self.bestPlan = copy.deepcopy(self.sentPlan)
				self.currWidth -= self.modifier
			else:
				self.currWidth += self.modifier

			self.bresenhamWeights = [self.currWidth for _ in range(len(self.effective_coords))]

			newPlan = [[0] * self.n for _ in range(self.n)]
			for pair in self.pairs:
				if abs(pair[0][1] - pair[1][1]) + abs(pair[0][0] - pair[1][0]) < 2:
					self.bresenham(newPlan, pair[0][1], pair[0][0], pair[1][1], pair[1][0])
			last_node = self.cw.popleft()
			while len(self.cw) > 0:
				next_node = self.cw.popleft()
				self.bresenham(newPlan, last_node[1], last_node[0], next_node[1], next_node[0])
				last_node = next_node
			self.sentPlan = copy.deepcopy(newPlan)
			self.modifier /= 2
			return copy.deepcopy(self.sentPlan)
		# elif self.count <= 6 + len(self.effective_coords):
		#	 self.r = 1
		#	 self.c = 3
		#	 if self.count > 6 and queryOutputs[l - 1]:
		#		 self.bestPlan = copy.deepcopy(self.sentPlan)
		#		 self.count -= 1
		#		 self.bresenhamWeights[self.count - 7] = int(self.bresenhamWeights[self.count - 7] * 0.75)
		#		 # print("optimized iteration")

		#	 newPlan = [[0] * self.n for _ in range(self.n)]
		#	 for pair in self.pairs:
		#		 if abs(pair[0][1] - pair[1][1]) + abs(pair[0][0] - pair[1][0]) < 5:
		#			 self.mod_bresenham(newPlan, pair[0][1], pair[0][0], pair[1][1], pair[1][0], self.bresenhamWeights[self.count - 7])
		#			 continue
		#		 for coord in pair:
		#			 self.mod_bresenham(newPlan, int(self.xsum + 0.5), int(self.ysum + 0.5), coord[1], coord[0], self.bresenhamWeights[self.count - 7])

		newPlan = copy.deepcopy(self.bestPlan)
		# depths = self.calculate_depth(newPlan, self.pairset[0])
		# # print(depths)
		# for i in range(self.n):
		#	 for j in range(self.n):
		#		 if depths[i][j] == -1:
		#			 newPlan[i][j] = 0

		roadCount = 1
		for i in range(self.n):
			for j in range(self.n):
				roadCount += newPlan[i][j]

		while self.count <= 45 and roadCount > q:

			while True:
				if self.mode:
					self.c += 4
					if (self.c >= 15):
						self.c = 3
						self.r += 2
					if (self.r >= 16):
						self.r = 2
						self.c = 1
						self.count = 46
						break

					if self.mode:
						while self.r < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r][self.c - 1] == 1 or newPlan[self.r][self.c - 2] == 1 or newPlan[self.r][self.c-3] == 1) and [self.r, self.c] not in self.pairset and [self.r, self.c - 3] not in self.pairset ):
							self.c += 4
							if (self.c >= 15):
								self.c = 3
								self.r += 2

					if (self.r >= 16):
						self.r = 2
						self.c = 1
						self.count = 46
						break

				if self.r >= 16 or self.c >= 16:
					self.count = 46
					break

				newPlan[self.r][self.c - 1] = 0
				newPlan[self.r][self.c - 2] = 0
				newPlan[self.r][self.c - 3] = 0
				newPlan[self.r][self.c] = 0
				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c - 1] = 1
					newPlan[self.r][self.c - 2] = 1
					newPlan[self.r][self.c - 3] = 1
					newPlan[self.r][self.c] = 1
					self.count += 1
				else:
					break

			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 90 and roadCount > q:
			while True:
				if self.mode:
					self.r += 2
					if (self.r >= 15):
						self.r = 2
						self.c += 2
					if (self.c >= 16):
						self.c = 0
						self.r = 0
						self.count = 91
						break

					if self.mode:
						while self.c < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r - 1][self.c] == 1) and [self.r, self.c] not in self.pairset and [self.r - 1, self.c] not in self.pairset):
							self.r += 2
							if (self.r >= 15):
								self.r = 2
								self.c += 2

					if (self.c >= 16):
						self.c = 0
						self.r = 0
						self.count = 91
						break

				if self.r >= 16 or self.c >= 16:
					self.count = 91
					break

				newPlan[self.r][self.c] = 0
				newPlan[self.r - 1][self.c] = 0

				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c] = 1
					newPlan[self.r - 1][self.c] = 1
					self.count += 1
				else:
					break
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 10:
			if self.mode:
				self.c += 2
				if (self.c >= 15):
					self.c = 1
					self.r += 2
				if (self.r >= 16):
					self.r = 2
					self.c = 1
					self.count = 136
					break

				if self.mode:
					while self.r < 16 and not (newPlan[self.r][self.c] == 1 and newPlan[self.r][self.c + 1] == 1 and [self.r, self.c] not in self.pairset and [self.r, self.c - 1] not in self.pairset ):
						self.c += 2
						if (self.c >= 15):
							self.c = 1
							self.r += 2

				if (self.r >= 16):
					self.r = 2
					self.c = 1
					self.count = 136
					break

			if self.r >= 16 or self.c >= 16:
				self.count = 136
				break

			newPlan[self.r][self.c] = 0
			newPlan[self.r][self.c + 1] = 0
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 356:
			while True:
				if self.mode:
					self.c += 1
					if (self.c >= 16):
						self.c = 0
						self.r += 1
					if (self.r >= 16):
						return self.bestPlan

					if self.mode:
						while self.r < 16 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
							self.c += 1
							if (self.c >= 16):
								self.c = 0
								self.r += 1

					if (self.r >= 16):
						return self.bestPlan

				if self.r >= 16 or self.c >= 16:
					return self.bestPlan

				newPlan[self.r][self.c] = 0
				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c] = 1
					self.count += 1
				else:
					break
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		return self.bestPlan

	
	def task2(self, q, queryOutputs):
		self.count += 1
		l = len(queryOutputs)

		if l > 0 and queryOutputs[l - 1]:
			self.bestPlan = copy.deepcopy(self.sentPlan)

		if self.count <= 6:
			self.cw = copy.deepcopy(self.cw_backup)
			self.r = 1
			if l > 0 and queryOutputs[l - 1]:
				self.bestPlan = copy.deepcopy(self.sentPlan)
				self.currWidth -= self.modifier
			else:
				self.currWidth += self.modifier

			self.bresenhamWeights = [self.currWidth for _ in range(len(self.effective_coords))]

			newPlan = [[0] * self.n for _ in range(self.n)]
			for pair in self.pairs:
				if abs(pair[0][1] - pair[1][1]) + abs(pair[0][0] - pair[1][0]) < 2:
					self.bresenham(newPlan, pair[0][1], pair[0][0], pair[1][1], pair[1][0])
			last_node = self.cw.popleft()
			while len(self.cw) > 0:
				next_node = self.cw.popleft()
				self.bresenham(newPlan, last_node[1], last_node[0], next_node[1], next_node[0])
				last_node = next_node
			self.sentPlan = copy.deepcopy(newPlan)
			self.modifier /= 2
			return copy.deepcopy(self.sentPlan)
		# elif self.count <= 6 + len(self.effective_coords):
		#	 self.r = 1
		#	 self.c = 3
		#	 if self.count > 6 and queryOutputs[l - 1]:
		#		 self.bestPlan = copy.deepcopy(self.sentPlan)
		#		 self.count -= 1
		#		 self.bresenhamWeights[self.count - 7] = int(self.bresenhamWeights[self.count - 7] * 0.75)
		#		 # print("optimized iteration")

		#	 newPlan = [[0] * self.n for _ in range(self.n)]
		#	 for pair in self.pairs:
		#		 if abs(pair[0][1] - pair[1][1]) + abs(pair[0][0] - pair[1][0]) < 5:
		#			 self.mod_bresenham(newPlan, pair[0][1], pair[0][0], pair[1][1], pair[1][0], self.bresenhamWeights[self.count - 7])
		#			 continue
		#		 for coord in pair:
		#			 self.mod_bresenham(newPlan, int(self.xsum + 0.5), int(self.ysum + 0.5), coord[1], coord[0], self.bresenhamWeights[self.count - 7])

		newPlan = copy.deepcopy(self.bestPlan)
		# depths = self.calculate_depth(newPlan, self.pairset[0])
		# # print(depths)
		# for i in range(self.n):
		#	 for j in range(self.n):
		#		 if depths[i][j] == -1:
		#			 newPlan[i][j] = 0

		roadCount = 1
		for i in range(self.n):
			for j in range(self.n):
				roadCount += newPlan[i][j]

		while self.count <= 45 and roadCount > q:

			while True:
				if self.mode:
					self.c += 4
					if (self.c >= 15):
						self.c = 3
						self.r += 2
					if (self.r >= 16):
						self.r = 2
						self.c = 1
						self.count = 46
						break

					if self.mode:
						while self.r < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r][self.c - 1] == 1 or newPlan[self.r][self.c - 2] == 1 or newPlan[self.r][self.c-3] == 1) and [self.r, self.c] not in self.pairset and [self.r, self.c - 3] not in self.pairset ):
							self.c += 4
							if (self.c >= 15):
								self.c = 3
								self.r += 2

					if (self.r >= 16):
						self.r = 2
						self.c = 1
						self.count = 46
						break

				if self.r >= 16 or self.c >= 16:
					self.count = 46
					break

				newPlan[self.r][self.c - 1] = 0
				newPlan[self.r][self.c - 2] = 0
				newPlan[self.r][self.c - 3] = 0
				newPlan[self.r][self.c] = 0
				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c - 1] = 1
					newPlan[self.r][self.c - 2] = 1
					newPlan[self.r][self.c - 3] = 1
					newPlan[self.r][self.c] = 1
					self.count += 1
				else:
					break

			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 90 and roadCount > q:
			while True:
				if self.mode:
					self.r += 2
					if (self.r >= 15):
						self.r = 2
						self.c += 2
					if (self.c >= 16):
						self.c = 0
						self.r = 0
						self.count = 91
						break

					if self.mode:
						while self.c < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r - 1][self.c] == 1) and [self.r, self.c] not in self.pairset and [self.r - 1, self.c] not in self.pairset):
							self.r += 2
							if (self.r >= 15):
								self.r = 2
								self.c += 2

					if (self.c >= 16):
						self.c = 0
						self.r = 0
						self.count = 91
						break

				if self.r >= 16 or self.c >= 16:
					self.count = 91
					break

				newPlan[self.r][self.c] = 0
				newPlan[self.r - 1][self.c] = 0

				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c] = 1
					newPlan[self.r - 1][self.c] = 1
					self.count += 1
				else:
					break
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 10:
			if self.mode:
				self.c += 2
				if (self.c >= 15):
					self.c = 1
					self.r += 2
				if (self.r >= 16):
					self.r = 2
					self.c = 1
					self.count = 136
					break

				if self.mode:
					while self.r < 16 and not (newPlan[self.r][self.c] == 1 and newPlan[self.r][self.c + 1] == 1 and [self.r, self.c] not in self.pairset and [self.r, self.c - 1] not in self.pairset ):
						self.c += 2
						if (self.c >= 15):
							self.c = 1
							self.r += 2

				if (self.r >= 16):
					self.r = 2
					self.c = 1
					self.count = 136
					break

			if self.r >= 16 or self.c >= 16:
				self.count = 136
				break

			newPlan[self.r][self.c] = 0
			newPlan[self.r][self.c + 1] = 0
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		while self.count <= 356:
			while True:
				if self.mode:
					self.c += 1
					if (self.c >= 16):
						self.c = 0
						self.r += 1
					if (self.r >= 16):
						return self.bestPlan

					if self.mode:
						while self.r < 16 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
							self.c += 1
							if (self.c >= 16):
								self.c = 0
								self.r += 1

					if (self.r >= 16):
						return self.bestPlan

				if self.r >= 16 or self.c >= 16:
					return self.bestPlan

				newPlan[self.r][self.c] = 0
				if not self.verify(newPlan, self.pairs):
					newPlan[self.r][self.c] = 1
					self.count += 1
				else:
					break
			self.sentPlan = copy.deepcopy(newPlan)
			self.how_is_my_program_not_tle_yet(self.sentPlan)
			return self.sentPlan

		return self.bestPlan

	def task3(self, q, queryOutputs):
		self.count += 1
		l = len(queryOutputs)
		if l > 0 and queryOutputs[l - 1]: self.bestPlan = copy.deepcopy(self.sentPlan)
		if self.count <= 6:
			if l > 0 and queryOutputs[l - 1]:
				self.bestPlan = copy.deepcopy(self.sentPlan)
				self.bestWidth = self.currWidth
				self.currWidth -= self.modifier
			else: self.currWidth += self.modifier

			newPlan = [[0] * self.n for _ in range(self.n)]
			self.bresenham(newPlan, self.pairset[0][1], self.pairset[0][0], self.pairset[1][1], self.pairset[1][0])
			self.sentPlan = copy.deepcopy(newPlan)
			self.modifier /= 2
			return copy.deepcopy(self.sentPlan)
		
		if self.count == 7:
			for i in range(ceil(self.bestWidth / 2) + 1, 2, -1): self.bresenham_util(self.pairset[0][1], self.pairset[0][0], self.pairset[1][1], self.pairset[1][0], i)

		newPlan = copy.deepcopy(self.bestPlan)
		depths = self.calculate_depth(newPlan, self.pairset[0])
		roadCount = 1
		for i in range(self.n):
			for j in range(self.n): roadCount += newPlan[i][j]
		
		while self.count <= 290:
			if roadCount > q:
				while self.count <= 45:
					while True:
						if self.mode:
							self.c += 4
							if (self.c >= 15):
								self.c = 3
								self.r += 2
							if (self.r >= 16):
								self.r = 2
								self.c = 1
								self.count = 46
								break
	
							if self.mode:
								while self.r < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r][self.c - 1] == 1 or newPlan[self.r][self.c - 2] == 1 or newPlan[self.r][self.c-3] == 1) and [self.r, self.c] not in self.pairset and [self.r, self.c - 3] not in self.pairset ):
									self.c += 4
									if (self.c >= 15):
										self.c = 3
										self.r += 2
	
							if (self.r >= 16):
								self.r = 2
								self.c = 1
								self.count = 46
								break
	
						if self.r >= 16 or self.c >= 16:
							self.count = 46
							break
	
						newPlan[self.r][self.c - 1] = 0
						newPlan[self.r][self.c - 2] = 0
						newPlan[self.r][self.c - 3] = 0
						newPlan[self.r][self.c] = 0
						if not self.verify(newPlan, self.pairs):
							newPlan[self.r][self.c - 1] = 1
							newPlan[self.r][self.c - 2] = 1
							newPlan[self.r][self.c - 3] = 1
							newPlan[self.r][self.c] = 1
							self.count += 1
						else: break
	
					self.sentPlan = copy.deepcopy(newPlan)
					self.how_is_my_program_not_tle_yet(self.sentPlan)
					return self.sentPlan
	
				while self.count <= 90:
					while True:
						if self.mode:
							self.r += 2
							if (self.r >= 15):
								self.r = 2
								self.c += 2
							if (self.c >= 16):
								self.c = 0
								self.r = 1
								self.count = 91
								break
	
							if self.mode:
								while self.c < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r - 1][self.c] == 1) and [self.r, self.c] not in self.pairset and [self.r - 1, self.c] not in self.pairset):
									self.r += 2
									if (self.r >= 15):
										self.r = 2
										self.c += 2
	
							if (self.c >= 16):
								self.c = 0
								self.r = 1
								self.count = 91
								break
	
						if self.r >= 16 or self.c >= 16:
							self.count = 91
							break
	
						newPlan[self.r][self.c] = 0
						newPlan[self.r - 1][self.c] = 0
	
						if not self.verify(newPlan, self.pairs):
							newPlan[self.r][self.c] = 1
							newPlan[self.r][self.c - 1] = 1
							self.count += 1
						else:
							break
					self.sentPlan = copy.deepcopy(newPlan)
					self.how_is_my_program_not_tle_yet(self.sentPlan)
					return self.sentPlan

			self.r = 0
			self.c = -1
			self.target_zero = copy.deepcopy(self.bestPlan)
			if len(self.tryList) == 0:
				self.count = 291
				continue
			next_coord = self.tryList.popleft()
			# print(next_coord)
			if newPlan[next_coord[0]][next_coord[1]] == 0:
				self.count += 1
				continue
			newPlan[next_coord[0]][next_coord[1]] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[next_coord[0]][next_coord[1]] = 1
				self.count += 1
			else:
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		# print("FINISHED")
		while self.count <= 500:
			if self.mode:
				self.c += 1
				if (self.c >= 16):
					self.c = 0
					self.r += 1
				if (self.r >= 16): 
					self.count = 501
					self.c = 15
					self.r = 15
					break
				if self.mode:
					while self.r < 16 and self.c < 16 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
						self.c += 1
						if (self.c >= 16):
							self.c = 0
							self.r += 1
					if (self.r >= 16): 
						self.count = 501
						break
			if self.r >= 16 or self.c >= 16: 
				self.count = 501
				self.c = 15
				self.r = 15
				break
			newPlan[self.r][self.c] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[self.r][self.c] = 1
				self.count += 1
			else:
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		
		if self.count == 501:

			# self.bestPlan = copy.deepcopy(self.target_zero)
			newPlan = copy.deepcopy(self.bestPlan)
			self.c = 16
			self.r = 15
		
		while self.count <= 750:
			if self.mode:
				self.c -= 1
				if (self.c < 0):
					self.c = 15
					self.r -= 1
				if (self.r < 0): return self.bestPlan
				if self.mode:
					while self.r >= 0 and self.c >= 0 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
						self.c -= 1
						if (self.c < 0):
							self.c = 15
							self.r -= 1
					if (self.r < 0): 
						return self.bestPlan
			if self.r < 0 or self.c < 0: 
				return self.bestPlan
			newPlan[self.r][self.c] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[self.r][self.c] = 1
				self.count += 1
			else:
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		return self.bestPlan


	def task4(self, q, queryOutputs):
		self.count += 1
		l = len(queryOutputs)

		if l > 0 and queryOutputs[l - 1]: self.bestPlan = copy.deepcopy(self.sentPlan)
		if self.count <= 6:
			if l > 0 and queryOutputs[l - 1]:
				self.bestPlan = copy.deepcopy(self.sentPlan)
				self.bestWidth = self.currWidth
				self.currWidth -= self.modifier
			else: self.currWidth += self.modifier
			newPlan = [[0] * self.n for _ in range(self.n)]
			self.bresenham(newPlan, self.pairset[0][1], self.pairset[0][0], self.pairset[1][1], self.pairset[1][0])
			self.sentPlan = copy.deepcopy(newPlan)
			self.target_zero = copy.deepcopy(self.bestPlan)
			self.modifier /= 2
			# print("running")
			return copy.deepcopy(self.sentPlan)
		
		if self.count == 7:
			for i in range(ceil(self.bestWidth / 2) + 1, 1, -1): self.bresenham_util(self.pairset[0][1], self.pairset[0][0], self.pairset[1][1], self.pairset[1][0], i)

		newPlan = copy.deepcopy(self.bestPlan)
		depths = self.calculate_depth(newPlan, self.pairset[0])
		roadCount = 1
		for i in range(self.n): 
			for j in range(self.n): roadCount += newPlan[i][j]
		
		while self.count <= 290:
			if roadCount > q:
				while self.count <= 45:
					while True:
						if self.mode:
							self.c += 4
							if (self.c >= 15):
								self.c = 3
								self.r += 2
							if (self.r >= 16):
								self.r = 2
								self.c = 1
								self.count = 46
								break
	
							if self.mode:
								while self.r < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r][self.c - 1] == 1 or newPlan[self.r][self.c - 2] == 1 or newPlan[self.r][self.c-3] == 1) and [self.r, self.c] not in self.pairset and [self.r, self.c - 3] not in self.pairset ):
									self.c += 4
									if (self.c >= 15):
										self.c = 3
										self.r += 2
	
							if (self.r >= 16):
								self.r = 2
								self.c = 1
								self.count = 46
								break
	
						if self.r >= 16 or self.c >= 16:
							self.count = 46
							break
	
						newPlan[self.r][self.c - 1] = 0
						newPlan[self.r][self.c - 2] = 0
						newPlan[self.r][self.c - 3] = 0
						newPlan[self.r][self.c] = 0
						if not self.verify(newPlan, self.pairs):
							newPlan[self.r][self.c - 1] = 1
							newPlan[self.r][self.c - 2] = 1
							newPlan[self.r][self.c - 3] = 1
							newPlan[self.r][self.c] = 1
							self.count += 1
						else: break
	
					self.sentPlan = copy.deepcopy(newPlan)
					self.how_is_my_program_not_tle_yet(self.sentPlan)
					return self.sentPlan
	
				while self.count <= 90:
					while True:
						if self.mode:
							self.r += 2
							if (self.r >= 15):
								self.r = 2
								self.c += 2
							if (self.c >= 16):
								self.c = 0
								self.r = 1
								self.count = 91
								break
	
							if self.mode:
								while self.c < 16 and not ((newPlan[self.r][self.c] == 1 or newPlan[self.r - 1][self.c] == 1) and [self.r, self.c] not in self.pairset and [self.r - 1, self.c] not in self.pairset):
									self.r += 2
									if (self.r >= 15):
										self.r = 2
										self.c += 2
	
							if (self.c >= 16):
								self.c = 0
								self.r = 1
								self.count = 91
								break
	
						if self.r >= 16 or self.c >= 16:
							self.count = 91
							break
	
						newPlan[self.r][self.c] = 0
						newPlan[self.r - 1][self.c] = 0
	
						if not self.verify(newPlan, self.pairs):
							newPlan[self.r][self.c] = 1
							newPlan[self.r][self.c - 1] = 1
							self.count += 1
						else: break
					self.sentPlan = copy.deepcopy(newPlan)
					self.how_is_my_program_not_tle_yet(self.sentPlan)
					return self.sentPlan


			self.r = 0
			self.c = -1
			if len(self.tryList) == 0:
				self.count = 291
				self.r = 0
				self.c = -1
				continue
			next_coord = self.tryList.popleft()
			if newPlan[next_coord[0]][next_coord[1]] == 0:
				self.count += 1
				continue
			newPlan[next_coord[0]][next_coord[1]] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[next_coord[0]][next_coord[1]] = 1
				self.count += 1
			else:
				self.target_zero = copy.deepcopy(self.bestPlan)
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		while self.count <= 500:
			if self.mode:
				self.c += 1
				if (self.c >= 16):
					self.c = 0
					self.r += 1
				if (self.r >= 16): 
					self.count = 501
					self.c = 15
					self.r = 15
					break
				if self.mode:
					while self.r < 16 and self.c < 16 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
						self.c += 1
						if (self.c >= 16):
							self.c = 0
							self.r += 1
					if (self.r >= 16): 
						self.count = 501
						break
			if self.r >= 16 or self.c >= 16: 
				self.count = 501
				self.c = 15
				self.r = 15
				break
			newPlan[self.r][self.c] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[self.r][self.c] = 1
				self.count += 1
			else:
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		
		if self.count == 501:
			self.bestPlan = copy.deepcopy(self.target_zero)
			newPlan = copy.deepcopy(self.bestPlan)
			self.c = 16
			self.r = 15
		
		while self.count <= 750:
			if self.mode:
				self.c -= 1
				if (self.c < 0):
					self.c = 15
					self.r -= 1
				if (self.r < 0): return self.bestPlan
				if self.mode:
					while self.r >= 0 and self.c >= 0 and not (newPlan[self.r][self.c] == 1 and [self.r, self.c] not in self.pairset):
						self.c -= 1
						if (self.c < 0):
							self.c = 15
							self.r -= 1
					if (self.r < 0): 
						return self.bestPlan
			if self.r < 0 or self.c < 0: 
				return self.bestPlan
			newPlan[self.r][self.c] = 0
			if not self.verify(newPlan, self.pairs):
				newPlan[self.r][self.c] = 1
				self.count += 1
			else:
				self.sentPlan = copy.deepcopy(newPlan)
				self.how_is_my_program_not_tle_yet(self.sentPlan)
				return self.sentPlan
		return self.bestPlan

	def query(self, q, queryOutputs):
		if len(self.pairs) == 5 and self.bd == 0.25: return self.task1(q, queryOutputs)
		if len(self.pairs) == 5 and self.bd == 0.1: return self.task1(q, queryOutputs)
		if len(self.pairs) == 1 and self.bd == 0.25: return self.task3(q, queryOutputs)
		if len(self.pairs) == 1 and self.bd == 0.1: return self.task4(q, queryOutputs)
