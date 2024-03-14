# 12번

result = 0

try:
    [1, 2, 3][3]
    "a" + 1
    4 / 0
except TypeError:
    result += 1
except ZeroDivisionError:
    result += 2
except IndexError:
    result += 3
finally:
    result += 4

print(result)

## try 문에 있는 명령들은 순서대로 IndexError, TypeError, ZeroDivisionError 을 발생시킨다. 즉 시작하자마자 IndexError가 걸려 result에 3이 더해진 뒤 finally에서 4가 더해지고 result는 7이 된다.