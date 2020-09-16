'''
Name : Aditi Shah

ID : 2017H1120251P
'''
import turtle
import re

result_p1 = []

class Graphurtle():
    def __init__(self):
        pass

    def DrawGraphics(self):
        global result_p1
        n = 8
        self.result = [ [" " for i in range(n)] for j in range(n)]
        self.result[0][0] = "s"
        self.result[0][4] = "w"
        self.result[1][6] = 'p'
        self.result[2][7] = 'p'
        self.result[3][1] = 'p'
        self.result[4][3] = 'w'
        self.result[4][7] = 'w'
        self.result[5][1] = 'p'
        self.result[5][3] = 'w'
        self.result[7][2] = 'p'
        self.result[7][4] = 'p'
        self.result[5][5] = 'g'
        wn = turtle.Screen()
        tur = turtle.Turtle()
        tur.penup()
        tur.goto(-200, 200)
        tur.pendown()
        tur.write("Problem 1", font=("Arial", 12, "normal"))
        tur.penup()
        tur.home()
        tur.goto(-200+50, 200)
        for i in range(0, result_p1.__len__()):
            tur.home()
            tur.goto(-200+100, 200 - 30*i)
            tur.pendown()
            tur.write("Query " + str(i + 1) + " : " + str(result_p1[i]), font=("Arial", 12, "normal"))
            tur.penup()
        wn.delay(5)
        tur.penup()
        wn.clear()
        for i in range(0, n+1):
            tur.home()
            tur.goto(-200+i*50, -200)
            tur.left(90)
            tur.pendown()
            tur.forward(n*50)
            tur.penup()
        for i in range(0,n+1):
            tur.home()
            tur.goto(-200, -200 + i*50)
            tur.pendown()
            tur.forward(n*50)
            tur.penup()
        for i in range(0, n):
            for j in range(0, n):
                tur.goto(-175 +i*50, -175 + j*50)
                tur.pendown()
                tur.write(self.result[i][j], font=("Arial",12, "normal"))
                tur.penup()
        tur.clear()

        return

class FOL():
    def __init__(self):
        self.KB = set([])
        self.predicate = set([])
        self.variable = set([])
        self.factdict = []
        self.ruleDict = []
        self.operator = ("<=>", "=>", "&&", "||", "~", "<=")
        self.unifier = {}
        self.theta = {}

    def readPredicate(self, num):
        # f1 = open("predicateFile"+str(num)+".txt", r)
        # predicate_desc = f1.readline()
        f = open("ruleFile"+str(num)+".txt", "r")
        predicates = f.readline()
        for i in range(0, int(predicates)):
            predicate = f.readline()
            self.parsePredicate(predicate)
        rules = f.readline()
        for i in range(0, int(rules)):
            rule = f.readline()
            self.parseRule(rule)
        self.populate_FOL_KB()
        query = f.readline()
        for i in range(0, int(query)):
            query = f.readline()
            if query == "Path":
                continue
            self.parseQuery(query)
        f.close()
        return

    def parsePredicate(self, pred):
        pred_p = pred[:-1].split(" ")
        isfact = True
        self.predicate.add(pred_p[0])
        fact_n = pred[:-1]
        fact= []
        for i in range(pred_p.__len__()):
            if self.isVariable(pred_p[i]):
                isfact = False
            fact.append(pred_p[i])
        if isfact == True:
            self.factdict.append(fact)
        else:
            return fact
        return

    def isVariable(self, var):
        if var.__len__() == 1:
            return True
        return False

    def parseRule(self, rule):
        rule_s = rule[:-1].split(" ")
        # ant_con = rule_s.split("=>")
        self.ruleDict.append({"Variable":{}, "Rule" : [],"Predicate":[]})
        index = 0
        while True:
            if rule_s[index] == "For_every" or rule_s[index] == "There_exists":
                self.ruleDict[self.ruleDict.__len__()-1]["Variable"][rule_s[index+1]] = rule_s[index]
                index = index + 2
            else:
                break
        self.ruleDict[self.ruleDict.__len__() - 1]["Rule"] = rule_s[index:]

        regexPattern = '|'.join(map(re.escape, self.operator))
        # if "=>" in rule_s:
        #     antecon =  " ".join(rule_s[index:]).split("=>")
        #     antecedent = antecon[0]
        #     consequent = antecon[1]
        #     print "Antecedent Consequent",  antecedent, consequent
        #     antecedent_list = re.split(regexPattern, " ".join(antecedent))
        #     print "A List", antecedent_list, antecedent
        #     antecedent_list = [x.strip(' ') for x in antecedent_list]
        #     consequent_list = re.split(regexPattern, " ".join(consequent))
        #     print "C List", consequent_list
        #     consequent_list = [x.strip(' ') for x in consequent_list]
        #     print "Final list 1", antecedent_list, consequent_list, rule_s[index:]
        # else:
        predicate_list = re.split(regexPattern, " ".join(rule_s[index:]))
        predicate_list = [x.strip(' ') for x in predicate_list]
        if '' in predicate_list:
            predicate_list.remove('')
        self.ruleDict[self.ruleDict.__len__() - 1]["Predicate"] = predicate_list

#        self.populate_FOL_KB(predicate_list, rule_s[index:])
        return

    def parseQuery(self, query):
        global result_p1
        flag = 1
        query_s = query[:-1].split(" ")
        resolve = None
        if query_s[0] in self.predicate:
            for i in range(0, self.factdict.__len__()):
                if flag == 0:
                    break
                if self.factdict[i][0] == query_s[0]:
                    for j in range(0, query_s.__len__()):
                        if self.isVariable(query_s[j]):
                            resolve = True
                    if resolve:
                        result = self.Unify(self.factdict[i], query_s, {})
                        if result is not None:
                            result_p1.append(result['X'])
                            flag = 0
                    else:
                        result = self.Verify(self.factdict[i], query_s)
                        result_p1.append(result)
                        flag =0
        else:
            result_p1.append([])
        return

    def Verify(self, fact, query):
        for i in range(0, query.__len__()):
            if fact[i] != query[i]:
                return False
        return True

    def populate_FOL_KB(self):
        new_theta = {}
        new_pred = set([])
        for i in range(0, self.ruleDict.__len__()):
            for pred in self.ruleDict[i]['Predicate']:
                fact_pred = self.parsePredicate(pred+"\n")
                for j in range(0, self.factdict.__len__()):
                    try:
                        if fact_pred[0] == self.factdict[j][0]:
                            theta = self.Unify(fact_pred, self.factdict[j],{})
                            new_theta.update(theta)
                    except:
                        continue
            for theta_val in new_theta.keys():
                if 'X' in new_theta[theta_val]:
                    del(new_theta[theta_val])
            subs_rule =  " ".join(self.ruleDict[i]['Predicate'])
            predicate_rule = subs_rule.split(" ")
            for key, ele in enumerate(predicate_rule):
                if ele in new_theta:
                    predicate_rule[key] = new_theta[ele]
            for new_pred_t in self.ruleDict[i]['Predicate']:
                new_pred.add(new_pred_t.split(" ")[0])
            new_fact_add = []
            for data in predicate_rule:
                if data in new_pred:
                    self.parsePredicate(" ".join(new_fact_add)+"\n")
                    new_fact_add = []
                new_fact_add.append(data)
                print new_fact_add
        return

    def AssignValue(self):
        return

    def Unify_Var(self, x, y, theta):
        if self.isVariable(y) and self.isVariable(x):
            return theta
        if not self.isVariable(x):
            theta[y] = x
        if not self.isVariable(y):
           theta[x] = y
        if not self.isVariable(y) and not self.isVariable(x) and x != y:
            return False
        return theta

    def Unify(self, x, y, theta):
        try:
            if x== y:
                return theta
            if self.isVariable(x):
                theta = self.Unify_Var(x, y, theta)
            if self.isVariable(y):
                theta = self.Unify_Var(y, x, theta)
            if type(x) == list:
                if x[0] == y[0]:
                    self.Unify(x[1:] ,y[1:], theta)
                else:
                    theta  = self.Unify_Var(x[0], y[0], theta)
                    self.Unify(x[1:], y[1:], theta)
        except:
            pass
        return theta

class Driver():
    def __init__(self):
        pass

    def selectQuery(self, num):
        fol_c = FOL()
        fol_c.readPredicate(num)

class main():
    driver_c = Driver()
    driver_c.selectQuery(1)
    driver_c.selectQuery(2)
    graph_c = Graphurtle()
    graph_c.DrawGraphics()

if __name__ == '__main__':
    main()