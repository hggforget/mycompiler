import Functions_Scanner


class NFANode:
    def __init__(self,StatusNum,content):
        self.StatusNum=StatusNum
        self.content=content
        self.PathCh=[]
        self.NextNodes=[]
class NFA:
    def __init__(self,Productions):
        self.Vertexs=list()
        self.HeadNode=NFANode(0,"HeadNode")
        self.TailNode=NFANode(-1,"TailNode")
        self.pointers=list()
        for i in Productions.non_terminals:
            self.Vertexs.append(NFANode(i.Num,i.content))
        for i in Productions.terminals:
            self.pointers.append(i)
        nope= Functions_Scanner.Terminal('ε')
        self.pointers.append(nope)
        for i in self.Vertexs:
            self.HeadNode.PathCh.append(nope)
            self.HeadNode.NextNodes.append(i)
        self.Vertexs.append(self.HeadNode)
        for p in Productions.productions:
            node=self.Vertexs[p.non_terminal.Num-1]
            node.PathCh.append(p.rightend.terminal)
            if(p.rightend.non_terminal!=None):
                node.NextNodes.append(self.Vertexs[p.rightend.non_terminal.Num-1])
            else:
                node.NextNodes.append(self.TailNode)
        for i in self.Vertexs:
            for r in range(len(i.PathCh)):
                print(i.content+"->"+i.NextNodes[r].content+"("+i.PathCh[r].content+")")

class Grammar2NFA:
    def ToNFA(self,grammarlines):
        productions= Functions_Scanner.Productions(grammarlines)
        '''
        for i in productions.non_terminals:
            print(i.content+" "+i.Num.__str__())
        for i in productions.terminals:
            print(i.content+" "+i.Num.__str__())
        for p in productions.productions:
            str =""
            if p.rightend.non_terminal != None:
                str = p.rightend.non_terminal.content
            print(p.non_terminal.content + "->" + p.rightend.terminal.content + str)
        '''
        nfa=NFA(productions)
