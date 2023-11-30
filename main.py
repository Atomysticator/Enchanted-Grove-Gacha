from cmu_graphics import *
import random

from gachaPage import GachaSet
from explorePage import Dungeon, Maze, Cell, Room
from playerAndFae import Player, Fae
from utils import Button

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

def summonFae(app):
    # Perform a summon
    app.summonedFae = app.gachaSet.summonFromSet(app.player)
    if app.summonedFae:
        app.player.updateAfterSummon(app.summonedFae)
        # Display summon result
    else:
        app.broke = True

def onAppStart(app):
    app.background = 'lightGray'
    app.player = Player()
    app.dungeon = Dungeon(app.player)
    app.gachaSet = GachaSet(faeExamples, 10)
    app.summonedFae = None
    app.broke = False
    app.currentScreen = 'gacha'

    app.nextRoomButton = Button('Next Room', 100, 100, 100, 40, 
                                lambda: app.dungeon.completeRoom(app.player))
    app.gachaButton = Button('Go to Gacha Machine', app.width - 170, 
                             app.height - 50, 150, 30, 
                             lambda: changeScreen(app, 'gacha'))
    app.dungeonButton = Button('Go to Dungeon', 50, app.height - 50, 
                               120, 30, lambda: dungeonButtonHandler(app))
    app.summonButton = Button('Summon', 150, 100, 100, 40, lambda: summonFae(app))


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