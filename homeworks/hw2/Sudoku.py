import itertools
import sys
#sources used
#http://aima.cs.berkeley.edu/python/csp.html
#https://sandipanweb.wordpress.com/2017/03/17/solving-sudoku-as-a-constraint-satisfaction-problem-using-constraint-propagation-with-arc-consistency-checking-and-then-backtracking-with-minimum-remaning-value-heuristic-and-forward-checking/
#https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
rows = "ABCDEFGHI"
cols = "123456789"
row_blocks = ("ABC","DEF","GHI")
col_blocks = ("123","456","789")


class Sudoku:
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = []
        self.neighbors = {}
    """
    Sudoku Representation:
      1 2 3 4 5 6 7 8 9
    A . . . . . . . . .
    B . . . . . . . . .
    C . . . . . . . . .
    D . . . . . . . . .
    E . . . . . . . . .
    F . . . . . . . . .
    G . . . . . . . . .
    H . . . . . . . . .
    I . . . . . . . . .
    AC3:
    """
    

def get_empty(board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[i][j] == 0:
                return i,j
    return None
def isValid(board, guess, row, col):
    for i in range(DIMENSION):
        if board[row][i] == guess and col != i:
            return False
    for i in range(DIMENSION):
        if board[i][col] == guess and row != i:
            return False
    col_start = (col // 3)*3
    row_start = (row // 3)*3
    for i in range(row_start, row_start+3):
        for j in range(col_start, col_start+3):
            if board[i][j] == guess and (i,j) != (row,col):
                return False
    return True

def solve(board):
    test = get_empty(board)

    if test is None:
        return True
    else:
        r,c = get_empty(board)
    for num in range(1,10):
        if isValid(board, num, r,c):
            board[r][c] = num
            if solve(board):
                return True

        board[r][c] = 0
    return False

def build_board(input):
    input = input.replace(".","0")
    board = [[0 for i in range(DIMENSION)] for j in range(DIMENSION)]
    c = 0
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            board[i][j] = int(p1[c])
            c = c + 1
    return board

def print_board(grid):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            print(grid[i][j],end=" ")
        print()

if __name__ == "__main__":
    p1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    p2 = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."
    p1 = p1.replace(".","0")
    p2 = p2.replace(".","0")
    sudoku_grid = build_board(p1)
    print_board(sudoku_grid)
    solve(sudoku_grid)
    print()
    print_board(sudoku_grid)