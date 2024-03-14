# 14번

def Compress(a):
    answer = []
    stak = 0
    strtest = None
    for i in range(len(list(a))):
        if strtest == a[i]:
            stak += 1
            answer[len(answer) - 1] = str(stak)
        else:
            answer.append(a[i])
            strtest = a[i]
            stak = 1
            answer.append(str(stak))
    return ''.join(answer)

print(Compress('aaabbcccccca'))