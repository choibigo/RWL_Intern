class Calculator:
    def __init__(self):
        self.value = 0
    
    def add(self, val):
        self.value += val

class MaxLimitCalculator(Calculator):
    def add(self, val):
        a = self.value + val
        if a > 100:
            self.value = 100
        else:
            self.value = a

cal = MaxLimitCalculator()
cal.add(50)
cal.add(60)

print(cal.value)