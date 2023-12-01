from cmu_graphics import *
import random

from explorePage import Event
from playerAndFae import Fae

events = [
    Event('Fairy Tea Party', 'Fairies invite you to their magical tea party.', {'up': 'Share Stories', 'down': 'Sing Songs', 'left': 'Dance', 'right': 'Taste Tea'}, {'right', 'up'}, 10),
    Event('Goblin Market', 'A bustling goblin market with various trinkets.', {'up': 'Barter', 'down': 'Browse', 'left': 'Haggle', 'right': 'Buy'}, {'left', 'down'}, 15),
    Event('Enchanted Garden', 'A garden with talking flowers offering riddles.', {'up': 'Listen', 'down': 'Water', 'left': 'Prune', 'right': 'Plant'}, {'up', 'right'}, 20),
    Event('Mystical Pond', 'A serene pond with reflective waters showing visions.', {'up': 'Reflect', 'down': 'Fish', 'left': 'Swim', 'right': 'Skip Stones'}, {'up', 'left'}, 10),
    Event('Whimsical Library', 'An ancient library with books that whisper secrets.', {'up': 'Read', 'down': 'Write', 'left': 'Organize', 'right': 'Rest'}, {'up', 'right'}, 15),
    Event('Cottage Hearth', 'A cozy cottage with a warm hearth and delicious smells.', {'up': 'Cook', 'down': 'Eat', 'left': 'Clean', 'right': 'Nap'}, {'down', 'right'}, 20),
    Event('Moonlit Glade', 'A glade bathed in moonlight, with nocturnal creatures.', {'up': 'Stargaze', 'down': 'Explore', 'left': 'Meditate', 'right': 'Forage'}, {'left', 'up'}, 10),
    Event("Herbalist's Hut", 'A hut filled with herbs and potions, tended by a wise herbalist.', {'up': 'Learn', 'down': 'Assist', 'left': 'Brew', 'right': 'Gather'}, {'left', 'up'}, 15)
]

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
