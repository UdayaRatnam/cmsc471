import itertools
import sys
#sources used
#http://aima.cs.berkeley.edu/python/csp.html
#https://sandipanweb.wordpress.com/2017/03/17/solving-sudoku-as-a-constraint-satisfaction-problem-using-constraint-propagation-with-arc-consistency-checking-and-then-backtracking-with-minimum-remaning-value-heuristic-and-forward-checking/
#https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
rows = "ABCDEFGHI"
columns = "123456789"
row_blocks = ("ABC","DEF","GHI")
column_blocks = ("123","456","789")
DOMAIN = list(range(1,10))
characters = "ABCDEFGHI"
numbers = "123456789"

class Sudoku:
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
    def __init__(self, grid):
        self.variables = []
        self.domains = {}
        self.constraints = []
        self.neighbors = {}
        board = list(grid)
        #intiialize variables for each box, "A1,A2,A3..."
        self.variables = self.concatenate(rows,columns)
        #print(len(self.variables))
        
        print("_____________________________________")
        #initializing possible domain for each box in sudoku grid
        for index,box in enumerate(self.variables):
            if grid[index] == '0':
                self.domains[box] = DOMAIN
            else:
                self.domains[box] = int(grid[index])

        c1 = self.getColumnConstraints()#A1,B1,C1...
        c2 = self.getRowConstraints()#A1,A2,A3,A4...
        c3 = self.getBlockConstraints()#A1,A2,A3,B1,B2,B3,C1,C2,C3... (The 3x3 blocks)
        all_constraints = (c1+c2+c3)
        all_binary_constraints = []
        for constraint in all_constraints:
            binaries = []
            for binary in itertools.permutations(constraint,2):
                binaries.append(binary)
            for binary in binaries:
                arr = list(binary)
                if arr not in all_binary_constraints:
                    all_binary_constraints.append([arr[0],arr[1]])
        #print(all_binary_constraints)
        #print(len(all_binary_constraints))
        self.constraints = self.getBoardConstraints()
        print(self.constraints)
        print(len(self.constraints))
        

    def getBoardConstraints(self):
        c1 = self.getColumnConstraints()#A1,B1,C1...
        c2 = self.getRowConstraints()#A1,A2,A3,A4...
        c3 = self.getBlockConstraints()#A1,A2,A3,B1,B2,B3,C1,C2,C3... (The 3x3 blocks)
        all_constraints = (c1+c2+c3)
        all_binary_constraints = []
        for constraint in all_constraints:
            binaries = []
            for binary in itertools.permutations(constraint,2):
                binaries.append(binary)
            for binary in binaries:
                arr = list(binary)
                if arr not in all_binary_constraints:
                    all_binary_constraints.append([arr[0],arr[1]])
        return all_binary_constraints


    def getColumnConstraints(self):
        arr = []
        for c in columns:
            arr.append(self.concatenate(rows, c))
        return arr
    def getRowConstraints(self):
        arr = []
        for r in rows:
            arr.append(self.concatenate(r, columns))
        return arr
    def getBlockConstraints(self):
        arr = []
        for r in row_blocks:
            for c in column_blocks:
                arr.append(self.concatenate(r, c))
        return arr
        
    #helper functions
    def concatenate(self,x,y):
        arr = []
        for i in x:
            for j in y:
                arr.append(i+j)
        return arr

if __name__ == "__main__":
    p1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    p2 = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."
    p1 = p1.replace(".","0")
    p2 = p2.replace(".","0")
    """
    sudoku_grid = build_board(p1)
    print_board(sudoku_grid)
    solve(sudoku_grid)
    print()
    print_board(sudoku_grid)
    """
    test = Sudoku(p1)