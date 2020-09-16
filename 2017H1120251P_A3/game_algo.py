'''
Name : Aditi Shah

ID: 2017H1120251
'''

import turtle
import random
import numpy as np
import sys
import timeit
import time
import copy

glo_move = {1:{2: 3, 6: 12, 5: 10}, 2: {1: -1,6: 11, 7: 13 ,3: 4},
             3:{2: 1, 7: 12, 8: 14, 4: -1} , 4: {3: 2, 8: 13, 9: 15},
             5:{1: -1, 10 : -1, 11: 17, 6: 7}, 6:{5 :-1, 1: -1, 2: -1, 7:8, 12:18, 11:16 },
             7:{6: 5, 2 : -1, 3 : -1, 8:9, 13:19, 12:17},
             8:{7: 6, 3:-1, 4 :-1, 9: -1, 14: 20, 13:18}, 9:{4: -1, 8: 7, 14: 19, 15:-1},
             10:{5: 1, 11:12, 16:21 }, 11:{10: -1, 5: -1, 6:2, 12:13, 17:22, 16:-1},
             12:{11:10, 6:1,7:3, 13:14, 18:23, 17:21 } , 13:{12:11, 7:2, 8:4, 14:15, 19:24, 18:22},
             14 :{13:12, 8:3, 9:-1, 15: -1, 20 : -1, 19:23}, 15:{14:13, 9:4, 20:24},
             16: {10: -1, 11:6, 17:18, 21 :-1}, 17:{16: -1, 11:5, 12:7, 18:19 , 22:-1, 21:-1},
             18:{17:16, 12:6, 13:8, 19:20, 23:-1, 22:-1}, 19:{18:17, 13:7, 14:9, 20:-1, 24:-1, 23:-1},
             20:{19:18, 15:-1, 14:8, 24:-1}, 21:{16:10, 17:12, 22:23},
             22:{21:-1, 17:11, 18:13, 23:24}, 23:{22:21, 18:12,19:14, 24:-1},24:{23:22, 20:15, 19:13}
            }

glo_pos = {0: [-150, 200], 1:[-50, 200], 2:[50, 200], 3: [150, 200],
           4:[-200, 100],5:[-100, 100], 6:[0, 100 ], 7:[100, 100], 8:[200, 100],
           9:[-250, 0], 10:[-150, 0], 11:[-50, 0], 12:[50, 0], 13:[150, 0], 14:[250, 0],
           15:[-200, -100], 16:[-100, -100], 17:[0, -100 ], 18:[100, -100], 19:[200, -100],
           20: [-150, -200], 21: [-50, -200], 22: [50, -200], 23: [150, -200]
           }
wn = None
turn = 0
tur = 0

class TurtleGraphics():
    def __init__(self):
        pass

    def startScreen(self, initialState):
        global wn
        global tur
        wn = turtle.Screen()
        tur = turtle.Turtle()
        global glo_pos
        for i in range(0, 24):
            tur.penup()
            if initialState[i] == 1:
                tur.goto(glo_pos[i][0], glo_pos[i][1] + 25)
                tur.pendown()
                tur.dot(50, 'green')
            elif initialState[i] == 0:
                tur.goto(glo_pos[i][0], glo_pos[i][1])
                tur.pendown()
                tur.circle(25)
            elif initialState[i] == 2:
                tur.goto(glo_pos[i][0] , glo_pos[i][1]+ 25)
                tur.pendown()
                tur.dot(50, 'blue')
        return

    def moveCheckers(self, state1, state2, state3):
        return

    def getpos(self):
        global wn
        x1, y1 = wn.onclick(self.posit())
        x2, y2= wn.onclick(self.posit())
        state1 = self.getNumber(x1, y1)
        state2= self.getNumber(x2, y2)
        self.moveCheckers(state1, state2)
        return

    def getNumber(self, x, y):
        global glo_pos
        return

    def posit(self):
        global tur
        x1,x2 = tur.position()
        return x1, x2

class Checkers():
    def __init__(self):
        pass

    def initializeState(self, state):
        coin_c = 10
        coin_h = 10
        while coin_c != 0:
            key = random.randint(1,24)
            if state[key-1] == 0:
                state[key-1] = 1
                coin_c = coin_c - 1
        while coin_h != 0:
            key = random.randint(1, 24)
            if state[key-1] == 0:
                state[key-1] = 2
                coin_h = coin_h -1
        return state

    def printState(self, state):
        for i in range(0, len(state)):
            print state[i]
        return

    def Terminal_Test(self, state, turn):
        count_c = 0
        count_h = 0
        count_m = 0
        for i in state:
            if state[i] == 1:
                count_h = count_h + 1
            if state[i] == 2:
                count_c = count_c + 1
        if count_h == 0 or count_c == 0:
            return True
        for ind, pos in enumerate(state):
            if pos == turn:
                for edge in glo_move[pos]:
                    if state[edge] == 0:
                        count_m = count_m + 1
                    if state[edge] == 2 and state[glo_move[pos][edge]] == 0:
                        count_m = count_m  + 1
        if count_m == 0:
            return True
        return False

    def Utility_Value(self, state):
        count_c = 0
        count_h = 0
        for i in range(20):
            if state[i] == 1:
                count_c = count_c + 1
            if state[i] == 2:
                count_h = count_h + 1
        if count_h > count_c:
            return -count_h
        return count_c

class MiniMax():
    def __init__(self, state):
        self.state = state
        self.turtle_c = TurtleGraphics()
        self.checkers_c = Checkers()

    def MiniMaxValue(self):
        global glo_move
        player_chance = 1
        val = -sys.maxint - 1
        action = [25]*3
        while(True):
            if player_chance == 1:
                for ind,pos in enumerate(self.state):
                    if pos == 1:
                        for edge in glo_move[pos]:
                            if edge == 0:
                                value = self.MaxValue(copy.deepcopy(self.state))
                                if val < value:
                                    action[0] = ind
                                    action[1] = edge
                                    val = value
                            if  glo_move[pos][edge] == 0:
                                value = self.MaxValue(copy.deepcopy(self.state))
                                if val < value:
                                    action[0] = ind
                                    action[1] = glo_move[pos][edge]
                                    action[2] =edge
                                    val = value
                if action[2] != 25:
                    self.removeState(self.state, action[2])
                self.moveState(self.state, action[0]-1,action[1]-1)
                player_chance = 2
            else:
                self.state = self.turtle_c.getMoves(self.state)
                player_chance = 1
        return

    def moveState(self, state, x, y):
        state[x] = 0
        state[y] = 1
        return state

    def removeState(self, state, x ):
        state[x] = 0
        return state

    def MaxValue(self, state):
        val = -sys.maxint-1
        global glo_move
        if self.checkers_c.Terminal_Test(state):
            return self.checkers_c.Utility_Value(state)
        for ind, pos in enumerate(state):
            if pos == 1:
                for edge in glo_move[pos]:
                    if state[edge] == 0:
                        state = self.moveState(copy.deepcopy(state), ind, edge)
                        value = self.MinValue(copy.deepcopy(state))
                        if val > value:
                            val = value
                    if state[edge] == 2 and state[glo_move[pos][edge]] == 0:
                        state = self.removeState(copy.deepcopy(state), edge)
                        state = self.moveState(copy.deepcopy(state), ind, glo_move[pos][edge])
                        value = self.MinValue(copy.deepcopy(state))
                        if val > value:
                           val = value
        return val

    def MinValue(self, state):
        val = sys.maxint
        if self.checkers_c.Terminal_Test(state):
            return self.checkers_c.Utility_Value(state)
        for ind, pos in state:
            if pos == 2:
                for edge in glo_move[pos]:
                    if state[edge] == 0:
                        state = self.moveState(copy.deepcopy(state), ind, edge)
                        value = self.MaxValue(copy.deepcopy(state))
                        if val > value:
                            val = value
                    if state[edge] == 1 and state[glo_move[pos][edge]] == 0:
                        state = self.removeState(copy.deepcopy(state), edge)
                        state = self.moveState(copy.deepcopy(state), ind, glo_move[pos][edge])
                        value = self.MaxValue(copy.deepcopy(state))
                        if val > value:
                           val = value
        return val

    def SuccessorFnction(self, state, a):
        new_state = copy.deepcopy(state)
        for i in state:
            if state[i]== 1:
                if state[i-1] == 0:
                    return i-1
        return new_state

class AlphaBetaPruning():
    def __init__(self, state):
        self.state = state
        self.turtle_c = TurtleGraphics()
        self.checkers_c = Checkers()

    def MiniMaxValue(self):
        global glo_move
        player_chance = 1
        val = -sys.maxint - 1
        action = [25]*3
        alpha = val
        beta = val
        while(True):
            if player_chance == 1:
                for ind,pos in self.state:
                    if pos == 1:
                        for edge in glo_move[pos]:
                            if edge == 0:
                                value = self.MaxValue(copy.deepcopy(self.state))
                                if val < value:
                                    action[0] = ind
                                    action[1] = edge
                                    val = value
                            if  glo_move[pos][edge] == 0:
                                value = self.MaxValue(copy.deepcopy(self.state), alpha, beta)
                                if val < value:
                                    action[0] = ind
                                    action[1] = glo_move[pos][edge]
                                    action[2] =edge
                                    val = value
                move=self.MaxValue(copy.deepcopy(self.state))
                player_chance = 2
            else:
                self.state = self.turtle_c.getMoves()
                player_chance = 1
        return

    def moveState(self, state, x, y):
        state[x] = 0
        state[y] = 1
        return state

    def removeState(self, state, x ):
        state[x] = 0
        return state

    def MaxValue(self, state, alpha, beta):
        val = -sys.maxint-1
        global glo_move
        if self.Terminal_Test(state):
            return self.Utility_Value(state)
        for ind, pos in enumerate(state):
            if pos == 1:
                for edge in glo_move[pos]:
                    if state[edge] == 0:
                        state = self.moveState(copy.deepcopy(state), ind, edge)
                        value = self.MinValue(copy.deepcopy(state), alpha, beta)
                        if val > value:
                            val = value
                        if value > beta:
                            return
                    if state[edge] == 2 and state[glo_move[pos][edge]] == 0:
                        state = self.removeState(copy.deepcopy(state), edge)
                        state = self.moveState(copy.deepcopy(state), ind, glo_move[pos][edge])
                        value = self.MinValue(copy.deepcopy(state), alpha, beta)
                        if val > value:
                           val = value
                        if value > beta:
                            return
        return val

    def MinValue(self, state, alpha, beta):
        val = sys.maxint
        if self.Terminal_Test(state):
            return self.Utility_Value(state)
        for ind, pos in state:
            if pos == 2:
                for edge in glo_move[pos]:
                    if state[edge] == 0:
                        state = self.moveState(copy.deepcopy(state), ind, edge)
                        value = self.MaxValue(copy.deepcopy(state), alpha, beta)
                        if val > value:
                            val = value
                        if val < alpha:
                            return
                    if state[edge] == 1 and state[glo_move[pos][edge]] == 0:
                        state = self.removeState(copy.deepcopy(state), edge)
                        state = self.moveState(copy.deepcopy(state), ind, glo_move[pos][edge])
                        value = self.MaxValue(copy.deepcopy(state), alpha, beta)
                        if val > value:
                           val = value
                        if val < alpha:
                            return
        return val

class Node():
    def __init__(self):
        self.state = [0]*24
        self.action = []

class Driver():
    def __init__(self):
        self.turtle_c = TurtleGraphics()
        self.check = Checkers()
        self.state = [0]*24

    def selectOption(self, option):
        if option ==1:
            self.state = self.check.initializeState(self.state)
            self.turtle_c.startScreen(copy.deepcopy(self.state))
            self.turtle_c.moveCheckers(None, None, None)
            self.check.printState(self.state)
            return
        if option ==2:
            self.minimax_c = MiniMax(self.state)
            self.minimax_c.MiniMaxValue()
        if option ==3:
            self.alphabeta_c = AlphaBetaPruning(self.state)
            self.alphabeta_c.MaxValue()
        if option ==4:
            pass

def main():
    driverC = Driver()
    driverC.selectOption(1)
    time.sleep(2)
    driverC.selectOption(2)
    driverC.selectOption(3)
    driverC.selectOption(4)

if __name__ == '__main__':
    main()