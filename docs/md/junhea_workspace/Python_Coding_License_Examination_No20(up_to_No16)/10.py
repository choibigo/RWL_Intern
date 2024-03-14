# 10번

class Calculator:
    def __init__ (self, a):
        self.all = a
        self.answer = 0
    
    def sum (self):
        self.answer = 0
        for i in self.all:
            self.answer += i
        return self.answer
    
    def avg (self):
        self.answer = 0
        for i in self.all:
            self.answer += i
        return self.answer / len(self.all)