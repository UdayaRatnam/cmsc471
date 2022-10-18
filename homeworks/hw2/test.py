
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
