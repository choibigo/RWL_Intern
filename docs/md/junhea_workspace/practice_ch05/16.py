import itertools

word = 'abcd'
linee = list(itertools.permutations(word,4))
for i in range(len(linee)):
    linee[i] = ''.join(linee[i])

print(linee)