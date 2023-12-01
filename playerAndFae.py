from cmu_graphics import *
import random

class Player: 
    def __init__(self):
        self.collection = []
        self.collectionSize = 0
        self.lastRarePull = 1
        self.summonHistory = []
        self.wallet = 10000
        self.lives = 3

    def updateAfterSummon(self, summonedFae):
        if summonedFae:
            self.collection.append(summonedFae)
            self.collectionSize = len(self.collection)

            self.summonHistory.append(summonedFae.rarity)
            if len(self.summonHistory) > 5:
                self.summonHistory.pop()
            if summonedFae.rarity in ["Mystic", "Ancient", "Legendary"]:
                self.lastRarePull = 1
            else:
                self.lastRarePull += 1
    
    def spendCurrency(self, amount):
        if self.wallet >= amount:
            self.wallet -= amount
            return True
        else:
            return False

    def earnCurrency(self, amount):
        self.wallet += amount
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, app, cellSize):
        drawCircle(self.x * cellSize + cellSize // 2, self.y * cellSize + cellSize // 2, cellSize // 2, fill = 'red')
    
    def move(self, direction, app):
        maze = app.maze
        # Movement logic based on the direction and maze walls
        currentCell = maze.grid[self.x][self.y]
        if direction == 'up' and not currentCell.walls['top']:
            self.y -= 1
        elif direction == 'down' and not currentCell.walls['bottom']:
            self.y += 1
        elif direction == 'left' and not currentCell.walls['left']:
            self.x -= 1
        elif direction == 'right' and not currentCell.walls['right']:
            self.x += 1
        newCell = maze.grid[self.x][self.y]
        if newCell.hasRoom and newCell != currentCell and newCell.room.isCompleted == False:
            newCell.onPlayerEnter(self, app)
        self.calculateVisibility(maze)

        if newCell == maze.endCell:
            maze.finished(app)
    
    def calculateVisibility(self, maze, visibilityRange=2):
            # Initialize visibility for the current cell
            maze.grid[self.x][self.y].visible = True
            directions = {'top': (0, -1), 'bottom': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
            for direction, (dx, dy) in directions.items():
                x, y = self.x, self.y
                for i in range(visibilityRange):
                    nextX, nextY = x + dx, y + dy
                    if 0 <= nextX < len(maze.grid) and 0 <= nextY < len(maze.grid[0]):
                        if maze.grid[x][y].walls[direction] == False:
                            maze.grid[nextX][nextY].visible = True
                            x, y = nextX, nextY
                        else:
                            break
                    else:
                        break
        

class Fae:
    def __init__(self, name, rarity, category, sprite, subType):
        self.name = name
        self.rarity = rarity
        self.category = category
        self.sprite = sprite
        self.subType = subType

    def __repr__(self):
        return(f'{self.name}: {self.rarity}')

