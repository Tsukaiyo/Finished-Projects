'''
"Tracer" game
Author: Maeve Fitzgerald
- Add leaderboard
'''

import pygame
import math
import time
import random

#Open at top of screen
x = 350
y = 0
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#Initializations
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Colours
BLUE = (10, 20, 50)
TEAL = (69, 240, 233)
PURPLE = (138, 28, 124)
GREEN = (127, 231, 105)
PINK = (218, 65, 103)
WHITE = (255, 255, 255)
YELLOW = (237, 237, 63)

#Team Colours
GREEN1 = (82, 220, 145)
GREEN2 = (171, 209, 45)
RED1 = (242, 84, 91)
RED2 = (211, 30, 85)

# Setup
Height = 800
Width = 800
size = [Height, Width]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tracer")
done = False
clock = pygame.time.Clock()

# Basic variables
winner = 0
speed = 4
players = 4
gameState = "Menu"
team = False
turnList = []
currentSquare = 0
size = 10
grid = 0
maze = True
mazeCreated = False
buttonsMade = False
scoreWritten = False
selected = 0
points = 0
lives = 5
explosions = 0
name = [0, 0, 0, 0]
selectedLetter = 0

# Game-timing variables
startTime = 0
endTime = 0
gameTime = 0
endOfRound = False
timeRecording = True  # Turn on for regular play, off for testing

# Object lists
dots = []
dots2 = []
dots3 = []
dots4 = []
animationDots = []
rockets = []
animationRockets = []
buttons = []
bloops = []
joysticks = []
arcButtons = []
particles = []

# Objects
class Dot(object):
    #Make up trails behind rockets
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

class Particle(object):
    #Used to animate explosions in maze-mode collisions
    def __init__(self, x, y, colour, startX, startY):
        self.x = x
        self.y = y
        self.colour = colour
        self.startX = startX
        self.startY = startY

class Rocket(object):
    #Player object
    def __init__(self, x, y, colour, playerNum, direction, startX, startY, timeOfDeath):
        self.x = x
        self.y = y
        self.colour = colour
        self.playerNum = playerNum
        self.direction = direction
        self.startX = startX
        self.startY = startY
        self.timeOfDeath = timeOfDeath

class aniRocket(object):
    #Animated rockets
    def __init__(self, x, y, colour, playerNum, direction, startX, startY, endX, endY):
        self.x = x
        self.y = y
        self.colour = colour
        self.playerNum = playerNum
        self.direction = direction
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

class Wall(object):
    #Maze walls
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Square(object):
    #Blocks that make up the screen in maze mode
    def __init__(self, nWall, eWall, sWall, wWall, x, y, visited):
        self.nWall = nWall
        self.eWall = eWall
        self.sWall = sWall
        self.wWall = wWall
        self.x = x
        self.y = y
        self.visited = visited

class Button(object):
    #Buttons on screen
    def __init__(self, text, size, colour, x, y):
        self.text = text
        self.size = size
        self.colour = colour
        self.x = x
        self.y = y
        self.toggle = False

class Bloop(object):
    #Point objects in maze mode
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visable = True

# Methods
#Rockets
def shoot(rockets, rocket):
    # Leaves Dot trails
    maxDots = 1000/len(rockets)
    if rocket == rockets[0]:
        dots.append(Dot(rocket.x, rocket.y, rocket.colour))
        if len(dots) > maxDots:
            del dots[0]
    if rocket == rockets[1]:
        dots2.append(Dot(rocket.x, rocket.y, rocket.colour))
        if len(dots2) > maxDots:
            del dots2[0]
    if len(rockets) > 2:
        if rocket == rockets[2]:
            dots3.append(Dot(rocket.x, rocket.y, rocket.colour))
            if len(dots3) > maxDots:
                del dots3[0]
    if len(rockets) == 4:
        if rocket == rockets[3]:
            dots4.append(Dot(rocket.x, rocket.y, rocket.colour))
            if len(dots4) > maxDots:
                del dots4[0]

def generateRockets(maze, players, team):
    #Creates rocket objects
    del rockets[:]
    if not team:
        if players == 2:
            rockets.append(Rocket(600, 200, TEAL, 2, "up", 600, 200, 0))
            rockets.append(Rocket(200, 200, PURPLE, 1, "up", 200, 200, 0))
        if players == 3 and maze:
            rockets.append(Rocket(600, 200, TEAL, 2, "up", 600, 200, 0))
            rockets.append(Rocket(200, 200, PURPLE, 1, "up", 200, 200, 0))
            rockets.append(Rocket(360, 600, GREEN, 3, "up", 360, 600, 0))
        if players == 3 and not maze:
            rockets.append(Rocket(600, 200, TEAL, 2, "up", 600, 200, 0))
            rockets.append(Rocket(250, 200, PURPLE, 1, "up", 250, 200, 0))
            rockets.append(Rocket(400, 600, GREEN, 3, "up", 400, 600, 0))
        if players == 4:
            rockets.append(Rocket(600, 200, TEAL, 2, "up", 600, 200, 0))
            rockets.append(Rocket(200, 200, PURPLE, 1, "up", 200, 200, 0))
            rockets.append(Rocket(200, 600, GREEN, 3, "up", 200, 600, 0))
            rockets.append(Rocket(600, 600, PINK, 4, "up", 600, 600, 0))
    else:
        rockets.append(Rocket(600, 200, GREEN1, 2, "up", 600, 200, 0))
        rockets.append(Rocket(250, 200, GREEN2, 1, "up", 250, 200, 0))
        rockets.append(Rocket(250, 600, RED1, 3, "up", 250, 600, 0))
        rockets.append(Rocket(600, 600, RED2, 4, "up", 600, 600, 0))

#Animations
def aniShoot():
    #Leaves dot trails in animations
    maxDots = 500
    for i in range(len(animationRockets)):
        animationDots[i].append(Dot(animationRockets[i].x, animationRockets[i].y, animationRockets[i].colour))
        if len(animationDots[i]) > maxDots:
            del animationDots[i][0]

def aniRocketSteering(aniRocket):
    #Decides where the animated rockets move
    closeToTarget = False
    if aniRocket.x < aniRocket.endX + 5 and aniRocket.x > aniRocket.endX - 5:
        closeToTarget = True
    if aniRocket.y < aniRocket.endY + 5 and aniRocket.y > aniRocket.endY - 5:
        closeToTarget = True
    targetOutOfRange = False
    if aniRocket.endX > 790 or aniRocket.endX < 10 or aniRocket.endY > 790 or aniRocket.endY < 10 :
        targetOutOfRange = True

    if targetOutOfRange or closeToTarget: #pick new direction
        newDirection = int(random.random() * 4)
        if newDirection == 0:
            aniRocket.endX = aniRocket.x + int(random.random()*200)
            #aniRocket.endY = aniRocket.y
        if newDirection == 1:
            aniRocket.endY = aniRocket.y + int(random.random()*200)
            #aniRocket.endX = aniRocket.x
        if newDirection == 2:
            aniRocket.endX = aniRocket.x - int(random.random()*200)
            #aniRocket.endY = aniRocket.y
        if newDirection == 3:
            aniRocket.endY = aniRocket.y - int(random.random()*200)
            #aniRocket.endX = aniRocket.x
    else: #move
        touchingDot = False
        for dots in animationDots:
            for i in range(len(dots)):
                if dist(dots[i], aniRocket) < 5 and not dots[i].colour == aniRocket.colour:  #Check if touching a dot of a different colour
                    touchingDot = True
        if touchingDot: #if touching a dot, reset
            aniRocket.x = aniRocket.startX
            aniRocket.endX = aniRocket.startX
            aniRocket.y = aniRocket.startY
            aniRocket.endY = aniRocket.startY
        else: #if not touching a dot, move towards target
            speed = 5
            if aniRocket.x < aniRocket.endX:
                aniRocket.x = aniRocket.x + speed
                aniRocket.direction = "right"
            if aniRocket.x > aniRocket.endX:
                aniRocket.x = aniRocket.x - speed
                aniRocket.direction = "left"
            if aniRocket.y < aniRocket.endY:
                aniRocket.y = aniRocket.y + speed
                aniRocket.direction = "down"
            if aniRocket.y > aniRocket.endY:
                aniRocket.y = aniRocket.y - speed
                aniRocket.direction = "up"
            aniShoot()

def animation():
    #Puts all the animation together
    if len(animationRockets) == 0:
        animationRockets.append(aniRocket(600, 200, TEAL, 2, "up", 600, 200, 600, 200))
        animationRockets.append(aniRocket(200, 200, PURPLE, 1, "up", 200, 200, 200, 200))
        animationRockets.append(aniRocket(200, 600, GREEN, 3, "up", 200, 600, 200, 600))
        animationRockets.append(aniRocket(600, 600, PINK, 4, "up", 600, 600, 600, 600))
        aDots1 = []
        aDots2 = []
        aDots3 = []
        aDots4 = []
        animationDots.append(aDots1)
        animationDots.append(aDots2)
        animationDots.append(aDots3)
        animationDots.append(aDots4)
    for rocket in animationRockets:
        aniRocketSteering(rocket)

#Controls
def keyControls(rocket, left, right, up, down, Height, Width):
    #Keyboard controls
    if rocket.timeOfDeath < time.time() - 1:
        keys = pygame.key.get_pressed()
        if keys[left] and rocket.x > 0:
            rocket.x -= speed
            rocket.direction = "left"
            shoot(rockets, rocket)
        if keys[right] and rocket.x < Width:
            rocket.x += speed
            rocket.direction = "right"
            shoot(rockets, rocket)
        if keys[up] and rocket.y > 0:
            rocket.y -= speed
            rocket.direction = "up"
            shoot(rockets, rocket)
        if keys[down] and rocket.y < Height - 10:
            rocket.y += speed
            rocket.direction = "down"
            shoot(rockets, rocket)

def joystickControls(rocket, joystick):
    #Controlling rockets with joysticks
    if rocket.timeOfDeath < time.time()-1:
        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        if x > 0 and rocket.x > 0:
            rocket.x -= speed
            rocket.direction = "left"
            shoot(rockets, rocket)
        if x == -1 and rocket.x < Width:
            rocket.x += speed
            rocket.direction = "right"
            shoot(rockets, rocket)
        if y > 0 and rocket.y > 0:
            rocket.y -= speed
            rocket.direction = "up"
            shoot(rockets, rocket)
        if y == -1 and rocket.y < Height:
            rocket.y += speed
            rocket.direction = "down"
            shoot(rockets, rocket)

def getArcButton():
    #Get which arcade button is being pressed
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            button = joystick.get_button(i)
            if joystick.get_button(i) == 1:
                return i

#Buttons
def drawButtons(selected):
    #Put the buttons on screen with an arrow pointing to the selected button
    for i in range(len(buttons)):
        text(buttons[i].text, 'impact', buttons[i].size, buttons[i].colour, buttons[i].x, buttons[i].y)
    if selected >= 0:
        arrowPos = ((buttons[selected].x - 15, buttons[selected].y + 25), (buttons[selected].x - 45, buttons[selected].y + 35),
                (buttons[selected].x - 45, buttons[selected].y + 15))
    else:
        arrowPos = ((850, 850), (825, 825), (810, 810))
    pygame.draw.polygon(screen, WHITE, arrowPos)

def scrollOptions(selection, options):
    #Use keyboard or joystick to scroll through things
    keys = pygame.key.get_pressed()
    # If there's a joystick connected, scroll with joystick
    if pygame.joystick.get_count() > 0:
        if joysticks[0].get_axis(1) > 0: #joystick up
            if selection == 0 or selection == -1:
                selection = len(options) - 1
            else:
                selection = selection - 1
        elif joysticks[0].get_axis(1) == -1: #joystick down
            if selection < len(options) - 1:
                selection = selection + 1
            else:
                selection = 0

    # If no joystick, scroll with keys
    elif keys[pygame.K_DOWN]:
        # increment the 'selection' variable and then mod with the len(buttons)
        if selection < len(options)-1:
            selection = selection + 1
        else:
            selection = 0
    elif keys[pygame.K_UP]:
        if selection == 0 or selection == -1:
            selection = len(options)-1
        else:
            selection = selection - 1
    return selection

def buttonSound():
    pygame.mixer.music.load('button.mp3')
    pygame.mixer.music.play()

def playMusic():
    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.play(-1)

#Text
def text(words, font, size, colour, x, y):
    # create text
    myfont = pygame.font.SysFont(font, size)
    textA = myfont.render(words, False, colour)
    screen.blit(textA, (x, y))

def centreText(words, size, colour, y):
    #create centred text
    myfont = pygame.font.SysFont('impact', size)
    textA = myfont.render(words, False, colour)
    text_rect = textA.get_rect(center=(800/ 2, y))
    screen.blit(textA, text_rect)

def playerNameInput(name, selectedLetter):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    name[selectedLetter] = scrollOptions(name[selectedLetter], letters)
    key = pygame.key.get_pressed()
    if len(joysticks) > 0:
        arcButton = getArcButton()
        if arcButton == 2 and selectedLetter < 3:
            selectedLetter = selectedLetter + 1
    elif key[pygame.K_SPACE] and selectedLetter < 3:
            selectedLetter = selectedLetter + 1
    return name, selectedLetter

def writeName(name):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    nameLetters = letters[name[0]] + letters[name[1]] + letters[name[2]]
    return nameLetters

#Files
def sortScores(file):
    #sort Scoreboard.txt by score, then by time
    with open(file, "r") as file1:
        f_list = [str(i) for line in file1 for i in line.split('\n') if i.strip()]

    # seperate out scores and times
    gameData = []
    scores = []
    times = []
    names = []
    highScoreList = []
    for i in range(len(f_list)):
        gameData.append(f_list[i].split(","))
    for i in range(len(gameData)):
        scores.append(int(gameData[i][0]))
        times.append(float(gameData[i][1]))
        names.append(gameData[i][2])
    while len(scores) > 0:
        # sort by highest scores, then find lowest times
        highScore = 0
        lowestTime = 2147483647
        highScoreTimes = []
        bestScoreIndex = []

        # get the highest score
        for i in range(len(scores)):
            if scores[i] > highScore:
                highScore = scores[i]

        # get the indices of the highest scores
        for i in range(len(scores)):
            if scores[i] == highScore:
                highScoreTimes.append(times[i])

        # find the lowest time with that scoreS
        for i in range(len(highScoreTimes)):
            if highScoreTimes[i] < lowestTime:
                lowestTime = highScoreTimes[i]

        #Find the index of the best score
        for i in range(len(times)):
            if times[i] == lowestTime and scores[i] == highScore:
                bestScoreIndex.append(i)

        # writing top scores
        counter = 0
        for i in range(len(bestScoreIndex)):
            highScoreList.append(
                str(scores[bestScoreIndex[i] - counter]) + "," + str(times[bestScoreIndex[i] - counter]) + "," + names[bestScoreIndex[i]] + "\n")
            del scores[bestScoreIndex[i] - counter]
            del times[bestScoreIndex[i] - counter]
            del names[bestScoreIndex[i] - counter]
            counter = counter + 1

    f = open('Scoreboard.txt', 'w').close()
    f = open("Scoreboard.txt", "a+")
    for i in range(len(highScoreList)):
        f.write(highScoreList[i])
    f.close()

def writeHighScores(score, gameTime, playerName):
    #Add a new score to the scoreboard
    f = open("Scoreboard.txt", "a+")
    scoreTEXT = str(score) + "," + str(gameTime) + "," + playerName + "\n"
    f.write(scoreTEXT)
    f.close()
    sortScores("Scoreboard.txt")

def printHighScores():
    #Write out the top 7 scores to the screen
    f = open("Scoreboard.txt", "a+")
    with open("Scoreboard.txt", "r") as file1:
        f_list = [str(i) for line in file1 for i in line.split('\n') if i.strip()]
    # seperate out scores and times
    gameData = []
    scores = []
    times = []
    names = []
    colour = 0
    for i in range(len(f_list)):
        gameData.append(f_list[i].split(","))
    for i in range(len(gameData)):
        scores.append(int(gameData[i][0]))
        times.append(float(gameData[i][1]))
        names.append(gameData[i][2])
    numScores = 7
    if len(scores) < 7:
        numScores = len(scores)
    for i in range(numScores):
        mins = int(times[i]/60)
        secs = int(times[i]%60)
        secs = str(secs)
        while len(secs) < 2:
            secs = "0" + secs
        txt = str(i+1) + ". " + names[i] + ": "+ str(scores[i]) + " Pts, " + str(mins) + ":" + str(secs)
        if i == 0:
            colour = RED2
        if i == 1:
            colour = RED1
        if i == 2:
            colour = YELLOW
        if i == 3:
            colour = GREEN
        if i == 4:
            colour = GREEN1
        if i == 5:
            colour = TEAL
        if i == 6:
            colour = PURPLE

        centreText(txt, 50, colour, (i*70)+ 250)

def write(words):
    #Append line to a text file
    f = open("Log.txt", "a+")
    f.write(words + "\n")
    f.close()

#Maze
def genGrid(size):
    #make the grid for the maze
    grid = []
    for x in range(size):
        grid.append([])
        for y in range(size):
            if y == 0:
                grid[x].append(Square(True, True, True, True, x, y, True))
            else:
                grid[x].append(Square(True, True, True, True, x, y, False))
    currentX = int(random.random() * size)
    currentY = int(random.random() * size-1) + 1
    currentSquare = grid[currentX][currentY]
    currentSquare.visited = True
    turnList.append(currentSquare)
    return grid, turnList, currentSquare

def unvisited(grid, size, currentSquare):
    #Check if any squares of the maze are unconnected to the rest
    if currentSquare.x > 0:
        if not grid[currentSquare.x-1][currentSquare.y].visited:
            return True
    if currentSquare.x < size-1:
        if not grid[currentSquare.x+1][currentSquare.y].visited:
            return True
    if currentSquare.y > 0:
        if not grid[currentSquare.x][currentSquare.y-1].visited:
            return True
    if currentSquare.y < size-1:
        if not grid[currentSquare.x][currentSquare.y+1].visited:
            return True
    return False

def makeMaze(grid, size, turnList, currentSquare):
    #Making a random path through the squares using a depth-first algorithm
    nextSquare = int(random.random()*4) #0 = left, 1 = up, 2 = right, 3 = down
    moveFwd = unvisited(grid, size, currentSquare)
    while moveFwd:
        if nextSquare == 0: #move left
            if currentSquare.x > 0:
                if grid[currentSquare.x-1][currentSquare.y].visited == False:
                    currentSquare.wWall = False
                    currentSquare = grid[currentSquare.x-1][currentSquare.y]
                    currentSquare.eWall = False
                    currentSquare.visited = True
                    turnList.append(currentSquare)
                    return turnList, currentSquare
                else:
                    nextSquare = 1
            else:
                nextSquare = 1
        if nextSquare == 1: #move up
            if currentSquare.y > 0:
                if grid[currentSquare.x][currentSquare.y-1].visited == False:
                    currentSquare.nWall = False
                    currentSquare = grid[currentSquare.x][currentSquare.y-1]
                    currentSquare.sWall = False
                    currentSquare.visited = True
                    turnList.append(currentSquare)
                    return turnList, currentSquare
                else:
                    nextSquare = 2
            else:
                nextSquare = 2
        if nextSquare == 2: #move right
            if currentSquare.x < size - 1:
                if not grid[currentSquare.x+1][currentSquare.y].visited:
                    currentSquare.eWall = False
                    currentSquare = grid[currentSquare.x+1][currentSquare.y]
                    currentSquare.wWall = False
                    currentSquare.visited = True
                    turnList.append(currentSquare)
                    return turnList, currentSquare
                else:
                    nextSquare = 3
            else:
                nextSquare = 3
        if nextSquare == 3: #move down
            if currentSquare.y < size - 1:
                if grid[currentSquare.x][currentSquare.y+1].visited == False:
                    currentSquare.sWall = False
                    currentSquare = grid[currentSquare.x][currentSquare.y+1]
                    currentSquare.nWall = False
                    currentSquare.visited = True
                    turnList.append(currentSquare)
                    return turnList, currentSquare
                else:
                    nextSquare = 0
            else:
                nextSquare = 0
    if moveFwd == False:
        if len(turnList) > 0:
            del turnList[len(turnList)-1] #back up
            currentSquare = turnList[len(turnList)-1]
        return turnList, currentSquare

def makePath(grid, size, turnList, currentSquare):
    #Puts the maze all together
    for x in range(size):
        for y in range(size):
            if not grid[x][y].visited:  # if any squares are unvisited,
                info2 = makeMaze(grid, size, turnList, currentSquare)
                turnList = info2[0]
                currentSquare = info2[1]
    return turnList, currentSquare

def makeBloops(size):
    #Fills the maze with points
    for x in range(size):
        for y in range(size-1):
            bloops.append(Bloop(int((x+0.5)*Width/size), int((y+1.5)*Height/size)))

#Collisions + losing lives
def dist(objA, objB):
    # calc distance between two objects
    return math.hypot(objA.x - objB.x, objA.y - objB.y)

def explosionStart(x, y, colour):
    #Create 8 particles at the site of the collision
    for i in range(8):
        particles.append(Particle(x, y, colour, x, y))

def exploding(explosions):
    #Spead particles out over a given area
    spread = 50
    rate = 5
    for i in range(explosions):
        if len(particles) >= 7+(i*8):
           if particles[0+(i*8)].x < particles[0+(i*8)].startX + spread:
                particles[0+(i*8)].x = particles[0+(i*8)].x + rate
                particles[1+(i*8)].x = particles[1+(i*8)].x + 0.70714285*rate
                particles[1+(i*8)].y = particles[1+(i*8)].y + 0.70714285*rate
                particles[2+(i*8)].y = particles[2+(i*8)].y + rate
                particles[3+(i*8)].x = particles[3+(i*8)].x - 0.70714285*rate
                particles[3+(i*8)].y = particles[3+(i*8)].y + 0.70714285*rate
                particles[4+(i*8)].x = particles[4+(i*8)].x - 0.70714285*rate
                particles[5+(i*8)].x = particles[5+(i*8)].x - 0.70714285*rate
                particles[5+(i*8)].y = particles[5+(i*8)].y - 0.70714285*rate
                particles[6+(i*8)].y = particles[6+(i*8)].y - rate
                particles[7+(i*8)].x = particles[7+(i*8)].x + 0.70714285*rate
                particles[7+(i*8)].y = particles[7+(i*8)].y - 0.70714285*rate
           else:
                explosions = explosions -1
                for i in range(8):
                    if len(particles) > 0:
                        del particles[0]
    return explosions

def lifeLost(lives, rocket, explosions, explosionStarted):
    #Stuff to do if a life is lost during maze mode
    lives = lives - 1
    if not explosionStarted:
        explosionStart(rocket.x, rocket.y, rocket.colour)
        explosions = explosions + 1
    rocket.timeOfDeath = time.time()
    rocket.x = rocket.startX
    rocket.y = rocket.startY
    return lives, explosions

#Core methods
def render(gameState, winner, endTime, endOfRound, startTime, players, team, grid, turnList, currentSquare, mazeCreated, buttonsMade, selected, maze, points, lives, explosions, name, selectedLetter, scoreWritten):
    #All the calculations are here
    key = pygame.key.get_pressed()
    if key[pygame.K_x]: #Return to main menu
        del buttons[:]
        buttonsMade = False
        del rockets[:]
        del bloops[:]
        gameState = "Menu"
    if gameState == "Menu":
        keys = pygame.key.get_pressed()
        #Resetting
        del rockets[:]
        del bloops[:]
        del dots[:]
        del dots2[:]
        del dots3[:]
        del dots4[:]
        del particles[:]
        team = False
        maze = False
        mazeCreated = False
        explosions = 0

        write("selected: " + str(selected))
        #button stuff
        if not buttonsMade:
            buttons.append(Button("2 Players", 60, PINK, 250, 300))
            buttons.append(Button("3 Players", 60, RED1, 250, 375))
            buttons.append(Button("4 Players", 60, GREEN, 250, 450))
            buttons.append(Button("Instructions", 60, TEAL, 250, 525))
            buttons.append(Button("High Scores", 60, PURPLE, 250, 600))
            selected = -1
            buttonsMade = True
        if len(joysticks) > 0:
            arcButton = getArcButton()
            if arcButton == 2:
                buttonsMade = False
                del buttons[:]
                if selected == 0:
                    gameState = "ToggleMaze"
                    players = 2
                elif selected == 1:
                    gameState = "ToggleMaze"
                    players = 3
                elif selected == 2:
                    gameState = "ToggleMaze"
                    players = 4
                elif selected == 3:
                    gameState = "Instructions"
                elif selected == 4:
                    gameState = "High scores"
                buttonSound()
                selected = -1
        elif keys[pygame.K_SPACE]:
            buttonsMade = False
            del buttons[:]
            if selected == 0:
                gameState = "ToggleMaze"
                players = 2
            elif selected == 1:
                gameState = "ToggleMaze"
                players = 3
            elif selected == 2:
                gameState = "ToggleMaze"
                players = 4
            elif selected == 3:
                gameState = "Instructions"
            elif selected == 4:
                gameState = "High scores"
            buttonSound()
            selected = -1
        selected = scrollOptions(selected, buttons)
    elif gameState == "Instructions":
        #All this code is button stuff
        if not buttonsMade:
            buttons.append(Button("Main Menu", 60, PINK, 250, 700))
            buttonsMade = True
        keys = pygame.key.get_pressed()
        selected = scrollOptions(selected, buttons)
        if len(joysticks) > 0:
            arcButton = getArcButton()
            if arcButton == 2 and selected == 0:
                del buttons[:]
                buttonsMade = False
                gameState = "Menu"
                buttonSound()
                selected = -1
        elif keys[pygame.K_SPACE] and selected == 0:
            del buttons[:]
            buttonsMade = False
            gameState = "Menu"
            buttonSound()
            selected = -1
    elif gameState == "High scores":
        # All this code is button stuff
        if not buttonsMade:
            buttons.append(Button("Main Menu", 60, PINK, 250, 700))
            buttonsMade = True
        keys = pygame.key.get_pressed()
        selected = scrollOptions(selected, buttons)
        if len(joysticks) > 0:
            arcButton = getArcButton()
            if arcButton == 2 and selected == 0:
                del buttons[:]
                buttonsMade = False
                gameState = "Menu"
                buttonSound()
                selected = -1
        elif keys[pygame.K_SPACE] and selected == 0:
            del buttons[:]
            buttonsMade = False
            gameState = "Menu"
            buttonSound()
            selected = -1
    elif gameState == "Team": # toggle team mode
        #More Buttons
        if not buttonsMade:
            buttons.append(Button("Play 2 vs 2", 75, GREEN2, 200, 400))
            buttons.append(Button("Play Free for All", 75, RED1, 150, 500))
            buttonsMade = True
        selected = scrollOptions(selected, buttons)
        keys = pygame.key.get_pressed()
        if len(joysticks) > 0:
            arcButton = getArcButton()
            if arcButton == 2:
                del buttons[:]
                buttonsMade = False
                if selected == 0:
                    team = True
                    gameState = "Play"
                    generateRockets(maze, players, team)
                    playMusic()
                    selected = -1
                    startTime = time.time()
                if selected == 1:
                    selected = -1
                    team = False
                    gameState = "Play"
                    startTime = time.time()
                    generateRockets(maze, players, team)
                    playMusic()
        elif keys[pygame.K_SPACE]:
            del buttons[:]
            buttonsMade = False
            if selected == 0:
                team = True
                gameState = "Play"
                generateRockets(maze, players, team)
                playMusic()
                startTime = time.time()
                selected = -1
            if selected == 1:
                selected = -1
                team = False
                gameState = "Play"
                startTime = time.time()
                generateRockets(maze, players, team)
                playMusic()
    elif gameState == "ToggleMaze":
        if not buttonsMade:
            buttons.append(Button("Co-op Maze Mode", 75, GREEN2, 200, 400))
            buttons.append(Button("Competitive Mode", 75, RED1, 150, 500))
            buttonsMade = True
        selected = scrollOptions(selected, buttons)
        keys = pygame.key.get_pressed()
        if len(joysticks) > 0:
            arcButton = getArcButton()
            if arcButton == 2:
                del buttons[:]
                buttonsMade = False
                if selected == 0:
                    generateRockets(maze, players, maze)
                    maze = True
                    gameState = "Play"
                    generateRockets(maze, players, team)
                    startTime = time.time()
                    playMusic()
                    selected = -1
                if selected == 1:
                    selected = -1
                    maze = False
                    if players == 4:
                        gameState = "Team"
                    else:
                        gameState = "Play"
                        startTime = time.time()
                        generateRockets(maze, players, team)
                    playMusic()
        elif keys[pygame.K_SPACE]:
            del buttons[:]
            buttonsMade = False
            if selected == 0:
                generateRockets(maze, players, maze)
                maze = True
                gameState = "Play"
                generateRockets(maze, players, team)
                startTime = time.time()
                playMusic()
                selected = -1
            if selected == 1:
                selected = -1
                maze = False
                if players == 4:
                    gameState = "Team"
                else:
                    gameState = "Play"
                    generateRockets(maze, players, team)
                    startTime = time.time()
                playMusic()
    elif gameState == "Play":  # main play state
        if maze == True and mazeCreated == False:
            info1 = genGrid(size)
            grid = info1[0]
            turnList = info1[1]
            currentSquare = info1[2]
            mazeCreated = True
            makeBloops(size)
            lives = 5
        # Rocket controls
        if len(joysticks) == 0:
            keyControls(rockets[0], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, Height, Width)
            keyControls(rockets[1], pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, Height, Width)
            if players > 2:
                keyControls(rockets[2], pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_g, Height, Width)
            if players == 4:
                keyControls(rockets[3], pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k, Height, Width)
        if len(joysticks) == 1:
            joystickControls(rockets[0], joysticks[0])
            keyControls(rockets[1], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, Height, Width)
            if players > 2:
                keyControls(rockets[2], pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, Height, Width)
            if players == 4:
                keyControls(rockets[3], pygame.K_f, pygame.K_h, pygame.K_t, pygame.K_g, Height, Width)
        if len(joysticks) == 2:
            joystickControls(rockets[0], joysticks[1])
            joystickControls(rockets[1], joysticks[0])
            if players > 2:
                keyControls(rockets[2], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, Height, Width)
            if players == 4:
                keyControls(rockets[3], pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, Height, Width)
        if len(joysticks) == 3:
            joystickControls(rockets[0], joysticks[1])
            joystickControls(rockets[1], joysticks[0])
            if players > 2:
                joystickControls(rockets[2], joysticks[2])
            if players == 4:
                keyControls(rockets[3], pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, Height, Width)
        if len(joysticks) == 4:
            joystickControls(rockets[0], joysticks[1])
            joystickControls(rockets[1], joysticks[0])
            if players > 2:
                joystickControls(rockets[2], joysticks[2])
            if players == 4:
                joystickControls(rockets[3], joysticks[3])
        # Dot functionality
        for dot in dots:
            if not team:
                if dist(rockets[1], dot) < 5:
                    if not maze:
                        winner = rockets[0]
                        endOfRound = True
                        endTime = time.time()
                        gameState = "End"
                    else:
                        lives = lives - 1
                        rockets[1].x = rockets[1].startX
                        rockets[1].y = rockets[1].startY
            if players > 2:
                if dist(rockets[2], dot) < 5:
                    if not maze:
                        winner = rockets[0]
                        endTime = time.time()
                        endOfRound = True
                        gameState = "End"
                    else:
                        lives = lives - 1
                        rockets[2].x = rockets[2].startX
                        rockets[2].y = rockets[2].startY
            if players > 3:
                if dist(rockets[3], dot) < 5:
                    if not maze:
                        winner = rockets[0]
                        endTime = time.time()
                        endOfRound = True
                        gameState = "End"
                    else:
                        rockets[3].x = rockets[3].startX
                        rockets[3].y = rockets[3].startY
        for dot in dots2:
            if not team:
                if dist(rockets[0], dot) < 5:
                    if not maze:
                        winner = rockets[1]
                        endTime = time.time()
                        endOfRound = True
                        gameState = "End"
                    else:
                        lives = lives - 1
                        rockets[0].x = rockets[0].startX
                        rockets[0].y = rockets[0].startY
            if players > 2:
                if dist(rockets[2], dot) < 5:
                    if not maze:
                        winner = rockets[1]
                        gameState = "End"
                        endTime = time.time()
                        endOfRound = True
                    else:
                        lives = lives - 1
                        rockets[2].x = rockets[2].startX
                        rockets[2].y = rockets[2].startY
            if players > 3:
                if dist(rockets[3], dot) < 5:
                    if not maze:
                        winner = rockets[1]
                        endTime = time.time()
                        endOfRound = True
                        gameState = "End"
                    else:
                        lives = lives - 1
                        rockets[3].x = rockets[3].startX
                        rockets[3].y = rockets[3].startY
        for dot in dots3:
            if dist(rockets[1], dot) < 5:
                if not maze:
                    winner = rockets[2]
                    endTime = time.time()
                    endOfRound = True
                    gameState = "End"
                else:
                    lives = lives - 1
                    rockets[1].x = rockets[1].startX
                    rockets[1].y = rockets[1].startY
            if dist(rockets[0], dot) < 5:
                if not maze:
                    winner = rockets[2]
                    endTime = time.time()
                    endOfRound = True
                    gameState = "End"
                else:
                    lives = lives - 1
                    rockets[0].x = rockets[0].startX
                    rockets[0].y = rockets[0].startY
            if players == 4:
                if not team:
                    if dist(rockets[3], dot) < 5:
                        if not maze:
                            winner = rockets[2]
                            endTime = time.time()
                            endOfRound = True
                            gameState = "End"
                        else:
                            lives = lives - 1
                            rockets[3].x = rockets[3].startX
                            rockets[3].y = rockets[3].startY
        for dot in dots4:
            if dist(rockets[0], dot) < 5:
                if not maze:
                    winner = rockets[3]
                    endTime = time.time()
                    endOfRound = True
                    gameState = "End"
                else:
                    lives = lives - 1
                    rockets[0].x = rockets[0].startX
                    rockets[0].y = rockets[0].startY
            if dist(rockets[1], dot) < 5:
                if not maze:
                    winner = rockets[3]
                    endTime = time.time()
                    endOfRound = True
                    gameState = "End"
                else:
                    lives = lives - 1
                    rockets[1].x = rockets[1].startX
                    rockets[1].y = rockets[1].startY
            if not team:
                if dist(rockets[2], dot) < 5:
                    if not maze:
                        winner = rockets[3]
                        endTime = time.time()
                        endOfRound = True
                        gameState = "End"
                    else:
                        lives = lives - 1
                        rockets[3].x = rockets[3].startX
                        rockets[3].y = rockets[3].startY
        if maze == True:
            #collecting points
            for bloop in bloops:
                for rocket in rockets:
                    if dist(rocket, bloop) < 15 and bloop.visable:
                        points = points + 25
                        bloop.visable = False
            #wall collision detection
            for x in range(size):
                for y in range(size):
                    for rocket in rockets:
                        explosionStarted = False
                        if grid[x][y].nWall:
                            if (y*Height/size) - 5 < rocket.y and (y*Height/size)+5 > rocket.y and x*Width/size < rocket.x and (x+1)*Width/size > rocket.x:
                                lives = lifeLost(lives, rocket, explosions, explosionStarted)[0]
                                explosions = lifeLost(lives, rocket, explosions, explosionStarted)[1]
                                explosionStarted = True
                        if grid[x][y].eWall:
                            if ((x+1)*Width/size) - 5 < rocket.x and ((x+1)*Width/size) + 5 > rocket.x and y*Height/size < rocket.y and (y+1)*Height/size > rocket.y:
                                lives = lifeLost(lives, rocket, explosions, explosionStarted)[0]
                                explosions = lifeLost(lives, rocket, explosions, explosionStarted)[1]
                                explosionStarted = True
                        if grid[x][y].sWall:
                            if ((y+1)*Height/size) - 5 < rocket.y and ((y+1)*Height/ size) + 5 > rocket.y and x*Width/size < rocket.x and (x+1)*Width/size > rocket.x:
                                lives = lifeLost(lives, rocket, explosions, explosionStarted)[0]
                                explosions = lifeLost(lives, rocket, explosions, explosionStarted)[1]
                                explosionStarted = True
                        if grid[x][y].wWall:
                            if (x*Width/size) - 5 < rocket.x and (x*Width/size) + 5 > rocket.x and y*Height/size < rocket.y and (y+1)*Height/size > rocket.y:
                                lives = lifeLost(lives, rocket, explosions, explosionStarted)[0]
                                explosions = lifeLost(lives, rocket, explosions, explosionStarted)[1]
                                explosionStarted = True
                        if rocket.y > Height - 9:
                            lives = lifeLost(lives, rocket, explosions, explosionStarted)[0]
                            explosions = lifeLost(lives, rocket, explosions, explosionStarted)[1]
                            explosionStarted = True
            exploding(explosions)

            #end of game detection
            gameFinished = True
            for bloop in bloops:
                if bloop.visable:
                    gameFinished = False
            if lives <= 0:
                gameFinished = True
                #time up
            timeLimit = 300 / players
            gameTime = time.time() - startTime
            timeRemaining = timeLimit - gameTime
            if timeRemaining < 0:
                gameFinished = True
            if gameFinished:
                gameState = "End"
                winner = 5
                endOfRound = True
                endTime = time.time()
                scoreWritten = False
                name = [0, 0, 0, 0]
                selectedLetter = 0
    elif gameState == "End":
        #reset all existing game objects
        del dots[:]
        del dots2[:]
        del dots3[:]
        del dots4[:]
        del rockets[:]
        if not buttonsMade:
            buttons.append(Button("Main Menu", 70, TEAL, 250, 600))
            buttons.append(Button("Replay", 70, PURPLE, 250, 700))
            buttonsMade = True
        keys = pygame.key.get_pressed()

        if maze:
            nameInfo = playerNameInput(name, selectedLetter)
            name = nameInfo[0]
            selectedLetter = nameInfo[1]
            if selectedLetter == 3:
                gameTime = endTime - startTime
                if not scoreWritten:
                    writeHighScores(points, gameTime, writeName(name))
                    scoreWritten = True
                selected = scrollOptions(selected, buttons)
                if len(joysticks) > 0:
                    arcButton = getArcButton()
                    if arcButton == 2:
                        if selected == 0:
                            gameState = "Menu"
                            selected = -1
                            del buttons[:]
                            lives = 5
                            points = 0
                            buttonsMade = False
                            mazeCreated = False
                        if selected == 1:
                            gameState = "Play"
                            generateRockets(maze, players, team)
                            startTime = time.time()
                            selected - 1
                            del buttons[:]
                            lives = 5
                            points = 0
                            buttonsMade = False
                            mazeCreated = False
                elif keys[pygame.K_SPACE]:
                    if selected == 0:
                        gameState = "Menu"
                        selected = -1
                        del buttons[:]
                        lives = 5
                        points = 0
                        buttonsMade = False
                        mazeCreated = False
                    if selected == 1:
                        gameState = "Play"
                        generateRockets(maze, players, team)
                        startTime = time.time()
                        selected = -1
                        del buttons[:]
                        lives = 5
                        points = 0
                        buttonsMade = False
                        mazeCreated = False
        else:
            selected = scrollOptions(selected, buttons)
            if len(joysticks) > 0:
                arcButton = getArcButton()
                if arcButton == 2:
                    del buttons[:]
                    lives = 5
                    points = 0
                    buttonsMade = False
                    mazeCreated = False
                    if selected == 0:
                        gameState = "Menu"
                        selected = -1
                    if selected == 1:
                        gameState = "Play"
                        generateRockets(maze, players, team)
                        startTime = time.time()
                        selected -1
            elif keys[pygame.K_SPACE]:
                del buttons[:]
                lives = 5
                points = 0
                buttonsMade = False
                mazeCreated = False
                if selected == 0:
                    gameState = "Menu"
                    selected = -1
                if selected == 1:
                    gameState = "Play"
                    generateRockets(maze, players, team)
                    startTime = time.time()
                    selected = -1

    return gameState, winner, endTime, endOfRound, startTime, players, team, grid, turnList, currentSquare, mazeCreated, buttonsMade, selected, maze, points, lives, explosions, name, selectedLetter, scoreWritten

def draw(gameState, winner, grid, size, mazeCreated, selected, points, lives, gameTime, startTime, name): # Display on screen
    #Putting stuff on the screen
    if gameState == "Menu":
        screen.fill(BLUE)
        #animate rockets
        animation()
        for aniRocket in animationRockets:
            if aniRocket.direction == "up":
                rocketPos = ((aniRocket.x, aniRocket.y - 15), (aniRocket.x - 10, aniRocket.y + 15), (aniRocket.x + 10, aniRocket.y + 15))
            if aniRocket.direction == "down":
                rocketPos = ((aniRocket.x, aniRocket.y + 15), (aniRocket.x - 10, aniRocket.y - 15), (aniRocket.x + 10, aniRocket.y - 15))
            if aniRocket.direction == "left":
                rocketPos = ((aniRocket.x - 15, aniRocket.y), (aniRocket.x + 15, aniRocket.y - 10), (aniRocket.x + 15, aniRocket.y + 10))
            if aniRocket.direction == "right":
                rocketPos = ((aniRocket.x + 15, aniRocket.y), (aniRocket.x - 15, aniRocket.y - 10), (aniRocket.x - 15, aniRocket.y + 10))
            pygame.draw.polygon(screen, aniRocket.colour, rocketPos)
        # draw all dots
        for aDots in animationDots:
            for dot in aDots:
                dotPos = (dot.x, dot.y)
                pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)
        text("tRACER", 'impact', 100, PURPLE, 245, 145)
        text("tRACER", 'impact', 100, TEAL, 250, 150)
        if len(buttons) > 0:
            drawButtons(selected)
    if gameState == "Instructions":
        screen.fill(BLUE)
        text("INSTRUCTIONS", 'impact', 100, PURPLE, 100, 75)
        text("INSTRUCTIONS", 'impact', 100, TEAL, 105, 80)
        text("As you move your rocket, you leave behind a trail.", 'impact', 30, GREEN2, 100, 225)
        text("You can pass through your own trail, but other", 'impact', 30, GREEN2, 100, 275)
        text("players can't.", 'impact', 30, GREEN2, 100, 325)
        text("Original mode: Use your trail to cut off another player", 'impact', 30, RED2, 100, 375)
        text("Team mode: You and your teammate can cross each", 'impact', 30, PURPLE, 100, 425)
        text("other's paths. Cut off another team's player to win!", 'impact', 30, PURPLE, 100, 475)
        text("Maze mode: Navigate a maze and collect points.", 'impact', 30, TEAL, 100, 525)
        text("Be careful not to run into walls or other players' paths!", 'impact', 30, TEAL, 100, 575)
        text("You all win when all points are collected", 'impact', 30, TEAL, 100, 625)

        if len(buttons) > 0:
            drawButtons(selected)
    if gameState == "High scores":
        screen.fill(BLUE)
        text("HIGH SCORES", 'impact', 100, PURPLE, 125, 75)
        text("HIGH SCORES", 'impact', 100, TEAL, 130, 80)
        if len(buttons) > 0:
            drawButtons(selected)
        #Write out high scores
        printHighScores()
    if gameState == "Team":
        screen.fill(BLUE)
        if len(buttons) > 0:
            drawButtons(selected)
        text("Team mode", 'impact', 100, PURPLE, 180, 245)
        text("Team mode", 'impact', 100, TEAL, 185, 250)
    if gameState == "ToggleMaze":
        screen.fill(BLUE)
        if len(buttons) > 0:
            drawButtons(selected)
        text("Maze mode", 'impact', 100, PURPLE, 180, 245)
        text("Maze mode", 'impact', 100, TEAL, 185, 250)
    if gameState == "Play":
        screen.fill(BLUE)
        for rocket in rockets:
            if rocket.direction == "up":
                rocketPos = ((rocket.x, rocket.y - 15), (rocket.x - 10, rocket.y + 15), (rocket.x + 10, rocket.y + 15))
            if rocket.direction == "down":
                rocketPos = ((rocket.x, rocket.y + 15), (rocket.x - 10, rocket.y - 15), (rocket.x + 10, rocket.y - 15))
            if rocket.direction == "left":
                rocketPos = ((rocket.x - 15, rocket.y), (rocket.x + 15, rocket.y - 10), (rocket.x + 15, rocket.y + 10))
            if rocket.direction == "right":
                rocketPos = ((rocket.x + 15, rocket.y), (rocket.x - 15, rocket.y - 10), (rocket.x - 15, rocket.y + 10))
            if rocket.timeOfDeath < time.time() - 1:
                pygame.draw.polygon(screen, rocket.colour, rocketPos)
        # draw all dots
        for dot in dots:
            dotPos = (dot.x, dot.y)
            pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)
        for dot in dots2:
            dotPos = (dot.x, dot.y)
            pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)
        for dot in dots3:
            dotPos = (dot.x, dot.y)
            pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)
        for dot in dots4:
            dotPos = (dot.x, dot.y)
            pygame.draw.circle(screen, dot.colour, dotPos, 5, 0)
        if mazeCreated == True:
            for x in range(size):
                for y in range(size):
                    if y == 0:
                        pygame.draw.line(screen, WHITE, (x * Width / size, y * Height / size),
                                         ((x + 1) * Width / size, y * Height / size), 2)
                        pygame.draw.line(screen, WHITE, (x * Width / size, (y + 1) * Height / size),
                                         ((x + 1) * Width / size, (y + 1) * Height / size), 2)
                    else:
                        if grid[x][y].nWall:
                            pygame.draw.line(screen, WHITE, (x * Width / size, y * Height / size),
                                             ((x + 1) * Width / size, y * Height / size), 2)
                        if grid[x][y].eWall:
                            pygame.draw.line(screen, WHITE, ((x + 1) * Width / size, y * Height / size),
                                             ((x + 1) * Width / size, (y + 1) * Height / size), 2)
                        if grid[x][y].sWall:
                            pygame.draw.line(screen, WHITE, (x * Width / size, (y + 1) * Height / size),
                                             ((x + 1) * Width / size, (y + 1) * Height / size), 2)
                        if grid[x][y].wWall:
                            pygame.draw.line(screen, WHITE, (x * Width / size, y * Height / size),
                                             (x * Width / size, (y + 1) * Height / size), 2)
            # timing
            timeLimit = 300 / players
            gameTime = time.time() - startTime
            timeRemaining = timeLimit - gameTime
            minsLeft = int(timeRemaining/60)
            secsLeft = str(int(timeRemaining%60))
            text("Points: " + str(points), 'impact', 40, WHITE, 80, 20)
            text("Lives: " + str(lives), 'impact', 40, WHITE, 600, 20)
            if len(secsLeft) == 1:
                secsLeft = "0"+secsLeft
            timeText = "Time Left: " + str(minsLeft) + ":" + secsLeft
            text(timeText, 'impact', 40, RED1, 300, 20)
        for bloop in bloops:
            if bloop.visable:
                bloopPos = (bloop.x, bloop.y)
                pygame.draw.circle(screen, WHITE, bloopPos, 8, 0)
        for particle in particles:
            particlePos = (int(particle.x), int(particle.y))
            pygame.draw.circle(screen, particle.colour, particlePos, 3, 0)
    if gameState == "End":  # displays endgame text
        screen.fill(BLUE)
        if winner == 5 and lives > 0:
            colour = TEAL
        elif winner == 5 and lives <= 0:
            colour = RED1
        else:
            colour = winner.colour
        centreText("GAME OVER", 70, colour, 150)
        if not team and not maze:
            centreText("Player " + str(winner.playerNum) + " wins!", 100, colour, 350)
        elif team:
            if winner.playerNum == 1 or winner.playerNum == 2:
                centreText("Green Team wins!", 90, colour, 300)
            else:
                centreText("Red Team wins!", 90, colour, 300)
        if maze:
            centreText("Your name: " + writeName(name), 80, colour, 350)
            if selectedLetter == 0:
                x = 545
                y = 395
            if selectedLetter == 1:
                x = 590
                y = 395
            if selectedLetter == 2:
                x = 635
                y = 395
            if selectedLetter == 3:
                x = 850
                y = 850
            letterArrowPos = ((x, y - 5), (x - 15, y + 10), (x + 15, y + 10))
            pygame.draw.polygon(screen, WHITE, letterArrowPos)
            if points == 2250:
                centreText("You win!", 100, PURPLE, 250)
                centreText("Your time: " + str(int(gameTime / 60)) + "mins, " + str(int(gameTime % 60)) + " secs", 50, GREEN, 450)
                centreText(str(points) + " Points", 50, PINK, 550)
            else:
                centreText("You lose...", 100, colour, 250)
                centreText("Your time: " + str(int(gameTime/60)) + "mins, " + str(int(gameTime%60)) + " secs", 50, colour, 450)
                centreText(str(points) + " Points", 50, colour, 550)
        if len(buttons) > 0:
            drawButtons(selected)

# Ready a new log
f = open("Log.txt", "a+")
f = open('Log.txt', 'w').close()
# Joystick setup
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
# Main method
while not done:
    if gameState == "Play":
        clock.tick(120)
    else:
        clock.tick(8)

    # quit if window is closed or q is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        done = True

    # update game info
    info = render(gameState, winner, endTime, endOfRound, startTime, players, team, grid, turnList, currentSquare, mazeCreated, buttonsMade, selected, maze, points, lives, explosions, name, selectedLetter, scoreWritten)
    gameState = info[0]
    winner = info[1]
    players = info[5]
    team = info[6]
    grid = info[7]
    turnList = info[8]
    currentSquare = info[9]
    mazeCreated = info[10]
    buttonsMade = info[11]
    selected = info[12]
    maze = info[13]
    points = info[14]
    lives = info[15]
    explosions = info[16]
    name = info[17]
    selectedLetter = info[18]
    scoreWritten = info[19]

    if mazeCreated:
        info3 = makePath(grid, size, turnList, currentSquare)
        turnList = info3[0]
        currentSquare = info3[1]

    # game times
    endTime = info[2]
    endOfRound = info[3]
    startTime = info[4]
    gameTime = endTime - startTime

    draw(gameState, winner, grid, size, mazeCreated, selected, points, lives, gameTime, startTime, name)

    pygame.display.flip()

pygame.quit()