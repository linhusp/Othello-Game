import random
import sys
WIDTH= 8
HEIGHT= 8

# CREATE BOARD
def drawBoard(board):
    col= "  +---+---+---+---+---+---+---+---+"
    print(col)

    for y in range(HEIGHT-1, -1, -1):
        print(y+1, end= " ")
        for x in range(WIDTH):
            print("| %s" %board[x][y], end= " ")
        print("|")
        print(col)

    print("    1   2   3   4   5   6   7   8")

def getNewBoard():
    board= []
    
    for i in range(WIDTH):
        board.append([" "]*8)
        
    return board


# CHECK MOVE
def isOnBoard(x, y): 
    return x>=0 and x<=WIDTH-1 and y>=0 and y<=HEIGHT-1

def isValidMove(board, tile, xstart, ystart): 
    if board[xstart][ystart]!=" " or not isOnBoard(xstart, ystart):
        return False

    if tile=="X":
        otherTile= "O"
    else:
        otherTile= "X"

    flipTile= []

    for xd, yd in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y= xstart, ystart
        x+= xd
        y+= yd
        while isOnBoard(x, y) and board[x][y]==otherTile:
            x+= xd
            y+= yd 
            if isOnBoard(x, y) and board[x][y]==tile:
                while True:
                    x-= xd
                    y-= yd
                    if x==xstart and y==ystart:
                        break
                    flipTile.append([x, y])

    if len(flipTile)==0:
        return False

    return flipTile


# MAKE MOVE
def getBoardCopy(board):
    boardCopy= getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y]= board[x][y]
    
    return boardCopy

def getValidMoves(board, tile):
    validMoves= []

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y)!=False:
                validMoves.append([x, y])
    
    return validMoves

def getBoardWithValidMoves(board, tile):
    boardCopy= getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y]= "."
    
    return boardCopy

def getScoreOfBoard(board):
    xscore= 0
    oscore= 0

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y]=="X":
                xscore+= 1
            if board[x][y]=="O":
                oscore+= 1
    
    return {"X":xscore, "O":oscore}

def enterPlayerTile():
    tile= ""
    
    while not(tile=="X" or tile=="O"):
        tile= input("Do you want to be X or O?\n").upper()
    
    if tile=="X":
        return ["X", "O"]
    
    return ["O", "X"]

def whoGoesFirst():
    if random.randint(0, 1)==0:
        return "computer"

    return "player"

def makeMove(board, tile, xstart, ystart):
    tilesToFlip= isValidMove(board, tile, xstart, ystart)

    if tilesToFlip==False:
        return False

    board[xstart][ystart]= tile 

    for x, y in tilesToFlip:
        board[x][y]= tile
    
    return True 

# Player
def getPlayerMove(board, playerTile):
    DIGITS= "1 2 3 4 5 6 7 8".split()

    while True:
        move= input('Enter your move, "quit" to end game, or "hints" to toggle hints.\n').lower()

        if move=="quit" or move=="hints":
            return move

        if len(move)==2 and move[0] in DIGITS and move[1] in DIGITS:
            x= int(move[0])-1
            y= int(move[1])-1
            if isValidMove(board, playerTile, x, y)==False:
                continue
            else:
                break 
        else:
            print("That is not a valid move. Enter the column (1-8) and then the row (1-8).")
            
    return [x, y]


# AI
def isOnCorner(x, y):
    return(x==0 or x==WIDTH-1) and (y==0 or y==HEIGHT-1)

def getComputerMove(board, computerTile):
    possibleMoves= getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    #move corner if available
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    #highgest-scoring move
    bestScore= -1
    for x, y in possibleMoves:
        boardCopy= getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score= getScoreOfBoard(boardCopy)[computerTile]
        if score>bestScore:
            bestMove= [x, y]
            bestScore= score 
    
    return bestMove


# START
def printScore(board, playerTile, computerTile):
    scores= getScoreOfBoard(board)
    print("You: %s points. Computer: %s points." %(scores[playerTile], scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints= False
    turn= whoGoesFirst()
    print("The "+turn+" will go first.")

    #clear board
    board= getNewBoard()
    board[3][3]= "X"
    board[3][4]= "O"
    board[4][3]= "O"
    board[4][4]= "X"

    while True:
        playerValidMoves= getValidMoves(board, playerTile)
        computerValidMoves= getValidMoves(board, computerTile)

        if playerValidMoves==[] and computerValidMoves==[]:
            return board #end game
        
        elif turn=="player": #player's turn
            if playerValidMoves!=[]:
                if showHints:
                    validMovesBoard= getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                
                printScore(board, playerTile, computerTile)

                move= getPlayerMove(board, playerTile)
                if move=="quit":
                    print("Thanks for playing!")
                elif move=="hints":
                    showHints= not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            
            turn= "computer"
        
        elif turn=="computer": #com's turn
            if computerValidMoves!=[]:
                drawBoard(board)
                printScore(board, playerTile, computerTile)
                input("Press enter to see the computer's move.")
                move= getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            
            turn= "player"

# Out of code
print("Welcome to Reversegam!")
playerTile, computerTile= enterPlayerTile()

while True:
    finalBoard= playGame(playerTile, computerTile)
    drawBoard(finalBoard)
    scores= getScoreOfBoard(finalBoard)
    print("X scored %s points. O scored %s points." %(scores["X"], scores["O"]))

    if scores[playerTile]>scores[computerTile]:
        print("You beat the computer by %s points! Congratulation!" %(scores[playerTile]-scores[computerTile]))
    elif scores[playerTile]<scores[computerTile]:
        print("You lost. The computer beat you by %s points." %(scores[computerTile]-scores[playerTile]))
    else:
        print("The game was a tie!")

    if not input("Do you want to play again? (yes/no)\n").lower().startswith("y"):
        break
