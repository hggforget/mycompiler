class NFANode:
    def __init__(self,StatusNum,PathCh):
        self.StatusNum=StatusNum
        self.PathCh=PathCh
        self.NextNodes=[]
class NFA:
    def __init__(self,HeadNode,TailNode):
        self.HeadNode=HeadNode
        self.TailNode=TailNode
class GenerateNFAMethod:
    def __init__(self):

