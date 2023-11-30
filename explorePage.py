from cmu_graphics import *
import random

import playerAndFae 
import utils

# Exploration Mechanics
class Cell:
    def __init__(self, x, y, cellSize):
        self.hasRoom = False
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw(self, app):
        x, y, size = self.x * self.cellSize, self.y * self.cellSize, self.cellSize
        if self.hasRoom:
            drawRect(x, y, size, size, fill = 'blue', border = None, opacity = 60) 
        if self.walls['top']:
            drawLine(x, y, x + size, y, lineWidth=2)
        if self.walls['right']:
            drawLine(x + size, y, x + size, y + size, lineWidth=2)
        if self.walls['bottom']:
            drawLine(x, y + size, x + size, y + size, lineWidth=2)
        if self.walls['left']:
            drawLine(x, y, x, y + size, lineWidth=2)

class Maze:
    def __init__(self, width, height, cellSize):
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.grid = [[Cell(x, y, cellSize) for y in range(height)] for x in range(width)]

    def generateMaze(self):
        # Initialize all cells as unvisited
        for row in self.grid:
            for cell in row:
                cell.visited = False
    
        # Start with a single initial cell
        initialCell = self.grid[random.randint(0, self.width - 1)][random.randint(0, self.height - 1)]
        initialCell.visited = True
        cellsToProcess = [initialCell]
    
        # Process cells until there are no more cells in the set
        while cellsToProcess:
            currentCell = random.choice(cellsToProcess)
            neighbors = self.getUnvisitedNeighbors(currentCell)
    
            if neighbors:
                chosenNeighbor = random.choice(neighbors)
                self.removeWall(currentCell, chosenNeighbor)
                chosenNeighbor.visited = True
                cellsToProcess.append(chosenNeighbor)
            else:
                cellsToProcess.remove(currentCell)
            stack = []
            currentCell = self.grid[0][0]
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
                    if random.random() < 0.05: # 20% chance to become a room
                        chosenCell.hasRoom = True
                    stack.append(chosenCell)
        
    def draw(self, app):
        for row in self.grid:
            for cell in row:
                cell.draw(app)

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

class Room:
    def __init__(self, challengeType, requiredAttribute, requiredValue):
        self.challengeType = challengeType
        self.requiredAttribute = requiredAttribute
        self.requiredValue = requiredValue
        self.isCompleted = False

    def canCompleteWithFae(self, playerFaeCollection):
        # for fae in playerFaeCollection:
        #     if getattr(fae, self.requiredAttribute) == self.requiredValue:
        #         return True
        # return False
        return True

    def completeChallenge(self):
        self.isCompleted = True

    def __str__(self):
        return f"Room(Challenge: {self.challengeType}, Required Attribute: {self.requiredAttribute}, Required Value: {self.requiredValue}, Completed: {self.isCompleted})"
    
    def presentChallenge(self):
        # Present the challenge to the player
        pass

class Dungeon:
    def __init__(self, player):
        self.rooms = self.generateRooms(player.collectionSize + random.randint(1, 5))
        self.currentRoomIndex = 0

    def generateRooms(self, numberOfRooms):
        # Define potential challenges and their requirements
        challengeTypes = ["Battle", "Mystery", "Puzzle"]
        faeAttributes = ["category", "subType", "rarity"]
        faeValues = ["Water", "Fire", "Epic", "Mystic"]

        rooms = []
        for i in range(numberOfRooms):
            challengeType = random.choice(challengeTypes)
            requiredAttribute = random.choice(faeAttributes)
            requiredValue = random.choice(faeValues)
            room = Room(challengeType, requiredAttribute, requiredValue)
            rooms.append(room)
        return rooms

    def moveToNextRoom(self):
        if self.currentRoomIndex < len(self.rooms) - 1:
            self.rooms[self.currentRoomIndex].isCompleted = True
            self.currentRoomIndex += 1
            return True
        else:
            return False

    def getCurrentRoom(self):
        return self.rooms[self.currentRoomIndex]

    def __str__(self):
        return f"Dungeon(Current Room Index: {self.currentRoomIndex}, Total Rooms: {len(self.rooms)})"
    
    def enterDungeon(self, player):
        # Method to start dungeon exploration
        pass

    def drawDungeon(self, app):
        roomSize = 50
        spacing = 10
        totalRoomWidth = roomSize + spacing
        numRoomsPerRow = app.width // totalRoomWidth

        for i, room in enumerate(self.rooms):
            row = i // numRoomsPerRow
            col = i % numRoomsPerRow

            x = col * totalRoomWidth
            y = (row * totalRoomWidth) + (app.height / 2 - roomSize / 2) % app.height

            fillColor = 'green' if room.isCompleted else 'red'
            drawRect(x, y, roomSize, roomSize, fill=fillColor)

            if i == self.currentRoomIndex:
                # Highlight the current room
                drawRect(x, y, roomSize, roomSize, border='yellow', fill=None, borderWidth=3)

    def completeRoom(self, player):
        currentRoom = self.getCurrentRoom()
        if currentRoom.canCompleteWithFae(player.collection):
            currentRoom.completeChallenge()
            self.awardRoomReward(player)
            if not self.moveToNextRoom():
                self.awardFinalReward(player)
        else:
            # Handle failure to complete the challenge
            pass

    def awardRoomReward(self, player):
        roomReward = random.randint(3, 6)
        player.earnCurrency(roomReward)

    def checkDungeonCompletion(self, player):
        # Check if the dungeon is completed or the player failed
        pass

    def awardFinalReward(self, player):
        finalReward = 20
        player.earnCurrency(finalReward)

def onAppStart(app):
    from playerAndFae import Player
    
    # Initialize the player
    app.player = Player()
    app.player.setPosition(0, 0)  # Starting at the top-left corner
    app.maze = Maze(30, 30, 30)
    app.maze.generateMaze()

def redrawAll(app):
    app.player.draw(app, app.maze.cellSize)
    app.maze.draw(app)

def onKeyPress(app, key):
    # Handle player movement
    if key in ['up', 'down', 'left', 'right']:
        app.player.move(key, app.maze)
        # Update the player's current cell
        app.player.playerCell = app.maze.grid[app.player.x][app.player.y]
runApp()
