import random
from graphics import GraphWin, Rectangle, Point, Text
import copy
import time

def createRandomGrid(size):
    grid = []
    for _ in range(size):
        grid.append([random.randint(1, 4) for _ in range(size)])
    return grid

def getColor(number):
    match number:
        case 0:
            return "white"
        case 1:
            return "blue"
        case 2:
            return "purple"
        case 3:
            return "red"
        case 4:
            return "gray"

def display_array(matrix, win):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            x1, y1 = j * 50, i * 50
            x2, y2 = x1 + 50, y1 + 50

            rect = Rectangle(Point(x1, y1), Point(x2, y2))
            
            rect.draw(win)
            rect.setFill(getColor(matrix[i][j]))

            text = Text(Point((x1 + x2) / 2, (y1 + y2) / 2), str(matrix[i][j]))
            text.draw(win)

    return win

def get_clicked_element(win, matrix):
    while True:
        click_point = win.getMouse()
        col = click_point.getX() // 50
        row = click_point.getY() // 50

        if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
            return int(row),int(col)

def clickSquare(grid, clickedX, clickedY):
    adjacentSiblingCoords = set()
    getAllTouchingSiblings(grid,clickedX,clickedY,adjacentSiblingCoords)
    for coordinate in adjacentSiblingCoords:
        x, y = coordinate
        grid[x][y] = 0
    
    applyGravity(grid)
    return removeGaps(grid) #return empty col indexes used to determine if game is won



def isClickable(grid, x ,y):
    if (grid[x][y] != 0 and #if not 0 and all adjesents are not the clicked value
        ((0 <= x-1 < len(grid) and grid[x][y] == grid[x-1][y]) or
        (0 <= x+1 < len(grid) and grid[x][y] == grid[x+1][y]) or
        (0 <= y-1 < len(grid[x]) and grid[x][y] == grid[x][y-1]) or
        (0 <= y+1 < len(grid[x]) and grid[x][y] == grid[x][y+1]))):
        return True
    else:
        return False
    
def existsMoves(grid):
    for row in range(len(grid)):
        for col in range(len(gridNumbers[0])):
            if isClickable(grid, row, col):
                return True
    return False

def getAllTouchingSiblings(grid, x, y, adjacentSiblingCoords):
    adjacentSiblingCoords.add((x, y))
    if(0 <= x-1 < len(grid) and grid[x][y] == grid[x-1][y] and (x-1, y) not in adjacentSiblingCoords): #if adjesent that is equal and not already in set
        getAllTouchingSiblings(grid, x-1, y, adjacentSiblingCoords) # add him
    
    if(0 <= x+1 < len(grid) and grid[x][y] == grid[x+1][y] and (x+1, y) not in adjacentSiblingCoords):
        getAllTouchingSiblings(grid, x+1, y, adjacentSiblingCoords)

    if(0 <= y-1 < len(grid[x]) and grid[x][y] == grid[x][y-1] and (x, y-1) not in adjacentSiblingCoords):
        getAllTouchingSiblings(grid, x, y-1, adjacentSiblingCoords)
    
    if(0 <= y+1 < len(grid[x]) and grid[x][y] == grid[x][y+1] and (x, y+1) not in adjacentSiblingCoords):
        getAllTouchingSiblings(grid, x, y+1, adjacentSiblingCoords)

    return adjacentSiblingCoords

def applyGravity(array_of_arrays):
    # Get the number of rows and columns
    rows = len(array_of_arrays)
    cols = len(array_of_arrays[0]) if rows > 0 else 0

    # Iterate through each column
    for col in range(cols):
        # Find the first non-zero element from the bottom
        for i in range(rows - 1, 0, -1):
            if array_of_arrays[i][col] == 0:
                # Move the non-zero element down (if found)
                for j in range(i - 1, -1, -1):
                    if array_of_arrays[j][col] != 0:
                        array_of_arrays[i][col], array_of_arrays[j][col] = array_of_arrays[j][col], array_of_arrays[i][col]
                        break

def swapColumns(matrix, col1, col2):
    for row in matrix:
        row[col1], row[col2] = row[col2], row[col1]

def removeGaps(array_of_arrays):

    allEmptyColIndexes = []
    rows = len(array_of_arrays)
    cols = len(array_of_arrays[0]) if rows > 0 else 0

    for colIndex in range(cols-1 , -1 , -1):
        if( array_of_arrays[rows-1][colIndex] == 0):
            allEmptyColIndexes.append(colIndex)
    
    allEmptyColIndexes = sorted(allEmptyColIndexes, reverse=True)
    lastcolumn = cols -1
    for col in allEmptyColIndexes:
        if(lastcolumn == col):
            lastcolumn-=1
        else:
            moveColumnToEnd(array_of_arrays, col)
    
    return allEmptyColIndexes

def checkGameWon(array_of_arrays):
    for row in array_of_arrays:
        if any(row):
            return False
    return True


def moveColumnToEnd(matrix, column_index):
    for row in matrix:
        row.append(row.pop(column_index))

def isGameWon(grid):
    return all(element == 0 for row in grid for element in row)

def getPossibleMoves(grid):
    posibleMoves = []

    for rowIndex in range(len(grid)):
        for colIndex in range(len(grid[0])):
            if isClickable(grid, rowIndex, colIndex):
                siblings = set()
                siblings = getAllTouchingSiblings(grid, rowIndex, colIndex, siblings)
                if (siblings not in posibleMoves):
                    posibleMoves.append(siblings)
    
    return posibleMoves


def getSolution(grid):
    solutionArray = []

    print("solving....")
    if solveGame(grid, solutionArray):
        print("SOLUTION!")
        solutionArray.reverse()
        print(solutionArray)
    else:
        print("no solution :(")

    return solutionArray


def solveGame(grid, solutionSteps):
    unchangedGrid = copy.deepcopy(grid)
    posibilies =  getPossibleMoves(grid)

    if len(posibilies ) > 0:
        for posiblity in posibilies:
            grid = copy.deepcopy(unchangedGrid)
            moveRow, moveCol = next(iter(posiblity))

            clickSquare(grid, moveRow, moveCol)
            
            if solveGame(grid, solutionSteps):
                solutionSteps.append((moveRow+1, moveCol+1)) # making human readable
                return True

    elif isGameWon(grid):
        return True
    else:
        return False

def PlayGame():
    #initial
    gridNumbers = createRandomGrid(5)
    emptyColIndexes = []
    solutionSteps = []
    print(gridNumbers)

    #display stuff
    win_height = 50 * len(gridNumbers)
    win_width = 50 * len(gridNumbers[0])
    win = GraphWin("Dynamic Array Display", win_width, win_height)

    #solver and timer

    solutionSteps = getSolution(gridNumbers)


    while True:
        window = display_array(gridNumbers, win)

        # click interaction
        clickedX, clickedY = get_clicked_element(window, gridNumbers)
        # if True:
        if(isClickable(gridNumbers, clickedX, clickedY)):
            emptyColIndexes = clickSquare(gridNumbers,clickedX,clickedY)

        # solving using solution...
        # for step in solutionSteps:
        #     stepX, stepY = step
        #     clickSquare(gridNumbers,stepX-1,stepY-1)
        
        #end state
        if len(emptyColIndexes) >= len(gridNumbers[0]):
            break

    print("game won")

def solverTesting(gridSize):

    #initial
    
    gridNumbers = createRandomGrid(gridSize)
    
    print(gridNumbers)

    start_time = time.time()

    solution = getSolution(gridNumbers)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("solution took: ", elapsed_time)
    return elapsed_time, bool(solution)

def printStats(statsArray, extraMessage):
    minimum_value = min(statsArray, key=lambda x: x[0])
    maximum_value = max(statsArray, key=lambda x: x[0])
    average_value = sum(x[0] for x in statsArray) / len(statsArray) if len(statsArray) > 0 else 0  # Avoid division by zero if the array is empty

    solvedCount = 0
    for stat in statsArray:
        if stat[1]:
            solvedCount+=1
    true_percentage = (solvedCount / len(statsArray)) * 100

    # Print the results
    print(extraMessage)
    print(statsArray)

    print(f"Minimum Value: {minimum_value}")
    print(f"Maximum Value: {maximum_value}")
    print(f"Average Value: {average_value}")
    print(f"Solve Percent: {true_percentage}")


if __name__ == "__main__":
    # PlayGame()
    solverStats = []
    for i in range(20):
        solveTime, solutionExists = solverTesting(6)
        solverStats.append([solveTime,solutionExists])
    printStats(solverStats, "")
    


