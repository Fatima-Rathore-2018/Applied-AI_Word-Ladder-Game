import json
import string

# Note: node-to-node cost will always be unit cost because there is always one-letter difference between a node and its children.

#Creation of Class Node
class WordNode:
    def __init__(self, state, parent, actions, heuristic, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.heuristic = heuristic # h(n)
        self.totalCost = totalCost # g(n)

# Function to create a graph.
def createGraph(wordLadderDictionary):
    #Creation of Graph
    WordLadderGraph = {}
    for word in wordLadderDictionary:
        wordNode = WordNode(word, None, [], 0, 0)
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
    # print(finalPath)

    return finalPath

# Function to find the node with minimum path cost.
def findMinimumPathCostNode(frontier):
    minimumCost = float('inf')
    minimumNode = None
    for node in frontier:
        if minimumCost > frontier[node][1]:
            minimumCost = frontier[node][1]
            minimumNode = node
    return minimumNode

#Function to calcuate the heuristic cost of the current word and the goal word.
def findHeuristicCost(startState, goalState):
    heuristicCost = 0
    for i in range(len(goalState)):
        if(startState[i] != goalState[i]):
            heuristicCost = heuristicCost + 1
    
    return heuristicCost

def AssigningHeuristicCost(WorLadderGraph, goalState):
    for node in WorLadderGraph:
        WorLadderGraph[node].heuristic = findHeuristicCost(node, goalState)
    
    return WorLadderGraph

#Function for A* Search 
def AStarSearch(WordLadderGraph, startState, goalState):
    frontier = dict()
    explored = dict()
    frontier[startState] = (None, WordLadderGraph[startState].heuristic) # Stores nodes with their parent and cost

    while len(frontier) != 0:
        currentNode = findMinimumPathCostNode(frontier)
        currentCost = WordLadderGraph[currentNode].totalCost
        heuristicCost = WordLadderGraph[currentNode].heuristic
        del frontier[currentNode]

        # Goal Test.
        if currentNode == goalState:
            # for word, node in WordLadderGraph.items():
            #     print(f"{word}: {node.state}, {node.parent}, {node.actions}, {node.heuristic}, {node.totalCost}")
            return SequenceOfSteps(WordLadderGraph, startState, goalState)
        
        # Add the node to explored list.
        explored[currentNode] = (WordLadderGraph[currentNode].parent, currentCost + heuristicCost)
  
       # Explore child nodes for cost
        for child in  WordLadderGraph[currentNode].actions:
            currentCost=child[1] +  WordLadderGraph[currentNode].totalCost
            heuristicCost =  WordLadderGraph[child[0]].heuristic

            # if already looked at or initial state or cost lesser than current, continue
            if child[0] in explored:
                if  WordLadderGraph[child[0]].parent==currentNode or child[0]==startState or \
                    explored[child[0]][1] <= currentCost + heuristicCost:
                    continue

            # if not in frontier - add to it
            if child[0] not in frontier:
                WordLadderGraph[child[0]].parent=currentNode
                WordLadderGraph[child[0]].totalCost=currentCost
                frontier[child[0]]=( WordLadderGraph[child[0]].parent, currentCost + heuristicCost)

            # if in frontier - check cost
            else:
                #if cost is lesser - update graph with frontier
                if frontier[child[0]][1] > currentCost + heuristicCost:
                    frontier[child[0]]=(currentNode, currentCost + heuristicCost)
                    WordLadderGraph[child[0]].parent=frontier[child[0]][0]
                    WordLadderGraph[child[0]].totalCost=currentCost

        #print(explored)

# Function for Uniform-Cost Search (UCS)
def uniformCostSearch(WordLadderGraph, startState, goalState):
    frontier = dict()
    explored = []
    frontier[startState] = (None, 0) # Stores nodes with their parent and cost

    while len(frontier) != 0:
        currentNode = findMinimumPathCostNode(frontier)
        currentCost = frontier[currentNode][1]
        del frontier[currentNode]

        # Goal Test.
        if currentNode == goalState:
            # Print graph.
            # for word, node in WordLadderGraph.items():
            #     print(f"{word}: {node.state}, {node.parent}, {node.actions}, {node.heuristic}, {node.totalCost}")
            return SequenceOfSteps(WordLadderGraph, startState, goalState)
        
        # Add the node to explored list.
        explored.append(currentNode)

        #Expand the children of current node.
        for childNode in WordLadderGraph[currentNode].actions:
            updatedCost = currentCost + childNode[1]
            if childNode[0] not in frontier and childNode[0] not in explored:
                WordLadderGraph[childNode[0]].parent = currentNode
                WordLadderGraph[childNode[0]].totalCost = updatedCost
                frontier[childNode[0]] = (currentNode, updatedCost)
            elif childNode[0] in frontier and frontier[childNode[0]][1] > updatedCost:
                frontier[childNode[0]] = (currentNode, updatedCost)
                WordLadderGraph[childNode[0]].parent = frontier[childNode[0]][0]
                WordLadderGraph[childNode[0]].totalCost = frontier[childNode[0]][1]

        #print(explored)

                
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
            #print(explored)
            #If the childNode is not in frontier and explored
            if childNode[0] not in frontier and childNode[0] not in explored:
                
                #Perform goal test, if passed return.
                if childNode[0] == goalState:
                    WordLadderGraph[childNode[0]].parent = currentNode
                    return SequenceOfSteps(WordLadderGraph, startState, goalState)
                
                #Else add the childNode to frontier
                WordLadderGraph[childNode[0]].parent = currentNode
                
                frontier[childNode[0]] = currentNode

# Function to give hints
def giveHint(path, currentWord):
    if currentWord in path:
        currentWordIndex = path.index(currentWord)
        return path[currentWordIndex + 1]
    
    print("No hints available anymore.")

# Validate if a word exists.
def validateExistenceOfWordInActions(currentWord, playerChoice, wordLadderGraph):
    for childNode in wordLadderGraph[currentWord].actions:
        if childNode[0] == playerChoice:
            return True
        
    return False

# The gameplay function.
def gameplayFunction(wordLadderGraph, startWord, goalWord, graphHeuristics):
    print("Inside gameplay function.")
    currentWord = startWord
    path = [currentWord]
    numberOfTurns = len(startWord) * 2
    exploredPath = []
    optimalNumberOfMoves = len(AStarSearch(graphHeuristics, startWord, goalWord))
    score = optimalNumberOfMoves * 10
    print("Current Score: ", score, " - Your score will decrease each extra move you make.\n")

    while currentWord != goalWord:
        print("Current Score: ", score)
        print("Current word:", currentWord, " Target word: ", goalWord)
        print("Explored Path: ", path)
        requestForHint = input("\nDo you want a hint? (yes/no): ")
        while requestForHint != "yes" and requestForHint != "no":
            print ("Invalid Input. Enter yes/no: ") 
            requestForHint = input("\nDo you want a hint? (yes/no): ")
        if requestForHint == "yes":
            score -= 3 # Score will decrease by 3 for each hint requested.
            chooseSearchAlgorithm = input("\nChoose search algorithm (bfs/ucs/astar): ")
            if chooseSearchAlgorithm == "bfs":
                exploredPath = BreadthFirstSearch(wordLadderGraph, startWord, goalWord)
            elif chooseSearchAlgorithm == "ucs":
                exploredPath = uniformCostSearch(wordLadderGraph, startWord, goalWord)
            elif chooseSearchAlgorithm == "astar":
                exploredPath = AStarSearch(graphHeuristics, startWord, goalWord)

            nextWord = giveHint(exploredPath, currentWord)
            if nextWord is not None:
                print("Hint for next word:", nextWord)
            else:
                break
        
        playerChoice = input("Enter next word: ")
        if validateExistenceOfWordInActions(currentWord, playerChoice, wordLadderGraph):
            currentWord = playerChoice
            path.append(currentWord)
        else:
            score -= 7 # Score will decrease by 7 if word does not exist in the ladder.
            print("Invalid word choice. Try again.")

        numberOfTurns -= 1
        if numberOfTurns == 0:
            print("Number of turns have finished.")
            break

        # Check if score is to be updated or not.
        if numberOfTurns > optimalNumberOfMoves:
            score -= 5

    if currentWord == goalWord:
        print("Congratulations! You have completed the word ladder!")
    else:
        print("Game Over, Loser.") 

    print("----------- Final Score: ", score)

# Function to allow players to choose level of difficulty and word selection.
def chooseGameMode():
    print("Choose word selection mode:")
    print("1. Enter start and end words")
    print("2. Automatic selection of start and end words")
    print("3. Exit")
    wordSelectionMode = int(input("Enter your choice (1/2/3): "))
    while wordSelectionMode < 1 or wordSelectionMode > 3:
        print("Invalid Input.")
        print("Choose word selection mode:")
        print("1. Enter start and end words")
        print("2. Automatic selection of start and end words")
        print("3. Exit")
        wordSelectionMode = int(input("Enter your choice (1/2/3): "))

    difficulty = -1

    # if wordSelectionMode == 2:
    #     print("Choose difficulty level:")
    #     print("1. Beginner Mode (Simple word ladders)")
    #     print("2. Advanced Mode (Longer and complex ladders)")
    #     print("3. Challenge Mode (Restricted Letters, banned words etc.)")
    #     difficulty = int(input("Enter your choice (1/2/3): "))
        
    #     while wordSelectionMode < 1 or wordSelectionMode > 3:
    #         print("Choose difficulty level:")
    #         print("1. Beginner Mode (Simple word ladders)")
    #         print("2. Advanced Mode (Longer and complex ladders)")
    #         print("3. Challenge Mode (Restricted Letters, banned words etc.)")
    #         difficulty = int(input("Enter your choice (1/2/3): "))

    return difficulty, wordSelectionMode

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

    while 1:
        difficuly, selectionMode = chooseGameMode()

        if selectionMode == 3:
            exit(0)
        elif selectionMode == 2:
            #TO BE DETERMINED :(
            startWord = "dog"
            goalWord = "bat"
        else: 
            startWord = input("Enter start word: ")
            while startWord not in WordLadderDictionary:
                print("Error: Start word does not exist in the dictionary.\n")
                startWord = input("Enter start word: ")

            goalWord = input("Enter goal word: ")
            while goalWord not in WordLadderDictionary:
                print("Error: Goal word does not exist in the dictionary.\n")
                goalWord = input("Enter goal word: ")

            while len(startWord) != len(goalWord):
                startWord = input("Enter start word: ")
                while startWord not in WordLadderDictionary:
                    print("Error: Start word does not exist in the dictionary.\n")
                    startWord = input("Enter start word: ")

                goalWord = input("Enter goal word: ")
                while goalWord not in WordLadderDictionary:
                    print("Error: Goal word does not exist in the dictionary.\n")
                    goalWord = input("Enter goal word: ")

        graphHeuristics = AssigningHeuristicCost(wordLadderGraph, goalWord)
        # Game play.
        gameplayFunction(wordLadderGraph, startWord, goalWord, graphHeuristics)

if __name__ == "__main__":
    main()
