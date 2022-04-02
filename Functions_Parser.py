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
                if not First_Sets.get(p.non_terminal)&{productions.Nope}:
                    break
    '''
    for i in First_Sets:
        for j in First_Sets.get(i):
            print(j.content)
        print("---------" + i.content)
    '''
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
    '''
        for i in Follow_Sets:
        for j in Follow_Sets.get(i):
            print(j.content)
        print("-------------Follow  "+i.content)
    '''
Project_List=list()
pros=list()
class Project:
    def __init__(self,content,lookahead,prefix):
        self.content=content
        self.Lookahead=lookahead
        self.Prefix=prefix

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
            if not First_Sets[beta[i]]&{Nope}:
                flag=1
                break
    if flag==0:
        ret=ret|PreLookahead
    return ret
def AddProject(rightend,Lookahead,prefix):
    for i in Project_List:
        if not Lookahead-(Lookahead&i.Lookahead):
            if len(rightend)!=len(i.content) or len(prefix)!=len(i.Prefix):
                continue
            flag=0
            for j in range(len(rightend)):
                if rightend[j]!=i.content[j]:
                    flag=1
                    break
            for j in range(len(prefix)):
                if prefix[j]!=i.Prefix[j]:
                    flag=1
                    break
            if flag==0:
                return i
    tmp=Project(rightend,Lookahead,prefix)
    Project_List.append(tmp)
    return tmp

def Closure(I0,Productions,First_Sets):
    I=I0.copy()
    ret=I.copy()
    growth=1
    while(growth==1):
        growth=0
        for i in I:
            if len(i.content)==0 or i.content[0].Type==1:
                continue
            Lookahead=GetLookahead(i.content,First_Sets,Productions.Nope,i.Lookahead)
            for p in pros:
                if p.non_terminal==i.content[0]:
                        ret.add(AddProject(p.rightend,Lookahead,[p.non_terminal]))
                        #print(p.non_terminal.content)
        if ret-I:
            growth=1
            I=ret.copy()
    return ret
def Go(I,X):
    Projects=set()
    for i in I.Projects:
        if len(i.content) == 0:
            continue
        if i.content[0]==X:
            tmp_Prefix=i.Prefix.copy()
            tmp_Prefix.append(i.content[0])
            Projects.add(AddProject(i.content[1:len(i.content)],i.Lookahead,tmp_Prefix))
    return Projects
class Project_Clusters:
    Clusters_Num=0
    def __init__(self,Projects):
        Project_Clusters.Clusters_Num+=1
        self.Num=Project_Clusters.Clusters_Num
        self.Projects=Projects
        self.NextClusters=dict()
        self.isAcc=False
def Check(Projects,List):
    for l in List:
        if not Projects-(Projects&(l.Projects)):
            return False
    return True
def PrintCluster(Cluster):
        for k in Cluster.Projects:
            for j in k.Prefix:
                print(j.content, end="")
            print(".", end="")
            for j in k.content:
                print(j.content, end="")
            print(" ", end="")
            for j in k.Lookahead:
                print("/" + j.content, end="")
            print("")
        print("--------------")
def GenerateClusters(Initial_Projects,Productions,First_Sets):
    Clusters=list()
    growth=1
    stack=LifoQueue()
    tmp=Project_Clusters(Closure(Initial_Projects,Productions,First_Sets))
    stack.put(tmp)
    Clusters.append(tmp)
    while not stack.empty():
        I_tmp=stack.get()
        vis=set()
        for i in I_tmp.Projects:
            if len(i.content)==0:
                continue
            if not vis&{i.content[0]}:
                vis.add(i.content[0])
                tmp=Closure(Go(I_tmp,i.content[0]),Productions,First_Sets)
                if Check(tmp,Clusters):
                    tmp_Cluster=Project_Clusters(tmp)
                    I_tmp.NextClusters.update({i.content[0]:tmp_Cluster})
                    stack.put(tmp_Cluster)
                    Clusters.append(tmp_Cluster)
                else:
                    for l in Clusters:
                        if not tmp - (tmp & (l.Projects)):
                            I_tmp.NextClusters.update({i.content[0]:l})
                            break
    return Clusters
class Table:
    def __init__(self,Clusters,Acc):
        self.PathChs=set()
        self.Status=Clusters
        self.Table=dict()
        self.I0=Clusters[0]
        self.IsLR1=True
        for Cluster in Clusters:
            for p in Cluster.Projects:
                if len(p.content) == 0:
                    for pro in pros:
                        if pro.non_terminal != p.Prefix[0] or len(p.Prefix) != (len(pro.rightend) + 1):
                            continue
                        flag = 0
                        for i in range(1, len(p.Prefix)):
                            if p.Prefix[i] != pro.rightend[i - 1]:
                                flag = 1
                                break
                        if flag == 0:
                            if p.Prefix[0] == Acc:
                                Cluster.isAcc=True
                                print(Cluster.Num.__str__())
                            for lookahead in p.Lookahead:
                                if self.Table.get((Cluster, lookahead.content))==None:
                                    self.Table.update({(Cluster, lookahead.content): pro})
                                elif self.Table.get((Cluster, lookahead.content))!=pro:
                                    PrintCluster(Cluster)
                                    print(pro.non_terminal.content)
                                    print(pro)
                                    for k in pro.rightend:
                                        print(k.content)
                                    print("_______")
                                    print("Error:归约-归约冲突")
                                    print(self.Table.get((Cluster, lookahead.content)).non_terminal.content)
                                    print(self.Table.get((Cluster, lookahead.content)))
                                    for k in self.Table.get((Cluster, lookahead.content)).rightend:
                                        print(k.content)
                                    print("_______")
                                    self.IsLR1=False
                                    return

        vis=set()
        stack=LifoQueue()
        stack.put(self.I0)
        while not stack.empty():
            tmpI=stack.get()
            vis.add(tmpI)
            for i in tmpI.NextClusters:
                if self.Table.get((tmpI,i.content))==None:
                    self.Table.update({(tmpI,i.content):tmpI.NextClusters[i]})
                else:
                    if i.Type==1:
                        PrintCluster(tmpI)
                        print(i.content)
                        print("Error:移进-归约冲突")
                    else:
                        print("Error:移进-移进冲突")
                    self.IsLR1 = False
                    return
                self.PathChs.add(i)
                if not vis&{tmpI.NextClusters[i]}:
                    vis.add(tmpI.NextClusters[i])
                    stack.put(tmpI.NextClusters[i])