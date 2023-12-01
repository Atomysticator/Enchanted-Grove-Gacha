from cmu_graphics import *
import random

from playerAndFae import Player
import utils

# Exploration Mechanics
class Cell:
    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.hasRoom = False
        self.visible = False
    
    def onPlayerEnter(self, player, app):
        # Handle player entering the cell
        if self.hasRoom:
            # Transition to room event screen
            app.screen = 'roomEvent'
            app.currentRoom = self.room
            # Initialize room event
            self.room.startChallenge(app, player)
            # Render room event screen

    
    def draw(self, app):
        x, y, size = self.x * self.cellSize, self.y * self.cellSize, self.cellSize
        if self.hasRoom:
            drawRect(x, y, size, size, fill = 'blue' if self.room.isCompleted == False else 'red', border = None, opacity = 60) 
        if self == app.maze.endCell:
            drawRect(x, y, size, size, fill = 'green', border = None, opacity = 60)
        if self.walls['top']:
            drawLine(x, y, x + size, y, lineWidth=2)
        if self.walls['right']:
            drawLine(x + size, y, x + size, y + size, lineWidth=2)
        if self.walls['bottom']:
            drawLine(x, y + size, x + size, y + size, lineWidth=2)
        if self.walls['left']:
            drawLine(x, y, x, y + size, lineWidth=2)

    def drawFog(self, app):
        x, y, size = self.x * self.cellSize, self.y * self.cellSize, self.cellSize
        drawRect(x, y, size, size, fill = 'lightGrey', border = None, opacity = 60)

    def generateRoom(self):
        self.room = Room()

class Maze:
    def __init__(self, app, width, height):
        self.width = width
        self.height = height
        self.cellSize = min(app.width/width, app.height/height)
        self.grid = [[Cell(x, y, self.cellSize) for y in range(height)] for x in range(width)]
        self.roomCount = 0

    def generateMaze(self, app):
        for row in self.grid:
            for cell in row:
                cell.visited = False

        stack = []
        startX, startY = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        app.player.setPosition(startX, startY)
        currentCell = self.grid[startX][startY]
        currentCell.visited = True
        stack.append(currentCell)

        while stack:
            currentCell = stack.pop()
            neighbors = self.getUnvisitedNeighbors(currentCell)
            if neighbors:
                stack.append(currentCell)
                chosenCell = random.choice(neighbors)
                self.removeWall(currentCell, chosenCell)
                chosenCell.visited = True
                if random.random() < 0.1: # 10% chance to become a room
                    chosenCell.hasRoom = True
                    chosenCell.generateRoom()
                    self.roomCount += 1
                stack.append(chosenCell)

        self.endCell = chosenCell

        # ensure there are never 0 rooms
        while self.roomCount == 0:
            randomCell = random.choice(random.choice(self.grid))
            if randomCell.hasRoom == False and randomCell != self.endCell:
                self.roomCount += 1
                randomCell.hasRoom = True
                randomCell.generateRoom()

    def draw(self, app):
        for row in self.grid:
            for cell in row:
                if cell.visible == True:
                    cell.draw(app)
                else:
                    cell.drawFog(app)

    def getUnvisitedNeighbors(self, cell):
        neighbors = []
        if cell.x > 0 and not self.grid[cell.x - 1][cell.y].visited:
            neighbors.append(self.grid[cell.x - 1][cell.y])
        if cell.x < self.width - 1 and not self.grid[cell.x + 1][cell.y].visited:
            neighbors.append(self.grid[cell.x + 1][cell.y])
        if cell.y > 0 and not self.grid[cell.x][cell.y - 1].visited:
            neighbors.append(self.grid[cell.x][cell.y - 1])
        if cell.y < self.height - 1 and not self.grid[cell.x][cell.y + 1].visited:
            neighbors.append(self.grid[cell.x][cell.y + 1])
        return neighbors

    def removeWall(self, current, next):
        dx = current.x - next.x
        dy = current.y - next.y
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        elif dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False
    
    def finished(self, app):
        app.player.earnCurrency(30*app.roomsComplete)
        self.startDungeon(app)

    def startDungeon(self, app):
        app.maze = Maze(app, random.randrange(2,5) +  app.player.collectionSize//10, 
                        random.randrange(2,5) +  app.player.collectionSize//10)
        app.maze.generateMaze(app)
        app.player.calculateVisibility(app.maze)
        app.screen = 'dungeon'
        app.roomsComplete = 0
        

class Room:
    def __init__(self):      
        challengeTypes = ["Battle", "Mystery", "Puzzle"]
        faeAttributes = ["category", "subType", "rarity"]
        faeValues = ["Water", "Fire", "Epic", "Mystic"]

        self.challengeType = random.choice(challengeTypes)
        self.requiredAttribute = random.choice(faeAttributes)
        self.requiredValue = random.choice(faeValues)
        self.isCompleted = False

    def completeChallenge(self, app, result):
        self.isCompleted = True
        if result == True:
            app.player.earnCurrency(self.event.reward)
            app.roomsComplete += 1
            app.eventMessage = 'You Won!'
        else:
            app.player.lives -= 1
            if app.player.lives <=0:
                return 'Game Over'
            app.eventMessage = f'You Lost :( Lives Left: {app.player.lives}'
        app.screen = 'dungeon'

    def eventChoiceHandler(self, app, key):
        result = self.event.checkSuccess(key, app.player)
        return self.completeChallenge(app, result)

    def startChallenge(self, app, player):
        self.event = random.choice(app.events)

    def __str__(self):
        return f"Room(Challenge: {self.challengeType}, Required Attribute: {self.requiredAttribute}, Required Value: {self.requiredValue}, Completed: {self.isCompleted})"

class Event:
    def __init__(self, name, description, choices, answers, reward, size=20):
        self.name = name
        self.choices = choices
        self.answers = answers
        self.reward = reward
        self.size = size
        self.description = description
    
    def drawChoices(self, app):
        drawLabel(self.name, app.width/2, 50, size=30)
        drawLabel(self.description, app.width/2, 100, size=self.size)
        # Display choice options
        drawLabel(f'↑ - {self.choices["up"]}', app.width/2, 150, size=self.size)
        drawLabel(f'↓ - {self.choices["down"]}', app.width/2, 200, size=self.size)
        drawLabel(f'← - {self.choices["left"]}', app.width/2, 250, size=self.size)
        drawLabel(f'→ - {self.choices["right"]}', app.width/2, 300, size=self.size)
    
    def checkSuccess(self, choice, player):
        if choice in self.answers:
            return True
        return False

# def onAppStart(app):
#     startDungeon(app)

# def startDungeon(app):
#     # Initialize the player
#     app.player = Player()  # Starting at the top-left corner
#     app.maze = Maze(5, 5, 30)
#     app.maze.generateMaze(app)
#     app.player.calculateVisibility(app.maze)
#     app.currentScreen = 'dungeon'
#     app.roomsComplete = 0

# def redrawAll(app):
#     if app.currentScreen == 'roomEvent':
#         drawEvent(app)
#     if app.currentScreen == 'dungeon':
#         app.player.draw(app, app.maze.cellSize)
#         app.maze.draw(app)

# def drawEvent(app):
#     # Draw the room event screen
#     # Display event details
#     drawLabel('Room Event!', 200, 50, size=30, fill='black')
#     # Display choice options
#     drawLabel('Up - Option 1', 200, 100, size=20, fill='black')
#     drawLabel('Down - Option 2', 200, 150, size=20, fill='black')
#     drawLabel('Left - Option 3', 200, 200, size=20, fill='black')
#     drawLabel('Right - Option 4', 200, 250, size=20, fill='black')

# def onKeyPress(app, key):
#     if app.currentScreen == 'roomEvent':
#         if key in ['up', 'down', 'left', 'right']:
#             app.currentRoom.eventChoiceHandler(app, key)
#     # Handle player movement
#     if app.currentScreen == 'dungeon':
#         if key in ['up', 'down', 'left', 'right']:
#             app.player.move(key, app)
#             # Update the player's current cell
#             app.player.playerCell = app.maze.grid[app.player.x][app.player.y]
# runApp()
