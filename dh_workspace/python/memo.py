#memo.py

#필요한 기능은? 메모 추가하기, 메모 조회하기
#입력받는 값은? 메모 내용, 프로그램 실행 옵션
#출력하는 값은? memo.txt
#가장 먼저 해야 할 일은 메모를 추가하는 것이다. 다음 명령을 실행했을 때 메모를 추가할 수 있도록 만들어 보자.

#python memo.py -a "Life is too short"          : -a일 때는 적는다.
#python memo.py -v                              : -v일 때는 읽는다.

import sys

option=sys.argv[1]

if option=='-a':
    memo=sys.argv[2]
    f=open('mytxt','a')
    f.write(memo)
    f.write('\n')
    f.close()

elif option=='-v':
    f=open('mytxt','r')
    memo=f.read()
    f.close()
    print(memo)