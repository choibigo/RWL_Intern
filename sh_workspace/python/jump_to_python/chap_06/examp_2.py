# 10 미만의 자연수에서 3과 5의 배수를 구하면 3, 5, 6, 9이다. 이들의 총합은 23이다.
# 1,000 미만의 자연수에서 3의 배수와 5의 배수의 총합을 구하라.

def solve():
    result = 0

    for i in range(0,1000):
        if i % 3 == 0 or i % 5 == 0:
            result += i

    return result

a = solve()

print(a)



