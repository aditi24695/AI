'''
Name : Aditi Shah
ID: 2017H1120251

'''
import turtle
import copy
import timeit
import sys

count_dfs=0
count_csp = 0
count_heur =0
tur = None
wn = None

class GraphTurtle():
    def __init__(self):
        pass

    def DrawResult(self, n, result):
        global tur
        global wn
        wn = turtle.Screen()
        tur = turtle.Turtle()
        tur.penup()
        for i in range(0, n+1):
            tur.home()
            tur.goto(-200+i*100, -200)
            tur.left(90)
            tur.pendown()
            tur.forward(n*100)
            tur.penup()
        for i in range(0,n+1):
            tur.home()
            tur.goto(-200, -200 + i*100)
            tur.pendown()
            tur.forward(n*100)
            tur.penup()
        for i in range(0, n):
            for j in range(0, n):
                tur.goto(-150 +i*100, -150 + j*100)
                tur.pendown()
                tur.write(result[i][j], font=("Arial",12, "normal"))
                tur.penup()
        tur.clear()
        return

class Constraints():
    def __init__(self):
        pass

    def AllDiff(self, data):
        n = data.__len__()
        diff_val = [(i+1) for i in range(0, n*n)]
        for i in range(n):
            for j in range(n):
                if data[i][j] ==0:
                    continue
                if data[i][j] in diff_val :
                    diff_val.remove(data[i][j])
                else:
                    return False
        return True


    def sumConstraint(self, data, sum):
        diag_z = 1
        diagl_z = 1
        sum_d2 =0
        sum_d1 = 0
        for i in range(data.__len__()):
            sum_r=0
            sum_c=0
            row_z=1
            col_z = 1
            for j in range(data.__len__()):
                sum_r = sum_r +  data[i][j]
                sum_c = sum_c + data[j][i]
                if data[i][j] == 0: row_z = 0
                if data[j][i] == 0: col_z = 0
            if ((sum != sum_r and row_z!=0) or (sum != sum_c and col_z!= 0 )):
                return False
            if data[i][data.__len__()-i-1] == 0: diag_z = 0
            if data[i][i] == 0: diagl_z = 0
            sum_d1 = sum_d1 + data[i][data.__len__()-i-1]
            sum_d2 = sum_d2 + data[i][i]
        if (sum_d1 != sum and diag_z == 1)or (sum_d2 != sum  and diagl_z == 1):
            return False
        return True

class Heuristics():
    def __init__(self):
        pass

    def degree_based(self,n, var_list, G):
        max_degree = 0
        var = 0
        for i in range(0,n*n):
            if (var_list.__len__() ==0 or  (i+1) not in var_list ) and G.dict_data[i+1]['edges'].__len__() > max_degree:
                max_degree = G.dict_data[i+1]['edges'].__len__()
                var =i+1
        return var

    def MRV(self, n, var_list, G ):
        min_v = 100
        var = 0
        for i in range(0, n*n):
            if (var_list.__len__() ==0 or  (i+1) not in var_list ) and G.dict_data[i+1]['domain'].__len__() < min_v:
                var = i+1
                min_v = G.dict_data[i+1]['domain'].__len__()
        return var

    def boundary_square(self,n, var_list, G):
        var = 0
        for j in reversed(range(0, (n/2) + 1)):
            for i in range(0, n):
                if var_list.__len__ == 0 or (j + i*n + 1) not in var_list:
                    var = j + i*n + 1
                    break
            if var != 0:
                break
        if var == 0:
            for j in range(n/2, n):
                for i in range(0, n):
                    if var_list.__len__ == 0 or (j + i * n + 1) not in var_list:
                        var = j + i*n + 1
                        break
                if var != 0:
                    break
        return var

class DFS():
    def __init__(self, n):
        self.stack =[]
        self.heuristic = Heuristics()
        self.constraint = Constraints()
        self.var_select = []
        self.result = [ [0 for i in range(n)] for j in range(n)]
        self.visitedData = {}
        self.isLastPop = False

    def DFS_Iter(self,  n, G, node):
        while(True):
            if self.constraint.AllDiff(self.result) and self.constraint.sumConstraint(self.result, (n*n*(n*n + 1)/2) / (n)) and self.var_select.__len__() == n * n:
                print self.result
                break
            var = self.heuristic.degree_based(n, self.var_select, G)
            if self.isLastPop:
                action_list = copy.deepcopy(node.action)
            else:
                action_list = []
            if var != 0 and self.var_select.__len__() != n * n and self.selectValue(G, var, n, action_list) != 0 and self.constraint.AllDiff( self.result) and self.constraint.sumConstraint(self.result, n * (n * n + 1) / 2):
                global count_dfs
                count_dfs = count_dfs + 1
                self.var_select.append(var)
                value = self.selectValue(G, var, n, action_list)
                node_d = Node(value, var, action_list)
                self.result[(var - 1) / n][(var - 1) % n] = value
                node_d.addAction(value)
                self.stack.append(node_d)
                self.isLastPop = False
            else:
                node = self.stack.pop()
                self.var_select.remove(node.var)
                self.result[(node.var - 1) / n][(node.var - 1) % n] = 0
                self.isLastPop = True
        return self.result

    def selectValue(self, G, var, n, action):
        if var == 0:
            return 0
        val = 0
        if G.dict_data[var]['domain'].__len__() >= 0:
            for i in G.dict_data[var]['domain']:
                if action.__len__() == 0 or i not in action:
                    val= i
                    break
                else:
                    continue
        else:
            val =0
        return val

class DFS_heur():
    def __init__(self, n):
        self.stack =[]
        self.heuristic = Heuristics()
        self.constraint = Constraints()
        self.var_select = []
        self.result = [ [0 for i in range(n)] for j in range(n)]
        self.visitedData = {}
        self.isLastPop = False

    def DFS_Iter_heur(self,  n, G, node):
        while(True):
            if self.constraint.AllDiff(self.result) and self.constraint.sumConstraint(self.result, (n*n*(n*n + 1)/2) / (n)) and self.var_select.__len__() == n * n:
                print self.result
                break
            var = self.heuristic.boundary_square(n, self.var_select, G)
            if self.isLastPop:
                action_list = copy.deepcopy(node.action)
            else:
                action_list = []
            if var != 0 and self.var_select.__len__() != n * n and self.selectValue(G, var, n, action_list) != 0 and self.constraint.AllDiff( self.result) and self.constraint.sumConstraint(self.result, n * (n * n + 1) / 2):
                global count_heur
                count_heur = count_heur + 1
                self.var_select.append(var)
                value = self.selectValue(G, var, n, action_list)
                node_d = Node(value, var, action_list)
                self.result[(var - 1) / n][(var - 1) % n] = value
                node_d.addAction(value)
                self.stack.append(node_d)
                self.isLastPop = False
            else:
                node = self.stack.pop()
                self.var_select.remove(node.var)
                self.result[(node.var - 1) / n][(node.var - 1) % n] = 0
                self.isLastPop = True
        return self.result

    def selectValue(self, G, var, n, action):
        if var == 0:
            return 0
        val = 0
        if G.dict_data[var]['domain'].__len__() >= 0:
            for i in G.dict_data[var]['domain']:
                if action.__len__() == 0 or i not in action:
                    val= i
                    break
                else:
                    continue
        else:
            val =0
        return val

class CSP_DFS():
    def __init__(self, n):
        self.stack =[]
        self.heuristic = Heuristics()
        self.constraint = Constraints()
        self.var_select = []
        self.result = [ [0 for i in range(n)] for j in range(n)]
        self.visitedData = {}
        self.isLastPop = False
    def DFS_Iter(self,  n, G, node):
        while(True):
            if self.constraint.AllDiff(self.result) and self.constraint.sumConstraint(self.result, (n*n*(n*n + 1)/2) / (n)) and self.var_select.__len__() == n * n:
                print self.result
                break
            var = self.heuristic.degree_based(n, self.var_select, G)
            if self.isLastPop:
                action_list = copy.deepcopy(node.action)
            else:
                action_list = []
            if var != 0 and self.var_select.__len__() != n * n and self.selectValue(G, var, n, action_list) != 0 and self.constraint.AllDiff( self.result) and self.constraint.sumConstraint(self.result, n * (n * n + 1) / 2):
                global count_csp
                count_csp = count_csp + 1
                self.var_select.append(var)
                value = self.selectValue(G, var, n, action_list)
                self.constraintPropogation(G, value, n)
                node_d = Node(value, var, action_list)
                self.result[(var - 1) / n][(var - 1) % n] = value
                node_d.addAction(value)
                self.stack.append(node_d)
                self.constraintPropogation(G, value, n)
                self.isLastPop = False
            else:
                node = self.stack.pop()
                self.var_select.remove(node.var)
                self.addDomain(G, node.value, n)
                self.result[(node.var - 1) / n][(node.var - 1) % n] = 0
                self.isLastPop = True
        return self.result

    def selectValue(self, G, var, n, action):
        if var == 0:
            return 0
        val = 0
        if G.dict_data[var]['domain'].__len__() >= 0:
            for i in G.dict_data[var]['domain']:
                if action.__len__() == 0 or i not in action:
                    val= i
                    break
                else:
                    continue
        else:
            val =0
        return val

    def addDomain(self, G, val, n):
        for i in range(1, n*n+1):
            G.dict_data[i]['domain'].add(val)
        return G

    def constraintPropogation(self, G, val, n):
        for i in range(1, n*n+1):
            if val in G.dict_data[i]['domain']:
                G.dict_data[i]['domain'].remove(val)
        return G

class Graph():
    def __init__(self, n):
        self.dict_data = {}
        for i in range(0,n):
            for j in range(0,n):
                self.dict_data[i*n + j + 1] = {'value' : 0, 'domain' :set([(k+1) for k in range(n*n)]), 'edges': []}
        for i in range(0, 2*n + 2):
            self.dict_data[n*n + i+1] = {'edges':[], 'value': 0}
        return

    def addedges(self, n):
        for i in range(0, n*n):
            for j in range(0, n*n):
                if i != j:
                    self.dict_data[i+1]['edges'].append(j+1)
        for i in range(0, n):
            for j in range(0,n):
                self.dict_data[n*n + i+1]['edges'].append(i*n + j+1)
        for i in range(0, n):
            for j in range(0, n):
                self.dict_data[n*(n+1) + i+1]['edges'].append(j*n + i+1)
        for i in range(n):
            self.dict_data[n*(n+2)+1]['edges'].append(i+n*i+1)
        for i in range(n):
            self.dict_data[n*(n+2)+2]['edges'].append(n*(i+1) -i)
        return

class Node():
    def __init__(self, value, var, action):
        self.value = value
        self.var = var
        self.action = action

    def addAction(self, val):
        self.action.append(val)

class Driver():
    def __init__(self):
        self.n =3
        self.tur_c = GraphTurtle()
        self.G = Graph(self.n)
        self.G.addedges(self.n)
        self.csp = DFS(self.n)
        self.node = Node(0, 0, [])
        self.csp_D = CSP_DFS(self.n)
        self.csp_heur = DFS_heur(self.n)

    def selectOption(self, dr):
        if dr == 1:
            result = self.csp.DFS_Iter(self.n, copy.deepcopy(self.G), copy.deepcopy(self.node))
            self.tur_c.DrawResult(self.n, result)
        if dr == 2:
            result = self.csp_heur.DFS_Iter_heur(self.n, copy.deepcopy(self.G), copy.deepcopy(self.node))
            self.tur_c.DrawResult(self.n, result)
        if dr == 3:
            result = self.csp_D.DFS_Iter(self.n, copy.deepcopy(self.G), copy.deepcopy(self.node))
            self.tur_c.DrawResult(self.n, result)

        return

def main():
    n = 3
    node = Node(0, 0, [])
    driver = Driver()
    startDFS = timeit.default_timer()
    driver.selectOption(1)
    endDFS = timeit.default_timer()

    driver.selectOption(2)

    startCsp = timeit.default_timer()
    driver.selectOption(3)
    endCsp = timeit.default_timer()


    global count_dfs
    global count_csp
    global count_heur
    print "R1", count_dfs
    print "R2", sys.getsizeof(node)
    print "R3", n*n
    print "R4",endDFS - startDFS
    print "R5",count_heur
    print "R6", count_csp
    print "R7",(count_dfs - count_csp)/count_dfs
    print "R8", endCsp - startCsp

if __name__ == '__main__':
    main()
