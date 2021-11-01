class pathfinder:
	def __init__(self, world, xpos, ypos, xtarget, ytarget):
		self.world = []
		self.xpos = xpos
		self.ypos = ypos
		self.xtarget = xtarget
		self.ytarget = ytarget
		for i in world:
			line = []
			for j in i:
				line.append([j==0, 0, 0, 0, 0, False, False]) # is_walkable, dist from end, dist from begining, x of parent, y of parent, already generated, already generator
			self.world.append(line)

	def generate_neighbourgh(self, x, y):
		if x > 0 and self.world[y][x - 1][0] == True:
			if self.world[y][x - 1][5] == False:
				self.world[y][x - 1] = [True, abs(x - 1 - self.xtarget) + abs(y - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
			elif self.world[y][x - 1][2] > self.world[y][x][2] + 1:
				self.kill_son_of(y, x - 1)
				self.world[y][x - 1] = [True, abs(x - 1 - self.xtarget) + abs(y - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
		if y > 0 and self.world[y - 1][x][0] == True:
			if self.world[y - 1][x][5] == False:
				self.world[y - 1][x] = [True, abs(x - self.xtarget) + abs(y - 1 - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
			elif self.world[y - 1][x][2] > self.world[y][x][2] + 1:
				self.kill_son_of(y - 1, x)
				self.world[y - 1][x] = [True, abs(x - self.xtarget) + abs(y - 1 - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
		if y < len(self.world) - 1 and self.world[y + 1][x][0] == True:
			if self.world[y + 1][x][5] == False:
				self.world[y + 1][x] = [True, abs(x - self.xtarget) + abs(y + 1 - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
			elif self.world[y + 1][x][2] > self.world[y][x][2] + 1:
				self.kill_son_of(y + 1, x)
				self.world[y + 1][x] = [True, abs(x - self.xtarget) + abs(y + 1 - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
		if x < len(self.world[0]) - 1 and self.world[y][x + 1][0] == True:
			if self.world[y][x + 1][5] == False:
				self.world[y][x + 1] = [True, abs(x + 1 - self.xtarget) + abs(y - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
			elif self.world[y][x + 1][2] > self.world[y][x][2] + 1:
				self.kill_son_of(x + 1, y)
				self.world[y][x + 1] = [True, abs(x + 1 - self.xtarget) + abs(y - self.ytarget), self.world[y][x][2] + 1, x,y, True, False]
		self.world[y][x][6] = True

	def find_best(self):
		best = 99999999999
		best_arg1 = 99999999999
		coo = (-1, -1)
		for y in range(len(self.world)):
			for x in range(len(self.world[y])):
				if self.world[y][x][5] == True and self.world[y][x][6] == False:
					if self.world[y][x][1] + self.world[y][x][2] < best:
						best = self.world[y][x][1] + self.world[y][x][2]
						best_arg1 = self.world[y][x][1]
						coo = (y, x)
					elif self.world[y][x][1] + self.world[y][x][2] ==  best and self.world[y][x][1] < best_arg1:
						best = self.world[y][x][1] + self.world[y][x][2]
						best_arg1 = self.world[y][x][1]
						coo = (y, x)
		return coo

	def kill_son_of(self, oldx, oldy):
		print(oldx, oldy)
		for y in range(len(self.world)):
			for x in range(len(self.world[y])):
				if self.world[y][x][3] == oldx and self.world[y][x][4] == oldy:
					self.kill_son_of(x,y)
					self.world[y][x] = [True, 0, 0, 0, 0, False, False]

	def solve(self):
		self.world[self.ypos][self.xpos] = [True, abs(self.xpos - self.xtarget) + abs(self.ypos - self.ytarget), 0,-1,-1, True, False]
		x = self.xpos
		y = self.ypos
		while x != self.xtarget or y != self.ytarget:
			self.generate_neighbourgh(x,y)
			y,x = self.find_best()
	
	def __str__(self):
		to_ret = "[]" * (len(self.world[0]) + 2) + "\n[]"
		for y in self.world:
			for x in y:
				if x[0] == True:
					if x[2] > 9:
						to_ret += str(x[2])
					else:
						to_ret += str(x[2]) + ' '
				else:
					to_ret += "[]"
			to_ret += "[]\n[]"
		to_ret += "[]" * (len(self.world[0]) + 1)
		return to_ret

	def get_list_of_indices(self, x, y):
            currentx = x
            currenty = y
            ret = []
            while currentx != self.xpos or currenty != self.ypos:
                ret.append([currentx, currenty])
                nx = self.world[currenty][currentx][3]
                ny = self.world[currenty][currentx][4]
                currentx = nx
                currenty = ny
            ret.append([currentx, currenty])
            return ret[::-1]

	def get_list_of_moove(self, l):
            ret = []
            for i in range(len(l) - 1):
                if l[i + 1][0] == l[i][0] + 1:
                    ret.append("right")
                elif l[i + 1][1] == l[i][1] + 1:
                    ret.append("down")
                elif l[i + 1][1] == l[i][1] - 1:
                    ret.append("up")
                else:
                    ret.append("left")
            return ret
				
if __name__ == "__main__":
    world = [[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,1,1,1,1,1,1],[0,0,0,0,0,0,0]]
    test = 	pathfinder(world, 0,0,3,3)
    test.solve()
    l = test.get_list_of_indices(test.xtarget, test.ytarget)
    print(test)
    print(test.get_list_of_moove(l))
