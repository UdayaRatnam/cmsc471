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
#characters = "ABCDEFGHI"
#numbers = "123456789"

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
       
        board = list(grid)
        #intiialize variables for each box, "A1,A2,A3..."
        self.variables = self.concatenate(rows,columns)
        #print(len(self.variables))
        
        #print("_____________________________________")
        #initializing possible domain for each box in sudoku grid
        for index,box in enumerate(self.variables):
            if board[index] == '0':
                self.domains[box] = list(range(1,10))
            else:
                self.domains[box] = [int(board[index])]
        
        #self.domains = {v: list(range(1, 10)) if board[i] == '0' else [int(board[i])] for i, v in enumerate(self.variables)}

        self.constraints = self.getBoardConstraints()
        #print(self.constraints)
        #print(len(self.constraints))
        #neighbor values
        self.neighbors = {}
        for v in self.variables:
            self.neighbors[v] = []
            for c in self.constraints:
                if v == c[0]:
                    self.neighbors[v].append(c[1])
        #pruning values
        self.pruned = {}
        for index,var in enumerate(self.variables):
            if board[index] == '0':
                self.pruned[var] = []
            else:
                self.pruned[var] = int(board[index])
        #print("PRUNED")
        #print(self.pruned)
        #print(len(self.pruned))

    def fc(self, box, val, assignment):
        for n in self.neighbors[box]:
            if n not in assignment:
                if val in self.domains[n]:
                    self.domains[n].remove(val)
                    self.pruned[box].append((n,val))

    def assign(self, var,val,assignment):
        assignment[var] = val
        self.fc(var,val,assignment)
    def unassign(self, box, assignment):
        if box in assignment:
            for (x,y) in self.pruned[box]:
                self.domains[x].append(y)
            self.pruned[box] = []
            del assignment[box]
    def isConsistent(self, assignment, value, box ):
        consistency = True
        for key,val in assignment.items():
            if val == value and key in self.neighbors[box]:
                consistency = False
        return consistency

    def isDone(self):
        for x in self.variables:
            if len(self.domains[x]) > 1:
                return False
        return True

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
    
    def getNumOfConflicts(self,s,box,val):
        c = 0
        for n in s.neighbors[box]:
            if len(s.domains[n]) > 1 and val in s.domains[n]:
                c = c + 1
        return c


def isNotEqual(x,y):
    return x!=y

def revise(sudoku, xi, xj):
    revised = False
    for x in sudoku.domains[xi]:
        #print(x)
        #print("HEllo")
        if not any([isNotEqual(x,y) for y in sudoku.domains[xj]]):
            sudoku.domains[xi].remove(x)
            revised = True
        
    return revised
    
"""
def revise(s,x,y):
    revised = False
    for d in s.domains[x]:
        if not any([s.isNotEqual(d,b) for b in s.domains[y]]):
            s.domains[x].remove(d)
            revised = True
    return revised

"""

def ac3(sudoku_board):
    print("PLEASE TELL ME WE REACHED HERE")
    queue = list(sudoku_board.constraints)
    while queue:  
        i,j = queue.pop(0)
        #print(i,j)
        if revise(sudoku_board,i,j):
            #print("after if")
            if len(sudoku_board.domains[i]) == 0:
                print("Okay HOW ABOUT HERE")
                return False  
            for k in sudoku_board.neighbors[i]:
                if k != i:
                    queue.append([k,i])
    
    return True



def backtrack(assignment, sudoku):
    if len(assignment) == len(sudoku.variables):
        return assignment
    var = select_unassigned_variable(assignment, sudoku)
    for value in order_domain_values(sudoku, var):
        if sudoku.isConsistent(assignment, value, var):
            sudoku.assign(var, value, assignment)
            result = backtrack(assignment, sudoku)
            if result:
                return result
            sudoku.unassign(var, assignment)
    return False


# Most Constrained Variable heuristic
# Pick the unassigned variable that has fewest legal values remaining.
def select_unassigned_variable(assignment, sudoku):
    unassigned = [v for v in sudoku.variables if v not in assignment]
    return min(unassigned, key=lambda var: len(sudoku.domains[var]))

# Least Constraining Value heuristic
# Prefers the value that rules out the fewest choices for the neighboring variables in the constraint graph.
def order_domain_values(sudoku, var):
    if len(sudoku.domains[var]) == 1:
        return sudoku.domains[var]
    return sorted(sudoku.domains[var], key=lambda val: sudoku.getNumOfConflicts(sudoku, var, val))
##########################################################################################################
if __name__ == "__main__":
    p1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    p2 = "...26.7.168..7..9.19...45..82.1...4...46.29...5...3.28..93...74.4..5..367.3.18..."
    p1 = p1.replace(".","0")
    p2 = p2.replace(".","0")
    p3 = "000530000005000600000190503000004000000000164100370800008000040010000008004700921"
    print(len(p3))
    test = Sudoku(p3)
    #print(test.domains)
    print("_______________________________________________")
    if ac3(test):
        print("We made it this far")
        if test.isDone():
            print(test.variables)
            c = 0
            for v in test.variables:
                print(test.domains[v][0], end = " ")
                c+= 1
                if c%9 == 0:
                    print()
        else:
            print("Hey atleast u tried")
            assignment = {}
            for x in test.variables:
                if len(test.domains[x]) == 1:
                    assignment[x] = test.domains[x][0]
            assignment = backtrack(assignment, test)
            for d in test.domains:
                test.domains[d] = assignment[d] if len(d) > 1 else test.domains[d]
            if assignment:
                print("ALMOST DONE")
                #print(test.variables)
                c = 0
                for v in test.variables:
                    print(test.domains[v], end = " ")
                    c+= 1
                    if c%9 == 0:
                        print()



            
