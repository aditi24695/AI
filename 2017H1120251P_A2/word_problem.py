'''
Name : Aditi Shah

ID: 2017H1120251
'''
import turtle
import copy
import random
import numpy as np
import sys
import time
import timeit

path_cost_greedy_h1 = 0
path_cost_greedy_h2 = 0
path_cost_hill_h1 = 0
path_cost_hill_h2 = 0
min_cost_path = 0
path_greedy_h1 = []
path_greedy_h2 = []
path_hill_h1 = []
path_hill_h2 = []

class TurtleGraphics():
    def __init__(self):
        pass

    def startScreen(self, initialState):
        wn = turtle.Screen()
        tur = turtle.Turtle()
        tur.clear()
        tur.penup()
        for i in range(0, 10):
            leng = initialState[i].length()
            print i
            tur.goto(-300, -200)
            tur.pendown()
            tur.forward((i+1)*60)
            for j in range(0, leng):
                tur.left(90)
                tur.forward((j+1)*40)
                tur.left(90)
                tur.forward(40)
                tur.left(90)
                tur.forward((j+1)*40)
                tur.left(90)
                tur.forward(40)
            tur.penup()
        tur.penup()
        tur.goto(-300, 200)
        for i in range(0, 10):
            leng = initialState[i].length()
            for j in range(0, leng):
                tur.penup()
                tur.goto(-300 + (i+1)*60 - 25, -200 + (j+1)*40 -25)
                tur.pendown()
                tur.write(initialState[i].getValue(j), font=("Arial",12, "normal"))
                tur.penup()
        return

    def glow(self, x, y):
        self.fillcolor("red")
        return

    def unglow(self, x, y):
        self.fillcolor("")
        return

    def moveBlockU(self, x1, y1, x2, y2, val):
        tur = turtle.Turtle()
        tur.pencolor("white")
        tur.goto(-300 + (x1+1) * 60 , -200 + (y1-1) * 40 )
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.goto(-300 + (x1+1) * 60 - 25, -200 + (y1) * 40 - 25)
        tur.write(val, font=("Arial", 12, "normal"))
        tur.pencolor("green")
        tur.penup()
        tur.goto(-300 + (x2+1) * 60, -200 + (y2) * 40)
        tur.pendown()
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.left(90)
        tur.forward(40)
        tur.penup()
        tur.goto(-300 + (x2+1) * 60 - 25, -200 + (y2 + 1) * 40 - 25)
        tur.pendown()
        tur.write(val, font=("Arial", 12, "normal"))
        return

class BlockWord:
    def __init__(self):
        self.x_list = np.arange(0, 100).tolist()
        self.S = [Stack() for i in range(10)]
        self.shuffle = 30
        self.total = 0
        self.turtleDraw = TurtleGraphics()

    def initialStateGenerator(self):
        for i in range(0, 10):
            rand_n = random.randint(1, 10) - 1
            self.total = self.total + rand_n
            for j in range(0, rand_n):
                self.S[i].push(self.generateNumber())
            print "length initial State Generator", self.S[i].length()
        return self.S

    def generateNumber(self):
        x = 0
        while x == 0:
            x = random.randint(1, 100) - 1
            if self.x_list[x] != 0:
                self.x_list[x] = 0
            else:
                x = 0
        return x

    def printState(self, initialState):
        for i in range(0, 10):
            leng = initialState[i].length()
            print "length", leng
            for j in range(0, leng):
               print initialState[i].getValue(j)
        return

    def checkGoalState(self, CheckState, goalState):
        if CheckState == None or goalState == None:
            return False
        for i in range(0, 10):
            leng = goalState[i].length()
            nleng = CheckState[i].length()
            if leng != nleng :
                return False
            for j in range(0, leng):
                if goalState[i].getValue(j) != CheckState[i].getValue(j):
                    return False
        return True

    def generateGoalState(self, initialState):
        self.goalState = copy.deepcopy(initialState)
        #self.printState(initialState)
#        self.turtleDraw.startScreen(initialState)
        rand_shuf_block = self.total*self.shuffle/100
        while rand_shuf_block != 0:
            shuf_x = random.randint(1, 10) - 1
            shuf_y = random.randint(1, 10) - 1
            self.move(shuf_x, shuf_y)
            rand_shuf_block = rand_shuf_block - 1
   #     self.printState(self.goalState)
        return self.goalState

    def move(self, x, y):
#        print x, y, "x, y", self.goalState[x].length(), self.goalState[y].length();
        if self.goalState[y].length() >= 10 and self.goalState[x].length() <=0 and self.goalState[x].peek() != -1:
            return
        global min_cost_path
        min_cost_path = min_cost_path + 1
        self.goalState[y].push(self.goalState[x].pop())
 #       print self.goalState[x].length(), self.goalState[y].length();
        return

class Stack:
    def __init__(self):
        self.st = []

    def push(self, x):
        self.st.append(x)
        return

    def pop(self):
        if self.st.__len__() == 0:
            return -1
        else:
            return self.st.pop()

    def length(self):
        return self.st.__len__()

    def isEmpty(self):
        if self.st.__len__() == 0:
            return True
        else:
            return False

    def getValue(self, j):
        return self.st[j];

    def peek(self):
        if self.length() == 0:
            return -1
        val = self.pop()
        self.push(val)
        return val

class HeuristicFunction:
    def __init__(self):
        pass

    #This is maximization problem - We are trying to maximize the score.
    # Positive score for correct position and negative score for incorrect position
    def heuristicFunction_h1(self, currState, goalState):
        cost = 0
        for i in range(0, 10):
            leng = currState[i].length()
            nleng = goalState[i].length()
            for j in range(0, self.min(leng, nleng)):
                if goalState[i].getValue(j) == currState[i].getValue(j):
                    cost = cost + (11-j)
                else:
                    cost = cost - (11-j)
            if leng > nleng:
                for k in range(0, leng - nleng):
                    cost = cost -(11 - (nleng + k))
        return cost

    #This is minimization problem.
    def heuristicFunction_h2(self, currState, goalState):
        cost = 0
        for i in range(0, 10):
            leng = currState[i].length()
            nleng = goalState[i].length()
            cost_cum = 1
            for j in range(0, self.min(leng, nleng)):
                if goalState[i].getValue(j) == currState[i].getValue(j) and cost_cum == 1:
                    continue
                else:
                    cost = cost + (11 - j)
                    cost_cum = 0
            if leng > nleng:
                for k in range(0, leng - nleng):
                    cost = cost + (11-(k + nleng))
        return cost

    def min(self, a, b):
        if a< b:
            return a
        else:
            return b

class GreedyBestFirstAlgo:
    def __init__(self, initialNode, goalNode):
        self.initialNode = initialNode
        self.goalNode = goalNode
        self.heuristicC = HeuristicFunction()
        self.bWord = BlockWord()
        self.path_h1 = []
        self.path_h2 = []
        self.turtleC =TurtleGraphics()

    def nextState_h1(self, prevState):
        maxState = None
        movex = -1
        movey = -1
        mincost = -sys.maxint-1
        print "Goal State h1", self.heuristicC.heuristicFunction_h1(self.goalNode.state_h1, self.goalNode.state_h1)
        if self.bWord.checkGoalState(prevState, self.goalNode.state_h1):
            return maxState
        for i in range(0, 10):
            for j in range(0,10):
                if i != j and prevState[i].length() > 0 and prevState[j].length() <= 10:
                    newState = copy.deepcopy(prevState)
                    newState = self.moveBlock(i, j, newState)
                    cost = self.heuristicC.heuristicFunction_h1(newState, self.goalNode.state_h1)
                    if cost > mincost:
                        mincost = cost
                        maxState = copy.deepcopy(newState)
                        movex = i
                        movey = j
        self.turtleC.moveBlockU(movex, prevState[movex].length(), movey, prevState[movey].length(), prevState[movex].peek())
        print "Cost h1", mincost
        return maxState

    def nextState_h2(self, initialState):
        minState = None
        maxcost = sys.maxint
        movex = -1
        movey = -1
        print "Goal State h2", self.heuristicC.heuristicFunction_h2(self.goalNode.state_h1, self.goalNode.state_h1)
        if self.bWord.checkGoalState(initialState, self.goalNode.state_h1):
            return minState
        for i in range(0, 10):
            for j in range(0, 10):
                if i != j and initialState[i].length() >0 and initialState[j].length() <=10:
                    newState = copy.deepcopy(initialState)
                    newState = self.moveBlock(i, j, newState)
                    cost = self.heuristicC.heuristicFunction_h2(newState, self.goalNode.state_h1)
                    if cost < maxcost:
                        maxcost = cost
                        minState = copy.deepcopy(newState)
                        movex = i
                        movey = j
        self.turtleC.moveBlockU(movex, initialState[movex].length(), movey, initialState[movey].length(), initialState[movex].peek())
        print "Cost h2", maxcost
        return minState

    def moveBlock(self, x, y, currState):
        if currState[y].length() >= 10 and currState[x].length() <= 0:
            return currState
        currState[y].push(currState[x].pop())
        return currState

    def StateSearch(self, initialNode, goalNode):
        self.initialNode = initialNode
        self.goalNode = goalNode
        global path_greedy_h1
        path_greedy_h1.append(copy.deepcopy(initialNode.state_h1))
        global path_greedy_h2
        path_greedy_h2.append(copy.deepcopy(initialNode.state_h1))
        self.Node_h1 = copy.deepcopy(initialNode)
        self.Node_h2 = copy.deepcopy(initialNode)
        rec = 0
        while(True and rec < 100):
            rec = rec + 1
            if not self.Node_h1 == None:
                global path_cost_greedy_h1
                path_cost_greedy_h1 = path_cost_greedy_h1 + 1
                newState = self.nextState_h1(self.Node_h1.state_h1)
                if newState is None:
                    self.Node_h1 = None
                    continue
                path_greedy_h1.append(copy.deepcopy(newState))
                self.Node_h1 = Node(newState)
                self.pathHeuristic1(copy.deepcopy(newState))
            if not self.Node_h2 is None:
                global path_cost_greedy_h2
                path_cost_greedy_h2 = path_cost_greedy_h2 + 1
                newState = self.nextState_h2(self.Node_h2.state_h1)
                if newState == None:
                    self.Node_h2 = None
                    continue
                path_greedy_h2.append(copy.deepcopy(newState))
                self.Node_h2 = Node(newState)
                self.pathHeuristic2(copy.deepcopy(newState))
            if self.Node_h1 == None and self.Node_h2 == None:
                break
        return self.Node_h1, self.Node_h2

    def pathHeuristic1(self, newState):
        self.path_h1.append(newState)
        return

    def pathHeuristic2(self, newState):
        self.path_h2.append(newState)
        return

    def displayPath1(self):
        plength_1 = path_hill_h1.__len__()
        print plength_1
        for i in range(0, plength_1):
            print "Path", path_hill_h1[i], plength_1

    def displayPath2(self):
        plength_2 = path_hill_h2.__len__()
        print plength_2
        for i in range(0, plength_2):
            print "Path", path_hill_h2[i], plength_2

    def min(self, x, y):
        return x if x<y else y

    def max(self, x, y):
        return x if x>y else y

class HillClimbingAlgo:
    def __init__(self, initialNode, goalNode):
        self.initialNode = initialNode
        self.goalNode = goalNode
        self.heuristicC = HeuristicFunction()
        self.bWord = BlockWord()
        self.path_h1 = []
        self.path_h2 = []
        self.turtleC = TurtleGraphics()

    def nextState_h1(self, initialState):
        maxState1 = None
        maxState2 = None
        mincost1 = self.heuristicC.heuristicFunction_h1(initialState, self.goalNode.state_h1)
        mincost2 = self.heuristicC.heuristicFunction_h1(initialState, self.goalNode.state_h1)
        print "HC Cost h1" , self.heuristicC.heuristicFunction_h1(initialState, self.goalNode.state_h1)
        print "HC Goal State h1", self.heuristicC.heuristicFunction_h1(self.goalNode.state_h1, self.goalNode.state_h1)
        movex = -1
        movey = -1
        movex_2 = -1
        movey_2= -1
        if self.bWord.checkGoalState(initialState, self.goalNode.state_h1):
            return maxState1, maxState2
        for i in range(0, 10):
            for j in range(0,10):
                if i != j  and initialState[i].length() >0 and initialState[j].length() <=10:
                    newState = copy.deepcopy(initialState)
                    newState = self.moveBlock(i, j, newState)
                    cost = self.heuristicC.heuristicFunction_h1(newState, self.goalNode.state_h1)
                    if cost > mincost1 and cost > mincost2:
                        mincost2 = mincost1
                        maxState2 = copy.deepcopy(maxState1)
                        mincost1 = cost
                        maxState1 = copy.deepcopy(newState)
                        movex_2 =  movex
                        movey_2 = movey
                        movex = i
                        movey = j
                    elif cost > mincost2:
                        mincost2 = cost
                        maxState2 = copy.deepcopy(newState)
                        movex_2 = i
                        movey_2 = j
        if movex != -1:
            self.turtleC.moveBlockU(movex, initialState[movex].length(), movey, initialState[movey].length(), initialState[movex].peek())
        if movey_2 != -1:
            self.turtleC.moveBlockU(movex_2, initialState[movex_2].length(), movey_2, initialState[movey_2].length(),
                                initialState[movex_2].peek())
        return maxState1, maxState2

    def nextState_h2(self, initialState):
        minState1 = None
        minState2 = None
        mincost1 = self.heuristicC.heuristicFunction_h2(initialState, self.goalNode.state_h1)
        mincost2 = self.heuristicC.heuristicFunction_h2(initialState, self.goalNode.state_h1)
        print "HC Cost h2", self.heuristicC.heuristicFunction_h2(initialState, self.goalNode.state_h1)
        print "HC Goal State h2", self.heuristicC.heuristicFunction_h2(self.goalNode.state_h1, self.goalNode.state_h1)
        movex = -1
        movey = -1
        movex_2 = -1
        movey_2= -1
        if self.bWord.checkGoalState(initialState, self.goalNode.state_h1):
            return minState1, minState2
        for i in range(0, 10):
            for j in range(0, 10):
                if i != j and initialState[i].length() >0 and initialState[j].length() <=10:
                    newState = copy.deepcopy(initialState)
                    newState = self.moveBlock(i, j, newState)
                    cost = self.heuristicC.heuristicFunction_h2(newState, self.goalNode.state_h1)
                    if cost < mincost1 and cost < mincost2:
                        mincost2 = mincost1
                        minState2 = copy.deepcopy(minState1)
                        mincost1 = cost
                        minState1 = copy.deepcopy(newState)
                        movex_2 = movex
                        movey_2 = movey
                        movex = i
                        movey = j
                    elif cost < mincost2:
                        mincost2 = cost
                        minState2 = copy.deepcopy(newState)
                        movex_2 = i
                        movey_2 = j
        if movex != -1:
               self.turtleC.moveBlockU(movex, initialState[movex].length(), movey, initialState[movey].length(), initialState[movex].peek())
        if movex_2 != -1:
            self.turtleC.moveBlockU(movex_2, initialState[movex_2].length(), movey_2, initialState[movey_2].length(),
                               initialState[movex_2].peek())

        print "Min cost", mincost1, mincost2
        return minState1, minState2

    def StateSearch(self, initialNode, goalNode):
        self.initialNode = initialNode
        self.goalNode = goalNode
        self.Node_1_h1 = copy.deepcopy(initialNode)
        self.Node_2_h1 = copy.deepcopy(initialNode)
        self.Node_1_h2 = copy.deepcopy(initialNode)
        self.Node_2_h2 = copy.deepcopy(initialNode)
        global path_hill_h1
        path_hill_h1.append(copy.deepcopy(initialNode.state_h1))
        global path_hill_h2
        path_hill_h2.append(copy.deepcopy(initialNode.state_h1))
        while(True):
            if not self.Node_1_h1 == None:
                print "Entering"
                global path_cost_hill_h1
                path_cost_hill_h1 = path_cost_hill_h1 + 1
                newState1, newState2 = self.nextState_h1(self.Node_1_h1.state_h1)
                if self.Node_2_h1 is not None and self.Node_2_h1.state_h1 is not None:
                    newState3, newState4 = self.nextState_h1(self.Node_2_h1.state_h1)
                    newState1, newState2 = self.selectBest(newState1, newState2, newState3, newState4)
                if newState1 == None:
                    self.Node_1_h1 = None
                    continue
                path_hill_h1.append(copy.deepcopy(newState1))
                self.Node_1_h1 = Node(newState1)
                if newState2 == None:
                    self.Node_h2 = None
                self.Node_2_h1 = Node(newState2)
                self.pathHeuristic1(copy.deepcopy(newState1))
            if not self.Node_1_h2 ==None:
                print "Entering Hill"
                global path_cost_hill_h2
                path_cost_hill_h2 = path_cost_hill_h2 + 1
                newState1, newState2 = self.nextState_h2(self.Node_1_h2.state_h1)
                if self.Node_2_h2 is not None and self.Node_2_h2.state_h1 is not None:
                    newState3, newState4 = self.nextState_h2(self.Node_2_h2.state_h1)
                    newState1, newState2 = self.selectBest(newState1, newState2, newState3, newState4)
                if newState1 == None:
                    self.Node_1_h2 = None
                    continue
                path_hill_h2.append(copy.deepcopy(newState1))
                self.Node_1_h2 = Node(newState1)
                self.pathHeuristic2(copy.deepcopy(newState1))
                if newState2 == None:
                    self.Node_2_h2 = None
                    continue
                self.Node_2_h2 = Node(newState2)
            if self.Node_1_h1 == None and self.Node_1_h2 == None:
                break
        self.displayPath1()
        self.displayPath2()
        return self.Node_1_h1, self.Node_1_h2

    def selectBest(self, state1, state2, state3, state4):
        if not self.bWord.checkGoalState(state1, state2):
            return state1, state2
        elif not self.bWord.checkGoalState(state1, state3):
            return state1, state3
        elif self.bWord.checkGoalState(state1, state4):
            return state1, state4
        return state1, None

    def moveBlock(self, x, y, currState):
        if currState[y].length() >= 10 and currState[x].length() <= 0:
            return currState
        currState[y].push(currState[x].pop())
        return currState

    def pathHeuristic1(self, newState):
        self.path_h1.append(newState)
        return

    def pathHeuristic2(self, newState):
        self.path_h2.append(newState)
        return

    def displayPath1(self):
        plength_1 = path_hill_h1.__len__()
        print plength_1
        for i in range(0, plength_1):
            print "Path", path_hill_h1[i], plength_1

    def displayPath2(self):
        plength_2 = path_hill_h2.__len__()
        for i in range(0, plength_2):
            print "Path", path_hill_h2[i], plength_2

    def min(self, x, y):
        return x if x<y else y

    def max(self, x, y):
        return x if x>y else y

class Node:
    def __init__(self, state1):
        self.state_h1 = state1

class DriverFunction:
    def __init__(self):
        self.initialNode = None
        self.finalNode_h1 = None
        self.finalNode_h2= None
        self.goalState = None
        self.goalNode = None

    def selectOption(self, option):
        block_word= BlockWord()
        greedyBest = GreedyBestFirstAlgo(self.initialNode, self.goalNode)
        hillClimbing = HillClimbingAlgo(self.initialNode, self.goalNode)
        turtle_graph = TurtleGraphics()
        if option == 1:
            initialState = block_word.initialStateGenerator()
#            turtle_graph.startScreen(initialState)
#            turtle_graph.moveBlockU(3, initialState[3].length() , 5, initialState[5].length(), initialState[3].pop())
            self.initialNode = Node(initialState)
            goalState  = block_word.generateGoalState(self.initialNode.state_h1)
            self.goalNode = Node(goalState)
            return
        if option == 2:
            turtle_graph.startScreen(self.initialNode.state_h1)
            self.finalNode_h1, self.finalNode_h2 = greedyBest.StateSearch(copy.deepcopy(self.initialNode), copy.deepcopy(self.goalNode))
            return
        if option == 3:
            turtle_graph.startScreen(self.initialNode.state_h1)
            self.finalNode_h1, self.finalNode_h2 = hillClimbing.StateSearch(copy.deepcopy(self.initialNode), copy.deepcopy(self.goalNode))
            return
        if option == 4:
            greedyBest.displayPath1()
            greedyBest.displayPath2()
            hillClimbing.displayPath1()
            hillClimbing.displayPath2()
            return
        if option == 5:
            turtle_graph.startScreen(self.goalNode.state_h1)
            return

def main():
    driver = DriverFunction()
    greedy_time = 0
    hill_climbing_time = 0
    for i in range(0, 10):
        driver.selectOption(1)
        time.sleep(5)
        print sys.getsizeof(driver.initialNode.state_h1)
        start_greedy = timeit.default_timer()
        driver.selectOption(2)
        stop_greedy = timeit.default_timer()
        start_hill = timeit.default_timer()
        driver.selectOption(3)
        stop_hill = timeit.default_timer()
        driver.selectOption(4)
        driver.selectOption(5)
        greedy_time = greedy_time + (stop_greedy - start_greedy)
        hill_climbing_time = hill_climbing_time + (stop_hill - start_hill)

    print "Checking path", path_greedy_h1.__len__(), path_greedy_h2.__len__(), path_hill_h1.__len__(), path_hill_h2.__len__()
    # Greedy Best First Algorithm
    print "R1", sys.getsizeof(driver.initialNode.state_h1)
    print "R2", greedy_time/10
    print "R3 - h1", path_cost_greedy_h1/10, "h2", path_cost_greedy_h2/10
    print "R4", greedy_time/10
    print "R5", min_cost_path/10

    # Hill First Climbing Algorithm
    print "R6", sys.getsizeof(driver.initialNode.state_h1)
    print "R7", hill_climbing_time/10
    print "R8 - h1", path_cost_hill_h1/10, "h2",path_cost_hill_h2/10
    print "R9", hill_climbing_time/10
    print "R10", min_cost_path/10

    if path_cost_greedy_h1 > path_cost_greedy_h2:
        path_cost_greedy = path_cost_greedy_h2
    else:
        path_cost_greedy = path_cost_greedy_h1
    if path_cost_hill_h1 > path_cost_hill_h2:
        path_cost_hill = path_cost_hill_h2
    else:
        path_cost_hill = path_cost_hill_h1
    # Comparision
    print "R11", sys.getsizeof(driver.initialNode.state_h1)

    print "R12", path_cost_greedy/10, path_cost_hill/10

if __name__ == '__main__':
    main()