from cmu_graphics import *
import random

from gachaPage import GachaSet
from explorePage import Maze
from playerAndFae import Player
from utils import Button
from resources import faeExamples, events

set1 = GachaSet(faeExamples, 10)

def summonFae(app):
    # Perform a summon
    app.summonedFae = app.gachaSet.summonFromSet(app.player)
    if app.summonedFae:
        app.player.updateAfterSummon(app.summonedFae)
        # Display summon result
    else:
        app.broke = True

def onAppStart(app):
    app.width = 600
    app.height = 600
    app.player = Player()
    app.events = events
    app.eventMessage = None
    startHomeScreen(app)
    # Button Initialization
    app.gachaButton = Button('Summon!', app.width/2, 
                             app.height/2 + 50, 150, 30, 
                             lambda: startGacha(app))
    app.dungeonButton = Button('Explore!', app.width/2, app.height/2, 
                               150, 30, lambda: startDungeon(app))
    app.summonButton = Button('Summon', app.width/2, app.height/2 + 50, 100, 40, lambda: summonFae(app))

def startHomeScreen(app):
    app.screen = 'home'

def startGacha(app):
    app.gachaSet = set1
    app.summonedFae = None
    app.broke = False
    app.screen = 'gacha'

def startDungeon(app):
    app.maze = Maze(app, random.randrange(5,11) +  app.player.collectionSize//10, 
                    random.randrange(5,11) +  app.player.collectionSize//10)
    app.maze.generateMaze(app)
    app.player.calculateVisibility(app.maze)
    app.player.lives = 3 + app.player.collectionSize//10
    app.screen = 'dungeon'
    app.roomsComplete = 0

def redrawAll(app):
    if app.screen == 'gacha':
        drawGachaMachine(app)
    if app.screen == 'roomEvent':
        drawEvent(app)
    if app.screen == 'dungeon':
        drawMaze(app)
    if app.screen == 'home':
        drawHome(app)
    if app.eventMessage:
        drawLabel(app.eventMessage, app.width/2, app.height/2, size = 20, fill = 'Green', bold = True)

def drawMaze(app):
    app.player.draw(app, app.maze.cellSize)
    app.maze.draw(app)

def drawHome(app):
    app.gachaButton.draw()
    app.dungeonButton.draw()
    drawLabel('ENCHANTED GROVE B*TCH', app.width/2, 100, size=28, fill='black', bold = True)

def drawEvent(app):
    app.currentRoom.event.drawChoices(app)

def drawGachaMachine(app):
    app.summonButton.draw()
    if app.summonedFae:
        drawLabel(f'Summoned: {app.summonedFae.name}, {app.summonedFae.rarity}', app.width/2, app.height/2, size=15, fill='black')
    if app.broke:
        drawLabel('Not enough Essence', 150, 200, size=15, fill='red')
    drawLabel(f'Essence: {app.player.wallet}', 300, 50, size=15, fill='black')

def onMousePress(app, mx, my):
    if app.screen == 'gacha':
        app.summonButton.onClick(mx, my)
    if app.screen == 'home':
        app.dungeonButton.onClick(mx, my)
        app.gachaButton.onClick(mx, my)

def onKeyPress(app, key):
    app.eventMessage = None
    if key == 'escape':
        startHomeScreen(app)
    # Handle player movement
    elif app.screen == 'dungeon':
        if key in ['up', 'down', 'left', 'right']:
            app.player.move(key, app)
            # Update the player's current cell
            app.player.playerCell = app.maze.grid[app.player.x][app.player.y]
    elif app.screen == 'roomEvent':
        if key in ['up', 'down', 'left', 'right']:
            if app.currentRoom.eventChoiceHandler(app, key):
                app.eventMessage = 'Out of Lives! Try again :)'
                startDungeon(app)

def changeScreen(app, screen):
    app.screen = screen

def main():
    runApp()

main()