# 6번

a = str(input("덧셈을 원하는 수들을 입력하세요.(단, 수끼리는 ','로 구분합니다.): "))
num = a.split(',')
answer = 0
for i in num:
    answer += int(i)

print(answer)