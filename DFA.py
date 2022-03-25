from queue import LifoQueue

import NFA
def move(PathCh,X):
    I=set()
    for Vertex in X:
        for i in range(len(Vertex.PathCh)):
            if(PathCh==Vertex.PathCh[i]):
                I.add(Vertex.NextNodes[i])
    return list(I)
def closure(X,nope):
    I=set(X)
    ret=I.copy()
    growth=1
    while(growth):
        growth=0
        for Vertex in I:
            for i in range(len(Vertex.PathCh)):
                if(nope.Num==Vertex.PathCh[i].Num):
                    if(not ret&{Vertex.NextNodes[i]}):
                        growth=1
                        ret.add(Vertex.NextNodes[i])
    return list(ret)
class DFANode:
    def __init__(self,PathCh,NextNode):
        DFANode.MaxNodeNum+=1
        self.StatusNum = DFANode.MaxNodeNum
        self.PathCh = PathCh
        self.NextNode = NextNode
class DFA:
    def __init__(self):
        self.Vertexs=list()
        self.HeadNode=None
        self.TailNode=None
        self.Pointers=list()
def NFA2DFA(nfa):
    pointers=nfa.pointers
    Is=list()
    Status=LifoQueue()
    Status.put(closure({nfa.HeadNode},nfa.Nope))
    Is.append(closure({nfa.HeadNode},nfa.Nope))
    growth=1
    while(growth):
        growth=0
        s=Status.get()
        for PathCh in pointers:
            if PathCh==nfa.Nope:
                continue
            tmp=closure(set(move(PathCh,s)),nfa.Nope)
            if(not tmp):
                continue
            flag=0
            for i in Is:
                if set(i)==set(tmp):
                    flag=1
                    break
            if flag==0:
                growth=1
                Status.put(closure(set(tmp),nfa.Nope))
                Is.append(closure(set(tmp),nfa.Nope))
    for i in Is:
        for j in i:
            print(j.content)
        print("------")
    dfa=DFA()

