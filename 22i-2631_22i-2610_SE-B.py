import json
import string
import os
import time
import sys
import keyboard
from typing import Text
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
console = Console()

init(autoreset=True)

# Note: node-to-node cost will always be unit cost because there is always one-letter difference between a node and its children.

#Creation of Class Node
class WordNode:
    def __init__(self, state, parent, actions, heuristic, totalCost):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.heuristic = heuristic # h(n)
        self.totalCost = totalCost # g(n)

# Function to quit game.
def quitGame():
    console.print("\n\n[bold red]Exiting game...[/bold red]")
    os._exit(0)

keyboard.add_hotkey('q', quitGame)

# Function to create a graph.
def createGraph(wordLadderDictionary, difficulty, forbiddenWord, restrictedLetter):
    wordLength = 0
    if difficulty == 1: # Beginner's mode.
        wordLength = 3
    elif difficulty == 2: # Advanced mode.
        wordLength = 4
    else: # Challenge mode.
        wordLength = 5

    #Creation of Graph
    WordLadderGraph = {}
    for word in wordLadderDictionary:
        if len(word) == wordLength and word != forbiddenWord:
            wordNode = WordNode(word, None, [], 0, 0)
            WordLadderGraph[word] = wordNode

            wordCharacters = list(word) # Convert the word into a list of characters.
            for index in range(len(word)):
                originalCharacter = wordCharacters[index]

                for letter in string.ascii_lowercase: # Iterate through all the letters of the alphabet.
                    if letter != originalCharacter and letter != restrictedLetter:
                        wordCharacters[index] = letter
                        updatedWord = "".join(wordCharacters) # Convert list of characters into a string.
                        
                        if wordLadderDictionary.get(updatedWord) is not None and updatedWord != forbiddenWord:
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

# Function to give hints
def giveHint(path, currentWord):
    if currentWord in path:
        currentWordIndex = path.index(currentWord)
        return path[currentWordIndex + 1]
    return None

# Validate if a word exists.
def validateExistenceOfWordInActions(currentWord, playerChoice, wordLadderGraph):
    for childNode in wordLadderGraph[currentWord].actions:
        if childNode[0] == playerChoice:
            return True
        
    return False

# Check if word exists in the dictionary.
def validateExistenceOfWordInDictionary(currentWord, playerChoice, wordLadderDictionary):
    for word in wordLadderDictionary:
        if word == playerChoice:
            return True
        
    return False

def requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path):
    ladderContinues = True
    nextWord = ""
    while True:
        requestForHint = input("\n🤔 Would you like a hint? (yes/no): ").strip().lower()
        if requestForHint in ["yes", "no"]:
            break
        console.print("[bold red]❌ Invalid input. Please enter 'yes' or 'no'.[/bold red]")

    if requestForHint == "yes":
        score -= 3  # Deduct points for using a hint.
        #console.print(f"[bold red]-3 points for using hint! Current score: {score}[/bold red]")
        
        chooseSearchAlgorithm = input("\nChoose search algorithm (bfs/ucs/astar): ").strip().lower()
        
        while chooseSearchAlgorithm != "bfs" and chooseSearchAlgorithm != "ucs" and chooseSearchAlgorithm != "astar":
            console.print("[bold red]❌ Invalid algorithm choice.[/bold red]")
            chooseSearchAlgorithm = input("🔄 Please try again (bfs/ucs/astar): ")

        if chooseSearchAlgorithm == "bfs":
            exploredPath = BreadthFirstSearch(wordLadderGraph, startWord, goalWord)
        elif chooseSearchAlgorithm == "ucs":
            exploredPath = uniformCostSearch(wordLadderGraph, startWord, goalWord)
        elif chooseSearchAlgorithm == "astar":
            exploredPath = AStarSearch(graphHeuristics, startWord, goalWord)

        nextWord = giveHint(exploredPath, currentWord)
        if nextWord:
            console.print(Panel(
                f"[bold green]💡 Suggested next word: {nextWord}[/bold green]",
                style="green", width=60
            ))
        else:
            console.print("[bold red]❌ No more hints available![/bold red]")
            ladderContinues = False # No hints means there is no word in the graph that can precede the current one so broken ladder.
    
    return score, ladderContinues

def brokenLadder(graphHeuristics, startWord, goalWord, currentWord):
        
    exploredPath = AStarSearch(graphHeuristics, startWord, goalWord)

    nextWord = giveHint(exploredPath, currentWord)
    if nextWord:
        broken = True
    else:
        broken = False # No hints means there is no word in the graph that can precede the current one so broken ladder.

    return broken

# Function to check for duplicates in the path.
def isDuplicate(word, path):
    return word in path

#Player Class.
class Player: 
      def __init__(self, name, currentWord, listOfMoves, NumberOfMoves, hasWon):
        self.name = name
        self.currentWord = currentWord
        self.listOfMoves = [currentWord]
        self.NumberOfMoves = NumberOfMoves
        self.hasWon = hasWon


#The gameplay function for Multiplayer Mode.
def gameplayFunctionMutlplayerMode(wordLadderGraph, startWord, goalWord, graphHeuristics, forbiddenWord, restrictedLetter, wordLadderDictionary, player):
    time.sleep(0.8)
    os.system("cls")

    score = 0
    currentWord = player.currentWord
    path = player.listOfMoves
    
    console.print(Panel(
        f"[bold bright_red]🎯 Target Word:   {goalWord}[/bold bright_red]          [bold cyan]🔤 Current Word: {currentWord}[/bold cyan]\n\n"
        f"[bold magenta]🏁 Starting Word: {startWord}[/bold magenta]          [bold green]🎲 Number of Moves: {player.NumberOfMoves}[/bold green]",
        style="white",
        width=60,
        title=f"[bold yellow]🎮 Player {player.name}'s Turn[/bold yellow]",
        title_align="center"
    ))
    console.print(Panel(f"[bold blue]📈 Progress: {' → '.join(path)}[/bold blue]", style="white", width=60))
    score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)

    broken = brokenLadder(graphHeuristics, startWord, goalWord, currentWord)
    
    if broken == False:
        console.print(f"\n[bold red]⛔ Oops! The Ladder is between {currentWord} and {goalWord} is broken! [/bold red]")
        path.pop()
        currentWord = path[-1]
        console.print(Panel(
            f"[bold bright_red]🎯 Target Word:   {goalWord}[/bold bright_red]          [bold cyan]🔤 Current Word: {currentWord}[/bold cyan]\n\n"
            f"[bold magenta]🏁 Starting Word: {startWord}[/bold magenta]          [bold green]🎲 Number of Moves: {player.NumberOfMoves}[/bold green]",
            style="white",
            width=60,
            title=f"[bold yellow]🎮 Player {player.name}'s Turn[/bold yellow]",
            title_align="center"
        ))
        console.print(Panel(f"[bold blue]📈 Progress: {' → '.join(path)}[/bold blue]", style="white", width=60))
        score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
        broken = brokenLadder(graphHeuristics, startWord, goalWord, currentWord)

    if score == -3:
        player.NumberOfMoves += 2

    playerChoice = input("Enter next word: ")
    while isDuplicate(playerChoice, path):
        console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
        playerChoice = input("Enter a non-duplicate word: ")

    # Check if the word entered is a banned word.
    while playerChoice == forbiddenWord:
        console.print(f"[bold red]❌ {playerChoice} is a forbidden word! Try another.[/bold red]")
        score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
        if not ladderContinues:
                break 
        playerChoice = input("Now, enter word again: ")
        while isDuplicate(playerChoice, path):
            console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
            playerChoice = input("Enter a non-duplicate word: ")    

    
    # If word is a valid word, then check if it has a restricted letter.
    if validateExistenceOfWordInDictionary(currentWord, playerChoice, wordLadderDictionary):
        #currentWord = playerChoice
        # Check if the word entered has a restrcited letter.
        while True:
            isValid = True
            for letter in playerChoice:
                if letter == restrictedLetter:
                    console.print(f"[bold red]❌ The word {playerChoice} has a restricted letter! Try another.[/bold red]")

                    score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)

                    playerChoice = input("Now, enter word again: ")
                    while isDuplicate(playerChoice, path):
                        console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
                        playerChoice = input("Enter a non-duplicate word: ")

                    while playerChoice == forbiddenWord:
                        console.print(f"[bold red]❌ {playerChoice} is a forbidden word! Try another.[/bold red]")
                        score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
                        playerChoice = input("Now, enter word again: ")
                        while isDuplicate(playerChoice, path):
                            console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
                            playerChoice = input("Enter a non-duplicate word: ")

                    isValid = False

            if isValid:
                break
    
    # Validate if the children exist.
    if validateExistenceOfWordInActions(currentWord, playerChoice, wordLadderGraph):
        currentWord = playerChoice
        path.append(currentWord)

        player.currentWord = currentWord
        player.listOfMoves = path
        player.NumberOfMoves += 1
    else:
        console.print("[bold red]❌ Invalid word choice.[/bold red]\n")

    if player.currentWord == goalWord:
        console.print("\n[bold yellow]🎉 Congratulations! You've reached the goal word![/bold yellow]")
        player.hasWon = True


    return player

# The gameplay function.
def gameplayFunction(wordLadderGraph, startWord, goalWord, graphHeuristics, forbiddenWord, restrictedLetter, wordLadderDictionary):
    currentWord = startWord
    path = [currentWord]
    hasWon = False
    numberOfTurns = len(AStarSearch(graphHeuristics, startWord, goalWord)) + 5
    exploredPath = []
    optimalNumberOfMoves = len(AStarSearch(graphHeuristics, startWord, goalWord))
    ladderContinues = True
    actualNumberOfMoves = 0

    score = optimalNumberOfMoves * 10
    console.print(f"\n[bold green]Initial Score:[/bold green] {score} (Decreases with extra moves!)\n")

    while currentWord != goalWord:
        time.sleep(1)
        os.system("cls")
        console.print(Panel(f"[bold bright_red]🎯 Target Word:   {goalWord}[/bold bright_red]         [bold green] 📊 Current Score: {score}[/bold green]\n\n[bold magenta]🏁 Starting Word: {startWord}[/bold magenta]         [bold cyan] 🔤 Current Word: {currentWord}[/bold cyan]", style="white", width=60))

        console.print(Panel(f"[bold blue]📈 Your Progress: {' → '.join(path)}[/bold blue]", style="white", width=60))

        score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
        
        broken = brokenLadder(graphHeuristics, startWord, goalWord, currentWord)
        
        if broken == False:
            console.print(f"\n[bold red]⛔ Oops! The Ladder is between {currentWord} and {goalWord} is broken! [/bold red]")
            path.pop()
            currentWord = path[-1]
            console.print(f"\n[bold green]✅ The {currentWord} has been removed from the ladder! Try a new word or take the hint! [/bold green]")
            console.print(Panel(f"[bold bright_red]🎯 Target Word:   {goalWord}[/bold bright_red]         [bold green] 📊 Current Score: {score}[/bold green]\n\n[bold magenta]🏁 Starting Word: {startWord}[/bold magenta]         [bold cyan] 🔤 Current Word: {currentWord}[/bold cyan]", style="white", width=60))
            console.print(Panel(f"[bold blue]📈 Your Progress: {' → '.join(path)}[/bold blue]", style="white", width=60))
            print(path)
            score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
            broken = brokenLadder(graphHeuristics, startWord, goalWord, currentWord)

            
        playerChoice = input("Enter next word: ")
        while isDuplicate(playerChoice, path):
            console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
            playerChoice = input("Enter a non-duplicate word: ")

        # Check if the word entered is a banned word.
        while playerChoice == forbiddenWord:
            console.print(f"[bold red]❌ {playerChoice} is a forbidden word! Try another.[/bold red]")
            score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
            if not ladderContinues:
                    break 
            playerChoice = input("Now, enter word again: ")
            while isDuplicate(playerChoice, path):
                console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
                playerChoice = input("Enter a non-duplicate word: ")

        # If word is a valid word, then check if it has a restricted letter.
        if validateExistenceOfWordInDictionary(currentWord, playerChoice, wordLadderDictionary):
            #currentWord = playerChoice
            # Check if the word entered has a restrcited letter.
            while True:
                isValid = True
                for letter in playerChoice:
                    if letter == restrictedLetter:
                        console.print(f"[bold red]❌ The word {playerChoice} has a restricted letter! Try another.[/bold red]")

                        score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)

                        playerChoice = input("Now, enter word again: ")
                        while isDuplicate(playerChoice, path):
                            console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
                            playerChoice = input("Enter a non-duplicate word: ")

                        while playerChoice == forbiddenWord:
                            console.print(f"[bold red]❌ {playerChoice} is a forbidden word! Try another.[/bold red]")
                            score, ladderContinues = requestForHint(wordLadderGraph, graphHeuristics, startWord, goalWord, currentWord, score, path)
                            playerChoice = input("Now, enter word again: ")
                            while isDuplicate(playerChoice, path):
                                console.print(f"[bold red]❌ The word {playerChoice} has already been entered. Try another.[/bold red]")
                                playerChoice = input("Enter a non-duplicate word: ")

                        isValid = False

                if isValid:
                    break

        # Validate if the children exist.
        if validateExistenceOfWordInActions(currentWord, playerChoice, wordLadderGraph):
            currentWord = playerChoice
            path.append(currentWord)
        else:
            print(path)
            score -= 7 # Score will decrease by 7 if word does not exist in the ladder.
            console.print("[bold red]❌ -7 Invalid word choice. Try again.[/bold red]")

        numberOfTurns -= 1
        actualNumberOfMoves += 1
        if numberOfTurns == 0:
            console.print("[bold red]❗ Number of turns have finished.[/bold red]")
            break

        # Check if score is to be updated or not.
        if actualNumberOfMoves > optimalNumberOfMoves:
            score -= 5

    if currentWord == goalWord:
        time.sleep(1)
        os.system("cls")
        console.print(Panel(f"[bold bright_red]🎯 Target Word:   {goalWord}[/bold bright_red]         [bold green] 📊 Current Score: {score}[/bold green]\n\n[bold magenta]🏁 Starting Word: {startWord}[/bold magenta]         [bold cyan] 🔤 Current Word: {currentWord}[/bold cyan]", style="white", width=60))

        console.print(Panel(f"[bold blue]📈 Your Progress: {' → '.join(path)}[/bold blue]", style="white", width=60))

        console.print("\n[bold yellow]🎉 Congratulations! You have completed the word ladder![/bold yellow]")
        console.print(f"[bold yellow]🏆 Final Score: {score} [/bold yellow]")
        hasWon = True
    else:
        console.print("[bold red]You lost![/bold red]") 
        console.print(f"[bold yellow]Final Score: {score} [/bold yellow]")
        hasWon = False

    print("")
    return hasWon

# Function to allow players to choose level of difficulty and word selection.
def chooseGameMode():
    printGameName()
    print(Back.BLUE + Fore.WHITE + " Selection Mode Menu ")
    console.print("[bold blue]Choose word selection mode:[/bold blue]\n")
    console.print("[bold blue]1. Enter start and end words[/bold blue]")
    console.print("[bold blue]2. Automatic selection of start and end words[/bold blue]")
    console.print("[bold blue]3. Multiplayer with Automatic selection of start and end words[/bold blue]")
    console.print("[bold blue]4. Help[/bold blue]")
    console.print("[bold blue]5. Exit\n")

    wordSelectionMode = input("Enter your choice (1/2/3/4/5): ")
    wordSelectionMode = int(wordSelectionMode) 

    while wordSelectionMode < 1 or wordSelectionMode > 5:
        console.print("\n[bold red]❌ Invalid Input.[/]\n")
        print(Back.BLUE + Fore.WHITE + " Selection Mode Menu ")
        console.print("[bold blue]1. Enter start and end words[/bold blue]")
        console.print("[bold blue]2. Automatic selection of start and end words[/bold blue]")
        console.print("[bold blue]3. Multiplayer with Automatic selection of start and end words[/bold blue]")
        console.print("[bold blue]4. Help[/bold blue]")
        console.print("[bold blue]5. Exit\n")

        wordSelectionMode = input("Enter your choice (1/2/3/4/5): ")
        wordSelectionMode = int(wordSelectionMode) 

    return wordSelectionMode
    
# Choose difficulty level.
def chooseDifficultyLevel():
    print("")
    print(Back.BLUE + Fore.WHITE + " Difficulty Mode Menu ")
    console.print("[bold blue]Choose difficulty level:[/bold blue]\n")
    console.print("[bold green]1. Beginner Mode (Simple word ladders)[/bold green]")
    console.print("[bold dark_orange]2. Advanced Mode (Longer and complex ladders)[/bold dark_orange]")
    console.print("[bold red]3. Challenge Mode (Restricted Letters, banned words etc.)[/bold red]")
    console.print("[bold blue]4. Go back to main menu.[/bold blue]")
    difficulty = int(input("\nEnter your choice (1/2/3/4): "))

    while difficulty < 1 or difficulty > 4:
        console.print("\n[bold red]❌ Invalid Input.[/]\n")
        console.print("[bold green]1. Beginner Mode (Simple word ladders)[/bold green]")
        console.print("[bold dark_orange]2. Advanced Mode (Longer and complex ladders)[/bold dark_orange]")
        console.print("[bold red]3. Challenge Mode (Restricted Letters, banned words etc.)[/bold red]")
        console.print("[bold blue]4. Go back to main menu.[/bold blue]")
        difficulty = int(input("\nEnter your choice (1/2/3/4): "))

    return difficulty

console = Console()

def displayGameRules():
    os.system('cls') 
    time.sleep(0.5) 
    
    console.print(Panel(
        "[bold cyan]How to Play:[/bold cyan]\n"
        "> Change one letter at a time to form new words\n"
        "> Each word must be valid in the dictionary\n"
        "> Transform the starting word into the target word\n"
        "> Shorter paths give you more points!\n"
        "> Watch out for forbidden words and restricted letters in Challenge Mode\n"
        "> Use💡 hints if you're stuck (costs points)\n"
        "> Press q at any point in the game to exit",
        style="white",
        width=60,
        title="[bold yellow]W O R D   L A D D E R   G A M E   R U L E S[/bold yellow]",
        title_align="center"
    ))
    
    console.print("\n[bold yellow]Press Enter to continue...[/bold yellow]")
    randomInput = input()
    os.system('cls') 

def printGameName():
    os.system('cls') 
    time.sleep(0.5)

    print("")
    console.print(" [bold #8B4513]  W O R D   L A D D E R   G A M E 🪜[/bold #8B4513]".center(180))
    print("")

def printManualMode():
    os.system('cls') 
    time.sleep(0.5)

    print("")
    console.print(" [bold blue]  M A N U A L   S E L E C T I O N   M O D E 🛠️[/bold blue]".center(180))
    print("")

def printAutomaticMode():
    os.system('cls') 
    time.sleep(0.5)

    print("")
    console.print(" [bold green]  A U T O M A T I C   S E L E C T I O N   M O D E ⚙️[/bold green]".center(180))
    print("")

def printMultiPlayerMode():
    os.system('cls') 
    time.sleep(0.5)

    print("")
    console.print(" [bold magenta]  M U L T I   P L A Y E R   M O D E 👥[/bold magenta]".center(180))
    print("")



# Main Function.
def main():

    # Predefined lists:
    # Beginner Mode.
    beginnersModeList = [("hot", "dog"), ("tie", "dye"),  ("cap", "mop"), ("sky", "fly"), ("pet", "pan"), ("cat", "dog"), ("cot", "mop"), ("wig", "mug"), ("cup", "pat"), ("rug", "hat"), ("dip", "fry"), ("ear", "eye")]

    # Advanced Mode.
    advancedModeList = [("cold", "fall"), ("head", "tail"), ("slow", "down"), ("calf", "lamb"), ("many", "rule"), ("lost", "here"), ("hunt", "gone"), ("rich", "poor"), ("hook", "fish"), ("coal", "mine"), ("fish", "bird"), ("jump", "boat"), ("hair", "comb"), ("swim", "home")]

    # Challenge Mode.
    challengeModeList = [("wheat", "bread"), ("eager", "minds"), ("sweet", "dream"), ("cross", "river"), ("black", "white"), ("whole", "point"), ("smart", "brain"), ("speed", "quick")]

    #Reading words from words_dictionary.json
    with open("Dicticonay.json", "r") as words_dictonary:
        wordsData = json.load(words_dictonary)

    #Creating a dictionary for the game.
    WordLadderDictionary = dict()

    forbiddenWords = ["cleat", "", "sheep", "", "whine", "", "bears", "suits"]
    restrictedLetters = ["", "p", "", "p", "", "s", "", ""]
    beginnerCount = 0
    advancedCount = 0
    challengeCount = 0
    multiplayerCount = 0

    #Filtering out words with length greater than equal to 3 and less than 6.
    for word in wordsData: 
        if 3 <= len(word) < 6:
            WordLadderDictionary[word] = wordsData[word]

    while 1:
        selectionMode = chooseGameMode()
    
        # Exit game.
        if selectionMode == 5:
            console.print("\n[bold red]Exiting Game...[/]\n")
            exit(0)

        # See game rules for help.
        elif selectionMode == 4:
            displayGameRules()

        # Single Player - Automatic selection of start and end words.
        elif selectionMode == 2:
            printAutomaticMode()
            while True:
                difficulty = chooseDifficultyLevel()
                
                # Creating the graph.
                wordLadderGraph = createGraph(WordLadderDictionary, difficulty, "", "")

                #Beginner mode - Single Player.
                if difficulty == 1:

                    graphHeuristics = AssigningHeuristicCost(wordLadderGraph, beginnersModeList[beginnerCount][1])
                
                    canProceed = gameplayFunction(wordLadderGraph, beginnersModeList[beginnerCount][0], beginnersModeList[beginnerCount][1], graphHeuristics, "", "", WordLadderDictionary)
                    
                    if canProceed == True:
                        console.print("\n[bold green]🎉 You won! You can proceed to the next word pair.[/bold green]")
                        beginnerCount += 1
                    else:
                        console.print("\n[bold red]❌ You lost! To move to the next word pair, win this level.[/bold red]")

                    if(beginnerCount == len(beginnersModeList)):
                        print("You've Completed Beginner Level!")
                        beginnerCount = 0

                #Advance mode - Single Player.
                elif difficulty == 2:
                
                    graphHeuristics = AssigningHeuristicCost(wordLadderGraph, advancedModeList[advancedCount][1])
                
                    canProceed = gameplayFunction(wordLadderGraph, advancedModeList[advancedCount][0], advancedModeList[advancedCount][1], graphHeuristics, "", "", WordLadderDictionary)

                    if canProceed == True:
                        console.print("\n[bold green]🎉 You won! You can proceed to the next word pair.[/bold green]")
                        advancedCount += 1
                    else:
                        console.print("\n[bold red]❌ You lost! To move to the next word pair, win this level.[/bold red]")

                    if(advancedCount == len(advancedModeList)):
                        print("You've Completed Beginner Level!")
                        advancedCount = 0 

                # Challenge mode - Single Player.
                elif difficulty == 3:
                    # Recreate the graph without forbidden words.
                    wordLadderGraphF = createGraph(WordLadderDictionary, difficulty, forbiddenWords[challengeCount], restrictedLetters[challengeCount])

                    graphHeuristics = AssigningHeuristicCost(wordLadderGraphF, challengeModeList[challengeCount][1])
                
                    canProceed = gameplayFunction(wordLadderGraphF, challengeModeList[challengeCount][0], challengeModeList[challengeCount][1], graphHeuristics, forbiddenWords[challengeCount], restrictedLetters[challengeCount], WordLadderDictionary)

                    if canProceed == True:
                        console.print("\n[bold green]🎉 You won! You can proceed to the next word pair.[/bold green]")
                        challengeCount += 1
                    else:
                        console.print("\n[bold red]❌ You lost! To move to the next word pair, win this level.[/bold red]")

                    if(challengeCount == len(challengeModeList)):
                        print("You've Completed Beginner Level!")
                        challengeCount = 0 

                else:
                    os.system('cls') 
                    break

                print("Press Enter to continue...")
                input()
                os.system('cls')
                printManualMode() 

        # Words chosen by player.
        elif selectionMode == 1: 
            os.system('cls')
            printManualMode() 
            lengthOfWord = 0

            startWord = input("Enter start word: ")
            while startWord not in WordLadderDictionary:
                console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                startWord = input("\nEnter start word: ")
                while len(startWord) != 3 and len(startWord) != 4 and len(startWord) != 5:
                    console.print("[bold blue]You can only enter 3, 4 or 5 letter words.[/bold blue]")
                    startWord = input("\nEnter start word again: ")

            goalWord = input("\nEnter goal word: ")
            while goalWord not in WordLadderDictionary:
                console.print("\n[bold red]❌ Error: Goal word does not exist in the dictionary.[/bold red]")
                goalWord = input("\nEnter goal word: ")
                while len(goalWord) != 3 and len(goalWord) != 4 and len(goalWord) != 5:
                    console.print("[bold blue]You can only enter 3, 4 or 5 letter words.[/bold blue]")
                    goalWord = input("\nEnter start word again: ")

            while len(startWord) != len(goalWord):
                console.print("\n[bold red]❌ Error: Start Word and Goal Word should have the same length![/bold red]")
                console.print("[bold blue]Try again![\bold blue]")
                startWord = input("\nEnter start word: ")
                while startWord not in WordLadderDictionary:
                    console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                    startWord = input("\nEnter start word: ")
                    while len(startWord) != 3 and len(startWord) != 4 and len(startWord) != 5:
                        console.print("[bold blue]You can only enter 3, 4 or 5 letter words.[/bold blue]")
                        startWord = input("\nEnter start word again: ")

                goalWord = input("Enter goal word: ")
                while goalWord not in WordLadderDictionary:
                    console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                    goalWord = input("\nEnter goal word: ")
                    while len(goalWord) != 3 and len(goalWord) != 4 and len(goalWord) != 5:
                        console.print("[bold blue]You can only enter 3, 4 or 5 letter words.[/bold blue]")
                        goalWord = input("\nEnter start word again: ")

            lengthOfWord = len(startWord)
            if lengthOfWord == 3:
                difficulty = 1
            elif lengthOfWord == 4:
                difficulty = 2
            elif lengthOfWord == 5:
                difficulty = 3

            wordLadderGraph = createGraph(WordLadderDictionary, difficulty, "", "")
            
            path = BreadthFirstSearch(wordLadderGraph, startWord, goalWord)
            
            while path is None:
                console.print(f"\n[bold red]⛔ Oops! No path exists between {startWord} and {goalWord} [/bold red]")
                console.print("[bold blue]Try again![/bold blue]")
                startWord = input("\nEnter start word: ")
                while startWord not in WordLadderDictionary:
                    console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                    startWord = input("\nEnter start word: ")

                goalWord = input("Enter goal word: ")
                while goalWord not in WordLadderDictionary:
                    console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                    goalWord = input("\nEnter goal word: ")
                
                while len(startWord) != len(goalWord):
                    console.print("\n[bold red]❌ Error: Start Word and Goal Word should have the same length![/bold red]")
                    console.print("[bold blue]Try again![/bold blue]")
                    startWord = input("\nEnter start word: ")
                    while startWord not in WordLadderDictionary:
                        console.print("\n[bold red]❌ Error: Start word does not exist in the dictionary.[/bold red]")
                        startWord = input("\nEnter start word: ")
                        while len(startWord) != 3 and len(startWord) != 4 and len(startWord) != 5:
                            console.print("[bold blue]You can only enter 3, 4 or 5 letter words.[/bold blue]")
                            startWord = input("\nEnter start word again: ")

                path = BreadthFirstSearch(wordLadderGraph, startWord, goalWord)
            
            graphHeuristics = AssigningHeuristicCost(wordLadderGraph, "")
            gameplayFunction(wordLadderGraph, startWord, goalWord, graphHeuristics, forbiddenWords[0], restrictedLetters[challengeCount], WordLadderDictionary)

        # Multiplayer Mode.
        elif selectionMode == 3:
            beginnerMultiplayerCount = 0
            advancedMultiplayerCount = 0
            challengeMultiplayerCount = 0

            printMultiPlayerMode()
           
            while True:

                difficulty = chooseDifficultyLevel()
                # Creating the graph.
                wordLadderGraph = createGraph(WordLadderDictionary, difficulty, "", "")

                # Beginner mode - Multiplayer.
                if difficulty == 1:
                    
                    player01Name = input("\nEnter name of Player 01 🎮: ")
                    player02Name = input("Enter name of Player 02 🎮: ")


                    player01 = Player(player01Name, beginnersModeList[beginnerMultiplayerCount][0], 0, 0, False)
                    player02 = Player(player02Name, beginnersModeList[beginnerMultiplayerCount][0], 0, 0, False)
                    
                    graphHeuristics = AssigningHeuristicCost(wordLadderGraph, beginnersModeList[beginnerMultiplayerCount][1])

                    while True:
                        if player01.hasWon == False:
                            player01 =  gameplayFunctionMutlplayerMode(wordLadderGraph, beginnersModeList[beginnerMultiplayerCount][0], beginnersModeList[beginnerMultiplayerCount][1], graphHeuristics, "", "", WordLadderDictionary, player01)
                        
                        if player02.hasWon == False:
                            player02 =  gameplayFunctionMutlplayerMode(wordLadderGraph, beginnersModeList[beginnerMultiplayerCount][0], beginnersModeList[beginnerMultiplayerCount][1], graphHeuristics, "", "", WordLadderDictionary, player02)
                        
                        if player01.hasWon == True and player02.hasWon == True:
                            if player01.NumberOfMoves < player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow]Winner of the Game is Player {player01.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player01.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player01.NumberOfMoves}[/bold green]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            elif player01.NumberOfMoves > player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow] Winner of the Game is Player {player02.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player02.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player02.NumberOfMoves}[/bold blue]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            else:
                                console.print(Panel(f"[bold cyan]🤝 It's a draw[/bold cyan]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                        
                    beginnerMultiplayerCount += 1

                # Advanced Mode - Multiplayer.
                elif difficulty == 2:
                    
                    player01Name = input("\nEnter name of Player 01 🎮: ")
                    player02Name = input("Enter name of Player 02 🎮: ")


                    player01 = Player(player01Name, advancedModeList[advancedMultiplayerCount][0], 0, 0, False)
                    player02 = Player(player02Name, advancedModeList[advancedMultiplayerCount][0], 0, 0, False)
                    
                    graphHeuristics = AssigningHeuristicCost(wordLadderGraph, advancedModeList[advancedMultiplayerCount][1])

                    while True:
                        if player01.hasWon == False:
                            player01 =  gameplayFunctionMutlplayerMode(wordLadderGraph, advancedModeList[advancedMultiplayerCount][0], advancedModeList[advancedMultiplayerCount][1], graphHeuristics, "", "", WordLadderDictionary, player01)
                        
                        if player02.hasWon == False:
                            player02 =  gameplayFunctionMutlplayerMode(wordLadderGraph, advancedModeList[advancedMultiplayerCount][0], advancedModeList[advancedMultiplayerCount][1], graphHeuristics, "", "", WordLadderDictionary, player02)
                    
                        if player01.hasWon == True and player02.hasWon == True:
                            if player01.NumberOfMoves < player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow]Winner of the Game is Player {player01.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player01.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player01.NumberOfMoves}[/bold green]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            elif player01.NumberOfMoves > player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow] Winner of the Game is Player {player02.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player02.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player02.NumberOfMoves}[/bold green]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            else:
                                console.print(Panel(f"[bold cyan]🤝 It's a draw[/bold cyan]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                    advancedMultiplayerCount += 1

                # Challenge Mode - Multiplayer.
                elif difficulty == 3:

                    player01Name = input("\nEnter name of Player 01 🎮: ")
                    player02Name = input("Enter name of Player 02 🎮: ")



                    player01 = Player(player01Name,  challengeModeList[challengeMultiplayerCount][0], 0, 0, False)
                    player02 = Player(player02Name,  challengeModeList[challengeMultiplayerCount][0], 0, 0, False)
                    
                    wordLadderGraphF = createGraph(WordLadderDictionary, difficulty, forbiddenWords[challengeMultiplayerCount], restrictedLetters[challengeMultiplayerCount])

                    graphHeuristics = AssigningHeuristicCost(wordLadderGraphF, challengeModeList[challengeMultiplayerCount][1])

                    while True:
                        if player01.hasWon == False:
                            player01 =  gameplayFunctionMutlplayerMode(wordLadderGraph, challengeModeList[challengeMultiplayerCount][0], challengeModeList[challengeCount][1], graphHeuristics, forbiddenWords[challengeMultiplayerCount], restrictedLetters[challengeMultiplayerCount], WordLadderDictionary, player01)
                        
                        if player02.hasWon == False:
                            player02 =  gameplayFunctionMutlplayerMode(wordLadderGraph, challengeModeList[challengeMultiplayerCount][0], challengeModeList[challengeMultiplayerCount][1], graphHeuristics, forbiddenWords[challengeMultiplayerCount], restrictedLetters[challengeMultiplayerCount], WordLadderDictionary, player02)
                        
                        if player01.hasWon == True and player02.hasWon == True:
                            if player01.NumberOfMoves < player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow]Winner of the Game is Player {player01.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player01.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player01.NumberOfMoves}[/bold green]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            elif player01.NumberOfMoves > player02.NumberOfMoves:
                                console.print(Panel(f"🏅 [bold yellow] Winner of the Game is Player {player02.name}[/bold yellow]"
                                f"\n📈 [bold blue]Progress: {player02.listOfMoves}[/bold blue]"
                                f"\n🎲 [bold green]Number of Moves: {player02.NumberOfMoves}[/bold green]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                            else:
                                console.print(Panel(f"[bold cyan]🤝 It's a draw[/bold cyan]", title="[bold yellow]Match Result[/bold yellow]", style="white", width=60))
                                console.print("[bold yellow]Press Enter to Continue...[/bold yellow]")
                                input()
                                break
                    challengeMultiplayerCount += 1
                
                elif difficulty == 4:
                    os.system('cls') 
                    break

                # print("Press Enter to continue...")
                # input()
                os.system('cls')
                printMultiPlayerMode() 

if __name__ == "__main__":
    main()