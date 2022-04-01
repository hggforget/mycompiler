from Functions import Non_Terminal, Raw_Production,Terminal
from queue import LifoQueue

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
        self.isAcc = False
        if len(content)==0:
            self.isAcc=True
        self.content=content
        self.Lookahead=lookahead

def isSame(P1,I):
    for i in I:
        if len(i.content)!=len(P1):
            continue
        flag=0
        for j in range(len(i.content)):
            if P1[j]!=i.content[j]:
                flag=1
                break
        if flag==0:
            return True
    return False
def GetLookahead(beta,First_Sets,Nope,PreLookahead):
    ret=set()
    flag=0
    for i in range(1,len(beta)):
        if beta[i].Type==1:
            ret.add(beta[i])
            flag=1
            break
        else:
            ret=ret|(First_Sets[beta[i]]-{Nope})
            if First_Sets[beta[i]]&{Nope}:
                flag=1
                break
    if flag==0:
        ret=ret|PreLookahead
    return ret
def Closure(I0,Productions,First_Sets):
    I=I0.copy()
    ret=I.copy()
    pros=list()
    for p in Productions.productions:
        tmp=list()
        for i in range(len(p.rightend)):
            if p.rightend[i]!=Productions.Nope:
                tmp.append(p.rightend[i])
        pros.append(Production(p.non_terminal,tmp))
    growth=1
    while(growth==1):
        growth=0
        for i in I:
            if len(i.content)==0 or i.content[0].Type==1:
                continue
            Lookahead=GetLookahead(i.content,First_Sets,Productions.Nope,i.Lookahead)
            for p in pros:
                if p.non_terminal==i.content[0]:
                    if not isSame(p.rightend,I):
                        ret.add(Project(p.rightend,Lookahead))
                        #print(p.non_terminal.content)
        if ret-I:
            growth=1
            I=ret.copy()
    return ret
def Go(I,X):
    Projects=set()
    for i in I:
        if len(i.content) == 0:
            continue
        if i.content[0]==X:
            Projects.add(Project(i.content[1:len(i.content)],i.Lookahead))
    return Projects
class Project_Clusters:
    Clusters_Num=0
    def __init__(self,Projects):
        Project_Clusters.Clusters_Num+=1
        self.Num=Project_Clusters.Clusters_Num
        self.Projects=Projects
        self.NextClusters=dict()


def GenerateProjects(Initial_Projects,Productions,First_Sets):
    Clusters=list()
    growth=1
    stack=LifoQueue()
    tmp=Closure(Initial_Projects,Productions,First_Sets)
    stack.put(tmp)
    Clusters.append(tmp)
    while not stack.empty():
        I_tmp=stack.get()
        vis=set()
        for i in I_tmp:
            if len(i.content)==0:
                continue
            if not vis&{i.content[0]}:
                print(i.content[0].content+"asds")
                for k in I_tmp:
                    for j in k.content:
                        print(j.content)
                    print("---")
                print("--------------")
                vis.add(i.content[0])
                tmp=Closure(Go(I_tmp,i.content[0]),Productions,First_Sets)
                for k in tmp:
                    for j in k.content:
                        print(j.content)
                    print("---")
                print("--------------")
                stack.put(tmp)
                Clusters.append(tmp)
    return Clusters








class Table:
    def __init__(self,PathChs,Status,):
        self.PathChs=PathChs
        self.Status=Status
        self.Table=dict()
