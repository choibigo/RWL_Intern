# 7번

while 1:
    try:
        a = int(input("구구단을 출력할 숫자를 입력하세요(2~9): "))
    except:
        print("숫자만 입력 가능합니다.")
        continue
    if a < 2 or a > 9:
        print("숫자는 2에서 9까지만 입력 가능합니다.")
    else:
        break

for i in range(1, 10):
    print(i*a, end=' ')