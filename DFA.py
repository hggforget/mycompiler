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
    MaxNodeNum=0
    def __init__(self,content):
        DFANode.MaxNodeNum+=1
        self.StatusNum = DFANode.MaxNodeNum
        self.content=content
        self.NextNodes =dict()
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
    first=DFANode(set(closure({nfa.HeadNode},nfa.Nope)))
    Status.put(first)
    Is.append(first)
    while(not Status.empty()):
        s=Status.get()
        for PathCh in pointers:
            if PathCh==nfa.Nope:
                continue
            tmp=closure(set(move(PathCh,s.content)),nfa.Nope)
            if(not tmp):
                continue
            flag=0
            for i in Is:
                if i.content==set(tmp):
                    s.NextNodes.update({PathCh:i})
                    flag=1
                    break
            if flag==0:
                newNode=DFANode(set(tmp))
                s.NextNodes.update({PathCh:newNode})
                Status.put(newNode)
                Is.append(newNode)
    for i in Is:
        for j in i.content:
          print(j.content)
        print("该状态编号为 "+i.StatusNum.__str__())
        print("——————")
        for j in i.NextNodes:
            print(i.StatusNum.__str__()+"->"+i.NextNodes[j].StatusNum.__str__()+"("+j.content+")")
        print("------")

    dfa=DFA()

