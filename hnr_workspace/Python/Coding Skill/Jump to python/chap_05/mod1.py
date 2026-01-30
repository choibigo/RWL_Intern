# mod1.py
def add(a, b):
    return a + b

def sub(a, b): 
    return a-b

print(__name__)

if __name__ == "__main__": #name 이라는 것이 main 일때만 실행해라 
    print(add(1, 4))
    print(sub(4, 2))