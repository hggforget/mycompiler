from Functions import Non_Terminal, Raw_Production
from Functions import Terminal

keywords={
"bool",
"break",
"case",
"catch",
"char",
"class",
"const",
"continue",
"default",
"delete",
"do",
"double",
"else",
"false",
"float",
"for",
"if",
"int",
"long",
"main",
"namespace",
"new",
"private",
"protected",
"public",
"return",
"short",
"sizeof",
"static",
"struct",
"switch",
"this",
"throw",
"true",
"try",
"void",
"while",
}
def isLetter(ch):
    if(ch>='a' and ch<='z') or (ch>='A' and ch<='Z'):
        return True
    return False
def isDigit(ch):
    if(ch>='0' and ch<='9'):
        return True
    return False
def isQualifier(ch):
    if ch==',' or ch==';' or ch=='{' or ch=='}':
        return True
    return False
def isCal(str,index):
    if str[index]=='+' or str[index]=='-' or str[index]=='*' or str[index]=='/'or \
        str[index]=='%' or str[index]=='=' or str[index]=='(' or str[index]==')':
        return index
    elif str[index]=='>' or str[index]=='<':
        if index+1>=len(str):
             return index
        elif str[index+1]=='=':
             return index+1
        else:
             return index
    return -1
def isKeyWord(str):
    for i in keywords:
        if i==str:
            return True
    return False
class RightEnd:
    def __init__(self):
        self.terminal=None
        self.non_terminal=None
class Production:
    def __init__(self,leftend,re):
        self.non_terminal=leftend
        self.rightend=re
class Productions:
    def __init__(self,grammarlines):
        Non_Terminal.Non_Terminal_Num=0
        Terminal.Terminal_Num=0
        self.non_terminals=list()
        self.terminals=list()
        self.productions=list()
        self.Nope=Terminal('ε')
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
                flag=0
                re = RightEnd()
                tmp_terminal = None
                tmp_non_termonal = None
                for i in range(len(r)):
                    if(non_terminals&{r[i:len(r)]}):
                        terminals.add(r[0:i])
                        tmp_terminal=r[0:i]
                        tmp_non_termonal=r[i:len(r)]
                        flag=1
                        break
                if flag==0:
                    tmp_terminal = r[0:len(r)]
                for i in self.non_terminals:
                    if(i.content==tmp_non_termonal):
                        re.non_terminal=i
                        break
                flag1=0
                for i in self.terminals:
                    if(tmp_terminal=="" or i.content==tmp_terminal):
                        re.terminal=i
                        flag1=1
                        break
                if flag1==0:
                    re.terminal=Terminal(tmp_terminal)
                    self.terminals.append(re.terminal)
                self.productions.append(Production(leftend,re))
class Token:
    Token_Num=0
    def __init__(self,Content,Type):
        Token.Token_Num+=1
        self.Num=Token.Token_Num
        self.Content=Content
        self.Type=Type






