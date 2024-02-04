import random
import numpy as np
from graphics import GraphWin, Rectangle, Point, Text

def createRandomGrid():
    grid = []
    for _ in range(9):
        grid.append([random.randint(1, 4) for _ in range(9)])
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

# colors = [1,2,3,4] #blue, purple, red, black


# grid = createRandomGrid()
# for row in grid:
#     print(row)


def display_array(matrix, win):
    

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
    
    



def amIClickable(grid, x ,y):
    if (grid[x][y] != 0 and #if not 0 and all adjesents are not the clicked value
        ((0 <= x-1 < len(grid) and grid[x][y] == grid[x-1][y]) or
        (0 <= x+1 < len(grid) and grid[x][y] == grid[x+1][y]) or
        (0 <= y-1 < len(grid[x]) and grid[x][y] == grid[x][y-1]) or
        (0 <= y+1 < len(grid[x]) and grid[x][y] == grid[x][y+1]))):
        return True
    else:
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

    # for col in range(cols-emptyCols):
    #     if(array_of_arrays[rows-1][col] == 0):
    #         moveColumnToEnd(array_of_arrays, col)
    #         removeGaps(array_of_arrays)
            # if col != 0:
            #     swapColumns(array_of_arrays, col, cols-1)
            #     removeGaps(array_of_arrays)
            # else:
            #     swapColumns(array_of_arrays, col, col+1)


def checkGameWon(array_of_arrays):
    for row in array_of_arrays:
        if any(row):
            return False
    return True


def moveColumnToEnd(matrix, column_index):
    for row in matrix:
        row.append(row.pop(column_index))


if __name__ == "__main__":
    # Example matrix (replace with your own)
    # array_of_arrays = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 9]
    # ]

    gridNumbers = createRandomGrid()
    print(gridNumbers)
    # gridNumbers = [
    #     [4, 2, 2, 3, 3, 2, 4, 1, 4], 
    #     [4, 3, 2, 1, 1, 2, 3, 1, 2], 
    #     [4, 3, 1, 4, 1, 2, 1, 2, 4], 
    #     [3, 1, 4, 3, 3, 1, 1, 1, 1], 
    #     [1, 2, 2, 4, 3, 1, 2, 1, 1], 
    #     [2, 2, 4, 2, 1, 4, 4, 3, 1], 
    #     [4, 3, 3, 2, 2, 3, 2, 3, 1], 
    #     [2, 4, 2, 4, 3, 2, 4, 2, 4], 
    #     [2, 4, 3, 3, 3, 3, 1, 3, 1]]


#     gridNumbers = [[3, 3, 1, 2, 1, 3, 2, 4, 1], [2, 4, 3, 4, 2, 2, 4, 3, 1], [3, 3, 4, 2, 3, 1, 3, 1, 2], [1, 2, 3, 4, 2, 3, 3, 1, 1], [1, 4, 3, 2, 1, 4, 3, 3, 1], [4, 4, 3, 4, 3, 3, 1, 3, 4], [4, 1, 3, 2, 4, 1, 2, 2, 1], [4, 2, 4, 1, 1, 
# 3, 2, 4, 4], [2, 2, 2, 2, 4, 4, 2, 2, 4]] #double gap
    

#     [[3, 2, 1, 4, 2, 4, 4, 3, 3], [3, 1, 2, 4, 3, 3, 2, 1, 3], [3, 2, 3, 3, 1, 4, 3, 2, 3], [3, 4, 1, 1, 3, 1, 1, 3, 3], [3, 2, 3, 1, 1, 2, 4, 4, 2], [1, 1, 4, 4, 2, 1, 1, 1, 4], [4, 2, 2, 3, 4, 1, 3, 3, 2], [2, 3, 4, 3, 3, 
# 4, 3, 4, 2], [1, 1, 2, 4, 2, 3, 3, 2, 4]] #c letter case
    # Display the array
    emptyColIndexes = []
    
    rows = len(gridNumbers)
    cols = len(gridNumbers[0])
    win_width = 50 * cols
    win_height = 50 * rows
    win = GraphWin("Dynamic Array Display", win_width, win_height)
    # Get clicked element and print it in the console

    while True:
        window = display_array(gridNumbers, win)
        clickedX, clickedY = get_clicked_element(window, gridNumbers)


        if(amIClickable(gridNumbers, clickedX, clickedY)):
        # if True:
            clickSquare(gridNumbers,clickedX,clickedY)
            applyGravity(gridNumbers)
            emptyColIndexes = removeGaps(gridNumbers)

        if len(emptyColIndexes) >= cols:
            break
        # print(f"Clicked element: {clickedX, clickedY}")

    print("game won")


    # Close the window on click
