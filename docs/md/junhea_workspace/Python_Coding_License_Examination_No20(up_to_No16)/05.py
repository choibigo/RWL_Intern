# 5번

while 1:
    try:
        a = int(input("피보나치 수열을 출력합니다. 원하는 출력 갯수를 입력하세요: "))
    except:
        print("숫자만 입력 가능합니다.")
        continue
    if a<0:
        print("0 이상의 수만 입력 가능합니다.")
    else:
        break

answer = []
if a > 2:
    answer = answer + [0, 1]
    for i in range(a-2):
        answer.append(answer[i] + answer[i + 1])
elif a == 2:
    answer = answer + [0, 1]
elif a == 1:
    answer.append(0)

print(answer)