import itertools
#sources used
#https://norvig.com/sudoku.html
#http://aima.cs.berkeley.edu/python/csp.html
#https://sandipanweb.wordpress.com/2017/03/17/solving-sudoku-as-a-constraint-satisfaction-problem-using-constraint-propagation-with-arc-consistency-checking-and-then-backtracking-with-minimum-remaning-value-heuristic-and-forward-checking/
#https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
#https://www.w3schools.com/python/ref_func_sorted.asp
#https://github.com/aimacode/aima-python/blob/master/csp.py
#https://docs.python.org/3/library/itertools.html#itertools.combinations
#https://rebec.casa/2019/01/13/a-python-sudoku-solver/
#https://steven.codes/blog/constraint-satisfaction-with-sudoku/
rows = "ABCDEFGHI"
columns = "123456789"
row_blocks = ("ABC","DEF","GHI")
column_blocks = ("123","456","789")
class Sudoku:
    """
    Sudoku Representation:
      1 2 3 4 5 6 7 8 9
    A . . . . . . . . . (A1,A2,A3,A4,A5,A6,A7,A8,A9)
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
        board = []
        for c in grid:
            board.append(c)
        #intiialize variables for each box, "A1,A2,A3..."
        self.variables = self.concatenate(rows,columns)
        #initializing possible domain for each box in sudoku grid
        self.domains = {}
        for index,box in enumerate(self.variables):
            if board[index] == '.':
                self.domains[box] = list(range(1,10))
            else:
                self.domains[box] = [int(board[index])]
        self.constraints = self.getBoardConstraints()
        self.neighbors = {}
        for v in self.variables:
            self.neighbors[v] = []
            for c in self.constraints:
                (x,y) = (c[0],c[1])
                if x == v:
                    self.neighbors[v].append(y)
        self.pruned = {}
        for index,var in enumerate(self.variables):
            if board[index] == '.':
                self.pruned[var] = []
            else:
                self.pruned[var] = int(board[index])
    #add the boxes value to assignment 
    def assign(self, var,val,assignment):
        assignment[var] = val
        #starts forward check to prune values
        for n in self.neighbors[var]:
            if n not in assignment:
                if val in self.domains[n]:
                    self.domains[n].remove(val)
                    self.pruned[var].append((n,val))
    #remove the boxes value from the assignment
    def unassign(self, box, assignment):
        if box in assignment:
            for x,y in self.pruned[box]:
                self.domains[x].append(y)
            self.pruned[box] = []
            del assignment[box]
    #If a domain of a variable is >1 that means Sudoku is not solved     
    def isDone(self):
        for x in self.variables:
            if len(self.domains[x]) > 1:
                return False
        return True
    #This function gets the row, column, and 3x3 constraints
    #essentially the rules of sudoku
    #Then converts into binary constraints for AC3 algorithm
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
    #checks all constraints
    def isConsistent(self, assignment, value, box ):
        consistency = True
        for key,val in assignment.items():
            if val == value and key in self.neighbors[box]:
                consistency = False
        return consistency
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
    #makes the sudoku boards coordinates
    def concatenate(self,x,y):
        arr = []
        for i in x:
            for j in y:
                arr.append(i+j)
        return arr
    def getNumOfConflicts(self,s,box,val):
        c = 0
        for n in s.neighbors[box]:
            if len(s.domains[n]) > 1 and val in s.domains[n]:
                c = c + 1
        return c
def revise(sudoku, xi, xj):
    revised = False
    for x in sudoku.domains[xi]:
        remove_element = True
        for y in sudoku.domains[xj]:
            if x != y:
                remove_element = False         
        if remove_element:
            revised = True
            sudoku.domains[xi].remove(x)
    return revised
def ac3(sudoku_board):
    queue = list(sudoku_board.constraints)
    while queue:  
        i,j = queue.pop(0)
        if revise(sudoku_board,i,j):
            if len(sudoku_board.domains[i]) == 0:
                return False  
            for k in sudoku_board.neighbors[i]:
                if k != i:
                    queue.append([k,i])
    return True
def backtrack(assignment, puzzle):
    if len(assignment) == len(puzzle.variables):
        return assignment
    var = mcv(assignment, puzzle)
    for value in lcv(puzzle, var):
        if puzzle.isConsistent(assignment, value, var):
            puzzle.assign(var, value, assignment)
            result = backtrack(assignment, puzzle)
            if result:
                return result
            puzzle.unassign(var, assignment) 
    return False
# Most Constrained Variable
def mcv(assignment, sudoku):
    unassigned = []
    for v in sudoku.variables:
        if v not in assignment:
            unassigned.append(v)
    return min(unassigned, key=lambda var: len(sudoku.domains[var]))
# Least Constrained Value
def lcv(sudoku, var):
    if len(sudoku.domains[var]) == 1:
        return sudoku.domains[var]
    return sorted(sudoku.domains[var], key=lambda val: sudoku.getNumOfConflicts(sudoku, var, val))
def print_board(boardObj, solved):
    print()
    c = 0
    d = 0
    for b in boardObj.variables:
        if solved:
            print(boardObj.domains[b][0], end = " ")
        else:
            print(boardObj.domains[b], end = " ")
        c+=1
        d+=1
        if c % 3 == 0 and c != 9 :
            print("|", end = " ")
        if c % 9 == 0:
            c = 0
            print()
            if d%27 == 0:
                d = 0
                print("----------------------")
    print()
def print_str(sudoku_str):
    print()
    c = 0
    d = 0
    for s in sudoku_str:
        print(s, end = " ")
        c+=1
        d+=1
        if c % 3 == 0 and c != 9:
            print("|", end = " ")
        if c % 9 == 0:
            c = 0
            print()
            if d % 27 == 0:
                d = 0
                print("----------------------")
    print()
##########################################################################################################
if __name__ == "__main__":
    p1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    p2 = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."
    p3 = "4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......"
    test = Sudoku(p3)
    print("Sudoku Board Puzzle 1 -- Before Solving")
    print_str(p3)
    arc_consistency = ac3(test)
    done = test.isDone()
    if done:
        print("AC3 WORKS")
        print_board(test,done)
    else:
        print("AC3 FAILED")
        print("STARTING THE BACKTRACK")
        assignment = {}
        assignment = backtrack(assignment, test)
        for d in test.domains:
            test.domains[d] = assignment[d]
        print_board(test, done)