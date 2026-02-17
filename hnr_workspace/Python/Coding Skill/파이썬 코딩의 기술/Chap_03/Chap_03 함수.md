# Chap_03 함수

## 19. 함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹 하지 말라

```python
def get_stats(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    return minimum, maximum
# 함수의 정의 
# return minimum, maximum 부분을 보면 값이 쉼표로 연결되어 있다. 파이썬은 이를 자동으로 (minimum, maximum)이라는 하나의 튜플로 묶어서 반환

lengths = [63, 73, 72, 60, 67, 66, 71, 61, 72, 70]

minimum, maximum = get_stats(lengths)  
# 왼쪽에 변수 이름을 minimum, maximum 순서대로 적어주면, 
# 파이썬이 패키지 풀어서 첫 번째 값은 첫 번째 변수에, 두 번째 값은 두 번째 변수에 순서대로 집어넣어 이를 언패킹이라고 한다.

print(f'최소: {minimum}, 최대: {maximum}')
```

- 악어 개체의 몸 길이가 전체 개체군의 몸 길이 평균에 비해 얼마나 큰지 계산하는 함수 작성

```python
def get_avg_ratio(numbers):
		# 1. 평균 계산
    average = sum(numbers) / len(numbers)
    # 2. 리스트 컴프리헨션: 각 원소가 평균 대비 몇 %인지 계산 (Scaling)
    scaled = [x / average for x in numbers]
    # 3. 내림차순(큰 수에서 작은 수 순서) 정렬
    scaled.sort(reverse=True)
    return scaled

longest, * middle, shortest = get_avg_ratio(lengths)

print(f"최대 길이:  {longest:>4.0%}") # 최대 길이:  130%
print(f"최소 길이:  {shortest:>4.0%}") # 최소 길이:   50%
```

## 21. **변수 영역과 클로저의 상호 작용 방식을 이해하라.**

- 클로저와 도우미 함수
    - 함수가 정의된 영역 밖의 변수(Free variable)를 기억하고 있다가, 함수가 호출될 때 그 변수에 접근하는 기술
    - `helper` 함수에 `group`이라는 데이터를 매번 인자로 전달하지 않아도, `helper`는 자기가 태어난 곳 주변에 있던 `group`을 기억
    
    ```python
    def sort_priority(values, group):
        def helper(x):
            # x는 helper의 인자지만, group은 helper 밖의 변수
            # 파이썬은 이 group을 helper가 나중에 쓸 수 있게 보관
            if x in group:
                return (0, x)
            return (1, x)
        values.sort(key=helper)
    ```
    
- 일급 시민으로서의 함수
    - 함수를 정수나 문자열처럼 취급할 수 있다는 뜻
    - 변수에 담거나, 다른 함수의 인자로 넘길 수 있다.
    
    ```python
    def my_helper(x):
        return x % 2
    
    # 1. 변수에 대입 가능
    func = my_helper 
    
    # 2. 다른 함수의 인자로 전달 가능 (일급 시민이기 때문에)
    numbers = [1, 2, 3, 4]
    numbers.sort(key=func) 
    
    # 3. 리스트나 딕셔너리에 담기 가능
    functions = [my_helper, len, str]
    ```
    
    ```python
    def my_helper(x):
        return x % 2  # 나머지가 0이면 짝수(우선순위 높음), 1이면 홀수(우선순위 낮음)
    
    # 1. 변수에 함수 대입하기
    # 함수 이름 뒤에 괄호()를 붙이지 않으면 함수 '그 자체'가 변수에 담긴다.
    func = my_helper 
    print(f"1. 변수에 담긴 함수 확인: {func}")
    print(f"   직접 호출 결과(3 % 2): {func(3)}\n")
    
    # 2. 다른 함수의 인자로 함수 전달하기
    numbers = [1, 2, 3, 4]
    
    # key에 함수를 넘겨주면, sort는 내부적으로 'func(숫자)'를 실행해 정렬
    numbers.sort(key=func) 
    print(f"2. 함수를 인자로 써서 정렬한 결과: {numbers}")
    print("   (나머지가 0인 2, 4가 앞으로, 1인 1, 3이 뒤로 정렬됨)\n")
    
    # 3. 리스트에 여러 함수 담아보기
    functions = [my_helper, len, str]
    print(f"3. 리스트에 담긴 함수들: {functions}")
    
    # 리스트에서 함수를 꺼내서 바로 써볼 수 있음
    test_val = "Hanyang"
    length_func = functions[1] # len 함수를 꺼냄
    print(f"   리스트에서 len을 꺼내 실행: '{test_val}'의 길이는 {length_func(test_val)}")
    ```
    
    ```python
    1. 변수에 담긴 함수 확인: <function my_helper at 0x000001D88BA8ED40>
       직접 호출 결과(3 % 2): 1
    
    2. 함수를 인자로 써서 정렬한 결과: [2, 4, 1, 3]
       (나머지가 0인 2, 4가 앞으로, 1인 1, 3이 뒤로 정렬됨)
    
    3. 리스트에 담긴 함수들: [<function my_helper at 0x000001D88BA8ED40>, <built-in function len>, <class 'str'>]
       리스트에서 len을 꺼내 실행: 'Hanyang'의 길이는 7
    ```
    
- 시퀀스(Tuple) 비교 규칙
    
    ```python
    # 파이썬 내부의 판단
    print((0, 5) < (1, 2))  # True (0이 1보다 작으므로 뒤는 보지도 않음)
    print((0, 3) < (0, 7))  # True (0은 같으므로 두 번째 값 3과 7을 비교)
    ```
    
    - `helper`가 `(0, x)`를 반환하면 "0번 그룹(우선순위 높음)"이 되고, `(1, x)`를 반환하면 "1번 그룹(우선순위 낮음)"이 된다.
    - 파이썬의 `sort`는 이 튜플의 앞자리 숫자(0 또는 1)를 먼저 보고 그룹을 크게 나눈 뒤, 그 안에서 실제 숫자 `x`를 보고 줄을 세우게 된다.
- 파이썬의 변수 참조 순서 (LEGB 규칙)
    1. **L (Local):** 현재 내 함수 안에 있는가?
    2. **E (Enclosing):** 나를 감싸고 있는 바깥 함수 안에 있는가? 
    3. **G (Global):** 이 파일(모듈) 전체에서 공통으로 쓰는 변수인가?
    4. **B (Built-in):** 파이썬에 기본적으로 내장된 것인가? (`len`, `print` 등)
    
    ```python
    # [B] Built-in: 파이썬이 원래 알고 있는 것 (예: len, print)
    # [G] Global: 이 파일(모듈) 어디서든 보이는 거실
    x = "Global (거실)"
    
    def outer_function():
        # [E] Enclosing: 나를 감싸고 있는 엄마 방
        x = "Enclosing (엄마 방)"
        
        def inner_function():
            # [L] Local: 지금 내가 있는 내 방
            x = "Local (내 방)"
            print(f"현재 출력되는 x는? {x}")
            
        inner_function()
    
    outer_function()
    ```
    

## 22. 변수 위치 인자를 사용해 시각적인 잡음을 줄여라

- 가변 인자가 없을 때의 불편함

```python
def log(message, values):
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('내 숫자는 ', [1, 2]) # 리스트로 감싸서 보내야 함
log('안녕 ', [])         # 보낼 게 없어도 빈 리스트([])를 써야 함
```

```python
내 숫자는 : 1, 2
안녕
```

- `*args` (가변 인자)의 등장
    - 인자 이름 앞에 `*`를 붙이면, 파이썬은 그 뒤에 오는 모든 인자를 하나의 튜플(tuple)로 묶어서 `values`에 담아준다.

```python
def log(message, *values): 
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{message}: {values_str}')

log('내 숫자는 ', 1, 2)    # 리스트 기호([])가 사라짐
log('안녕')               # 빈 리스트를 넘길 필요가 없음

내 숫자는 : 1, 2
안녕
```

- 기존 리스트를 '풀어서' 전달하기
    - 이미 리스트(`favorites`)가 있을 때는 리스트 앞에 * 를 붙여서 호출
    - 리스트 통째로 주지 말고, 리스트 안에 있는 알맹이들을 낱개로 풀어서(Unpacking) 전달. 결과적으로 `log('...', 7, 33, 99)`와 동일함

```python
favorites = [7, 33, 99]
log('좋아하는 숫자는', *favorites)
```

```python
좋아하는 숫자는: 7, 33, 99
```

- 제네레이터와 메모리 주의사항
    - 제네레이터(데이터를 하나씩 생성하는 도구)를 로 풀어서 `args`에 넘긴다.
    - 위험성 : `args`는 들어오는 모든 데이터를 일단 튜플로 한꺼번에 메모리에 저장한다.
        - 만약 제네레이터가 10개가 아니라 1,000만 개의 데이터를 뱉는다면? 컴퓨터 메모리가 부족해서 프로그램이 터질 수 있다. `args`는 인자 개수가 적당할 때만 써야 한다.

```python
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
# packing -> 함수를 정의하는 경우
    print(args)

it = my_generator()
my_func(*it)
# unpacking -> 함수를 호출하는 경우
```

- packing 과 unpacking 이 동시에 발생

```python
it = [0, 1, 2] # 묶여 있는 상태

# 1단계: *it (언패킹 - 짐 풀기)
# 이 순간 [0, 1, 2]가 0, 1, 2 로 낱개가 되어 함수로 던져진다.
my_func(*it) 

# 2단계: def my_func(*args): (패킹 - 다시 짐 싸기)
# 함수 입구에서 *args가 낱개로 들어오는 0, 1, 2를 
# 다시 하나의 튜플 (0, 1, 2)로 묶어서 args 변수에 담는다.
```

- 가변 인자(`*values`)를 사용하는 함수의 인자 목록 앞에 새로운 인자를 추가하면, 기존 코드가 망가진다.

```python
def log(sequence, message, *values):
    if not values:
        print(f'{sequence} - {message}')
    else:
        values_str = ', '.join(str(x) for x in values)
        print(f'{sequence} - {message}: {values_str}')

log(1, '좋아하는 숫자는', 7, 33)   # 새 코드에서 가변 인자를 사용. 문제 없음
log(1, '안녕')                   # 새 코드에서 가변 인자 없이 메시지만 사용. 문제 없음
log('좋아하는 숫자는', 7, 33)      # 예전 방식 코드는 깨짐
```

## **23. 키워드 인자로 선택적인 기능을 제공하라.**

```python
def remainder(number, divisor):
    return number % divisor

assert remainder(20, 7) == 6
```

- 위치 인자(Positional Arguments)
    - 첫 번째 값 `20`은 첫 번째 자리(`number`)로, 두 번째 값 `7`은 두 번째 자리(`divisor`)로 들어간다.
    - 가장 단순하지만, 인자가 많아지면 "어떤 숫자가 무슨 의미인지" 알기 어렵다.

```python
remainder(20, 7)
```

- 키워드 인자(Keyword Arguments)
    - `이름=값` 형태로 명시
    - 파이썬이 이름을 보고 칸을 찾아가기 때문에 순서를 바꿔도 결과가 같다.

```python
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)
```

- 위치 인자와 키워드 인자의 혼합
    - 앞부분은 순서대로 채우고, 뒷부분은 이름표를 붙여서 채운다.
    - 흔하게 쓰이는 방식이지만, 여기서부터 **규칙**이 중요하다.

```python
remainder(20, divisor=7)
```

- 오류가 나는 이유
    - 오류상황 1
    
    ```python
    remainder(number=20, 7)
    ```
    
    → 위치인자는 반드시 키원드 인자보다 앞에 와야한다.
    
    - 오류상황2
    
    ```python
    remainder(20, number=7)
    ```
    
    → 첫번째 칸 `number`를 이미 20으로 채워버림. 그런데 뒤에서 `number=7` 이라고 하면 에러가남.
    

- 딕셔너리 통째로 넘기기 (`**my_kwargs`)
    - `**my_kwargs`라고 쓰는 순간, 파이썬은 딕셔너리를 해체해서 `remainder(number=20, divisor=7)`로 바꿔서 실행
    - 함수에 넘길 인자가 10개, 20개로 많아질 때 호출 코드가 깔끔해진다.

```python
my_kwargs = {
    'number': 20,
    'divisor': 7,
}
assert remainder(**my_kwargs) == 6
```

- 일반 인자와 딕셔너리 섞기

```python
my_kwargs = {
    'divisor': 7,
}
assert remainder(number=20, **my_kwargs) == 6
```

- 여러 개의 딕셔너리 합쳐서 넘기기

```python
my_kwargs = {'number': 20}
other_kwargs = {'divisor': 7}

assert remainder(**my_kwargs, **other_kwargs) == 6
```

- 만능 키워드 인자 주머니(`**kwargs`)
    - 앞서 배운 `**`가 호출할 때 '보따리를 푸는' 역할이었다면, 함수 정의(`def`)에 붙은 `**`는 '보따리에 담는' 역할을 한다. (아이템 22에서 배운 `*args`가 튜플로 묶어주듯, 이건 딕셔너리로 묶어준다.)
    - `alpha=1.5`라고 던지면, 파이썬은 "함수 정의에 딱 맞는 이름이 없네? 그럼 `kwargs`라는 딕셔너리 주머니에 넣어야겠다 라고 판단
    - 함수 안에서 `kwargs`는 `{'alpha': 1.5, 'beta': 9, '감마': 4}`라는 딕셔너리가 된다.
    - 함수를 만들 때 미리 인자 이름을 정해둘 필요가 없다. 어떤 이름의 설정값이 들어오든 `kwargs.items()`를 통해 하나씩 꺼내 쓸 수 있다.

```python
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, 감마=4)
```

- 유량을 계산하는 함수가 밑에와 같이 존재한다고 하자

```python
def flow_rate(weight_diff, time_diff):
    return weight_diff / time_diff

weight_diff = 0.5
time_diff = 3
flow = flow_rate(weight_diff, time_diff)
print(f'{flow:.3} kg/s')
```

- `Period` 라는 인자의 추가
    - 기존에 `flow_rate(0.5, 3)`이라고 썼던 수만 개의 코드가 전부 에러
    - 가독성의 저하

```python
def flow_rate(weight_diff, time_diff, period):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff, 1)
```

- `period=1` : Default Value
    - 누군가 `period` 값을 주면 그 값을 쓰고, 아무것도 안 주면 그냥 `1`이라고 판단
    - `period`는 필수가 아닌 선택 사항

```python
def flow_rate(weight_diff, time_diff, period=1):
    return (weight_diff / time_diff) * period

flow_per_second = flow_rate(weight_diff, time_diff)
flow_per_hour = flow_rate(weight_diff, time_diff, period=3600)
```

- `period=1`,  `units_per_kg=1` : Default Value 추가

```python
def flow_rate(weight_diff, time_diff,
              period=1, units_per_kg=1):
    return ((weight_diff * units_per_kg) / time_diff) * period

pounds_per_hour = flow_rate(weight_diff, time_diff,
                            period=3600, units_per_kg=2.2)

pounds_per_hour = flow_rate(weight_diff, time_diff, 3600, 2.2)
```

## **24. None과 독스트링을 사용해 동적인 디폴트 인자를 지정하라**

- 파이썬 함수의 Definition time
    - 통념 : `log()`  를 실행할 때마다 `datetime.now()` 가 작동해서 현재 시각을 내놓을 것 같음
    - BUT : `def log()` 를 만나는 그 순간(함수를 정의할 때) 딱 한번 `datetime.now()`를 계산해서 그 값을 `when`이라는 서랍에 넣어둔다.
- 코드 흐름 추적
    - 함수 정의 단계: 파이썬이 `def log`를 읽는다. 이때 `datetime.now()`가 호출되어 예를 들어 `14:51:17.658683`이라는 값이 나온다. 이 값은 `log` 함수의 디폴트 값으로 고정된다.
    - 첫 번째 호출 `log('안녕!')`: `when` 인자를 안 줬으니, 아까 고정된 `14:51:17.658683`을 사용
    - `sleep(0.1)`: 프로그램이 0.1초 쉰다. 실제 시간은 `14:51:17.758683`이 되었을 것이다.
    - 두 번째 호출 `log('다시 안녕!')`: 여전히 `when` 인자를 주지 않았다. 그렇기 때문에 파이썬은 다시 아까 고정해둔 `14:51:17.658683` 를 꺼내서 쓴다.
- 왜 그런가?
    - 파이썬 입장에서는 함수를 부를 때마다 디폴트 값을 새로 계산하는 것보다, 처음에 딱 한 번 계산해서 저장해두는 게 성능상 더 유리하다.
    - 하지만 `datetime.now()`처럼 “부르는 순간마다 값이 변해야 하는 것"을 디폴트 인자로 쓰면 오류가 나온다.

```python
from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('안녕!')
sleep(0.1)
log('다시 안녕!')
```

```python
2026-02-12 14:52:17.658683: 안녕!
2026-02-12 14:52:17.658683: 다시 안녕!
```

- `when = None` 을 통한 해결

```python
def log(message, when=None):
    """메시지와 타임스탬프를 로그에 남긴다.

    Args:
        message: 출력할 메시지.
        when: 메시지가 발생한 시각(datetime).
            디폴트 값은 현재 시간이다.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')

log('안녕!')
sleep(0.1)
log('다시 안녕!')
```

```python
2026-02-12 15:20:11.098062: 안녕!
2026-02-12 15:20:11.198711: 다시 안녕!
```

- `default={}`: 여기서 빈 딕셔너리(`{}`)는 함수가 정의되는 시점에 딱 한 번만 생성된다.
- 파이썬은 이 딕셔너리를 `decode` 함수 전용 보관함에 넣어두고, 호출될 때마다 이 '동일한' 딕셔너리를 재사용한다.

```python
def decode(data, default={}): 
    try:
        return json.loads(data)
    except ValueError:
        return default
```

- `foo`는 이제 그 '하나뿐인 기본 딕셔너리'를 가리키게 되고, 거기에 `stuff: 5`라는 값을 적는다.

```python
foo = decode('잘못된 데이터')  # JSON 파싱 실패 -> default({}) 반환
foo['stuff'] = 5             # 반환받은 default 딕셔너리에 데이터 추가
```

- `bar`가 받은 `default`는 아까 `foo`가 값을 넣었던 그 딕셔너리이다.
- 이미 `stuff: 5`가 들어있는 상태에서 `meep: 1`이 추가된다.

```python
bar = decode('또 잘못된 데이터') # JSON 파싱 실패 -> default 반환
bar['meep'] = 1                # 반환받은 default 딕셔너리에 데이터 추가
```

- 결과 확인

```python
print('Foo:', foo) # Foo: {'stuff': 5, 'meep': 1}
print('Bar:', bar) # Bar: {'stuff': 5, 'meep': 1}
assert foo is bar  # True : 둘은 이름만 다를 뿐 '같은 물건'
```

→ 디폴트 인자는 "공유"된다

- 파이썬에서 함수의 기본값(Default Argument)은 함수가 호출될 때 새로 만들어지는 것이 아니라, 함수가 정의될 때 딱 한 번 만들어진다.
- 특히 리스트(`[]`)나 딕셔너리(`{}`)처럼 내용물을 바꿀 수 있는 객체를 기본값으로 쓰면, 모든 함수 호출이 그 객체를 공유하게 되어 의도치 않은 데이터 오염이 발생한다.
하
- 함수가 실행될 때마다 새 딕셔너리를 생성하라

```python
def decode(data, default=None):
    """문자열에로부터 JSON 데이터를 읽어온다

    Args:
        data: 디코딩할 JSON 데이터.
        default: 디코딩 실패시 반환할 값이다.
            디폴트 값은 빈 딕셔너리다.
    """
    try:
        return json.loads(data)
    except ValueError:
        if default is None:
            default = {}
        return default

foo = decode('잘못된 데이터')
foo['stuff'] = 5
bar = decode('또 잘못된 데이터')
bar['meep'] = 1
print('Foo:', foo)
print('Bar:', bar)
assert foo is not bar
```

```python
def decode(data, default=None):
```

- `{}` 대신 `None`
- 이제 함수의 비밀 금고(`__defaults__`)에는 '아무것도 없음'이라는 정보만 박제
- `None`은 불변(Immutable) 객체라 아무리 여러 번 호출해도 오염될 걱정 X

```python
except ValueError:
    if default is None:
        default = {}  # <- 함수가 실행될 때 새로 만듦
    return default
```

- JSON 해석에 실패했을 때만 이 코드가 돌아간다.
- 여기서 `default = {}`는 함수가 호출될 때(실행될 때) 실행된다. 즉, `decode`를 부를 때마다 매번 완전히 새로운 빈 딕셔너리가 메모리에 만들어진다.

```python
Foo: {'stuff': 5}
Bar: {'meep': 1}
```

- `foo = decode('에러1')`
    - `default`가 `None`이므로 새로운 딕셔너리 **A**가 생성되어 `foo`에 전달
    - `foo['stuff'] = 5`는 딕셔너리 **A**만 수정
- `bar = decode('에러2')`
    - 다시 함수가 실행. `default`는 또 `None`으로 시작
    - 이번엔 새로운 딕셔너리 **B**가 생성되어 `bar`에 전달
- 결과:
    - `foo`는 `{'stuff': 5}`, `bar`는 `{'meep': 1}`을 각각 가진다.
    - `assert foo is not bar`: 둘은 서로 다른 메모리 주소를 가진 별개의 물체이므로 이 조건은 True(참)가 된다.

```python
from typing import Optional

def log_typed(message: str,
              when: Optional[datetime]=None) -> None:
    """메시지와 타임스탬프를 로그에 남긴다.

    Args:
        message: 출력할 메시지.
        when: 메시지가 발생한 시각(datetime).
            디폴트 값은 현재 시간이다.
    """
    if when is None:
        when = datetime.now()
    print(f'{when}: {message}')
```

- `message: str`: "`message` 자리에는 글자(String)만 넣기
- `-> None` : 반환 값이 없음
- `when: Optional[datetime] = None` :
    - `datetime`: "시간 데이터가 들어올 거야."
    - `Optional[...]`: "그런데 이 데이터는 있을 수도 있고, 없을 수도 있어."
    - `= None`: "만약 사용자가 아무것도 안 주면, 일단 `None`(비어있음)이라고 생각할게."

## **25. 위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 해서 함수 호출을 명확하게 만들라.**

```python
def safe_division(number, divisor,
                  ignore_overflow,
                  ignore_zero_division):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

#
result = safe_division(1.0, 10**500, True, False)
print(result)

result = safe_division(1.0, 0, False, True)
print(result)
```

```python
0
inf
```

- 함수의 목적 : “안전하게 나누기”

보통 숫자를 `0`으로 나누면 프로그램이 에러(`ZeroDivisionError`)를 내며 멈춘다.

이 함수는 그런 예외 상황을 '무시'하고 특정 값을 돌려줄지 선택할 수 있게 설계되었다.

- `number / divisor`: 기본적인 나눗셈
- `OverflowError` 처리: 숫자가 너무 커서 계산이 안 될 때, `ignore_overflow`가 `True`라면 에러 대신 `0`을 return
- `ZeroDivisionError` 처리: `0`으로 나눌 때, `ignore_zero_division`이 `True`라면 에러 대신 무한대(`inf`)를 return
- 가독성의 문제점
    
    ```python
    result = safe_division(1.0, 0, False, True)
    ```
    
    - 위의 코드를 보았을때, 각각이 뭘 의미하는지 통 알 수 없음
    
    → 인자의 순서에만 의존해서 값을 넣는 방식을 위치 인자(Positional Arguments) 라고 하는데, 인자가 2개인 경우에는 괜찮지만, 지금처럼 4개가 넘어가면 짜는 사람과 읽는 사람 모두 헷갈릴 수 있음
    

```python
def safe_division_b(number, divisor,
                    ignore_overflow=False,       # 변경
                    ignore_zero_division=False): # 변경
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division_b(1.0, 10**500, ignore_overflow=True)
print(result)

result = safe_division_b(1.0, 0, ignore_zero_division=True)
print(result)

assert safe_division_b(1.0, 10**500, True, False) == 0
```

- 기본값(`=False`)의 도입
    - 아무것도 안적으면 기본값 `False` 임
    - 함수 호출할 때 `ignore_overflow=True`라고 적을 수 있음
    - 다음처럼 가독성을 높일 수 있음

```python
# (1) 오버플로 무시 옵션만 켜고 싶을 때
result = safe_division_b(1.0, 10**500, ignore_overflow=True)

# (2) 0으로 나누기 무시 옵션만 켜고 싶을 때
result = safe_division_b(1.0, 0, ignore_zero_division=True)
```

```python
def safe_division_c(number, divisor, *,         # 변경
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
safe_division_c(1.0, 10**500, True, False)

result = safe_division_c(1.0, 0, ignore_zero_division=True)
assert result == float('inf')

try:
    result = safe_division_c(1.0, 0)
except ZeroDivisionError:
    pass # 예상대로 작동함

assert safe_division_c(number=2, divisor=5) == 0.4
assert safe_division_c(divisor=5, number=2) == 0.4
assert safe_division_c(2, divisor=5) == 0.4
```

- `*` 기호 (Keyword-Only Arguments)
    - 별표 기준 오른쪽인자들은 이제 `True, False`라고 순서대로 적으면 에러가 난다. 반드시 `ignore_overflow=True`처럼 이름 (키워드)를 명시해야한다.
    - `number`와 `divisor`는 별표 왼쪽에 있으므로, 위치로 넣든(`2, 5`) 이름을 부르든(`number=2, divisor=5`) 자유롭게 쓸 수 있다. 이름을 부르면 순서를 바꿔서 호출해도 파이썬이 알아서 짝을 맞춰준다.

```python
def safe_division_c(numerator, denominator, *,    # 변경
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
safe_division_c(number=2, divisor=5)
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[31], line 18
     15             raise
     17 # 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
---> 18 safe_division_c(number=2, divisor=5)

TypeError: safe_division_c() got an unexpected keyword argument 'number'
```

- `이름=값` (키워드 인자) 형태를 쓰지 못하게 막으라
- 특히 `number`나 `divisor`처럼 굳이 이름을 안 써도 순서만으로 충분히 의미가 전달되는 핵심 인자들은, 차라리 "이름으로 부르지 못하게" 막는 것이 좋음

```python
def safe_division_d(numerator, denominator, /, *, # 변경
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        return numerator / denominator
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

assert safe_division_d(2, 5) == 0.4

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#safe_division_d(numerator=2, denominator=5)
```

```python
def safe_division_d(numerator, denominator, /, *, ...)
```

- `numerator`와 `denominator`는 이제 위치 전용 인자(Positional-only arguments)가 된다.
- 성공**:** `safe_division_d(2, 5)`
    - 사용자가 이름 없이 숫자 `2`와 `5`만 순서대로 넣었다.

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[1], line 20
     17 assert safe_division_d(2, 5) == 0.4
     19 # 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
---> 20 safe_division_d(numerator=2, denominator=5)

TypeError: safe_division_d() got some positional-only arguments passed as keyword arguments: 'numerator, denominator'
```

- 실패: `safe_division_d(numerator=2, denominator=5)`
    - / 기호의 왼쪽 인자들은 이름을 붙이면 안된다.

```python
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                 # 변경
                    ignore_overflow=False,
                    ignore_zero_division=False):
    try:
        fraction = numerator / denominator         # 변경
        return round(fraction, ndigits)            # 변경
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise

result = safe_division_e(22, 7)
print(result)

result = safe_division_e(22, 7, 5)
print(result)

result = safe_division_e(22, 7, ndigits=2)
print(result)
```

```python
def safe_division_e(numerator, denominator, /, ndigits=10, *, ignore_overflow=False, ...)
```

- Zone 1: 위치 전용 (`/` 왼쪽) - `numerator`, `denominator`
    - 무조건 순서대로 (이름 사용 불가)
- Zone 2: 하이브리드 (`/`와  `*`사이) - `ndigits`
    - 위치로 넣어도 되고, 이름을 불러서 넣어도 된다.
- Zone 3: 키워드 전용 ( `*`오른쪽) - `ignore_...`
    - 무조건 이름을 명시해서 넣어야 한다.
- `safe_division_e(22, 7)`
    - `ndigits` X. 기본값인 `10`이 적용되어 소수점 10자리까지 나옴.
- `safe_division_e(22, 7, 5)`
    - 세 번째 자리에 `5`를 넣었다. 위치 인자로 인식되어 소수점 5자리까지 반올림.
- `safe_division_e(22, 7, ndigits=2)`
    - 이름을 불러서 키워드 인자로 넣었음. 소수점 2자리까지 나온다.

## **26. functools.wrap을 사용해 함수 데코레이터를 정의하라**
