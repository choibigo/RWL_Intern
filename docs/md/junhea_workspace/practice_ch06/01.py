# ch06-2 3과 5의 배수를 모두 더하기

# 10 미만의 자연수에서 3과 5의 배수를 구하면 3, 5, 6, 9이다. 이들의 총합은 23이다.
# 1,000 미만의 자연수에서 3의 배수와 5의 배수의 총합을 구하라.

answer = 0
for i in range(1000):
    if i % 3 == 0:
        answer += i
    elif i % 5 == 0:
        answer += i

print(answer)