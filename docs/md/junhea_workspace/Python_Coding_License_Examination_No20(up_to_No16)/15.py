# 15번

def Duplicate_Numbers(a):
    inputnum = a.split()
    answer = []
    for i in range(len(inputnum)):
        ans = 'True'
        for a in range(10):
            if str(a) not in list(inputnum[i]):
                ans = 'False'
                break
            elif list(inputnum[i]).count(str(a)) > 1:
                ans = 'False'
                break
        answer.append(ans)
    return ' '.join(answer)

print(Duplicate_Numbers('0123456789 01234 01234567890 6789012345 012322456789'))