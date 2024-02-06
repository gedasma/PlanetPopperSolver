#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include <set>
#include <algorithm>
#include <chrono>

using namespace std;

std::vector<std::vector<int>> readMatrixFromFile(const std::string& file_path) {
    std::ifstream file(file_path);

    if (!file.is_open()) {
        std::cerr << "Error opening file: " << file_path << std::endl;
        return {};
    }

    std::vector<std::vector<int>> matrix;

    std::string line;
    while (std::getline(file, line)) {
        std::vector<int> row;

        std::istringstream iss(line);
        std::string token;
        while (std::getline(iss, token, ',')) {
            row.push_back(std::stoi(token));
        }

        matrix.push_back(row);
    }

    file.close();

    return matrix;
}

std::vector<std::vector<int>> createRandomGrid(int size) {
    std::vector<std::vector<int>> grid;

    // Seed the random number generator
    std::srand(std::time(0));

    for (int i = 0; i < size; ++i) {
        std::vector<int> row;
        for (int j = 0; j < size; ++j) {
            // Generate a random integer between 1 and 4
            row.push_back(std::rand() % 4 + 1);
        }
        grid.push_back(row);
    }

    return grid;
}

void getAllTouchingSiblings(const std::vector<std::vector<int>>& grid, int x, int y, std::set<std::pair<int, int>>& adjacentSiblingCoords) {
    adjacentSiblingCoords.insert(std::make_pair(x, y));

    if (x - 1 >= 0 && grid[x][y] == grid[x - 1][y] && adjacentSiblingCoords.find(std::make_pair(x - 1, y)) == adjacentSiblingCoords.end()) {
        getAllTouchingSiblings(grid, x - 1, y, adjacentSiblingCoords);
    }

    if (x + 1 < grid.size() && grid[x][y] == grid[x + 1][y] && adjacentSiblingCoords.find(std::make_pair(x + 1, y)) == adjacentSiblingCoords.end()) {
        getAllTouchingSiblings(grid, x + 1, y, adjacentSiblingCoords);
    }

    if (y - 1 >= 0 && grid[x][y] == grid[x][y - 1] && adjacentSiblingCoords.find(std::make_pair(x, y - 1)) == adjacentSiblingCoords.end()) {
        getAllTouchingSiblings(grid, x, y - 1, adjacentSiblingCoords);
    }

    if (y + 1 < grid[x].size() && grid[x][y] == grid[x][y + 1] && adjacentSiblingCoords.find(std::make_pair(x, y + 1)) == adjacentSiblingCoords.end()) {
        getAllTouchingSiblings(grid, x, y + 1, adjacentSiblingCoords);
    }
}

void applyGravity(std::vector<std::vector<int>>& array_of_arrays) {
    int rows = array_of_arrays.size();
    int cols = (rows > 0) ? array_of_arrays[0].size() : 0;

    for (int col = 0; col < cols; ++col) {
        for (int i = rows - 1; i > 0; --i) {
            if (array_of_arrays[i][col] == 0) {
                for (int j = i - 1; j >= 0; --j) {
                    if (array_of_arrays[j][col] != 0) {
                        std::swap(array_of_arrays[i][col], array_of_arrays[j][col]);
                        break;
                    }
                }
            }
        }
    }
}

void moveColumnToEnd(std::vector<std::vector<int>>& matrix, int column_index) {
    for (auto& row : matrix) {
        row.push_back(row[column_index]);
        row.erase(row.begin() + column_index);
    }
}

std::vector<int> removeGaps(std::vector<std::vector<int>>& array_of_arrays) {
    std::vector<int> allEmptyColIndexes;

    int rows = array_of_arrays.size();
    int cols = (rows > 0) ? array_of_arrays[0].size() : 0;

    for (int colIndex = cols - 1; colIndex >= 0; --colIndex) {
        if (array_of_arrays[rows - 1][colIndex] == 0) {
            allEmptyColIndexes.push_back(colIndex);
        }
    }

    std::sort(allEmptyColIndexes.rbegin(), allEmptyColIndexes.rend());  // Use std::sort

    int lastcolumn = cols - 1;
    for (int col : allEmptyColIndexes) {
        if (lastcolumn == col) {
            lastcolumn -= 1;
        } else {
            moveColumnToEnd(array_of_arrays, col);
        }
    }

    return allEmptyColIndexes;
}

std::vector<int> clickSquare(std::vector<std::vector<int>>& grid, std::set<std::pair<int, int>> adjacentSiblingCoords) {

    for (const auto& coordinate : adjacentSiblingCoords) {
        int x, y;
        std::tie(x, y) = coordinate;
        grid[x][y] = 0;
    }

    applyGravity(grid);
    return removeGaps(grid); // return empty col indexes used to determine if the game is won
}

bool isClickable(const std::vector<std::vector<int>>& grid, int x, int y) {
    if (grid[x][y] != 0 &&
        ((x - 1 >= 0 && grid[x][y] == grid[x - 1][y]) ||
         (x + 1 < grid.size() && grid[x][y] == grid[x + 1][y]) ||
         (y - 1 >= 0 && grid[x][y] == grid[x][y - 1]) ||
         (y + 1 < grid[x].size() && grid[x][y] == grid[x][y + 1]))) {
        return true;
    } else {
        return false;
    }
}

bool isGameWon(const std::vector<std::vector<int>>& grid) {
    return std::all_of(grid.begin(), grid.end(),
                       [](const std::vector<int>& row) {
                           return std::all_of(row.begin(), row.end(), [](int element) { return element == 0; });
                       });
}

void getAllTouchingSiblings(const std::vector<std::vector<int>>& grid, int x, int y, std::set<std::pair<int, int>>& adjacentSiblingCoords);

std::vector<std::set<std::pair<int, int>>> getPossibleMoves(const std::vector<std::vector<int>>& grid) {
    std::vector<std::set<std::pair<int, int>>> possibleMoves;

    for (int rowIndex = 0; rowIndex < grid.size(); ++rowIndex) {
        for (int colIndex = 0; colIndex < grid[rowIndex].size(); ++colIndex) {
            if (isClickable(grid, rowIndex, colIndex)) {
                std::set<std::pair<int, int>> siblings;
                getAllTouchingSiblings(grid, rowIndex, colIndex, siblings);
                if (std::find(possibleMoves.begin(), possibleMoves.end(), siblings) == possibleMoves.end()) {
                    possibleMoves.push_back(siblings);
                }
            }
        }
    }

    return possibleMoves;
}

bool solveGame(std::vector<std::vector<int>>& grid, std::vector<std::pair<int, int>>& solutionSteps) {
    std::vector<std::vector<int>> unchangedGrid = grid;
    std::vector<std::set<std::pair<int, int>>> possibilities = getPossibleMoves(grid);

    if (!possibilities.empty()) {
        for (const auto& possibility : possibilities) {
            grid = unchangedGrid;

            // auto it = possibility.begin();
            int moveRow = possibility.begin()->first;
            int moveCol = possibility.begin()->second;

            clickSquare(grid, possibility);

            if (solveGame(grid, solutionSteps)) {
                solutionSteps.push_back(std::make_pair(moveRow + 1, moveCol + 1)); // Making it human-readable
                return true;
            }
        }
    } else if (isGameWon(grid)) {
        return true;
    }

    return false;
}

std::vector<std::pair<int, int>> getSolution(std::vector<std::vector<int>>& grid) {

    std::vector<std::pair<int, int>> solutionArray;
    std::vector<std::vector<std::vector<int>>> encounteredStates;

    std::cout << "Solving...\n";
    if (solveGame(grid, solutionArray)) {
        std::cout << "SOLUTION!\n";
        std::reverse(solutionArray.begin(), solutionArray.end());
        for (const auto& step : solutionArray) {
            std::cout << "(" << step.first << ", " << step.second << ") ";
        }
        std::cout << '\n';
    } 
    else {
        std::cout << "No solution :(\n";
    }

    return solutionArray;
}

int main(){
    
    std::string file_path = "matrix_from_image.txt";
    std::vector<std::vector<int>> mapGrid = readMatrixFromFile(file_path);
    // int gridSize = 6;
//     std::vector<std::vector<int>> mapGrid = createRandomGrid(gridSize);
//     std::vector<std::vector<int>> mapGrid = {
//         {2, 3, 4, 3, 3, 1, 1, 1, 3},
// {1, 1, 1, 2, 3, 2, 4, 3, 2},
// {3, 1, 2, 2, 4, 1, 2, 2, 1},
// {1, 2, 3, 3, 3, 1, 3, 2, 3},
// {2, 1, 2, 2, 2, 2, 1, 1, 2},
// {3, 2, 4, 3, 1, 4, 3, 2, 4},
// {4, 4, 4, 1, 4, 3, 4, 4, 1},
// {2, 2, 2, 2, 3, 1, 3, 3, 3},
// {1, 1, 2, 4, 1, 4, 3, 4, 2}
//     };

    // Display the grid
    for (const auto& row : mapGrid) {
        for (int value : row) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
    }
    //timer start
    auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::pair<int, int>> solution = getSolution(mapGrid);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - start;
    std::cout << "Solution took: " << duration.count() << " seconds" << std::endl;

    // for (int i = 0; i < 10; ++i) {
    // std::vector<std::vector<int>> testMap = mapGrid;

    // //timer start
    // auto start = std::chrono::high_resolution_clock::now();
    // //solution calculation
    // std::vector<std::pair<int, int>> testSolution = getSolution(testMap);
    // //timer end
    // auto end = std::chrono::high_resolution_clock::now();
    // std::chrono::duration<double> duration = end - start;
    // std::cout << "Time taken: " << duration.count() << " seconds" << std::endl;
    // }

    // std::cout << "Solution from main:\n";
    // for (const auto& step : solution) {
    //     std::cout << "(" << step.first << ", " << step.second << ") ";
    // }
    std::cout << "Press anything to close...";
    std::cin.ignore();

    return 0;
}