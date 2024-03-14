import sys

a = sys.argv[1:]
yes = 0
for i in a:
    yes += int(i)
print(yes)
## cmd에서 cd\ 를 입력한 뒤 cd (파일 경로) 를 입력하고 python (파일이름).py 1 2 3 4 5 6 7 8 9 10 을 입력하면 55가 출력된다.