from Functions_Parser import *
class Parser:
    def __init__(self,tokens,grammar,instring):
        f = open(grammar, encoding='utf-8')
        grammarlines = f.readlines()
        f.close()
        f = open(instring, encoding='utf-8')
        strlines = f.readlines()
        f.close()
        productions=Productions(grammarlines)
        #初始化
        Acc=Non_Terminal(productions.S.content+'‘')
        pros.append(Production(Acc,[productions.S]))
        for p in productions.productions:
            tmp = list()
            for i in range(len(p.rightend)):
                if p.rightend[i] != productions.Nope:
                    tmp.append(p.rightend[i])
            pros.append(Production(p.non_terminal, tmp))
        First_Sets=First(productions)
        Follow_Sets=Follow(productions,First_Sets)
        I0=set()
        I0.add(AddProject([productions.S],{productions.End},[Acc]))
        Clusters=GenerateClusters(I0,productions,First_Sets)
        table = Table(Clusters, Acc)
        if not table.IsLR1:
            print("Error: 该文法不是LR(1)文法")
        else:
            Status_Stack = LifoQueue()
            Status_Stack.put(table.I0)
            Ch_Stack = LifoQueue()
            Ans_Stack = LifoQueue()
            Ch_Stack.put('#')
            for i in range(len(tokens) - 1, -1, -1):
                if tokens[i].Type == "标识符":
                    Ch_Stack.put('a')
                elif tokens[i].Type == "常数":
                    Ch_Stack.put('b')
                elif tokens[i].Content == "double" or tokens[i].Content == "float" \
                        or tokens[i].Content == "int" or tokens[i].Content == "char" or \
                        tokens[i].Content == "bool":
                    Ch_Stack.put('c')
                elif tokens[i].Content == "if":
                    Ch_Stack.put('d')
                elif tokens[i].Content == "while":
                    Ch_Stack.put('e')
                elif tokens[i].Content == ">=":
                    Ch_Stack.put('g')
                elif tokens[i].Content == "<=":
                    Ch_Stack.put('l')
                else:
                    Ch_Stack.put(tokens[i].Content)
            while not Status_Stack.empty():
                Status = Status_Stack.get()
                Status_Stack.put(Status)
                Ch = Ch_Stack.get()
                Next_Status = table.Table.get((Status, Ch))
                #PrintCluster(Status)
                #print(Ch)
                #print("__________")
                if isinstance(Next_Status,Project_Clusters):
                    Status_Stack.put(Next_Status)
                    Ans_Stack.put(Ch)
                elif isinstance(Next_Status,Production):
                    Reduction = Next_Status
                    Ch_Stack.put(Ch)
                    for k in Reduction.rightend:
                        Ans_Stack.get()
                        Status_Stack.get()
                    if not Status.isAcc:
                        Ch_Stack.put(Reduction.non_terminal.content)
                    else:
                        print("Success!")
                        Status_Stack.get()
                else:
                    print("Failure " + " Error at " + (len(tokens) - Ch_Stack.qsize()).__str__() + " " + Ch)
                    print(Status_Stack.qsize().__str__())
                    break








