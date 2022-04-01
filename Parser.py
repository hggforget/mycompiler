from Functions_Parser import *
class Parser:
    def __init__(self,tokens,grammar):
        f = open(grammar, encoding='utf-8')
        grammarlines = f.readlines()
        f.close()
        productions=Productions(grammarlines)
        First_Sets=First(productions)
        Follow_Sets=Follow(productions,First_Sets)
        I0=set()
        I0.add(Project([productions.S],{productions.End}))
        GenerateProjects(I0,productions,First_Sets)





