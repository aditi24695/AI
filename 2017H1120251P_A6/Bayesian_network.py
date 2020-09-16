'''
Name : Aditi Shah
ID: 2017H1120251
'''
from Tkinter import *
import copy

class GraphTurtle(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.var_list = ["A", "B", "C", "D", "F", "G", "H", "L", "N", "O", "P", "R", "T", "X", "Y"]
        Scrollbar(self, orient=VERTICAL)
        self.pack()
        self.DrawResult()
        self.query =[]
        self.conditional = []
        self.bn_c = BayesianNetwork()
        self.bn_c.createBayesianNetwork()
        self.bn_c.MarkovBlanket('B')
        self.bn_c.calcPriorProbability()

    def DrawResult(self):
        var = Button(self, text="  Query Variables   ")
        var.grid( row = 0 , column = 0, padx = 10)
        var = Button(self, text="Condition Variables")
        var.grid( row = 0 , column = 2, padx = 10)

        for i in range(self.var_list.__len__()):
            for j in range(0, 4):
                if j%2 == 0:
                    var = Button(self, text = self.var_list[i], height =1, width = 20 ,padx = 10, command = lambda va_i = i, va_j = j:self.AddToQuery(va_i, va_j))
                else:
                    var = Button(self, text = "~" + self.var_list[i], height =1, width = 20, padx = 10, command = lambda va_i = i,va_j = j:self.AddToQuery(va_i, va_j))
                if j >1:
                    var.grid( row = i+1 , column = j , pady = 2, padx = 5)
                else:
                    var.grid(row =i+1, column = j, pady =2,padx = 5)

        var = Button(self, text="  Query Variables   ")
        var.grid(row=16, column=0)
        var = Button(self, text="  Clear  ",command = lambda :self.clearQuery())
        var.grid(row=16, column=3)

        var = Button(self, text="Answer", command = lambda : self.calculateProb())
        var.grid(row=17, column=0)

        return


    def calculateProb(self):
        ante, cond = self.bn_c.createExpression(self.query, self.conditional)
        value = self.bn_c.computeProbability(ante, cond)
        var = Button(self, text= value)
        var.grid(row=17, column=1)
        return value

    def clearQuery(self):
        self .query = []
        self.conditional = []
        var = Button(self, text= "" , width = 20)
        var.grid(row=16, column=1)
        var.grid_slaves(16, 1)
        var = Button(self, text= "" , width = 20)
        var.grid(row=17, column=1)
        var.grid_slaves(17, 1)

        return

    def AddToQuery(self, i, j):
        query_s = ""
        condition_s = ""
        query_f = ""
        if j == 0:
            self.query.append(self.var_list[i])
        elif j == 1:
            self.query.append("~" + self.var_list[i])
        elif j == 2:
            self.conditional.append(self.var_list[i])
        else:
            self.conditional.append("~" + self.var_list[i])
        if self.query.__len__() > 0:
            query_s = " ".join(self.query)
        if self.conditional.__len__()>0:
            condition_s = " ".join(self.conditional)
        if query_s != " " or condition_s != " ":
            query_f = query_s + " | " + condition_s
        var = Button(self, text= query_f , width = 20)
        var.grid(row=16, column=1)
        return


class BayesianNetwork():
    def __init__(self):
        self.graph = {}
        self.table = {}
        self.varlist = ["O", "R", "P", "G", "X", "N", "H", "B", "A", "T", "L", "Y",  "F", "C", "D"]
        self.arrange = ["D", "~D", "Y", "~Y", "C", "~C", "F", "~F", "A", "~A", "G", "~G", "X", "~X", "N", "~N",
                        "L", "~L", "T", "~T", "B", "~B", "H", "~H", "P", "~P", "O", "~O", "R", "~R"]

    def createBayesianNetwork(self):
        for i in range(1, 2):
            f = open("input"+str(i)+".txt", "r")
            while True:
                data = f.readline()
                if data == "":
                    break
                data_s = data[:-1].strip(" ").split(" ")
                count = 0
                for i in range(0, len(data_s)):
                    if count == 0 and data_s[0].__len__() == 1:
                        self.graph[data_s[0]] = []
                    if data_s[i] == ">>":
                        count = count + 1
                        if i > data_s[i].__len__() - 2:
                            self.table[data_s[0]] = []
                    if count == 1:
                        data_s[i]   = data_s[i].strip('[],')
                        if data_s[i].__len__() == 1 :
                            self.graph[data_s[0]].append(data_s[i])
                    if count == 2 and data_s[i] != ">>":
                        self.table[data_s[0]].append(data_s[i])
        return

    def calcPriorProbability(self):
        len_var = self.varlist.__len__()
        self.prior_var = {}
        for i in range(0, len_var):
            if self.table[self.varlist[i]].__len__() == 1:
                self.prior_var[self.varlist[i]] = self.table[self.varlist[i]][0]
            else:
                exp_list = [self.varlist[i]]
                parents = self.graph[self.varlist[i]]
                for parent in parents:
                    exp_list.extend(exp_list)
                    for ele in range(0, exp_list.__len__()/2):
                        exp_list[ele] = exp_list[ele] + " " + parent
                    for ele in range(exp_list.__len__()/2, exp_list.__len__()):
                        exp_list[ele] = exp_list[ele] + " ~" + parent
                self.calculateProb(exp_list)

        return

    def calculateProb(self, exp_list):
        total_prob = 0
        for exp in exp_list:
            query = ""
            ele = exp.split(" ")
            for i in range(0, len(ele)):
                if i == 0:
                    query = ele[0] + " |"
                else:
                    query = query + " " + ele[i]
            prob_val = self.calcExpression(query)
            for i in range(0, len(ele)):
                if i != 0:
                    if ele[i].__len__() == 1:
                        prob_val = prob_val * float(self.prior_var.get(ele[i]))
                    else:
                        pr = float(self.prior_var.get(ele[i][-1]))
                        prob_val = prob_val*( 1- pr)
            total_prob = total_prob + prob_val
            self.prior_var[exp_list[0].split(" ")[0]] = total_prob
        return

    def MarkovBlanket(self, node):
        blanket = set([node])
        for key in (self.graph):
            if node in self.graph[key]:
                blanket.add(key)
        blanket_p = copy.deepcopy(blanket)
        for ele in blanket:
            for val in self.graph[ele]:
                blanket_p.add(val)
        print "Markow Blanket of "+ node + ": ", blanket_p
        return blanket_p

    def arrangeArray(self, list):
        qc_list = []
        for ele in self.arrange:
            if ele in list:
                qc_list.append(ele)
        return qc_list

    def createExpression(self, query, conditional):
        quer =set(query)
        condition = set(conditional)
        quer = quer.union(condition)
        query = list(quer)
        conditional = list(condition)
        query = self.arrangeArray(query)
        conditional = self.arrangeArray(conditional)
        cond_exp = []
        if self.checkExpression(quer, condition):
            return [], []
        query_list = []
        conditional_list = []
        for i in query:
            quer_exp = []
            quer_exp.append(i)
            parents = self.graph.get(i[-1])
            for parent in parents:
                if parent in query:
                    for exp in range(0, len(quer_exp)):
                        quer_exp[exp] = quer_exp[exp] + " " + parent
                else:
                    quer_exp.extend(quer_exp)
                    for ele in range(0, quer_exp.__len__()/2):
                        quer_exp[ele] = quer_exp[ele] + " " + parent
                    for ele in range(quer_exp.__len__()/2, quer_exp.__len__()):
                        quer_exp[ele] = quer_exp[ele] + " ~" + parent
            query_list.append(quer_exp)

        for i in conditional:
            cond_exp = []
            cond_exp.append(i)
            parents = self.graph.get(i[-1])
            for parent in parents:
                if parent in conditional:
                    for exp in range(0, len(cond_exp)):
                        cond_exp[exp] = cond_exp[exp] + " " + parent
                else:
                    cond_exp.extend(cond_exp)
                    for ele in range(0, cond_exp.__len__()/2):
                        cond_exp[ele] = cond_exp[ele] + " " + parent
                    for ele in range(cond_exp.__len__()/2, cond_exp.__len__()):
                        cond_exp[ele] = cond_exp[ele] + " ~" + parent
            conditional_list.append(cond_exp)

        return query_list, conditional_list

    def computeProbability(self, quer_exp, cond_exp):
        query_val = 1
        cond_val = 1
        if quer_exp.__len__() == 0:
            return 0
        if cond_exp.__len__() == 0:
            cond_val = 1
        for query in quer_exp:
            part_prob = 0
            for exp in query:
                quer_create = ""
                quer_ele = exp.split(" ")
                min_prob = 1
                for ele in range(0, len(quer_ele)):
                    if ele == 0:
                        quer_create = quer_ele[ele] + " |"
                    else:
                        quer_create = quer_create + " " + quer_ele[ele]
                min_prob = self.calcExpression(quer_create)
                for ele in range(0, len(quer_ele)):
                    if ele != 0:
                        if quer_ele[ele].__len__()==1:
                            min_prob = min_prob * float(self.prior_var.get(quer_ele[ele]))
                        else:
                            min_prob = min_prob * float(1 - float(self.prior_var.get(quer_ele[ele][-1])))
                part_prob = part_prob + min_prob
            print "Partial Probability", part_prob
            query_val = query_val*part_prob

        for condition in cond_exp:
            part_prob = 0
            for exp in condition:
                cond_create = ""
                cond_ele = exp.split(" ")
                min_prob = 1
                for ele in range(0, len(cond_ele)):
                    if ele == 0:
                        cond_create = cond_ele[ele] + " |"
                    else:
                        cond_create = cond_create + " " + cond_ele[ele]
                min_prob = self.calcExpression(cond_create)
                for ele in range(0, len(cond_ele)):
                    if ele != 0:
                        if cond_ele[ele].__len__()==1:
                            min_prob = min_prob * float(self.prior_var.get(cond_ele[ele]))
                        else:
                            min_prob = min_prob * float(1 - float(self.prior_var.get(cond_ele[ele][-1])))
                part_prob = part_prob + min_prob
            cond_val = cond_val*part_prob
        print "Querry Val", query_val, "Conditional Val", cond_val
        val = query_val/float(cond_val)
        print "Probability", val
        return val

    def checkExpression(self, query, cond):
        query = query.union(cond)
        query_list= list(query)
        query_list = self.arrangeArray(query_list)
        for i in range(0, query_list.__len__()):
            query_list[i] = query_list[i][-1]
        if (set(query_list)).__len__()  == query_list.__len__():
            return False
        return True

    def calcExpression(self, query):
        index= 0
        query_ele = query.split(" ")
        data_val = self.table.get(query_ele[0][-1])
        val_len = query_ele.__len__()
        for j in range(2, query_ele.__len__()):
            if query_ele[j].__len__() == 1:
                index = index + (2 ** (val_len - j - 1))
        val = float(data_val[index])
        return val


def main():
    root = Tk()
    app = GraphTurtle(master = root)
    app.mainloop()
    root.detroy()
    gt = GraphTurtle()
    gt.DrawResult()

if __name__ == '__main__':
    main()