# ch06-4 간단한 메모장 만들기

# 원하는 메모를 파일에 저장하고 추기 및 조회가 가능한 간단한 메모장을 만들어 보자.
# 책에 있는 내용은 내용추가, 읽기밖에 없지만 나는 내용수정도 가능하게 할 것이다.
# 터미널에 python (이 프로그램 이름) (모드) (내용) 을 입력했을 때 파일내용에 접근할 수 있게 할 것이다. 단, 내용은 -r, -w일 때 입력할 필요가 없다.
# 모드 종류로는 -a 일 때 단순 내용 추가 -r 일 때 저장된 내용 출력 -w 일 때 전체 내용 확인 후 내용 수정이 가능하게 할 것이다.

import sys

mod = sys.argv[1]
if len(sys.argv) > 2:
    memo = sys.argv[2]

if mod == '-a':
    try:
        f = open('C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/ch06-4 textfile.txt', 'a')
    except (FileNotFoundError):
        f = open('C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/ch06-4 textfile.txt', 'w')
    f.write(memo)
    f.write('\n')
    f.close()
elif mod == '-r':
    f = open('C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/ch06-4 textfile.txt', 'r')
    things = f.readlines()
    for i in things:
        i.strip()
        print(i)
    f.close()
elif mod == '-w':
    f = open('C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/ch06-4 textfile.txt', 'r')
    things = f.readlines()
    for i in things:
        i.strip()
        print(i)
    f.close()
    if things != []:
        while 1:
            try:
                rewrite = int(input('수정을 원하는 줄을 입력하세요 :'))
            except:
                print("숫자만 입력하셔야 합니다.")
                continue
            if rewrite > len(things):
                print("해당 줄이 존재하지 않습니다.")
            elif rewrite < 1:
                print("0보다 큰 수를 입력해야 합니다.")
            else:
                break
        memo2 = str(input("수정할 내용을 입력하세요 : "))
        if memo2 != '':
            things[rewrite-1] = memo2 + '\n'
        else:
            del things[rewrite-1]
        f = open('C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/ch06-4 textfile.txt', 'w')
        for i in range(len(things)):
            f.write(things[i])
        f.close()
    else:
        print("파일이 존재하지 않거나 내용이 없습니다. -w 대신 -a사용을 추천 드립니다.")
else:
    print("undefined variable")