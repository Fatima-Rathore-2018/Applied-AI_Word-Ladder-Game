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