multiline='''
Life is too short
You need python
'''

print(multiline)

print(f"안녕, 지금은 정렬 연습 중이야 {"hi":>10}")
print(f"안녕, 지금은 정렬 연습 중이야 {"hi":*^20}")


a = "Life is too short"
print(a.replace("Life", "Your leg"))
print(a)

a = []


a = list()
print(a)

a = [1, 2]
result = a.append(3)
print(result) # None (돌려준 게 없음)
print(a)      # [1, 2, 3] (원본이 변함)


import time

def myfunc():
    start = time.time()
    print("함수가 실행됩니다.")
    end = time.time()
    print("함수 수행시간: %f 초" % (end-start))

myfunc()


# decorator.py
import time

def elapsed(original_func):   # 기존 함수를 인수로 받는다.
    def wrapper():
        start = time.time()
        result = original_func()    # 기존 함수를 수행한다.
        end = time.time()
        print("함수 수행시간: %f 초" % (end - start))  # 기존 함수의 수행시간을 출력한다.
        return result  # 기존 함수의 수행 결과를 반환한다.
    return wrapper

def myfunc():
    print("함수가 실행됩니다.")

decorated_myfunc = elapsed(myfunc)
decorated_myfunc()


# decorator.py
import time

def elapsed(original_func):   # 기존 함수를 인수로 받는다.
    def wrapper():
        start = time.time()
        result = original_func()    # 기존 함수를 수행한다.
        end = time.time()
        print("함수 수행시간: %f 초" % (end - start))  # 기존 함수의 수행시간을 출력한다.
        return result  # 기존 함수의 수행 결과를 반환한다.
    return wrapper

@elapsed
def myfunc():
    print("함수가 실행됩니다.")

# decorated_myfunc = elapsed(myfunc)  # @elapsed 데코레이터로 인해 더이상 필요하지 않다.
# decorated_myfunc()

myfunc()


# decorator2.py
import time

def elapsed(original_func):   # 기존 함수를 인수로 받는다.
    def wrapper(*args, **kwargs):   # *args, **kwargs 매개변수 추가
        start = time.time()
        result = original_func(*args, **kwargs)  # 전달받은 *args, **kwargs를 입력파라미터로 기존함수 수행
        end = time.time()
        print("함수 수행시간: %f 초" % (end - start))  # 수행시간을 출력한다.
        return result  # 함수의 결과를 반환한다.
    return wrapper

@elapsed
def myfunc(msg):
    """ 데코레이터 확인 함수 """
    print("'%s'을 출력합니다." % msg)

@elapsed
def add(a,b):
    print(a+b)

myfunc("You need python")
add(1,2)


a = [1, 2, 3]
ia = iter(a)
print(ia)


# generator2.py
import time

def longtime_job():
    print("job start")
    time.sleep(0.1)  # 1초 지연 - 실제로는 데이터베이스 조회, 파일 처리 등을 시뮬레이션
    return "done"

# 리스트 컴프리헨션: 5번의 작업을 모두 실행해서 리스트로 만든다
list_job = [longtime_job() for i in range(5)]
print(list_job[0])  # 첫 번째 결과만 필요한 상황
print(list_job)

# generator2.py
import time

def longtime_job():
    print("job start")
    time.sleep(1)
    return "done"

# 제너레이터 표현식: 함수를 미리 실행하지 않고 필요할 때만 실행
list_job = (longtime_job() for i in range(5))
print(next(list_job))  # 첫 번째 값만 요청
print(list_job)


def add(a,b):
    return a + b


add(1, 2)

def add(a: int, b: float) -> int: 
    return a + b


print(add(1, 1.2))


def greet(name: str) -> str:
    return f"안녕하세요, {name}님!"

def get_user_info(user_id: int) -> dict:
    return {"id": user_id, "name": "홍길동"}


add()
