# ch06-5 탭 문자를 공백 문자 4개로 바꾸기

# 터미널에 python (이 프로그램 이름) (대상 파일) (변조 후 저장할 파일) 을 입력했을 때 작업이 되도록 할 것이다.

import sys

if len(sys.argv) != 3:
    print("undefined variable")
else:
    fir = 'C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/' + sys.argv[1]
    sec = 'C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch06/' + sys.argv[2]
    f = open(fir, 'r')
    linee = f.read()
    f.close()
    relinee = linee.replace('\t', '    ')
    f = open(sec, 'w')
    f.write(relinee)
    f.close()