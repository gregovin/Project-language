import re
current = []
def identity(x):
    return x
class NamePair:
    func = identity
    params = 1
    paranames = ['x']
    def __init__(self, func, params, paranames):
        self.func = func
        self.params = params
        self.paranames = paranames
    def evaluate(self, parames):
        awesomeness = [i for i,val in enumerate(parames) if re.search("\([^()]*\)",val)]
        while len(awesomeness) > 0:
            #intese regexing
            usefulstring = parames[awesomeness[0]]
            #this function should replace the depest instance of unsimplified things with simplified things
            new = parames[:awesomeness[0]]
            new.append(re.sub("\(([^()]*)\)",str(functions[re.search("(?:\()([^()]*)(?:\))",usefulstring).group(0).split(" ")[0][1:]].\
                                    evaluate(endParenRemove(re.search("\(([^()]*)\)",usefulstring).group(0).split(" ")[1:]))),\
                                    usefulstring, 1))
            parames = new + parames[awesomeness[0]+1:]
            #this gets all the indecies of the parameters that are not simplified
            awesomeness = [i for i,val in enumerate(parames) if re.search("\([^()]*\)",val)]
        if self.params == 0 and type(self.func) != str:
            return self.func()
        elif self.params == 1 and type(self.func) != str:
            return self.func(parames[0])
        elif self.params == 2 and type(self.func) != str:
            return self.func(parames[0],parames[1])
        elif self.params == 3 and type(self.func) != str:
            return self.func(parames[0],parames[1],parames[2])
        elif self.params == 4 and type(self.func) != str:
            return self.func(parames[0],parames[1],parames[2],parames[3])
        elif self.params == 0:
            return functions['ident'].evaluate([self.func])
        elif self.params == 1:
            return scEvalulator(re.sub('\\b'+self.paranames[0]+'\\b',parames[0],self.func))
        elif self.params == 2:
            return scEvalulator(re.sub('\\b'+self.paranames[0]+'\\b',parames[0],re.sub('\\b'+self.paranames[1]+'\\b',parames[1],self.func)))
        elif self.params == 3:
            return scEvalulator(re.sub('\\b'+self.paranames[0]+'\\b',parames[0],re.sub('\\b'+self.paranames[1]+'\\b',parames[1],re.sub('\\b'+self.paranames[2]+'\\b',parames[2],self.func))))
        elif self.params == 4:
            return scEvalulator(re.sub('\\b'+self.paranames[0]+'\\b',parames[0],re.sub('\\b'+self.paranames[1]+'\\b',parames[1],re.sub('\\b'+self.paranames[2]+'\\b',parames[2],re.sub('\\b'+self.paranames[3]+'\\b', parames[3], self.func)))))
def endParenRemove(ls):
    temp = ls[:-1]
    temp += ls[-1][:-1]
    return temp
def parenthasize(thing):
    res = ""
    for i in thing[:-1]:
        res = res + i + " "
    res += thing[-1]
    return res
def deparenthisize(thing):
    temp = thing.split(" ")
    coolstuff = [i for i,val in enumerate(temp[2:]) if re.match('[^)]*\)', val)][0]+1
    return [temp[0], temp[1], temp[2:coolstuff+2], parenthasize(temp[coolstuff+2:])]
#"(define func (args) body)"
def addDef(thing):
        current.append(thing)
        tempList = deparenthisize(thing)
        argnum = len(tempList[2])
        if argnum >2:
            functions[tempList[1]] = NamePair(tempList[3][:-1],argnum,[tempList[2][0][1:], tempList[2][1:-1], tempList[2][-1][:-1]])
        elif argnum == 2:
            functions[tempList[1]] = NamePair(tempList[3][:-1],argnum,[tempList[2][0][1:], tempList[2][-1][:-1]])
        elif argnum == 1:
            functions[tempList[1]] = NamePair(tempList[3][:-1],argnum,[tempList[2][0][1:-1]])
        else:
            functions[tempList[1]] = NamePair(tempList[3][:-1],argnum,[])
        print(thing)
def scEvalulator(thing):
    fname = thing.split(" ")[0][1:]
    func = functions[fname].func
    parts = thing[thing.index(" ")+1:]
    paren = 0
    pars = False
    i = 0
    tN =""
    special = False
    while i<len(thing) and (thing[i] != ' ' or paren != 0):
        if thing[i] == '(':
            paren += 1
            pars = True
        elif thing[i] == ')':
            paren -= 1
        i += 1
    if func == ifN:
        j = 0
        paren = 0
        pars = False
        while j < len(thing[4:]) and (thing[j+4] != ' ' or paren >0):
            if thing[j+4] == '(':
                paren += 1
                pars =True
            if thing[j+4] == ')':
                paren -= 1
            j += 1
        if pars:
            awesomething = scEvalulator(thing[4:j+5])
            thing = thing[:4]+awesomething+' '+thing[j+5:]
            j = 4
            special = True
        if thing.split(" ")[1] != 'False':
            tN = thing[j+5:]
            k = 0
            pars =False
            while k < len(tN) and (tN[k] != ' ' or paren != 0):
                if tN[k] == ')':
                    paren -= 1
                elif tN[k] == '(':
                    paren += 1
                    pars = True
                k += 1
            if pars:
                return scEvalulator(tN[:k+1])
            else:
                return tN[:k+1]
        else:
            if special:
                j += 1
            tn = thing[j+3:]
            k = 2
            paren = 0
            pars = False
            while (tn[-k] != ' ' or paren != 0) and k < len(tn):
                if tn[-k] == '(':
                   paren -= 1
                   pars = True
                elif tn[-k] == ')':
                    paren += 1
                k += 1
            if pars:
                return scEvalulator(thing[len(thing)-k+1:len(thing)-3])
            else:
                return tn[len(tn)-k+1:len(tn)-1]
    elif func == orN:
        j = 4
        paren = 0
        pars = False
        while j < len(thing)-1 and (paren != 0 or thing[j] != ' '):
            if thing[j] == '(':
                paren += 1
                pars = True
            elif thing[j] == ')':
                paren -= 1
            j +=1
        if pars:
            thing = thing[:3] + scEvalulador(thing[3:j]) + things[j:]
        if thing.split(" ")[1] != "False":
            return "True"
        else:
            k = 2
            tN = thing[j:]
            paren = 0
            pars = False
            while (tN[-k] != ' ' or paren != 0) and k < len(tN):
                if tN[-k] ==')':
                    paren -= 1
                    pars = True
                elif tN[-k]== '(':
                    paren += 1
                k += 1
            if pars:
                return scEvalulator(tN[1:-2])
            else:
                return thing[len(thing)-k+1:len(thing)-1]
    else:
        awesomeness = [i for i, var in enumerate([thing]) if re.search("\(.*?\([^()]*\).*?\)", var)]
        while len(awesomeness) > 0:
            #intese regexing
            usefulstring = thing
            #this function should replace the depest instance of unsimplified things with simplified things
            new = re.sub("\(([^()]*)\)",str(scEvalulator(re.search("\([^()]*\)",usefulstring).group(0).split(" ")[0]\
                                                             + re.search(" .*",re.search("\(([^()]*)\)",usefulstring).group(0)).group(0))),\
                                    usefulstring, 1)
            thing = new
            #this gets all the indecies of the parameters that are not simplified
            awesomeness = [i for i,val in enumerate([thing]) if re.search("\(.*?\([^()]*\).*?\)",val)]
        params = functions[fname].params
        function = func
        names = functions[fname].paranames
        thing1 = thing.split(" ")
        if params == 0 and type(function) != str:
            return function()
        elif params == 1 and type(function) != str:
            return function(thing1[1][:-1])
        elif params == 2 and type(function) != str:
            return function(thing1[1],thing1[2][:-1])
        elif params == 3 and type(function) != str:
            return function(thing1[1],thing1[2],thing1[3][:-1])
        elif params == 4 and type(function) != str:
            return function(thing1[1],thing1[2],thing1[3],things1[4][:-1])
        elif params == 0:
            return scEvalulator(function)
        elif params == 1:
            return scEvalulator(re.sub('\\b'+names[0]+'\\b',thing1[1][:-1],function))
        elif params == 2:
            return scEvalulator(re.sub('\\b'+names[0]+'\\b',thing1[1],re.sub('\\b'+names[1]+'\\b',thing1[2],function)))
        elif params == 3:
            return scEvalulator(re.sub('\\b'+names[0]+'\\b',thing1[1],re.sub('\\b'+names[1]+'\\b',thing1[2],re.sub('\\b'+names[2]+'\\b',thing1[3],function))))
        elif params == 4:
            return scEvalulator(re.sub('\\b'+names[0]+'\\b',thing1[1],re.sub('\\b'+names[1]+'\\b',thing1[2],re.sub('\\b'+names[2]+'\\b',thing1[3],re.sub('\\b'+names[3]+'\\b', thing1[4], function)))))
def addDefs():
    temp = []
    print("stop adding by responding at any time with DONE")
    latest = input("What definitition do you want to add?\n")
    while latest != "DONE":
        temp.append(latest)
        latest = input("What definition do you want to add?\n")
    for i in temp:
        if i not in current:
            addDef(i)
def importDefs(loc):
    f = open(loc, "r")
    for i in f:
        if i not in current:
            addDef(i)
def whileLoop(cond, inc, do, init):
    var = float(init)
    while functions[cond].evaluate([var]) == 'True':
        init = functions[do].evaluate([init])
        var += 1
    return init
def updateDef(thing, n):
    current[n] = thing
    print(current)
def removeDef(n):
    current[n:n+1] = []
    del functions[[i.split(" ") for i in re.split("[()]",current[n])][1][2]]
    print(current)
def add(num1, num2):
    return float(num1) + float(num2)
def sub(num1, num2):
    return float(num1) - float(num2)
def mult(num1, num2):
    return float(num1) * float(num2)
def div(num1, num2):
    return float(num1) / float(num2)
def ifN(cond, thing1, thing2):
    if cond == 'True':
        return thing1
    else:
        return thing2
def moar(thing1, thing2):
    return str(float(thing1) > float(thing2))
def less(thing1, thing2):
    return str(float(thing1) < float(thing2))
def andN(cond1, cond2):
    return cond1 == 'True' and cond2 == 'True'
def orN(cond1, cond2):
    return cond1 == 'True' or cond2 == 'True'
def notN(cond):
    if cond == "False":
        return 'True'
    return 'False'
def equal(thing1, thing2):
    return thing1 == thing2
def first(thing):
    return thing[0]
def bf(thing):
    return thing[1:]
def last(thing):
    return thing[-1]
def bl(thing):
    return thing[:-1]
def item(n, thing):
    return thing[int(n)]
def word(thing1, thing2):
    return thing1 + thing2
def expt(n1, n2):
    return float(n1) ** float(n2)
def count(thing):
    return len(thing)
functions = {"+":NamePair(add, 2, ['num1','num2']),"-":NamePair(sub, 2,['num1','num2']),"or":NamePair(orN, 2, ['cond1','cond2']),\
             "*":NamePair(mult, 2, ['num1', 'num2']), "/":NamePair(div, 2, ['num1', 'num2']), "not":NamePair(notN, 1, ['cond']),\
             "if":NamePair(ifN, 3, ['cond', 'thing1', 'thing2']), "and":NamePair(andN, 2, ['cond1','cond2']), "count":NamePair(count,2, ['thing']),\
             "expt":NamePair(expt, 2, ['n1', 'n2']), "ident":NamePair(identity, 1, ["thing"]), '>':NamePair(moar, 2, ["thing1","thing2"]),\
             "<":NamePair(less, 2, ["thing1", "thing2"]), 'equal?':NamePair(equal, 2, ["thing1","thing2"]),\
             "first":NamePair(first, 1, ["thing"]), "last":NamePair(last, 1, ["thing"]), "item":NamePair("Item", 2, ["n","thing"]),\
             "bf":NamePair(bf, 1, ["thing"]), "bl":NamePair(bl, 1, ["thing"]), "word":NamePair(word, 2, ["thing1","thing2"]),\
             "while":NamePair(whileLoop, 4, ["cond", "inc", "do","init"])}
def evalulator():
    print("Stop by typing DONE")
    inp = input("What would you like to evaluate?\n")
    while inp != "DONE":
        print(scEvalulator(inp))
        inp = input("What would you like to evaluate?\n")
