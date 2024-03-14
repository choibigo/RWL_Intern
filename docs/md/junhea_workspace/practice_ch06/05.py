# ch06-6 하위 디렉터리 검색하기

# 특정 디렉터리부터 시작해서 그 하위의 모든 파일 중 파이썬 파일만 출력해 주는 프로그램이다.

import os

for (path, dir, files) in os.walk("C:/"):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.py':
            print(f'{path}/{filename}')