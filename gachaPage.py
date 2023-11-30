from cmu_graphics import *
import random

from playerAndFae import Player, Fae

# Gacha Mechanics
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
            rarityProbabilities = self.calculateRarityProbabilities(
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

    def calculateRarityProbabilities(self, collectionSize, lastRarePull, summonHistory):
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
