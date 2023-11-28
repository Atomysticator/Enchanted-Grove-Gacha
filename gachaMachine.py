from cmu_graphics import *
import random

### Main classes and methods ###

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

class Fae:
    def __init__(self, name, rarity, category, sprite, subType):
        self.name = name
        self.rarity = rarity
        self.category = category
        self.sprite = sprite
        self.subType = subType

    def __repr__(self):
        return(f'{self.name}: {self.rarity}')
    

class Button:
    def __init__(self, label, x, y, width, height, action, fillColor='gray', textColor='black'):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.fillColor = fillColor
        self.textColor = textColor

    def draw(self):
        self.rect = drawRect(self.x, self.y, self.width, self.height, fill=self.fillColor)
        self.text = drawLabel(self.label, self.x + self.width / 2, self.y + self.height / 2, fill=self.textColor)

    def isClicked(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def onClick(self, x, y):
        if self.isClicked(x, y):
            self.action()

### Gacha section ###

class GachaSet:
    def __init__(self, faeList, pullCost):
        self.faeList = {rarity: set() for rarity in 
                        ["Mythic", "Ancient", "Legendary", "Epic", 
                         "Rare", "Uncommon", "Common"]}
        for fae in faeList:
            if isinstance(fae, Fae):
                self.faeList[fae.rarity].add(fae)
        
        self.pullCost = pullCost

    def summonFromSet(self, player):
        # summon a Fae from the set
        if player.wallet >= self.pullCost:
            rarityProbabilities = calculateRarityProbabilities(
                player.collectionSize, player.lastRarePull, player.summonHistory)
            
            chosenRarity = self.chooseRarity(rarityProbabilities)
            chosenFae = self.chooseFaeFromRarity(chosenRarity)

            player.spendCurrency(self.pullCost)

            return chosenFae
        else:
            return None

    def chooseRarity(self, rarityProbabilities):
        rarities = list(rarityProbabilities.keys())
        probabilities = list(rarityProbabilities.values())
        chosenRarity = random.choices(rarities, weights=probabilities, k=1)[0]
        if self.faeList[chosenRarity] == set():
            return self.chooseRarity(rarityProbabilities)
        return chosenRarity
    
    def chooseFaeFromRarity(self, chosenRarity):
        possibleFaes = self.faeList[chosenRarity]
        chosenFae = random.choice(list(possibleFaes))
        return chosenFae

    
def calculateRarityProbabilities(collectionSize, lastRarePull, summonHistory):
    rarityProbabilities = {
        "Mythic": 0.01,
        "Ancient": 0.05,
        "Legendary": 0.1,
        "Epic": 0.15,
        "Rare": 0.2,
        "Uncommon": 0.25,
        "Common": 0.3
    }

    # Adjust probabilities based on player's collection size
    for rarity, probability in rarityProbabilities.items():
        # larger collection slightly increases the chance for rarer Fae
        adjustedProbability = probability * (1 + collectionSize / 1000)
        # Ensure probabilities don't exceed 100%
        rarityProbabilities[rarity] = min(adjustedProbability, 1) 
    
    # Max 50% increase in probability
    pityFactor = min(lastRarePull / 10, 1.5)  
    for rarity, probability in rarityProbabilities.items():
        adjustedProbability = probability * pityFactor
        rarityProbabilities[rarity] = min(adjustedProbability, 1)

    for rarity in rarityProbabilities.keys():
        if rarity not in summonHistory:
            # Increase chance for unsummoned Fae
            rarityProbabilities[rarity] *= 1.1

    return rarityProbabilities

def summonFae(app):
    # Perform a summon
    app.summonedFae = app.gachaSet.summonFromSet(app.player)
    if app.summonedFae:
        app.player.updateAfterSummon(app.summonedFae)
        # Display summon result
    else:
        app.broke = True


faeExamples = [
    Fae("Mushrella", "Mythic", "Fungoid", "sprite1", " "),
    Fae("Toadstool", "Mythic", "Fungoid", "sprite2", " "),
    Fae("Frogsworth", "Ancient", "Anurian", "sprite3", " "),
    Fae("Lilypad", "Ancient", "Anurian", "sprite4", " "),
    Fae("Pixelle", "Legendary", "Faerie", "sprite5", " "),
    Fae("Wingdust", "Legendary", "Faerie", "sprite6", " "),
    Fae("Goblo", "Epic", "Goblinoid", "sprite7", " "),
    Fae("Grimmle", "Epic", "Goblinoid", "sprite8", " "),
    Fae("Shroomkin", "Rare", "Fungoid", "sprite9", " "),
    Fae("Fungar", "Rare", "Fungoid", "sprite10", " "),
    Fae("Hopper", "Uncommon", "Anurian", "sprite11", " "),
    Fae("Ribbita", "Uncommon", "Anurian", "sprite12", " "),
    Fae("FaeLight", "Common", "Faerie", "sprite13", " "),
    Fae("Starling", "Common", "Faerie", "sprite14", " "),
    Fae("Boggle", "Mythic", "Goblinoid", "sprite15", " "),
    Fae("Nix", "Mythic", "Goblinoid", "sprite16", " "),
    Fae("Sporeling", "Ancient", "Fungoid", "sprite17", " "),
    Fae("Croaker", "Ancient", "Anurian", "sprite18", " "),
    Fae("Spritekin", "Legendary", "Faerie", "sprite19", " "),
    Fae("Gremlin", "Legendary", "Goblinoid", "sprite20", " ")
]

def testGachaSystem():
    gachaSet = GachaSet(faeExamples, 100)

    player = Player()

    for i in range(10):
        summonedFae = gachaSet.summonFromSet(player)
        player.updateAfterSummon(summonedFae)
    print(player.collection)

testGachaSystem()

### Exploration Section ###

# MAZE METHOD

class Cell:
    def __init__(self, x, y, cellSize):
        self.x = x
        self.y = y
        self.cellSize = cellSize
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw(self, app):
        x, y, size = self.x * self.cellSize, self.y * self.cellSize, self.cellSize
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

# def onAppStart(app):
#     app.mazeWidth, app.mazeHeight, app.cellSize = 10, 10, 50
#     app.maze = Maze(app.mazeWidth, app.mazeHeight, app.cellSize)
#     app.maze.generateMaze()
#     app.background = 'white'

# def redrawAll(app):
#     app.maze.draw(app)

# def main():
#     runApp()

# main()

# PROCEDURAL DUNGEON METHOD

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

# Example usage
def testDungeonSystem():
    player = Player()
    dungeon = Dungeon(player)
    generatedRooms = [str(room) for room in dungeon.rooms]
    print(generatedRooms)

# testDungeonSystem()

def onAppStart(app):
    app.background = 'lightGray'
    app.player = Player()
    app.dungeon = Dungeon(app.player)
    app.gachaSet = GachaSet(faeExamples, 10)
    app.summonedFae = None
    app.broke = False

    app.nextRoomButton = Button('Next Room', 100, 100, 100, 40, 
                                lambda: app.dungeon.completeRoom(app.player))
    app.gachaButton = Button('Go to Gacha Machine', app.width - 170, 
                             app.height - 50, 150, 30, 
                             lambda: changeScreen(app, 'gacha'))
    app.dungeonButton = Button('Go to Dungeon', 50, app.height - 50, 
                               120, 30, lambda: dungeonButtonHandler(app))
    app.summonButton = Button('Summon', 150, 100, 100, 40, lambda: summonFae(app))

    app.currentScreen = 'gacha'

def redrawAll(app):
    if app.currentScreen == 'gacha':
        drawGachaMachine(app)
    elif app.currentScreen == 'dungeon':
        app.nextRoomButton.draw()
        app.dungeon.drawDungeon(app)
    drawNavigationButtons(app)

def drawNavigationButtons(app):
    app.gachaButton.draw()
    app.dungeonButton.draw()

def changeScreen(app, screen):
    app.currentScreen = screen

def drawGachaMachine(app):
    app.summonButton.draw()
    if app.summonedFae:
        drawLabel(f'''Summoned: {app.summonedFae.name}, {app.summonedFae.rarity}, 
                {app.summonedFae.category}''', 150, 200, size=15, fill='black')
    if app.broke:
        drawLabel('Not enough currency', 150, 200, size=15, fill='red')
    drawLabel(f'Currency: {app.player.wallet}', 300, 50, size=15, fill='black')

def onMousePress(app, mx, my):
    if app.currentScreen == 'dungeon':
        app.nextRoomButton.onClick(mx, my)
    if app.currentScreen == 'gacha':
        app.summonButton.onClick(mx, my)
    app.dungeonButton.onClick(mx, my)
    app.gachaButton.onClick(mx, my)

def dungeonButtonHandler(app):
    changeScreen(app, 'dungeon')
    app.dungeon = Dungeon(app.player)

def main():
    runApp()

main()
