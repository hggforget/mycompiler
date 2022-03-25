# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import NFA
import Functions_Scanner
from DFA import NFA2DFA


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
f=open("grammar.txt",encoding='utf-8')
grammarlines=f.readlines()

f.close()

g2n= NFA.Grammar2NFA()
nfa=g2n.ToNFA(grammarlines)
dfa=NFA2DFA(nfa)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
