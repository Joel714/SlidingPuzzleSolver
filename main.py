import sys, os, random

#Global "constant" variables
HILL_CLIMBING_ALG = 1
BREADTH_FIRST_ALG = 2
A_STAR = 3

COUNT_TILES_HEURISTIC = 1
SUM_OF_DISTANCE_HEURISTIC = 2
TILE_REVERSALS_HEURISTIC = 3
ALL_THREE_HEURISTIC = 4

MOVE_UP = 1
MOVE_RIGHT = 2
MOVE_DOWN = 3
MOVE_LEFT = 4

#Puzzle board class
class PuzzleBoard:
    def __init__(self, initBoard):
        
        self.board = [[0 for x in range(3)] for x in range(3)]
        for y in range(3):
            for x in range(3):
                self.board[y][x] = initBoard[y][x]
                
        #variables to keep track of where this board is in a tree
        self.heuristicValue = 0
        self.parentNode = None
        self.level = 0

#create the board that is the goal we want to reach
def create_goal():
    tempBoard = [[0 for x in range(3)] for x in range(3)]
    tempBoard[0][0] = 1
    tempBoard[0][1] = 2
    tempBoard[0][2] = 3
    tempBoard[1][0] = 4
    tempBoard[1][1] = 5
    tempBoard[1][2] = 6
    tempBoard[2][0] = 7
    tempBoard[2][1] = 8
    goalBoard = PuzzleBoard(tempBoard)
    return goalBoard

#prompt user to pick an algorithm, then return the choice
def select_algorithm():
    print('Please select an algorithm by typing the numer and pressing enter:')
    print('1. Steepest ascent (or descent) hill climbing')
    print('2. Breadth first search')
    print('3. A*')
    
    while True: 
        userInput = input()
        if(userInput == '1'):
            return HILL_CLIMBING_ALG
        elif(userInput == '2'):
            return BREADTH_FIRST_ALG
        elif(userInput == '3'):
            return A_STAR
        else:
            print('Bad input, must be between 1 and 3')

#prompt user to pick an heuristic, then return the choice
def select_heuristic(algorithm):
    print('Please select an heuristic by typing the numer and pressing enter:')
    print('1. Count out of place tiles')
    print('2. Sum of distances of out of place tiles')
    print('3. Tile reversals')
    print('4. Combination of all the above')

    if(algorithm == BREADTH_FIRST_ALG):
        return 0
    
    while True: 
        userInput = input()
        if(userInput == '1'):
            return COUNT_TILES_HEURISTIC
        elif(userInput == '2'):
            return SUM_OF_DISTANCE_HEURISTIC
        elif(userInput == '3'):
            return TILE_REVERSALS_HEURISTIC
        elif(userInput == '4'):
            return ALL_THREE_HEURISTIC
        else:
            print('Bad input, must be between 1 and 4')


def boards_are_equal(boardOne, boardTwo):
    for y in range(3):
            for x in range(3):
                if(boardOne[y][x] != boardTwo[y][x]):
                    return False
    return True


def default_board_one():
    tempBoard = [[0 for x in range(3)] for x in range(3)]
    tempBoard[0][0] = 5
    tempBoard[0][1] = 8
    tempBoard[0][2] = 0
    tempBoard[1][0] = 1
    tempBoard[1][1] = 7
    tempBoard[1][2] = 2
    tempBoard[2][0] = 4
    tempBoard[2][1] = 6
    tempBoard[2][2] = 3
    defaultBoard = PuzzleBoard(tempBoard)
    return defaultBoard

def default_board_two():
    tempBoard = [[0 for x in range(3)] for x in range(3)]
    tempBoard[0][0] = 0
    tempBoard[0][1] = 1
    tempBoard[0][2] = 3
    tempBoard[1][0] = 4
    tempBoard[1][1] = 2
    tempBoard[1][2] = 5
    tempBoard[2][0] = 7
    tempBoard[2][1] = 8
    tempBoard[2][2] = 6
    defaultBoard = PuzzleBoard(tempBoard)
    return defaultBoard

def default_board_three():
    tempBoard = [[0 for x in range(3)] for x in range(3)]
    tempBoard[0][0] = 2
    tempBoard[0][1] = 8
    tempBoard[0][2] = 3
    tempBoard[1][0] = 1
    tempBoard[1][1] = 6
    tempBoard[1][2] = 4
    tempBoard[2][0] = 7
    tempBoard[2][1] = 0
    tempBoard[2][2] = 5
    defaultBoard = PuzzleBoard(tempBoard)
    return defaultBoard

#prompt user to select a default board to solve
def create_board():
    print('Please select a board by typing the numer and pressing enter:')
    print('1. Default board below')
    print('   5 8  \n   1 7 2\n   4 6 3')
    print('2. Default board below')
    print('     1 3\n   4 2 5\n   7 8 6')
    print('3. Default board below')
    print('   2 8 3\n   1 6 4\n   7   5')
    while True: 
        userInput = input()
        if(userInput == '1'):
            return default_board_one()
        elif(userInput == '2'):
            return default_board_two()
        elif(userInput == '3'):
            return default_board_three()
        else:
            print('Bad input, must be between 1 and 3')

#create a child puzzle node based on a possible move from a parent
def create_child(parent, move):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    #find the position on the board of where the 0 is and store it in x1 and y1
    for y in range(3):
        for x in range(3):
            if(parent.board[y][x] == 0):
                x1 = x
                y1 = y

    #get position of x2 and y2 based on the next move to be made
    #and check to make sure move isn't out of bounds
    if(move == MOVE_UP and y1 > 0):
        x2 = x1
        y2 = y1 - 1
    elif(move == MOVE_RIGHT and x1 < 2):
        x2 = x1 + 1
        y2 = y1
    elif(move == MOVE_DOWN and y1 < 2):
        x2 = x1
        y2 = y1 + 1
    elif(move == MOVE_LEFT and x1 > 0):
        x2 = x1 - 1
        y2 = y1
    else:
        return None

    #create new child puzzle board
    #then swap x1,y1 with x2,y2
    newChild = PuzzleBoard(parent.board)

    tempInt = newChild.board[y1][x1]
    newChild.board[y1][x1] = newChild.board[y2][x2]
    newChild.board[y2][x2] = tempInt

    return newChild

#check to see if a board is already in the list of moves
def in_list_of_moves(listOfMoves, childBoard):
    for move in listOfMoves:
        if (boards_are_equal(move.board, childBoard.board)):
            return True
        
    return False

#count the number of tiles that do not match the goal board
def count_tiles(childBoard, goalBoard):
    heuristicCount = 0

    for y in range(3):
        for x in range(3):
            if(childBoard[y][x] != goalBoard[y][x]):
                heuristicCount = heuristicCount + 1
                
    return heuristicCount


#sum up the distance of how far away each out of place tile is
def sum_of_distance(childBoard, goalBoard):
    heuristicCount = 0

    for y1 in range(3):
        for x1 in range(3):
            if(childBoard[y1][x1] != goalBoard[y1][x1]):
                for y2 in range(3):
                    for x2 in range(3):
                        if(childBoard[y1][x1] == goalBoard[y2][x2]):
                            heuristicCount = heuristicCount + abs(x1 - x2)
                            heuristicCount = heuristicCount + abs(y1 - y2)

    return heuristicCount

#gives the number of how many two adjacent tiles are in each other's spot
def tile_reversals(childBoard, goalBoard):
    heuristicCount = 0
    #for each position, check if either the numbers above, below, right or left should be swapped
    for y in range(3):
        for x in range(3):
            if((childBoard[y][x] != goalBoard[y][x]) and ( childBoard[y][x] != 0) and ( goalBoard[y][x] != 0)):
                if((y > 0) and (childBoard[y][x] == goalBoard[y - 1][x]) and (childBoard[y - 1][x] == goalBoard[y][x])):
                    heuristicCount = heuristicCount + 1
                elif((x < 2) and (childBoard[y][x] == goalBoard[y][x + 1]) and (childBoard[y][x + 1] == goalBoard[y][x])):
                    heuristicCount = heuristicCount + 1
                elif((y < 2) and (childBoard[y][x] == goalBoard[y + 1][x]) and (childBoard[y + 1][x] == goalBoard[y][x])):
                    heuristicCount = heuristicCount + 1
                elif((x > 0) and (childBoard[y][x] == goalBoard[y][x - 1]) and (childBoard[y][x - 1] == goalBoard[y][x])):
                    heuristicCount = heuristicCount + 1
                    
    return heuristicCount
            
#an algorithm that picks the "best" choice given a heuristic, and keeps going until it finds a solution
def hill_climbing(heuristic, goal, start):
    listOfMoves = []
    listOfMoves.append(start)
    goalFound = False

    while(not goalFound):
	#create all possible moves from the last element in the list of moves
        childUp = create_child(listOfMoves[-1], MOVE_UP)
        childRight = create_child(listOfMoves[-1], MOVE_RIGHT)
        childDown = create_child(listOfMoves[-1], MOVE_DOWN)
        childLeft = create_child(listOfMoves[-1], MOVE_LEFT)

        listOfChildren = []
        #add new child only if the move was valid and it's not already in the list of moves
        if((childUp != None) and (not in_list_of_moves(listOfMoves, childUp))):
            listOfChildren.append(childUp)

        if((childRight != None) and (not in_list_of_moves(listOfMoves, childRight))):
            listOfChildren.append(childRight)

        if((childDown != None) and (not in_list_of_moves(listOfMoves, childDown))):
            listOfChildren.append(childDown)

        if((childLeft != None) and (not in_list_of_moves(listOfMoves, childLeft))):
            listOfChildren.append(childLeft)

        #check if any of the child nodes are the goal
        #if it is then return list of moves
        #otherwise give it a heuristic value
        for i in range(len(listOfChildren)):
            if (boards_are_equal(listOfChildren[i].board, goal.board)):
                listOfMoves.append(listOfChildren[i])
                return listOfMoves
            
            if (heuristic == COUNT_TILES_HEURISTIC):
                listOfChildren[i].heuristicValue = count_tiles(listOfChildren[i].board, goal.board)
            elif(heuristic == SUM_OF_DISTANCE_HEURISTIC):
                listOfChildren[i].heuristicValue = sum_of_distance(listOfChildren[i].board, goal.board)
            elif(heuristic == TILE_REVERSALS_HEURISTIC):
                listOfChildren[i].heuristicValue = tile_reversals(listOfChildren[i].board, goal.board)
            elif(heuristic == ALL_THREE_HEURISTIC):
                listOfChildren[i].heuristicValue = count_tiles(listOfChildren[i].board, goal.board) + sum_of_distance(listOfChildren[i].board, goal.board) + tile_reversals(listOfChildren[i].board, goal.board)


        #find the possible move to continue trying to solve the puzzle
        #if there is none, then there is no solution using this hill climbing approach
        best = None
        for i in range(len(listOfChildren)):
            if ((best == None) or (listOfChildren[i].heuristicValue < best.heuristicValue)):
                best = listOfChildren[i]

        if(best == None):
            print("No solution was found using this algorithm and heuristic")
            return listOfMoves


        listOfMoves.append(best)
        
#set the list of moves from start to end goal
def goal_to_start_list(goalNode):
    currentNode = goalNode
    moveList = []
    moveList.insert(0, currentNode)

    while(currentNode.parentNode != None):
        currentNode = currentNode.parentNode
        moveList.insert(0, currentNode)

    return moveList

#algorithm that creates all possilbe moves, checks if any of them are the goal state
#if it isn't then keep on making more moves
def breadth_first(heuristic, goal, start):
    openState = []
    closedState = []
    openState.append(start)

    while(len(openState) > 0):
        currentNode = openState.pop(0)
        #create possible moves that will be the child nodes to the current node
        childUp = create_child(currentNode, MOVE_UP)
        childRight = create_child(currentNode, MOVE_RIGHT)
        childDown = create_child(currentNode, MOVE_DOWN)
        childLeft = create_child(currentNode, MOVE_LEFT)

        listOfChildren = []
        #check to make sure the child node is a valid move 
        #and not already in the openState or closedState of moves
        #if it is then put it in openstate and list of child nodes
        if((not childUp == None) and (not in_list_of_moves(openState, childUp)) and (not in_list_of_moves(closedState, childUp))):
            childUp.parentNode = currentNode
            openState.append(childUp)
            listOfChildren.append(childUp)

        if((not childRight == None) and (not in_list_of_moves(openState, childRight)) and (not in_list_of_moves(closedState, childRight))):
            childRight.parentNode = currentNode
            openState.append(childRight)
            listOfChildren.append(childRight)

        if((not childDown == None) and (not in_list_of_moves(openState, childDown)) and (not in_list_of_moves(closedState, childDown))):
            childDown.parentNode = currentNode
            openState.append(childDown)
            listOfChildren.append(childDown)

        if((not childLeft == None) and (not in_list_of_moves(openState, childLeft)) and (not in_list_of_moves(closedState, childLeft))):
            childLeft.parentNode = currentNode
            openState.append(childLeft)
            listOfChildren.append(childLeft)

        closedState.append(currentNode)

        #check if any of the child nodes are the goal
        for i in range(len(listOfChildren)):
            if (boards_are_equal(listOfChildren[i].board, goal.board)):
                return goal_to_start_list(listOfChildren[i])
        
def give_heuristic_value(heuristic, childNode, goal):
    if (heuristic == COUNT_TILES_HEURISTIC):
        childNode.heuristicValue = count_tiles(childNode.board, goal.board)
    elif(heuristic == SUM_OF_DISTANCE_HEURISTIC):
        childNode.heuristicValue = sum_of_distance(childNode.board, goal.board)
    elif(heuristic == TILE_REVERSALS_HEURISTIC):
        childNode.heuristicValue = tile_reversals(childNode.board, goal.board)
    elif(heuristic == ALL_THREE_HEURISTIC):
        childNode.heuristicValue = count_tiles(childNode.board, goal.board) + sum_of_distance(childNode.board, goal.board) + tile_reversals(childNode.board, goal.board)

def a_star(heuristic, goal, start):
    openState = []
    closedState = []
    openState.append(start)

    while(len(openState) > 0):
        currentNode = openState.pop(0)
        #print(currentNode.board)

        childUp = create_child(currentNode, MOVE_UP)
        childRight = create_child(currentNode, MOVE_RIGHT)
        childDown = create_child(currentNode, MOVE_DOWN)
        childLeft = create_child(currentNode, MOVE_LEFT)

        listOfChildren = []

        #Check if childUp is in open or closed and place it in the right spot
        if(not childUp == None):
            childUp.parentNode = currentNode
            childUp.level = currentNode.level + 1
            give_heuristic_value(heuristic, childUp, goal)

        if((not childUp == None) and (not in_list_of_moves(openState, childUp)) and (not in_list_of_moves(closedState, childUp))):
            for i in range(len(openState)):
                if((childUp.heuristicValue <= openState[i].heuristicValue) or (i == len(openState) - 1)):
                    openState.insert(i, childUp)
                    break

            if(len(openState) == 0):
                openState.append(childUp)

            listOfChildren.append(childUp)

        elif(not childUp == None):
            #check open for child
            for i in range(len(openState)):
                if(boards_are_equal(childUp.board, openState[i].board)):
                    if(childUp.level < openState[i].level):
                        openState[i].parentNode = currentNode
                    

            for i in range(len(closedState)):
                if(boards_are_equal(childUp.board, closedState[i].board)):
                    if(childUp.level < closedState[i].level):
                        tempNode = closedState.pop(i)
                        for j in range(len(openState)):
                            if(childUp.heuristicValue <= openState[j].heuristicValue):
                                openState.insert(j, childUp)
                    break
                                
        #Check if childRight is in open or closed and place it in the right spot
        if(not childRight == None):
            childRight.parentNode = currentNode
            childRight.level = currentNode.level + 1
            give_heuristic_value(heuristic, childRight, goal)

        if((not childRight == None) and (not in_list_of_moves(openState, childRight)) and (not in_list_of_moves(closedState, childRight))):
            for i in range(len(openState)):
                if((childRight.heuristicValue <= openState[i].heuristicValue) or (i == len(openState) - 1)):
                    openState.insert(i, childRight)
                    break

            if(len(openState) == 0):
                openState.append(childRight)
            listOfChildren.append(childRight)
        elif(not childRight == None):
            #check open for child
            for i in range(len(openState)):
                if(boards_are_equal(childRight.board, openState[i].board)):
                    if(childRight.level < openState[i].level):
                        openState[i].parentNode = currentNode
                    
                   

            for i in range(len(closedState)):
                if(boards_are_equal(childRight.board, closedState[i].board)):
                    if(childRight.level < closedState[i].level):
                        tempNode = closedState.pop(i)
                        for j in range(len(openState)):
                            if(childRight.heuristicValue <= openState[j].heuristicValue):
                                openState.insert(j, childRight)
                    break
                                
        #Check if childDown is in open or closed and place it in the right spot
        if(not childDown == None):
            childDown.parentNode = currentNode
            childDown.level = currentNode.level + 1
            give_heuristic_value(heuristic, childDown, goal)

        if((not childDown == None) and (not in_list_of_moves(openState, childDown)) and (not in_list_of_moves(closedState, childDown))):
            for i in range(len(openState)):
                if((childDown.heuristicValue <= openState[i].heuristicValue) or (i == len(openState) - 1)):
                    openState.insert(i, childDown)
                    break

            if(len(openState) == 0):
                openState.append(childDown)      
            listOfChildren.append(childDown)
        elif(not childDown == None):
            #check open for child
            for i in range(len(openState)):
                if(boards_are_equal(childDown.board, openState[i].board)):
                    if(childDown.level < openState[i].level):
                        openState[i].parentNode = currentNode
                    

            for i in range(len(closedState)):
                if(boards_are_equal(childDown.board, closedState[i].board)):
                    if(childDown.level < closedState[i].level):
                        tempNode = closedState.pop(i)
                        for j in range(len(openState)):
                            if(childDown.heuristicValue <= openState[j].heuristicValue):
                                openState.insert(j, childDown)
                    break
                                
        #Check if childLeft is in open or closed and place it in the right spot
        if(not childLeft == None):
            childLeft.parentNode = currentNode
            childLeft.level = currentNode.level + 1
            give_heuristic_value(heuristic, childLeft, goal)

        if((not childLeft == None) and (not in_list_of_moves(openState, childLeft )) and (not in_list_of_moves(closedState, childLeft ))):
            for i in range(len(openState)):
                if((childLeft.heuristicValue <= openState[i].heuristicValue) or (i == len(openState) - 1)):
                    openState.insert(i, childLeft)
                    break

            if(len(openState) == 0):
                openState.append(childLeft)     
            listOfChildren.append(childLeft)
        elif(not childLeft == None):
            #check open for child
            for i in range(len(openState)):
                if(boards_are_equal(childLeft.board, openState[i].board)):
                    if(childLeft.level < openState[i].level):
                        openState[i].parentNode = currentNode
                    

            for i in range(len(closedState)):
                if(boards_are_equal(childLeft.board, closedState[i].board)):
                    if(childLeft.level < closedState[i].level):
                        tempNode = closedState.pop(i)
                        for j in range(len(openState)):
                            if(childLeft.heuristicValue <= openState[j].heuristicValue):
                                openState.insert(j, childLeft)
                    break

        #move current node to closed state
        closedState.append(currentNode)

        #check if any of the child nodes are the goal
        for i in range(len(listOfChildren)):
            if (boards_are_equal(listOfChildren[i].board, goal.board)):
                return goal_to_start_list(listOfChildren[i])

def solve_board(algorithm, heuristic, goal, start):
    if(algorithm == HILL_CLIMBING_ALG):
        return hill_climbing(heuristic, goal, start)
    elif(algorithm == BREADTH_FIRST_ALG):
        return breadth_first(heuristic, goal, start)
    elif(algorithm == A_STAR):
        return a_star(heuristic, goal, start)
    else:
        print('Error')

def output_moves(algorithm, heuristic, moveList):
    if(algorithm == HILL_CLIMBING_ALG):
        print("Hill climbing Algoritm")
    elif(algorithm == BREADTH_FIRST_ALG):
        print("Breadth first Algorithm")
    elif(algorithm == A_STAR):
        print("A* Algoritm")

    if (heuristic == COUNT_TILES_HEURISTIC):
        print("Count out of place tiles Heuristic")
    elif(heuristic == SUM_OF_DISTANCE_HEURISTIC):
        print("Sum of distance Heuristic")
    elif(heuristic == TILE_REVERSALS_HEURISTIC):
        print("Tile reversal Heuristic")
    elif(heuristic == ALL_THREE_HEURISTIC):
        print("All three Heuristic")
    elif(heuristic == 0):
        print("Heuristic does not apply in this case")

    print("Number of steps: " + str(len(moveList) - 1))
        
    for i in moveList:
        for y in range(3):
            print("%d %d %d" %(i.board[y][0], i.board[y][1], i.board[y][2]))
        #print(i.board)
        print("")
        
        

def main():
    goal = create_goal()
    print('This program will solve the 8 puzzle problem using different algrorithms and heuristics')
    algorithm = select_algorithm()
    heuristic = select_heuristic(algorithm)
    start = create_board()
    moveList = solve_board(algorithm, heuristic, goal, start)
    output_moves(algorithm, heuristic, moveList)


if __name__ == '__main__':
    main()

