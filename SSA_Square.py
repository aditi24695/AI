import turtle
import numpy as np
import math
import collections
from bitarray import bitarray
import random
import gc
import copy
import sys
import timeit

class TurtleGraphics():
    def __init__(self):
        pass

    def startScreen(self, State):
        print "State", State
        wn = turtle.Screen()
        tur = turtle.Turtle()
        tur.penup()
        tur.home()
        for i in range(0, n*(n+1)):
            row=i/n
            col = i%n
            tur.setpos(col*40, -row*40)
            if State[0][i] == True:
                tur.pendown()
                tur.forward(40)
                tur.dot(5)
                tur.penup()
        for i in range(0, n*(n+1)):
            row = i/n
            col= i%n
            tur.setpos(row*40, -col*40)
            if State[1][i] == True:
                print "row1", "col1", row, col, tur.xcor(), tur.ycor()
                tur.pendown()
                tur.right(90)
                tur.forward(40)
                tur.penup()
                tur.left(90)
        wn.reset()
        return

class Stick_sq():
    def __init__(self):
        pass

    def initialStateGenerator(self, n, p):
        num_sq = n*n;
        get_sq = n*n*p/100;
        state = [n*(n+1)*bitarray('0'), n*(n+1)*bitarray('0')]
        state = self.generateSquare(get_sq, n, state)
        return  state

    def generateSquare(self, get_sq, n, state):
        if (get_sq < (n * n / 2) and random.randint(0, 2) == 1):
            sq_num = random.randint(0, (n-1)*(n-1))
            row = sq_num/(n-1)
            col = sq_num%(n-1)
            if matrix[row][col] == 0 and matrix[row][col+1] == 0 and matrix[row+1][col] == 0 and matrix[row+1][col+1]== 0:
                state = self.update_vector(row, col, state, 2)
                get_sq = get_sq-1
                matrix[row][col] = True
                matrix[row+1][col] =True
                matrix[row][col+1] =True
                matrix[row+1][col+1] = True

        while get_sq > 0:
            sq_num = random.randint(0, n * n-1)
            row = sq_num / n
            col = sq_num % n
            if matrix[row][col] == 0:
                state = self.update_vector(row, col, state, 1)
                get_sq = get_sq-1
                matrix[row][col] = 1;
        return state

    def update_vector(self, row, col, state, sq_formed):
        if sq_formed == 2:
            state[0][(row)*n + col]  = True
            state[0][(row)*n + col +1] = True
            state[0][(row+2)*n + col]  = True
            state[0][(row+2)*n + col+1]  = True

            state[1][(col)*n + row] = True
            state[1][(col)*n + row+1] = True
            state[1][(col+2)*n + row] = True
            state[1][(col+2)*n + row+1] = True
        else:
            state[0][(row)*n + col]  = True
            state[0][(row+1)*n + col]  = True
            state[1][(col) * n + row] = True
            state[1][(col+1) * n + row ] = True
        return  state

    def checkGoalTest(self, isGoalNode):
        newMatrix = [[0 for x in range(n)] for y in range(n)]
        newState = copy.deepcopy(isGoalNode.state)
        count = 0
        for i in range(0, n*n-1):
            sq_num = i
            row_nu = i/n
            col_nu = i%n
            addc = self.check(isGoalNode, i)
            if addc == 1:
                newMatrix[row_nu][col_nu] = 1
                newState[0][(row_nu) * n + col_nu] = False
                newState[0][(row_nu + 1) * n + col_nu] = False
                newState[1][(col_nu) * n + row_nu] = False
                newState[1][(col_nu + 1) * n + row_nu] = False
            if addc == 2:
                newMatrix[row_nu][col_nu] = 1
                newMatrix[row_nu][col_nu+1] = 1
                newMatrix[row_nu+1][col_nu] = 1
                newMatrix[row_nu+1][col_nu+1] = 1
                newState[0][(row_nu) * n + col_nu] = False
                newState[0][(row_nu + 2) * n + col_nu] = False
                newState[1][(col_nu) * n + row_nu] = False
                newState[1][(col_nu + 2) * n + row_nu] = False
                newState[0][(row_nu) * n + col_nu+1] = False
                newState[0][(row_nu + 2) * n + col_nu+1] = False
                newState[1][(col_nu) * n + row_nu+1] = False
                newState[1][(col_nu + 2) * n + row_nu+1] = False
            count = count + addc
        if not count == goalSq:
            return False
        else:
            if newState[0].any() or newState[1].any():
                return False
            return True

    def check(self, isGoalNode, i):
        row_nu = i/n
        col_nu = i%n
        if isGoalNode.state[0][row_nu*n + col_nu] and isGoalNode.state[0][(row_nu+1)*n + col_nu] and isGoalNode.state[1][col_nu*n + row_nu] and isGoalNode.state[1][(col_nu + 1)*n + row_nu]:
            return 1
        try:
            if isGoalNode.state[0][row_nu*n + col_nu] and isGoalNode.state[0][row_nu*n + col_nu + 1] and isGoalNode.state[0][(row_nu+2)*n + col_nu] and isGoalNode.state[0][(row_nu+2)*n + col_nu+1] \
                    and isGoalNode.state[1][col_nu*n + row_nu] and isGoalNode.state[1][(col_nu+2)*n + row_nu]and isGoalNode.state[1][col_nu*n + row_nu+1] and isGoalNode.state[1][(col_nu+2)*n + row_nu + 1]:
                return 2
        except:
            return 0
        try:
            if isGoalNode.state[0][row_nu * n + col_nu] and isGoalNode.state[0][row_nu * n + col_nu + 1] and isGoalNode.state[0][row_nu * n + col_nu + 2] and \
                    isGoalNode.state[0][(row_nu + 3) * n + col_nu] and isGoalNode.state[0][(row_nu + 3) * n + col_nu + 1] and isGoalNode.state[0][
                                        (row_nu + 3) * n + col_nu + 2] \
                    and isGoalNode.state[1][col_nu * n + row_nu] and isGoalNode.state[1][col_nu * n + row_nu + 2] and isGoalNode.state[1][(col_nu + 2) * n + row_nu] and \
                    isGoalNode.state[1][col_nu * n + row_nu + 1] and isGoalNode.state[1][(col_nu + 2) * n + row_nu + 1] and isGoalNode.state[1][(col_nu + 2) * n + row_nu + 2]:
                return 3
        except:
            return 0
        return 0

    def displayResult(self):
        pass

class DFS():
    def __init__(self, n, p, goalSq):
        self.stack = [];
        self.n = n
        self.p= p
        self.goalSq = goalSq
        self.currNode = None
        self.finalNode = None
        self.myDict = {}
        self.max_stack = 0
        self.count_dfs_node = 0

    def saveDictionary(self, state):
        newState = state[0].append(state[1])
        self.myDict[newState] = 1
        return True

    def checkState(self, state):
        newState = state[0].append(state[1])
        if newState in self.myDict:
            return True
        return False

    def createRootNode(self):
        Stick_square = Stick_sq()
        initialState = Stick_square.initialStateGenerator(self.n, self.p)
        initialNodeGen = Node(initialState)
        return initialNodeGen

    def expandNode(self, ENode):
        self.stack.append(ENode)
        self.count_dfs_node = self.count_dfs_node  + 1
        for i in range(0, n*(n+1)):
            if ENode.state[0][i] == 1 and not ENode.actionList.__contains__(i):
                newNode = copy.deepcopy(ENode)
                newNode.state[0][i] = 0
                self.stack.append(newNode)
                self.count_dfs_node = self.count_dfs_node + 1
                ENode.actionList.append(i)
                return newNode
            if ENode.state[1][i] == 1 and not ENode.actionList.__contains__(n*(n+1)+i):
                newNode = copy.deepcopy(ENode)
                newNode.state[1][i] = 0
                self.stack.append(newNode)
                self.count_dfs_node = self.count_dfs_node + 1
                ENode.actionList.append(n*(n+1) + i)
                return newNode
        return None

    def pathCost(self):
        turtle_gr = TurtleGraphics()
        count = self.stack.__len__()
        while self.stack.__len__() != 0:
            CheckState = self.stack.pop().state
            turtle_gr.startScreen(CheckState)
            print CheckState
        return count

    def stateSearch(self, initialNode):
 #       initialNode = self.createRootNode();
        currentNode = initialNode
        print "Initial State", initialNode.state
        self.DFSUtil(initialNode)

    def DFSUtil(self, initialNode):
        if self.finalNode is not None: return
        expand_Node = self.expandNode(initialNode)
        Stick_square = Stick_sq()
        if Stick_square.checkGoalTest(initialNode):
            self.finalNode = initialNode
            print "Final State", self.finalNode
            return initialNode
        if not expand_Node is None:
            initialNode.children = expand_Node
            expand_Node.parent = initialNode
            self.DFSUtil(expand_Node)
        if self.finalNode is not None: return
        self.stack.pop()
        self.DFSUtil(self.stack.pop())
        gc.collect()

class BFS():
    def __init__(self, n, p , goalSq):
        self.q  = []
        self.n = n
        self.p= p
        self.goalSq = goalSq
        self.currNode = None
        self.count_bfs_node = 0
        self.max_queue = 0

    def createRootNode(self, initialState):
        initialNodeGen = Node(initialState)
        return initialNodeGen

    def expandNode(self, ENode):
        first = 0
        tempNode = ENode
        for i in range(0, n*(n+1)):
            if ENode.state[0][i] == True:
                if first == 0:
                    first = 1
                    newNode = copy.deepcopy(ENode)
                    newNode.state[0][i] = False
                    tempNode = newNode
                    newNode.parent= ENode
                    self.q.append(newNode)
                    self.count_bfs_node = self.count_bfs_node + 1
                else:
                    newNode = copy.deepcopy(ENode)
                    newNode.state[0][i] = False
                    newNode.parent = tempNode.parent
                    tempNode = newNode
                    self.q.append(newNode)
                    self.count_bfs_node = self.count_bfs_node + 1
            if ENode.state[1][i] == True:
               newNode =copy.deepcopy(ENode)
               newNode.state[1][i] = False
#               tempNode.addSiblingNode(newNode)
               newNode.parent = tempNode.parent
               self.q.append(newNode)
               self.count_bfs_node = self.count_bfs_node + 1
        return

    def stateSearch(self, initialNode):
        StickSquare = Stick_sq()
        self.q.append(initialNode)
        finalNode = None
        while(not self.q.__len__() == 0):
            if self.max_queue < self.q.__len__():
                self.max_queue = self.q.__len__()
            nextNode = self.q.pop(0)
            if StickSquare.checkGoalTest(nextNode) == True:
                finalNode = nextNode
                break
            self.expandNode(nextNode)
        return finalNode

    def pathCost(self, goalState):
        turtle_gr = TurtleGraphics()
        tempNode = goalState
        path = []
        count = 0
        while tempNode is not None:
            path.append(tempNode)
            turtle_gr.startScreen(tempNode.state)
            print "Final State", tempNode.state
            tempNode = tempNode.parent
            count  = count + 1
        return count

class Node():

    def __init__(self, state):
        self.state = state;
        self.actionList = [];
        self.parent = None

class DriverFunction():
    def __init__(self):
        pass
    def selectOption(self, option):
        n = 2
        p = 75
        goalSq = 2
        matrix = [[0 for x in range(n)] for y in range(n)]
        bfs_traversal = BFS(n, p, goalSq)
        dfs_traversal = DFS(n, p, goalSq)
        Stick_square = Stick_sq()
        if option == 1:
            Stick_square.initialStateGenerator(n, p)
        if option == 2:
            bfs_traversal.stateSearch()
        if option == 3:
            dfs_traversal.stateSearch()
        if option == 4:
            Stick_square.displayResult()

sys.setrecursionlimit(10000)

p = 75
goalSq = 2
n = 2

matrix = [[0 for x in range(n)] for y in range(n)]

stickSquare = Stick_sq()
TryState = stickSquare.initialStateGenerator(n, p)
turtle_c = TurtleGraphics()
turtle_c.startScreen(TryState)

start_bfs = timeit.default_timer()

bfs_traversal = BFS(n, p,goalSq)
rootNode = bfs_traversal.createRootNode(TryState)

print "R2 R7 - Size of Node", sys.getsizeof(rootNode)

finalNode = bfs_traversal.stateSearch(rootNode)
print(" final Node", finalNode)
bfs_cost = bfs_traversal.pathCost(finalNode)
stop_bfs = timeit.default_timer()

print "R4" , bfs_cost
print "R5" , stop_bfs - start_bfs
print "R1", bfs_traversal.count_bfs_node
print "R3", bfs_traversal.max_queue
del bfs_traversal

start_dfs = timeit.default_timer()
dfs_traversal = DFS(n, p, goalSq)
dfs_traversal.stateSearch(rootNode)
dfs_cost = dfs_traversal.pathCost()
stop_dfs = timeit.default_timer()


print "R9", dfs_cost
print "R10", stop_dfs - start_dfs
print "R6", dfs_traversal.count_dfs_node
print "R8", dfs_traversal.max_stack