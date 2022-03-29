import Functions_Scanner
from DFA import NFA2DFA
from NFA import Grammar2NFA


class Scanner:
    def __init__(self,changshu,biaoshifu,string):
        f=open(changshu,encoding='utf-8')
        changshulines=f.readlines()
        f.close()
        f=open(biaoshifu,encoding='utf-8')
        biaoshifulines=f.readlines()
        f.close()
        f = open(string, encoding='utf-8')
        strings = f.readlines()
        f.close()
        g2n= Grammar2NFA()
        nfa_changshu=g2n.ToNFA(changshulines)
        dfa_changshu=NFA2DFA(nfa_changshu)
        nfa_bsf = g2n.ToNFA(biaoshifulines)
        dfa_bsf = NFA2DFA(nfa_bsf)
        Functions_Scanner.Token.Token_Num=0
        tokens=list()
        for str in strings:
            str=str.strip('\n')
            flag=0
            index=0
            while index < len(str):
                if str[index]==' ' or str[index]==9 or str[index]==10 or str[index]==14:
                    index+=1
                elif Functions_Scanner.isQualifier(str[index]):
                    tokens.append(Functions_Scanner.Token(str[index], "限定符"))
                    index+=1
                else:
                    flag=Functions_Scanner.isCal(str,index)
                    if flag!=-1:
                        tokens.append(Functions_Scanner.Token(str[index:flag+1], "运算符"))
                        index=flag+1
                    elif Functions_Scanner.isLetter(str[index]):
                        pre=index
                        while index<len(str):
                            if Functions_Scanner.isDigit(str[index]) or Functions_Scanner.isLetter(str[index]):
                                index+=1
                            else:
                                break
                        if dfa_bsf.run(str[pre:index]):
                            if Functions_Scanner.isKeyWord(str[pre: index]):
                                tokens.append(Functions_Scanner.Token(str[pre: index], "关键字"))
                            else:
                                tokens.append(Functions_Scanner.Token(str[pre: index], "标识符"))
                        else:
                            tokens.append(Functions_Scanner.Token(str[pre: index], "非法标识符"))
                    elif Functions_Scanner.isDigit(str[index]) or str[index]=='.' or str[index]=='e':
                        pre = index
                        while index < len(str):
                            if str[index] == ' ' or str[index] == 9 or str[index] == 10 or str[index] == 14 or \
                                    Functions_Scanner.isCal(str, index) != -1 \
                                    or Functions_Scanner.isQualifier(str[index]):
                                if (str[index] == '+' or str[index] == '-') and\
                                        str[index - 1] == 'e' and Functions_Scanner.isDigit(str[index - 2]):
                                    index+=1
                                else:
                                    break
                            else:
                                index += 1
                        if dfa_changshu.run(str[pre:index]):
                            tokens.append(Functions_Scanner.Token(str[pre: index], "常数"))
                        else:
                            tokens.append(Functions_Scanner.Token(str[pre: index], "非法常数"))
                    else:
                        tokens.append(Functions_Scanner.Token(str[index], "未定义"))
                        index+=1
        self.Tokens=tokens
        for i in tokens:
            print("("+i.Num.__str__()+" , "+i.Content+" , "+i.Type+")")







