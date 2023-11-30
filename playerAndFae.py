from cmu_graphics import *
import random

class Player:
    
    def __init__(self):
        self.collection = []
        self.collectionSize = 0
        self.lastRarePull = 1
        self.summonHistory = []
        self.wallet = 10000

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
    
    def move(self, direction, maze):
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

class Fae:
    def __init__(self, name, rarity, category, sprite, subType):
        self.name = name
        self.rarity = rarity
        self.category = category
        self.sprite = sprite
        self.subType = subType

    def __repr__(self):
        return(f'{self.name}: {self.rarity}')

