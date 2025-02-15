import json

#Reading words from words_dictionary.json
with open("words_dictionary.json", "r") as words_dictonary:
    wordsData = json.load(words_dictonary)

#Creating a dictionary for the game.
WordLadderDictionary = {}

#Filtering out words with length greater than equal to 3 and less than equal to 6.
for word in wordsData: 
    if 3 <= len(word) <= 6:
        WordLadderDictionary[word] = wordsData[word]

#Creation of Class Node
class WordNode:
    def __init__(self, state, parent, actions, pathCost):
        self.state = state,
        self.parent = parent,
        self.actions = actions,
        self.pathCost = pathCost

#Creation of Graph
WordLadderGraph = {}