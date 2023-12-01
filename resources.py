from cmu_graphics import *

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

'''
Name:
Whatever as long as its on theme :)

Rarities:
"Mythic", "Ancient", "Legendary", "Epic", "Rare", "Uncommon", "Common"

Fae possible Categories: Fungoid (fungus/shrooms), Anurian (frogs/toads etc.),
Goblinoid (goblins and other nefarious Fae creatures), Faerie (Traditional Faerie)

Possible Subtypes: 
Moon (Characteristics like: Mischevious, mysterious, etherial),
Celestial (Characteristics like: Bright, cheery, light), 
Nature (Characteristics like: Dreary, natural, dark),
Klepto (Characteristics like: Crazy, chaotic, lots of accessories and items),
Decay (Characteristics like: Death, decay etc.)
'''

faeExamples = [
    # Fae("Mushrella", "Mythic", "Fungoid", " "),
    # Fae("Toadstool", "Mythic", "Fungoid", " "),
    # Fae("Frogsworth", "Ancient", "Anurian", " "),
    # Fae("Lilypad", "Ancient", "Anurian", " "),
    Fae("Pixelle", "Legendary", "Faerie", "Moon"),
    # Fae("Wingdust", "Legendary", "Faerie", " "),
    # Fae("Goblo", "Epic", "Goblinoid", " "),
    # Fae("Grimmle", "Epic", "Goblinoid", " "),
    # Fae("Shroomkin", "Rare", "Fungoid", " "),
    # Fae("Fungar", "Rare", "Fungoid", " "),
    # Fae("Hopper", "Uncommon", "Anurian", " "),
    # Fae("Ribbita", "Uncommon", "Anurian", " "),
    # Fae("FaeLight", "Common", "Faerie", " "),
    # Fae("Starling", "Common", "Faerie", " "),
    # Fae("Boggle", "Mythic", "Goblinoid", " "),
    # Fae("Nix", "Mythic", "Goblinoid", " "),
    # Fae("Sporeling", "Ancient", "Fungoid", " "),
    # Fae("Croaker", "Ancient", "Anurian", " "),
    # Fae("Spritekin", "Legendary", "Faerie", " "),
    # Fae("Gremlin", "Legendary", "Goblinoid", " ")
]