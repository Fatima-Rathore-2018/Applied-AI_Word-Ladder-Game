import json
import string

# Note: node-to-node cost will always be unit cost because there is always one-letter difference between a node and its children.

#Creation of Class Node
class WordNode:
    def __init__(self, state, parent, actions, heuristic, pathCost, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.heuristic = heuristic # h(n)
        self.pathCost = pathCost # g(n)
        self.totalCost = heuristic + pathCost # f(n) = g(n) + h(n) 

# Function to create a graph.
def createGraph(wordLadderDictionary):
    #Creation of Graph
    WordLadderGraph = {}
    for word in wordLadderDictionary:
        wordNode = WordNode(word, None, [], 0, 0, 0)
        WordLadderGraph[word] = wordNode

        wordCharacters = list(word) # Convert the word into a list of characters.
        for index in range(len(word)):
            originalCharacter = wordCharacters[index]

            for letter in string.ascii_lowercase: # Iterate through all the letters of the alphabet.
                if letter != originalCharacter:
                    wordCharacters[index] = letter
                    updatedWord = "".join(wordCharacters) # Convert list of characters into a string.
                    
                    if updatedWord in wordLadderDictionary:
                        WordLadderGraph[word].actions.append((updatedWord, 1))    


    return WordLadderGraph


# Main Function.
def main():
    #Reading words from words_dictionary.json
    with open("test_file.json", "r") as words_dictonary:
        wordsData = json.load(words_dictonary)

    #Creating a dictionary for the game.
    WordLadderDictionary = dict()

    #Filtering out words with length greater than equal to 3 and less than equal to 6.
    for word in wordsData: 
        if 3 <= len(word) <= 6:
            WordLadderDictionary[word] = wordsData[word]

    # Creating the graph.
    wordLadderGraph = createGraph(WordLadderDictionary)

    # Print graph.
    for word, node in wordLadderGraph.items():
        print(f"{word}: {node.state}, {node.parent}, {node.actions}, {node.heuristic}, {node.pathCost}, {node.totalCost}")

if __name__ == "__main__":
    main()
