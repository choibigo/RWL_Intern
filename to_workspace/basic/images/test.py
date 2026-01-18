# test.py
import sys

try:
    from calc import add
    r = (add(10, 20) == 30)
except Exception:
    print("Failed!")
    sys.exit(1) # 오류로 1반환

else:
    if r: 
        print("Success!")
        sys.exit(0) # 만약 True가 들어왔다면 성공으로 0반환
    else:
        print("Failed!")
        sys.exit(1)