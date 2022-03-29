from Functions_Parser import *
class Parser:
    def __init__(self,tokens,grammar):
        f = open(grammar, encoding='utf-8')
        grammarlines = f.readlines()
        f.close()
        productions=Productions(grammarlines)
        First_Sets=First(productions)
        Follow_Sets=Follow(productions,First_Sets)
        Projects=list()

        I0=Project_Clusters()




