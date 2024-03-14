# 13번

def DashInsert(a):
    test = list(a)
    state = -1
    i = 0
    for s in range(len(test)):
        if state == 0 and int(test[i]) % 2 == 0:
            test.insert(i, '*')
            i += 1
        elif state == 1 and int(test[i]) % 2 == 1:
            test.insert(i, '-')
            i += 1
        if int(test[i]) % 2 == 0:
            state = 0
        else:
            state = 1
        i += 1
    return ''.join(test)

print(DashInsert('4546793'))