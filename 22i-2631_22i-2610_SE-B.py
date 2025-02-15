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
