class Non_Terminal:
    Non_Terminal_Num=0
    def __init__(self,non_terminal):
        Non_Terminal.Non_Terminal_Num+=1
        self.Num=self.Non_Terminal_Num
        self.content=non_terminal
        self.Type=0
class Terminal:
    Terminal_Num=0
    def __init__(self,terminal):
        Terminal.Terminal_Num+=1
        self.Num=self.Terminal_Num
        self.content=terminal
        self.Type=1
class Raw_Production:
    def __init__(self,grammar):
        grammar = grammar.strip()
        for i in range(len(grammar)):
            if (grammar[i] == '-' and grammar[i + 1] == '>'):
                self.non_terminal=grammar[0:i]
                self.rightend=grammar[i+2:len(grammar)]