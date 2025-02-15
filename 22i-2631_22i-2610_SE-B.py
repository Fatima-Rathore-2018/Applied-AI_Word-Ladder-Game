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
                    
                    if wordLadderDictionary.get(updatedWord) is not None:
                        WordLadderGraph[word].actions.append((updatedWord, 1))    

            wordCharacters[index] = originalCharacter

    return WordLadderGraph


def SequenceOfSteps(WordLadderGraph, startState, goalState):
    finalPath = []
    currentNode = WordLadderGraph.get(goalState, None)
    while currentNode.state != startState:
        finalPath.insert(0, currentNode.state)
        currentNode = WordLadderGraph[currentNode.parent]
    
    finalPath.insert(0, startState)
    print(finalPath)


# Function to find the shortest path using Breadth First Search.
def BreadthFirstSearch(WordLadderGraph, startState ,goalState):
    frontier = dict() #To-Be-Explored Nodes -> FIFO QUEUE
    explored = [] #Nodes that have been explored.

    #Goal Test is performed.
    if startState == goalState:
        return SequenceOfSteps(WordLadderGraph,startState,goalState)
    
    frontier[startState] = (None) # FIFO Queue with intial state as it's only element

    #If intial state isn't goal state find the goal state
    #The loop terminated when goal state is found or when frontier is empty
    while len(frontier) != 0:

        #Getting the first/shallowest node in frontier.
        currentNode = next(iter(frontier))
        
        #Add this node to explored.
        explored.append(currentNode)

        del frontier[currentNode]

        #Expand the currentNode/ Explore the child nodes of the current node.
        for childNode in WordLadderGraph[currentNode].actions:
            #If the childNode is not in frontier and explored
            if childNode[0] not in frontier and childNode[0] not in explored:
                
                #Perform goal test, if passed return.
                if childNode[0] == goalState:
                    WordLadderGraph[childNode[0]].parent = currentNode
                    return SequenceOfSteps(WordLadderGraph, startState, goalState)
                
                #Else add the childNode to frontier
                WordLadderGraph[childNode[0]].parent = currentNode
                
                frontier[childNode[0]] = currentNode
        print(explored)

                
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

    BreadthFirstSearch(wordLadderGraph, "cat", "dog")

if __name__ == "__main__":
    main()
