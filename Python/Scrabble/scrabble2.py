from sys import stdin
import math
import sys
import random

TILES_USED = 0  # records how many tiles have been returned to user
CELL_WIDTH = 3  # cell width of the scrabble board
SHUFFLE = False  # records whether to shuffle the tiles or not


# inserts tiles into myTiles
def getTiles(myTiles):
    global TILES_USED
    while len(myTiles) < 7 and TILES_USED < len(Tiles):
        myTiles.append(Tiles[TILES_USED])
        TILES_USED += 1


# prints tiles and their scores
def printTiles(myTiles):
    tiles = ""
    scores = ""
    for letter in myTiles:
        tiles += letter + "  "
        thisScore = getScore(letter)
        if thisScore > 9:
            scores += str(thisScore) + " "
        else:
            scores += str(thisScore) + "  "

    print("\nTiles : " + tiles)
    print("Scores: " + scores)


# gets the score of a letter
def getScore(letter):
    for item in Scores:
        if item[0] == letter:
            return item[1]


# initialize n x n Board with empty strings
def initializeBoard(n):
    Board = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append("")
        Board.append(row)

    return Board


# put character t before and after the string s such that the total length
# of the string s is CELL_WIDTH.
def getString(s, t):
    global CELL_WIDTH
    s = str(s)
    rem = CELL_WIDTH - len(s)
    rem = rem // 2
    s = t * rem + s
    rem = CELL_WIDTH - len(s)
    s = s + t * rem
    return s


# print the Board on screen
def printBoard(Board):
    global CELL_WIDTH
    print("\nBoard:")
    spaces = CELL_WIDTH * " "
    board_str = "  |" + "|".join(getString(item, " ") for item in range(len(Board))) + "|"
    line1 = "--|" + "|".join(getString("", "-") for item in range(len(Board))) + "|"

    print(board_str)
    print(line1)

    for i in range(len(Board)):
        row = str(i) + " " * (2 - len(str(i))) + "|"
        for j in range(len(Board)):
            row += getString(Board[i][j], " ") + "|"
        print(row)
        print(line1)

    print()


scoresFile = open('scores.txt')
tilesFile = open('tiles.txt')

# read scores from scores.txt and insert in the list Scores
Scores = []
for line in scoresFile:
    line = line.split()
    letter = line[0]
    score = int(line[1])
    Scores.append([letter, score])
scoresFile.close()

# read tiles from tiles.txt and insert in the list Tiles
Tiles = []
for line in tilesFile:
    line = line.strip()
    Tiles.append(line)
tilesFile.close()

# decide whether to return random tiles
rand = input("Do you want to use random tiles (enter Y or N): ")
if rand == "Y":
    SHUFFLE = True
else:
    if rand != "N":
        print("You did not enter Y or N. Therefore, I am taking it as a Yes :P.")
        SHUFFLE = True
if SHUFFLE:
    random.shuffle(Tiles)

validBoardSize = False
while not validBoardSize:
    BOARD_SIZE = input("Enter board size (a number between 5 to 15): ")
    if BOARD_SIZE.isdigit():
        BOARD_SIZE = int(BOARD_SIZE)
        if BOARD_SIZE >= 5 and BOARD_SIZE <= 15:
            validBoardSize = True
        else:
            print("Your number is not within the range.\n")
    else:
        print("Are you a little tipsy? I asked you to enter a number.\n")

Board = initializeBoard(BOARD_SIZE)
printBoard(Board)

myTiles = []
getTiles(myTiles)
printTiles(myTiles)

########################################################################
# Write your code below this
########################################################################
import copy

"""
This function reads from the file inputted and appends each line to a list called dictionaryList, while also removing
\n. Its only parameter is filename.
"""
def readFromFile(filename):
    global dictionaryList
    dictionaryList = []
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        dictionaryList.append(line)
    file.close()
    return dictionaryList


"""
The purpose of this function is to collect a word input from the player. If the input is '***', the program will quit
Else the inputted characters are capitalised.
"""
def wordInput():
    global word

    word = input("\nEnter your word: ")     # ask player for word input

    if word == "***":                       # if input is '***', end program.
        quit()

    else:
        word = word.upper()                 # capitalise word input


"""
This function exists to obtain a location input from the player.
"""
def locationInput():
    global locationinput
    global locationList
    global row
    global col
    global direction

    locationinput = input("Enter the location in row:col:direction format: ")       # ask for location input

    if locationinput.count(":") == 2:                                               # if there are 2 ':' characters
        locationList = locationinput.split(":")                                     # put it into a list [row, col, direction]

        row = locationList[0]                       # sets respective index in locationList to row, col, and direction
        col = locationList[1]                       # for easier reference in future
        direction = locationList[2].upper()

    return

"""
The purpose of this function is to check if the word input belongs within the dictionary list (dictionaryList), from dictionary.txt.
If word is not contained within dictionary list, the function will return False.
It's only parameter is word. 
"""
def verifyDictionary(word):
    tempList = []               # create tempList in order to store word if word is found in dictionaryList
    if word in dictionaryList:
        tempList.append(word)

    if len(tempList) == 0:      # if word isn't in dictionaryList, length of tempList should be 0 and thus if so, return False
        return False


"""
The purpose of this function is to ensure the location input meets the required format of 'row:column:direction'.
If it meets the required format, it will not return anything. However, if it does not meet the required format, it will
return False.
Its parameters are locationinput, row, col, direction. locationinput is the raw input entered by the player,
"""
def verifyLocationFormat(locationinput, row, col, direction):
    if locationinput.count(":") != 2:                           # if raw input entered by player doesn't contain 2 ':'s
        return False

    if row.isdigit() == False or col.isdigit() == False:        # if row and column string entered by player is not a number
        return False

    if direction != "H" and direction != "V":                   # if the direction component is neither 'H' or 'V'
        return False


"""
The aim of this function is to verify whether or not the location entered is a valid one. It goes through 2 checks.
If the word exceeds the length of the board size when placed at a location (depending on H or V), it will return False.
If the row and column values are within the board size, then it will return True.
Its parameters are word, locationList. locationList is the location input in list form.
"""
def verifyLocation(word, locationList):
    global row
    global col
    global direction

    row = int(locationList[0])                  # converts row and column number strings to integers
    col = int(locationList[1])
    direction = locationList[2].upper()         # assigns direction to the third element of locationList (H or V)

    if direction == "H":
        if len(word) >= BOARD_SIZE - col + 1:   # if word exceeds board size at a location in the horizontal direction
            return False

    if direction == "V":
        if len(word) >= BOARD_SIZE - row + 1:   # if word exceeds board size at a location in the vertical direction
            return False

    if 0 <= row < BOARD_SIZE:                   # if row and col values are within the board size and greater than 0
        if 0 <= col < BOARD_SIZE:
            return True




"""
This function is concerned with the verification of tiles, including using on board tiles as well as tiles on hand from myTiles.
It ensures that at least one tile is used from the board every move excluding the first move and that the word can be made using
both the tiles on board and the tiles on hand.
It uses the parameters word, row, col, direction.
"""
def verifyTiles(word, row, col, direction):
    global myTiles
    global backupmyTiles
    global wordletterList
    global boardTilesUsed

    backupmyTiles = myTiles[:]                          # create a copy of myTiles
    wordletterList = [0 for i in range(len(word))]      # gnerate a list called wordletterList with amount of 0's
                                                        # corresponding to the length of word

    boardTilesUsed = []                                 # create list of tiles that belong on board that are to be used

    index = 0                                           # set index to 0

    if direction == "H":                            # if horizontal direction
        while index < len(word):                    # while index is less than length of word
            for j in range(col, col + len(word)):   # for the range of the starting column  to col + length of the word
                if Board[row][j] == "":             # if there is nothing on the board tile
                    index += 1                      # Go to next index

                else:
                    wordletterList[index] = Board[row][j]   # If letter at specific index matches board tile at j
                    boardTilesUsed.append(Board[row][j])    # Append letter to boardTilesUsed
                    index += 1                              # Go to next index

    if direction == "V":                            # same thing for vertical direction
        while index < len(word):
            for j in range(row, row + len(word)):
                if Board[j][col] == "":
                    index += 1
                else:
                    wordletterList[index] = Board[j][col]
                    boardTilesUsed.append(Board[j][col])
                    index += 1

    if Board != initial_Board:                                  # if it is not the first move,
        if wordletterList == [0 for i in range(len(word))]:     # and if wordletterList remains a list of 0's
            return False

    for index in range(len(word)):                          # at a specific index, in range of length of word
        if list(word)[index] in backupmyTiles:              # if tile in myTiles backup matches with letter of word
            if wordletterList[index] == 0:                  # and if wordletterList contains 0 at that index
                letter = list(word)[index]
                backupmyTiles.remove(letter)                # remove respective tile from myTiles backup
                wordletterList[index] = letter              # replace 0 in wondletterList with letter at the index
            if wordletterList == list(word):                # if wordletterList matches the word as a list,
                getscoreTilesUsed()                         # get the score of tiles used
                return True

    if wordletterList != list(word):                        # if wordletterList doesn't match word as a list
        return False


"""
This function obtains the score of a word as a sum of the score of individual letters within the word.
It's only parameter is word.
"""
def score(word):
    score = 0                           # set initial score to 0
    for letter in word:                 # iterate over each letter in word
        score += getScore(letter)       # continuously add the score of letter and update score

    return score

"""
The objective of this function is to obtain the actual score of a move. This is calculated by taking the sum of the scores
of individual tiles in the word and subtracting the sum of scores of individual tiles used from the board. i.e. because
tiles used from the board don't count towards the actual score.
"""
def getscoreTilesUsed():
    global scoreTilesUsed
    global wordletterList
    global boardTilesUsed

    scoreTilesUsed = 0                          # set initial score of tiles used to 0
    for letter in wordletterList:               # iterate over each letter in word
        scoreTilesUsed += getScore(letter)      # get the sum of individual letter scores and update it to score of tiles used

    for letter in boardTilesUsed:               # iterate over each tile in that was used on board
        scoreTilesUsed -= getScore(letter)      # continuously subtract the score of each tile from the score of tiles used


"""
The purpose of this function is to ensure a move is valid. If the move is deemed valid through a location and tile check
it will return True. If it fails one of these checks it will return False.
Its parameters are word, locationList. 
"""
def isMoveValid(word, locationList):
    if verifyLocation(word, locationList) is False:
        return False
    if verifyTiles(word, row, col, direction) is False:
        return False

    else:
        return True


"""
This function exists to place the tiles on the board in a horizontal direction.
Its only parameter is word.
"""
def setHorizontal(word):
    index = 0                                       # set index to 0
    while index < len(word):                        # for every letter in the word, place each letter consecutively one
        for j in range(col, col + len(word)):       # after the other in a horizontal direction
            Board[row][j] = list(word)[index]
            index += 1


"""
This function exists to place the tiles on the board in a vertical direction.
Its only parameter is word.
"""
def setVertical(word):
    index = 0                                       # set index to 0
    while index < len(word):                        # for every letter in the word, place each letter consecutively one
        for j in range(row, row + len(word)):       # after the other in a vertical direction
            Board[j][col] = list(word)[index]
            index += 1


"""
The purpose of this function is to generate a list of possible words that are less or equal to the board size.
It is designed to cut down the time complexity of finding the maximum move, by eliminating words that won't fit
on the board.
"""
def getPossibleWords():
    global possibleWords
    possibleWords = []                                          # create possibleWords list

    for word in dictionaryList:                                 # for each word in dictionaryList
        if len(word) <= BOARD_SIZE:                             # if the word is less than or equal to board size
            possibleWords.append(word)                          # add it to the list of possibleWords

    return possibleWords

"""
The objective of this function is to find the move which yields the maximum possible score for that turn.
It iterates over each word in the possibleWords list, and checks every single valid location  on the board
to see if the move is valid. If the move is valid, and the score of tiles used is greater than the maxScore, update
the maximum score and its respective word and location. It continues until it has tested out every word at every location.
"""
def maximum_move():
    global maxScore
    global maxWord
    global directionMax
    global rowMax
    global colMax
    print("\nCalculating maximum scoring move for next turn... ", end = "")
    possibleDirections = ["H", "V"]          # creates a list of possible directions
    maxScore = 0                             # set the initial value of maximum score to 0
    maxWord = ""                             # set the initial maximum word to an empty string

    if Board == initial_Board:                                                    # if it is the first move
        for word in possibleWords:                                                # for each word in possibleWords list
            for direction in possibleDirections:                                  # for each direction
                if isMoveValid(word, [midpoint, midpoint, direction]) is True:    # if the move is valid at a direction where col and row = midpoint
                    if scoreTilesUsed > maxScore:                                 # if the score of tiles used
                        maxScore = scoreTilesUsed                                 # is greater than the maximum score
                        maxWord = word
                        rowMax = copy.copy(midpoint)
                        colMax = copy.copy(midpoint)
                        directionMax = copy.copy(direction)                       # update maximum word, score and location
                        break
        return

    for word in possibleWords:                                              # if not the first move, for each word in possibleWords list
        for row in range(BOARD_SIZE):                                       # for each row within board size
            for col in range(BOARD_SIZE):                                   # for each column within board size
                for direction in possibleDirections:                        # for each direction
                    if isMoveValid(word, [row, col, direction]) is True:    # if the move is valid and score tiles used
                        if scoreTilesUsed > maxScore:                       # is greater than the maximum score
                            maxScore = scoreTilesUsed
                            maxWord = word
                            rowMax = copy.copy(row)
                            colMax = copy.copy(col)
                            directionMax = copy.copy(direction)             # update the maximum word, score and location
                            break
    return


readFromFile("dictionary.txt")

getPossibleWords()
initial_Board = copy.deepcopy(Board)     # create a copy of the initial board

midpoint = len(Board) // 2               # set midpoint of board to length of board integer division 2
total_score = 0                          # set initial total score to 0
outerLoop = True                         # set outerLoop to True (will remain True, until word input makes program quit)
innerLoop = False                        # set initial innerLoop to False

while outerLoop:
    if not innerLoop:                    # if innerLoop is False, a new turn occurs thus recalculate maximum move
        maximum_move()
        print("Done")
        innerLoop = True                 # once maximum move is found, set innerLoop to True

    while innerLoop:
        wordInput()
        locationInput()

        if verifyLocationFormat(locationinput, row, col, direction) is False:   # format is not valid, restart the inner loop
            print("Invalid Move!")
            break

        row = int(row)              # convert row and column to integers
        col = int(col)

        if Board == initial_Board:                              # if it is the first move
            if (int(row) and int(col)) != midpoint:             # if row and column are not equal to the midpoint of the board
                print(f"The location in the first move must be {midpoint}:{midpoint}:H or {midpoint}:{midpoint}:V\nInvalid Move!!!")
                break                                           # restart inner loop

        if verifyDictionary(word) is False:                     # if word doesn't belong in dictionary, restart inner loop
            print("This word doesn't exist in the dictionary!")
            break

        if isMoveValid(word, locationList) is False:            # if move is not valid, restart inner loop
            print("Invalid Move!")
            break

        myTiles = backupmyTiles[:]          # assigns myTiles to a copy of backupmyTiles if move is valid.


        if direction == "H":
            setHorizontal(word)             # place tiles horizontally

        if direction == "V":
            setVertical(word)               # place tiles vertically

        innerLoop = False                   # set innerLoop to False, to recalculate maximum move next turn
        total_score += scoreTilesUsed       # updates total score to previous total score + score this turn

        if maxWord == word or maxScore == scoreTilesUsed:       # if the user inputted word matches the maximum word
            print(f"Your move was the best move. Well done!")   # if the maximum score equals the score of tiles used
                                                                # print feedback

        print(f"Maximum possible score in this move was {maxScore} with word {maxWord} at {rowMax}:{colMax}:{directionMax}")
        print(f"Your score in this move: {scoreTilesUsed}\nYour total score is: {total_score}")

        printBoard(Board)               # reprints Board
        getTiles(myTiles)               # add more tiles to myTiles
        printTiles(myTiles)             # reprints myTiles



