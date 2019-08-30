from graphics import *
import time
import random
import math
import winsound
class Screen:
	def __init__(self, window):
		self.win = window
		self.win.setBackground('black')
		# lines down the middle
		rect = Rectangle(Point(498, 5), Point(502, 29))
		rect.setFill('white')
		rect.draw(self.win)
		for y in range(25):
			rect = rect.clone()
			rect.move(0, 30)
			rect.draw(self.win)
class Paddle:
	def __init__(self, fixed_x, window):
		self.win = window
		self.x = fixed_x
		self.y = 250
		self.rect = Rectangle(Point(self.x, self.y), Point(self.x + 25, self.y + 100))
		self.rect.setFill('white')
		self.rect.draw(self.win)
	def move(self, dy):
		if self.y <= 500 and self.y >= 0:
			newDY = self.y + dy
			if newDY > 500:
				dy = 50 - (newDY - 500)
			elif newDY < 0:
				dy = 50 - (0 - newDY)
			self.y += dy
			self.rect.move(0, dy)

class Ball:
	def __init__(self, window, direction, start_x=480, start_y=280):
		self.x = start_x
		self.y = start_y
		self.win = window
		self.rect = Rectangle(Point(self.x, self.y), Point(self.x + 20, self.y + 20))
		self.rect.setFill('white')
		self.rect.draw(self.win)
		self.speed = 1
		r = random.random
		self.theta = 0
		if direction == 'right':
			self.theta = random.random() * (math.pi / 2) - (math.pi / 4)
		else:
			self.theta = random.random() * (math.pi / 2) + (3 * math.pi / 4)

	def playSound(self):
		num = random.randrange(7) + 1
		sound = 'pong' + str(num) + '.wav'
		winsound.PlaySound(sound, winsound.SND_ALIAS | winsound.SND_ASYNC)

	def move(self, p1, p2, finish=False):
		# self.rect.move(math.cos(self.theta), math.sin(self.theta))
		dx = math.cos(self.theta) * self.speed
		dy = math.sin(self.theta) * self.speed
		if finish:
			self.rect.move(dx, dy)
			return 0
		score = 0
		newY = self.y + dy
		newX = self.x + dx
		if newY < 0:
			dy = self.y
			extraX = newY / math.tan(self.theta)
			dx -= extraX
			self.theta = -self.theta
		elif newY > 580:
			extraY = newY - 580
			extraX = extraY / math.tan(self.theta)
			dy = newY - extraY - self.y
			dx = newX - extraX - self.x
			self.theta = -self.theta
		elif newX < 50 and newX > 25 and (newY + 20) >= p1.y and newY <= (p1.y + 100):
			self.playSound()
			extraX = newX - 50
			extraY = extraX / math.tan(self.theta)
			dx -= extraX
			dy -= extraY
			self.theta = math.pi - self.theta
		elif newX > 930 and newX < 950 and (newY + 20) >= p2.y and newY <= (p2.y + 100):
			self.playSound()
			extraX = newX - 930
			extraY = extraX / math.tan(self.theta)
			dx -= extraX
			dy -= extraY
			self.theta = math.pi - self.theta
		elif newX < -20:
			return 1 # right scores
		elif newX > 1020:
			return -1 # left scores
		self.y += dy
		self.x += dx
		self.rect.move(dx, dy)

class Score:
	def __init__(self, x, window):
		self.win = window
		txt = Text(Point(x, 100), '0')
		txt.setSize(36)
		txt.setFill('white')
		txt.draw(self.win)
		self.txt = txt
		self.score = 0

	def scored(self):
		self.score += 1
		self.txt.setText(str(self.score))
		if self.score == 10:
			return 1
		return 0

def main():
	win = GraphWin("Merritt's Pong", 1000, 600)
	screen = Screen(win)
	paddle1 = Paddle(25, win)
	paddle2 = Paddle(950, win)
	ball = Ball(win, 'left')
	player1 = Score(250, win)
	player2 = Score(750, win)
	winner = ""
	scoredLast = 'left'
	currTime = time.perf_counter()
	lastTime = currTime
	interval = .003
	while not winner:
		currTime = time.perf_counter()
		if currTime - lastTime > interval:
			lastTime = time.perf_counter()
			score = ball.move(paddle1, paddle2)
			if score:
				interval -= .0001
				if score == -1:
					scoredLast = 'left'
					if player1.scored():
						winner = "Player 1"
				elif score == 1:
					scoredLast = 'right'
					if player2.scored():
						winner = "Player 2"
				ball = Ball(win, scoredLast)
		key = win.checkKey()
		if key == 'a':
			paddle1.move(-50)
		elif key == 'z':
			paddle1.move(50)
		elif key == 'k':
			paddle2.move(-50)
		elif key == 'm':
			paddle2.move(50)
	winsound.PlaySound('victory.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
	txt = Text(Point(500, 300), winner + " wins!")
	txt.setFill('yellow')
	txt.setSize(36)
	ball.rect.undraw()
	txt.draw(win)
	win.getMouse()

main()