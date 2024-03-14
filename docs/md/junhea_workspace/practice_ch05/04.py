def tf(a):
    if a >= 0:
        return True
    else:
        return False

print(list(filter(lambda x : tf(x), [1, -2, 3, -5, 8, -3])))