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
        self.TailNode=NFANode(0,"TailNode")
        self.pointers=list()
        self.HeadNode=NFANode(Productions.S.Num,Productions.S.content)
        self.Vertexs.append(self.HeadNode)
        for i in Productions.non_terminals:
            if(i.Num==self.HeadNode.StatusNum):
                continue
            self.Vertexs.append(NFANode(i.Num,i.content))
        for i in Productions.terminals:
            self.pointers.append(i)
        self.Nope=Productions.Nope
        self.pointers.append(self.Nope)
        self.Vertexs.append(self.TailNode)
        for p in Productions.productions:
            node=None
            for i in self.Vertexs:
                if i.StatusNum==p.non_terminal.Num:
                    node=i
                    break
            node.PathCh.append(p.rightend.terminal)
            if(p.rightend.non_terminal!=None):
                for i in self.Vertexs:
                    if i.StatusNum == p.rightend.non_terminal.Num:
                        node.NextNodes.append(i)
                        break
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
        return nfa
