from Functions import Non_Terminal, Raw_Production,Terminal

class Production:
    def __init__(self,leftend,rightend):
        self.non_terminal=leftend
        self.rightend=rightend
class Productions:
    def __init__(self,grammarlines):
        Non_Terminal.Non_Terminal_Num=0
        Terminal.Terminal_Num=0
        self.non_terminals=list()
        self.terminals=list()
        self.productions=list()
        self.Nope=Terminal('ε')
        self.End=Terminal('#')
        self.terminals.append(self.End)
        self.terminals.append(self.Nope)
        Raw_Productions=list()
        non_terminals=set()
        terminals=set()
        for grammar in grammarlines:
            Raw_Productions.append(Raw_Production(grammar))
        for i in Raw_Productions:
            non_terminals.add(i.non_terminal)
        for i in non_terminals:
            tmp=Non_Terminal(i)
            if(i==Raw_Productions[0].non_terminal):
                self.S=tmp
            self.non_terminals.append(tmp)
        for p in Raw_Productions:
            leftend=None
            for i in self.non_terminals:
                if(i.content==p.non_terminal):
                    leftend=i
                    break
            rightendlist=p.rightend.split('|')
            for r in rightendlist:
                rightend = list()
                for Ch in r:
                    flag1=0
                    for i in self.non_terminals:
                        if i.content==Ch:
                            rightend.append(i)
                            flag1=1
                            break
                    if flag1==0:
                        for i in self.terminals:
                            if i.content==Ch:
                                rightend.append(i)
                                flag1=1
                                break
                    if flag1==0:
                        tmp=Terminal(Ch)
                        self.terminals.append(tmp)
                        rightend.append(tmp)
                self.productions.append(Production(leftend,rightend))

def First(productions):
    First_Sets=dict()
    for p in productions.non_terminals:
        First_Sets.update({p:set()})
    growth=1
    while(growth):
        growth=0
        for p in productions.productions:
            for i in range(len(p.rightend)):
                if p.rightend[i].Type==1:
                    tmp=First_Sets.get(p.non_terminal).copy()
                    if not tmp&{p.rightend[i]}:
                        First_Sets.update({p.non_terminal:tmp|{p.rightend[i]}})
                        growth=1
                    break
                else:
                    tmp=First_Sets.get(p.non_terminal).copy()
                    if i == len(p.rightend) - 1:
                        tmp=tmp|First_Sets.get(p.rightend[i])
                    else:
                        tmp=tmp|(First_Sets.get(p.rightend[i])-{productions.Nope})
                    if tmp-First_Sets.get(p.non_terminal):
                        growth=1
                        First_Sets.update({p.non_terminal:tmp})
                if First_Sets.get(p.non_terminal)!=None and First_Sets.get(p.non_terminal)&{productions.Nope}:
                    break
    for i in First_Sets:
        for j in First_Sets.get(i):
            print(j.content)
        print("---------" + i.content)
    return First_Sets
def Follow(productions,First_Sets):
    Follow_Sets=dict()
    for p in productions.non_terminals:
        Follow_Sets.update({p:set()})
    Follow_Sets.update({productions.S:{productions.End}})
    growth=1
    while(growth):
        growth=0
        for p in productions.productions:
            for i in range(len(p.rightend)):
                if p.rightend[i].Type==1:
                    continue
                tmp=Follow_Sets.get(p.rightend[i]).copy()
                if i==len(p.rightend)-1:
                    tmp=tmp|Follow_Sets.get(p.non_terminal)
                elif p.rightend[i+1].Type==1:
                    tmp=tmp|{p.rightend[i+1]}
                else:
                    index=i+1
                    flag=1
                    while index<len(p.rightend):
                        if p.rightend[index].Type==1:
                            tmp=tmp|{p.rightend[index]}
                            flag=0
                        else:
                            tmp=tmp|(First_Sets.get(p.rightend[index])-{productions.Nope})
                            if not First_Sets.get(p.rightend[index])&{productions.Nope}:
                                flag=0
                        if flag==0:
                            break
                        index+=1
                    if flag==1:
                        tmp=tmp|Follow_Sets.get(p.non_terminal)
                if tmp-Follow_Sets.get(p.rightend[i]):
                    Follow_Sets.update({p.rightend[i]:tmp})
                    growth=1
    for i in Follow_Sets:
        for j in Follow_Sets.get(i):
            print(j.content)
        print("-------------Follow  "+i.content)

class Project:
    def __init__(self,content,lookahead):
        self.content=content
        self.Lookahead=lookahead

def GenerateProjects(Initial_Projects,Productions):
    I=Initial_Projects.copy()
    for project in I:
        if project[0].Type==1:
            continue
        for production in Productions.productions:
            if production.non_terminal==project[0]:
                new_P=Project(production.rightend,First())


class Project_Clusters:
    Clusters_Num=0
    def __init__(self,Projects):
        Project_Clusters.Clusters_Num+=1
        self.Num=Project_Clusters.Clusters_Num
        self.Projects=Projects
        self.NextClusters=dict()









class Table:
    def __init__(self,PathChs,Status,):
        self.PathChs=PathChs
        self.Status=Status
        self.Table=dict()
