import random
answer = []
while len(answer)<6:
    a = random.randint(1, 45)
    if a not in answer:
        answer.append(a)
answer.sort()
print(answer)