from queue import LifoQueue

import NFA
from Functions_Scanner import isDigit, isLetter


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
        self.isHead=False
        self.isTail=False
        self.NextNodes =dict()
class DFA:
    def __init__(self,Vertexs,HeadNode,TailNodes,Pointers):
        self.Vertexs=Vertexs
        self.HeadNode=HeadNode
        self.TailNodes=TailNodes
        self.Pointers=Pointers
    def run(self,str):
        status=self.HeadNode
        #print(str)
        flag=0
        index=-1
        for i in range(len(str)):
            isExist=0
            for PathCh in status.NextNodes.keys():
                if PathCh.content=='d':
                    if isDigit(str[i]):
                        isExist=1
                        status=status.NextNodes[PathCh]
                        break
                elif PathCh.content=='s':
                    if str[i] == '-' or str[i] == '+':
                        status=status.NextNodes[PathCh]
                        isExist=1
                        break
                elif PathCh.content=='l':
                    if isLetter(str[i]):
                        isExist=1
                        status = status.NextNodes[PathCh]
                        break
                elif PathCh.content==str[i]:
                    isExist=1
                    status=status.NextNodes[PathCh]
                    break
            if isExist==0:
                print("ERROR:没有该路径的转移（"+str[i]+"）"+"   ended at"+str[0:i])
                index=i
                flag=1
                break
        if flag==0:
            return True
        else:
            return False
def NFA2DFA(nfa):
    DFANode.MaxNodeNum=0
    pointers=nfa.pointers
    Is=list()
    Status=LifoQueue()
    first=DFANode(set(closure({nfa.HeadNode},nfa.Nope)))
    TailNodes=list()
    first.isHead=True
    for i in first.content:
        if (i.StatusNum == 0):
            first.isTail = True
            TailNodes.append(first)
            break
    HeadNode=first
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
                for i in newNode.content:
                    if(i.StatusNum==0):
                        newNode.isTail=True
                        TailNodes.append(newNode)
                        break
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
    dfa=DFA(Is,HeadNode,TailNodes,pointers)
    return dfa

