# Chap_02 리스트와 딕셔너리

## 11. 시퀀스를 슬라이싱 하는 방법을 익혀라

### 기억해야 할 내용

1. 슬라이싱할 때는 간결하게 하라. 시작 인덱스에 0을 넣거나, 끝 인덱스에 시퀀스 길이를 넣지 말라
2. 슬라이싱은 범위를 넘어가는 시작 인덱스나 끝 인덱스도 허용한다. 따라서 시퀀스의 시작이나 끝에서 길이를 제한하는 슬라이스를 쉽게 표현할 수 있다.
3. 리스트 슬라이스에 대입하면 원래 시퀀스에서 슬라이스가 가리키는 부분을 대입 연산자 오른쪽에 있는 시퀀스로 대치한다. 슬라이스와 대치되는 시퀀스의 길이가 달라도 된다.

```python
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
print('가운데 2개: ', a[3:5])
print('마지막을 제외한 나머지:', a[1:7])
assert a[:5] == a[0:5]
assert a[5:] == a[5:len(a)]
a[:]     # ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
a[:5]    # ['a', 'b', 'c', 'd', 'e']
a[:-1]   # ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a[4:]    # ['e', 'f', 'g', 'h']
a[-3:]   # ['f', 'g', 'h']
a[2:5]   # ['c', 'd', 'e']
a[2:-1]  # ['c', 'd', 'e', 'f', 'g']
a[-3:-1] # ['f', 'g']
```

- 리스트를 슬라이싱한 결과는 완전히 새로운 리스트이다.

```python
a = list(range(10))
b = a
```

## **12. 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라**

### 기억해야 할 내용

1. 슬라이스에 시작, 끝, 증가값을 함께 지정하면 코드의 의미를 혼동하기 쉽다
2. 시작이나 끝 인덱스가 없는 슬라이스를 만들 때는 양수 증가값을 사용하라. 가급적 음수 증가값을 피하라
3. 한 슬라이스 안에서 시작, 끝, 증가값을 함께 사용하지 말라. 새 파라미터를 모두 써야 하는 경우, 두 번 대입을 사용(한 번은 스트라이딩, 한 번은 슬라이싱)하거나 itertools 내장 모듈의 islice 를 사용하라

### 1. 슬라이스에 시작, 끝, 증가값을 함께 지정하면 코드의 의미를 혼동하기 쉽다

- 슬라이싱의 기본 문법은 x[start:end:stride] 이다.
- 보기 어려운 코드의 예시
    - 리스트 x 에서 특정 범위를 건너뛰며 가져오고 싶을때

```python
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# "뒤에서 두 번째('g')부터 시작해서 인덱스 2('c') 직전까지 역순으로 2칸씩"
result = x[-2:2:-2] 
print(result) # ['g', 'e']
```

- 가독성을 높인 코드 → 두번 대입

```python
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# 1단계: 먼저 원하는 간격(stride)으로 거른다 (스트라이딩)
# 짝수 번째 인덱스만 가져오기
odds = x[::2] # ['a', 'c', 'e', 'g']

# 2단계: 그 결과물에서 원하는 범위를 자른다 (슬라이싱)
# 양 끝을 제외하고 중간만 가져오기
result = odds[1:-1] # ['c', 'e']

print(result)
```

### 3. 한 슬라이스 안에서 시작, 끝, 증가값을 함께 사용하지 말라. 새 파라미터를 모두 써야 하는 경우, 두 번 대입을 사용(한 번은 스트라이딩, 한 번은 슬라이싱)하거나 itertools 내장 모듈의 islice 를 사용하라

- 읽기 편한 코드(두 번에 나누기)

```python
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# 1단계: 먼저 2칸 간격으로 뽑아낸다 (의도: 짝수 번째 인덱스만 추출)
stride_part = x[::2]       # ['a', 'c', 'e', 'g']

# 2단계: 그 결과에서 필요한 범위를 자른다 (의도: 첫 번째 원소 'a' 제외)
final_result = stride_part[1:] # ['c', 'e', 'g']

print(final_result)
```

- `itertools.islice` 사용하기

```python
from itertools import islice

x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

# islice(데이터, 시작, 끝, 증가값)
# 주의: 끝(stop) 인덱스는 포함되지 않는다.
# 인덱스 2부터 7까지, 2칸 간격
iter_result = islice(x, 2, 7, 2)

# 결과 확인을 위해 리스트로 변환
print(list(iter_result)) # ['c', 'e', 'g']
```

## 13. 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라

### 기억해야 할 내용

1. 언패킹 대입에 별표 식을 사용하면 언패킹 패턴에서 대입되지 않는 모든 부분을 리스트에 잡아낼 수 있다.
2. 별표 식은 언패킹 패턴의 어떤 위치에든 놓을 수 있다. 별표 식에 대입된 결과는 항상 리스트가 되며, 이 리스트에는 별표 식이 받은 값이 0개 또는 그 이상 들어간다
3. 리스트를 겹치지 않게 여러 조각으로 나눌 경우, 슬라이싱과 인덱싱을 사용하기보다는 나머지를 모두 잡아내는 언패킹을 사용해야 실수할 여지가 훨씬 줄어든다.

### 1. 언패킹 대입에 별표 식을 사용하면 언패킹 패턴에서 대입되지 않는 모든 부분을 리스트에 잡아낼 수 있다.

- 앞에서부터 몇 개만 필요할 때

```python
# 내림차순 정렬된 점수 리스트
scores = [100, 95, 80, 70, 60, 50]

# 1등, 2등만 변수에 담고 나머지는 'others'에 담기
first, second, *others = scores

print(f"우승: {first}")   # 100
print(f"준우승: {second}") # 95
print(f"기타 점수: {others}") # [80, 70, 60, 50] (리스트 형태로 저장)
```

- 끝부분이 중요할 때 (별표가 앞에 오는 경우)

```python
# 센서 데이터: [시간, 압력, 온도, 습도, 전압]
sensor_data = [12.5, 0.8, 25.4, 45.0, 5.0]

# 마지막 전압(voltage) 데이터만 따로 빼고 싶을 때
*measurements, voltage = sensor_data

print(f"측정값들: {measurements}") # [12.5, 0.8, 25.4, 45.0]
print(f"현재 전압: {voltage}")     # 5.0
```

### 2. 별표 식은 언패킹 패턴의 어떤 위치에든 놓을 수 있다. 별표 식에 대입된 결과는 항상 리스트가 되며, 이 리스트에는 별표 식이 받은 값이 0개 또는 그 이상 들어간다

- 별표 식은 어디든 놓일 수 있다.
    - 중간에 위치하는 경우

```python
car_ages = [20, 15, 10, 5, 1] # 내림차순 정렬된 차 연식

# 1. 별표가 중간에 있는 경우
oldest, *middle, youngest = car_ages
# 결과: oldest=20, youngest=1, middle=[15, 10, 5]

# 2. 별표가 맨 앞에 있는 경우
*others, second_youngest, youngest = car_ages
# 결과: youngest=1, second_youngest=5, others=[20, 15, 10]
```

- 결과는 항상 리스트가 된다.
    - *로 받아낸 데이터는 원본이 튜플이든, 제너레이터든 상관없이 무조건 list 타입으로 저장된다.

```python
# 튜플을 언패킹할 때
data = (1, 2, 3, 4)
first, *rest = data

print(type(rest)) # <class 'list'>
print(rest)       # [2, 3, 4]
```

- 값이 0개 여도 괜찮다.

```python
short_list = [1, 2]

# 변수는 3개(first, second, *rest)인데 값은 2개뿐
first, second, *rest = short_list

print(f"first: {first}")   # 1
print(f"second: {second}") # 2
print(f"rest: {rest}")     # [] 
```

### 3. 리스트를 겹치지 않게 여러 조각으로 나눌 경우, 슬라이싱과 인덱싱을 사용하기보다는 나머지를 모두 잡아내는 언패킹을 사용해야 실수할 여지가 훨씬 줄어든다.

- 슬라이싱 방식의 위험성
    - 리스트를 [첫 번째, 나머지, 마지막] 세 부분으로 나누고 싶다고 해보자.
    - 슬라이싱을 사용할 경우
    
    ```python
    items = ['robot', 'sensor', 'camera', 'motor', 'battery']
    
    first = items[0]
    last = items[-1]
    middle = items[1:-1] # '1'과 '-1'이라는 인덱스를 직접 계산해서 넣어야 함
    ```
    
- 별표 언패킹 방식의 안전함 → 경계선 자동 설정
    - 언패킹을 사용할 때
    
    ```python
    items = ['robot', 'sensor', 'camera', 'motor', 'battery']
    
    first, *middle, last = items
    
    print(first)  # 'robot'
    print(middle) # ['sensor', 'camera', 'motor']
    print(last)   # 'battery'
    ```
    

## **14. 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라**

### 기억해야 할 내용

- 리스트 타입에 들어 있는 sort 메서드를 사용하면 원소 타입이 문자열, 정수, 튜플 등과 같은 내장 타입인 경우 자연스러운 순서로 정렬할 수 있다.
- 원소 타입에 특별 메서드를 통해 자연스러운 순서가 정의돼 있지 않으면 sort 메서드를 쓸 수 없다. 하지만 원소 타입에 순서 특별 메서드를 정의하는 경우는 드물다.
- sort 메서드의 key 파라미터를 사용하면 리스트의 각 원소 대신 비교에 사용할 객체를 반환하는 도우미 함수를 제공할 수 있다.
- key 함수에서 튜플을 반환하면 여러 정렬 기준을 하나로 엮을 수 있다. 부호 반전 연산자를 사용하면 부호를 바꿀 수 있는 타입이 정렬 기준인 경우 정렬 순서를 반대로 바꿀 수 있다.
- 부호를 바꿀 수 없는 타입의 경우 여러 정렬 기준을 조합하려면 각 정렬 기준마다 reverse 값으로 정렬 순서를 지정하면서 sort 메서드를 여러 번 사용해야 한다. 이때 정렬 기준의 우선순위가 점점 노파지는 순서로 sort를 호출해야한다.

### 1. 리스트 타입에 들어 있는 sort 메서드를 사용하면 원소 타입이 문자열, 정수, 튜플 등과 같은 내장 타입인 경우 자연스러운 순서로 정렬할 수 있다.

- 정수/실수(숫자 타입)
    - 작은 숫자부터 큰 숫자 순서로 정렬

```python
numbers = [10, 1.5, 7, 3.2]
numbers.sort()

print(numbers) # [1.5, 3.2, 7, 10]
```

- 문자열(String)
    - 문자열은 사전식 순서를 따른다.

```python
words = ['cherry', 'apple', 'Banana', 'date']
words.sort()

print(words) # ['Banana', 'apple', 'cherry', 'date']
```

- 튜플
    - 튜플은 첫 번째 원소를 먼저 비교하고, 만약 같은 두 번째 원소를 비교하는 방식으로 작동

```python
# (나이, 이름) 튜플 리스트
people = [(25, '이몽룡'), (20, '성춘향'), (25, '홍길동')]
people.sort()

print(people) 
# [(20, '성춘향'), (25, '이몽룡'), (25, '홍길동')]
```

### 2. 원소 타입에 특별 메서드를 통해 자연스러운 순서가 정의돼 있지 않으면 sort 메서드를 쓸 수 없다. 하지만 원소 타입에 순서 특별 메서드를 정의하는 경우는 드물다.

- 파이썬이 무엇이 더 큰지 판단할 기준이 없으면 정렬을 포기한다.
    - 파이썬은 숫자($1 < 2$)나 문자열($'a' < 'b'$)은 누가 앞인지 이미 알고 있다. 하지만 직접 만든 '로봇 객체'나 '파일 객체'는 무엇을 기준으로 비교해야 할지 모름. 이 기준을 정하는 게 바로 `__lt__`(less than, $<$ ) 같은 특별 메서드.
    - **sort 메서드를 쓸 수 없다**: 기준이 없으니 당연히 순서대로 줄을 세울(정렬) 수 없어서 에러를 낸다.
    - **특별 메서드를 정의하는 경우는 드물다**: 클래스 안에 일일이 비교 규칙을 만드는 건 번거롭고, 상황에 따라 정렬 기준(이름순, 무게순 등)이 바뀔 수 있기 때문에 보통은 클래스 자체에 순서를 박아두지 않는다.

### 3. sort 메서드의 key 파라미터를 사용하면 리스트의 각 원소 대신 비교에 사용할 객체를 반환하는 도우미 함수를 제공할 수 있다.

- 권장하지 않는 코드

```python
class Robot:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __repr__(self):
        return f"Robot({self.name}, {self.weight})"

# 로봇 리스트 생성
robots = [
    Robot('Alpha', 50),
    Robot('Beta', 30),
    Robot('Gamma', 40)
]

# 여기서 에러
robots.sort()
```

- 해결 방안(Key 파라미터）

```python
# weight(무게)를 기준으로 정렬하라고 알려줌
robots.sort(key=lambda x: x.weight)

print(robots)
# 출력: [Robot(Beta, 30), Robot(Gamma, 40), Robot(Alpha, 50)]
```

### 4. key 함수에서 튜플을 반환하면 여러 정렬 기준을 하나로 엮을 수 있다. 부호 반전 연산자를 사용하면 부호를 바꿀 수 있는 타입이 정렬 기준인 경우 정렬 순서를 반대로 바꿀 수 있다.

- 정렬 기준이 하나가 아닐 때(예: 점수가 같으면 나이순으로) 사용. 튜플 `(기준1, 기준2)`를 주면 파이썬은 기준1로 먼저 줄을 세우고, 거기서 동점이 나오면 기준2로 순서를 정한다.
- 부호 반전 연산자(-)를 사용하면... 순서를 반대로 바꿀 수 있다: 보통은 작은 게 앞으로 오는 '오름차순'이다. 그런데 숫자 앞에 `-`를 붙이면 큰 게 앞으로 오는 '내림차순' 효과를 낼 수 있다.
- 코드 예시

```python
class Robot:
    def __init__(self, name, score, weight):
        self.name = name
        self.score = score
        self.weight = weight

    def __repr__(self):
        return f"[{self.name}: {self.score}점, {self.weight}kg]"

# 로봇 리스트
robots = [
    Robot('Alpha', 100, 50),
    Robot('Beta', 80, 30),
    Robot('Gamma', 100, 40), # Alpha와 점수 같음, 하지만 더 가벼움
    Robot('Delta', 80, 20),  # Beta와 점수 같음, 하지만 더 가벼움
]

# (점수는 내림차순, 무게는 오름차순)
# 점수(score) 앞에 -를 붙여서 큰 값이 작은 값처럼 취급되게 만든다.
robots.sort(key=lambda x: (-x.score, x.weight))

print(robots)
# 출력: [[Gamma: 100점, 40kg], [Alpha: 100점, 50kg], [Delta: 80점, 20kg], [Beta: 80점, 30kg]]
```

### 5. 부호를 바꿀 수 없는 타입의 경우 여러 정렬 기준을 조합하려면 각 정렬 기준마다 reverse 값으로 정렬 순서를 지정하면서 sort 메서드를 여러 번 사용해야 한다. 이때 정렬 기준의 우선순위가 점점 높아지는 순서로 sort를 호출해야한다.

- 부호를 바꿀 수 없는 타입 : 문자열(String)이 대표적. 점수는 `score`로 순서를 뒤집을 수 있지만, 이름은 -`name`이라고 할 수 없다.
- sort 메서드를 여러 번 사용: 한 번에 정렬이 안 되니까, 기준 하나당 한 번씩 정렬을 따로따로 실행
- 우선순위가 높아지는 순서(역순)로 호출: 최종적으로 가장 중요한 기준을 '가장 나중에' 정렬해야 한다.
- 예시 코드

```python
class Robot:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"({self.name}, {self.score})"

robots = [
    Robot('Alpha', 100),
    Robot('Gamma', 100),
    Robot('Beta', 80),
    Robot('Delta', 80),
]

# 1순위 이름(내림차순), 2순위 점수(오름차순)

# Step 1: 2순위인 '점수'를 먼저 정렬 (오름차순)
robots.sort(key=lambda x: x.score)

# Step 2: 1순위인 '이름'을 나중에 정렬 (내림차순으로 뒤집기 위해 reverse=True)
robots.sort(key=lambda x: x.name, reverse=True)

print(robots)
# 결과: [(Gamma, 100), (Delta, 80), (Beta, 80), (Alpha, 100)]
# 이름이 Gamma -> Delta -> Beta -> Alpha 순으로 정렬됨 (내림차순)
# 이름이 같은 경우는 없으므로, 점수 순서가 보존됨
```

## **15. 딕셔너리 삽입 순서에 의존할 때는 조심하라**

### 기억해야 할 내용

1. 파이썬 3.7부터는 dict 인스턴스에 들어 있는 내용을 이터레이션할 때 키를 삽입한 순서대로 돌려받는다는 사실에 의존할 수 있다.
2. 파이썬은 dict는 아니지만 딕셔너리와 비슷한 객체를 쉽게 만들 수 있게 해준다. 이런 타입의 경우 키 삽입 순서가 그대로 보존된다고 가정할 수 없다.
3. 딕셔너리와 비슷한 클래스를 조심스럽게 다루는 방법으로는 dict 인스턴스의 삽입 순서 보존에 의존하지 않고 코드를 작성하는 방법, 실행 시점에 명시적으로 dict 타입을 검사하는 방법, 타입 애너테이션과 정적 분석을 사용해 dict 값을 요구하는 방법이 있다.

### 1. 파이썬 3.7부터는 dict 인스턴스에 들어 있는 내용을 이터레이션할 때 키를 삽입한 순서대로 돌려받는다는 사실에 의존할 수 있다.

- 파이썬 3.7 이전과 이후
    - **파이썬 3.5 이하:** 딕셔너리에 '사과', '바나나', '포도' 순서로 데이터를 넣었어도, 나중에 꺼내보면 '포도', '사과', '바나나'처럼 **지**멋대로인 순서로 튀어나왔다.
    - **파이썬 3.7 이상:** 이제 파이썬은 내부적으로 데이터를 저장할 때 "사용자가 어떤 순서로 데이터를 넣었는지"를 기억한다. 그래서 꺼낼 때(이터레이션할 때) 항상 그 순서를 보장해준다
- 예시 코드

```python
# 관절 이름과 제어 각도를 순서대로 입력
joint_controls = {}
joint_controls['shoulder'] = 45
joint_controls['elbow'] = 90
joint_controls['wrist'] = 10

# 1. 키(Key)를 순회할 때
print("제어 순서:")
for joint in joint_controls:
    print(joint) 
# 출력 결과 (항상 일정): shoulder -> elbow -> wrist

# 2. popitem()을 사용할 때
# 3.7 이후부터는 항상 '가장 마지막'에 넣은 것을 꺼낸다.
last_item = joint_controls.popitem()
print(f"\n마지막에 추가된 제어: {last_item}") 
# 출력 결과: ('wrist', 10)
```

### 2. 파이썬은 dict는 아니지만 딕셔너리와 비슷한 객체를 쉽게 만들 수 있게 해준다. 이런 타입의 경우 키 삽입 순서가 그대로 보존된다고 가정할 수 없다.

- 파이썬에서는 `collections.abc.Mapping` 등을 상속받아 딕셔너리처럼 `d[key] = value` 형태로 쓸 수 있는 커스텀 객체를 만들 수 있다.
- "키 삽입 순서가 보존된다고 가정할 수 없다": 기본 `dict`는 내가 'A', 'B', 'C' 순으로 넣으면 나중에 꺼낼 때도 'A', 'B', 'C' 순서로 나온다. 하지만 딕셔너리를 흉내 낸 다른 객체들은 자기만의 방식(예: 알파벳순 정렬, 혹은 완전 무작위)으로 데이터를 저장할 수 있다.
- 코드를 짤 때 "내가 먼저 넣었으니까 먼저 나오겠지?"라는 생각으로 짜면, 나중에 이런 특수한 객체를 만났을 때 프로그램이 엉뚱하게 돌아갈 수 있다
- 예시 코드

```python
from collections.abc import MutableMapping

# 딕셔너리처럼 작동하지만, 순서를 보장하지 않는 '랜덤 딕셔너리' 클래스
class RandomDict(MutableMapping):
    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        # 일부러 알파벳 순서대로 정렬해서 내보낸다. (삽입 순서 무시)
        return iter(sorted(self._data.keys()))

    def __len__(self):
        return len(self._data)

# 실행해보기
def print_dict(d):
    for key, value in d.items():
        print(f"{key}: {value}")

# 1. 일반 dict (삽입 순서 보장됨)
print("--- 일반 dict 결과 ---")
standard_d = {}
standard_d['banana'] = 1
standard_d['apple'] = 2
standard_d['cherry'] = 3
print_dict(standard_d) 

# 2. RandomDict (삽입 순서 보장 안 됨 - 알파벳순으로 나옴)
print("\n--- RandomDict 결과 ---")
custom_d = RandomDict()
custom_d['banana'] = 1
custom_d['apple'] = 2
custom_d['cherry'] = 3
print_dict(custom_d)
```

```python
--- 일반 dict 결과 ---
banana: 1
apple: 2
cherry: 3

--- RandomDict 결과 ---
apple: 2
banana: 1
cherry: 3
```

### 3. 딕셔너리와 비슷한 클래스를 조심스럽게 다루는 방법으로는 dict 인스턴스의 삽입 순서 보존에 의존하지 않고 코드를 작성하는 방법, 실행 시점에 명시적으로 dict 타입을 검사하는 방법, 타입 애너테이션과 정적 분석을 사용해 dict 값을 요구하는 방법이 있다.

- 3가지 방어 전략
    - **순서 보존에 의존하지 않기**: "먼저 넣었으니 먼저 나오겠지”라는 믿음을 버리는 것. 아예 순서와 상관없이 결과가 똑같이 나오도록 코드를 설계하는 방법.
    - **명시적으로 dict 타입 검사**: 실행 중에 진짜 순서가 보장되는 표준 `dict` 가 맞는지 확인하고, 아니면 에러를 내서 진행을 막는 방법.
    - **타입 애너테이션과 정적 분석**
- 방법 1: 순서에 의존하지 않는 코드 → 순서가 확실한 리스트를 따로 관리

```python
# 딕셔너리는 정보 저장용으로만 쓰고, 순서는 리스트로 따로 관리
sensor_data = {'Lidar': 1, 'Camera': 2, 'Sonar': 3}
execution_order = ['Lidar', 'Camera', 'Sonar'] # 순서를 명시함

for sensor in execution_order:
    # 딕셔너리의 순서가 뒤죽박죽이어도 리스트 덕분에 순서대로 실행
    print(f"{sensor} 처리 중... 우선순위: {sensor_data[sensor]}")
```

- 방법 2: 실행 시점에 타입 검사 (isinstance)

```python
def process_sensors(sensors):
    # dict 인스턴스인지 확인
    # 순서를 무시하는 RandomDict 같은 유사품은 여기서 걸러진다.
    if not isinstance(sensors, dict):
        raise TypeError("표준 dict 타입을 사용해야 함")
    
    for name, priority in sensors.items():
        print(f"센서 {name} 가동 (우선순위: {priority})")

# 사용 예시
process_sensors({'Lidar': 1}) # 통과
# process_sensors(RandomDict()) # TypeError 발생
```

- 방법 3: 타입 애너테이션 사용
    - 타입 애너테이션의 모양
        - 함수를 만들 때 인자 뒤에 `:` (콜론)을 찍고 타입을 적어준다.

```python
from typing import Dict

# 이 함수는 유사 딕셔너리가 아닌 'dict'만 원한다고 명시
def start_robot(config: Dict[str, int]):
    for key, value in config.items():
        print(f"{key} 설정 완료: {value}")

# 이렇게 하면 VS Code 같은 에디터나 정적 분석 도구가 
# config 자리에 유사 딕셔너리가 들어오면 타입이 다르다고 경고해준다.
```

## **16. in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라**

### 기억해야 할 내용

1. 딕셔너리 키가 없는 경우를 처리하는 방법으로는 in 식을 사용하는 방법, keyError 예외를 사용하는 방법, get 메서드를 사용하는 방법, setdefault 메서드를 사용하는 방법이 있다.
2. 카운터와 같이 기본적인 타입의 값이 들어가는 딕셔너리를 다룰 때는 get 메서드가 가장 좋고, 딕셔너리에 넣을 값을 만드는 비용이 비싸거나 만드는 과정에 예외가 발생할 수 있는 경우에도 get 메서드를 사용하는 편이 더 낫다.
- 해결하려는 문제에 dict setdefault 메서드를 사용하는 방법이 가장 적합해 보인다면 setdefault 대신 defaultdict를 사용할지 고려해보라

### 1. 딕셔너리 키가 없는 경우를 처리하는 방법으로는 in 식을 사용하는 방법, keyError 예외를 사용하는 방법, get 메서드를 사용하는 방법, setdefault 메서드를 사용하는 방법이 있다.

- in 식을 사용하는 방법

```python
counters = {'apple': 2, 'banana': 1}
key = 'orange'

# orange가 counters 안에 있나 확인
if key in counters:
    count = counters[key] # 있으면 가져옴
else:
    count = 0             # 없으면 0으로 설정

counters[key] = count + 1
```

- `KeyError` 예외를 사용하는 방법 (일단 지르고 수습)

```python
try:
    count = counters[key]
except KeyError:
    # 키가 없으면 KeyError가 발생하고 이쪽으로 넘어온다.
    count = 0

counters[key] = count + 1
```

- `get` 메서드를 사용하는 방법

```python
# counters.get(key, 기본값)
count = counters.get(key, 0)
counters[key] = count + 1
```

- `setdefault` 메서드를 사용하는 방법

```python
votes = {'철수': ['사과']}
key = '영희'

# 영희가 없으면 빈 리스트 []를 딕셔너리에 넣고, 그 리스트를 돌려줌
names = votes.setdefault(key, [])
names.append('포도')

print(votes) # {'철수': ['사과'], '영희': ['포도']}
```

### 2. 카운터와 같이 기본적인 타입의 값이 들어가는 딕셔너리를 다룰 때는 get 메서드가 가장 좋고, 딕셔너리에 넣을 값을 만드는 비용이 비싸거나 만드는 과정에 예외가 발생할 수 있는 경우에도 get 메서드를 사용하는 편이 더 낫다.

- 기본적인 타입(숫자, 문자열) 처럼 메모리를 적게 쓰고 다루기 쉬운 데이터
    - in 을 쓰면 비효율적인 이유
    
    ```python
    counters = {'apple': 5}
    key = 'banana'
    
    if key in counters:      # 1. 딕셔너리에서 키를 찾음
        count = counters[key] # 2. 찾은 키의 값을 또 가져옴 (두 번 일함)
    else:
        count = 0
    ```
    
    - get 을 쓰면 효율적인 이유
    
    ```python
    count = counters.get(key, 0) # 한 번만 찾고, 없으면 바로 0을 반환(한 번만 일함)
    ```
    
    - `setdefault`를 쓰면 안 되는 이유
        - 이미 지도가 등록되어 있어도, `setdefault`는 인자로 넘겨진 함수를 먼저 실행해버림
    
    ```python
    # setdefault(key, 기본값)
    # 'map_data'가 있든 없든, 'create_heavy_map()' 함수는 무조건 먼저 실행
    data = {}
    my_map = data.setdefault('robot_field', create_heavy_map())
    ```
    
    - `get` 이 좋은 이유
    
    ```python
    data = {}
    
    # 1. 일단 가져와 본다.
    my_map = data.get('robot_field')
    
    # 2. 없을 때만 '비싼 작업'을 시작
    if my_map is None:
        my_map = create_heavy_map() # 필요할 때만 만든다
        data['robot_field'] = my_map
    ```
    

### 3. 해결하려는 문제에 dict setdefault 메서드를 사용하는 방법이 가장 적합해 보인다면 setdefault 대신 defaultdict를 사용할지 고려해보라

- setdefault 가 아쉬운점

```python
votes = {}
# 데이터를 넣을 때마다 '없으면 빈 리스트([])를 넣어라'라고 매번 써줘야 한다.
names = votes.setdefault('영희', [])
names.append('포도')
```

- defaultdict

```python
from collections import defaultdict

# 키가 없으면 자동으로 list(빈 리스트)를 만들어준다.
votes = defaultdict(list)

# setdefault나 if문 없이 바로 append를 쓸 수 있다.
votes['영희'].append('포도')
votes['철수'].append('사과')

print(votes) 
# 결과: defaultdict(<class 'list'>, {'영희': ['포도'], '철수': ['사과']})
```

## **17. 내부 상태에서 원소가 없는 경우를 처리할 떄는 setdefault보다 defaultdict를 사용하라**

### 기억해야 할 내용

- 키로 어떤 값이 들어올지 모르는 딕셔너리를 관리해야 하는데 collections 내장 모듈에 있는 defaultdict 인스턴스가 여러분의 필요에 맞아 떨어진다면 defaultdict를 사용하라
- 임의의 키가 들어 있는 딕셔너리가 여러분에게 전달됐고 그 딕셔너리가 어떻게 생성됐는지 모르는 경우, 딕셔너리의 원소에 접근하려면 우선 get을 사용해야 한다. 하지만 setdefault가 더 짧은 코드를 만들어내는 몇 가지 경우에는 setdefault를 사용하는 것도 고려해볼 만하다.

- 외부에서 받은 딕셔너리를 다룰 때(`get` vs `setdefault`)
    - 방식 A: `get`과 바다표범 연산자 (`:=`)
    
    ```python
    visits = {
        '미국': {'뉴욕', '로스엔젤레스'},
        '일본': {'하코네'},
    }
    
    if (japan := visits.get('일본')) is None:
        visits['일본'] = japan = set()
    japan.add('교토')
    ```
    
    - 방식 B : `setdefault`
    
    ```python
    visits.setdefault('프랑스', set()).add('칸')
    ```
    
- 클래스 내부에서 `setdefault` 사용하기
    
    ```python
    class Visits:
        def __init__(self):
            self.data = {}  # 일반 딕셔너리
    
        def add(self, country, city):
            # 키가 있든 없든 일단 set()을 가져오거나 생성함
            city_set = self.data.setdefault(country, set())
            city_set.add(city)
    ```
    
- 클래스 내부에서 `defaultdict` 사용하기
    
    ```python
    from collections import defaultdict
    
    class Visits:
        def __init__(self):
            # 이 딕셔너리는 키가 없으면 자동으로 set()을 만든다.
            self.data = defaultdict(set)
    
        def add(self, country, city):
            # 키가 있는지 물어볼 필요도, setdefault를 쓸 필요도 없다
            self.data[country].add(city)
    ```
    

** `defaultdict(list)`와 `defaultdict(set)`의 차이

```python
from collections import defaultdict

# 1. defaultdict(list) 사용
list_dict = defaultdict(list)
list_dict['영국'].append('바스')
list_dict['영국'].append('바스')  # 똑같은 데이터를 또 넣음
list_dict['영국'].append('런던')

# 2. defaultdict(set) 사용
set_dict = defaultdict(set)
set_dict['영국'].add('바스')
set_dict['영국'].add('바스')     # 똑같은 데이터를 또 넣음 (set은 add를 쓴다))
set_dict['영국'].add('런던')

print("--- [list] 결과 ---")
print(dict(list_dict))

print("\n--- [set] 결과 ---")
print(dict(set_dict))
```

```python
--- [list] 결과 ---
{'영국': ['바스', '바스', '런던']}

--- [set] 결과 ---
{'영국': {'바스', '런던'}}
```

## **18. __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라**

### 기억해야 할 내용

1. 디폴트 값을 만드는 계산 비용이 높거나 만드는 과정에서 예외가 발생할 수 있는 상황에서는 dict의 setdefault 메서드를 사용하지 말라
2. defaultdict에 전달되는 함수는 인자를 받지 않는다. 따라서 접근에 사용한 키 값에 맞는 디폴트 값을 생성하는 것은 불가능히다.
3. 디폴트 키를 만들 때 어떤 키를 사용했는지 반드시 알아야 하는 상황이라면 직접 dict의 하위 클래스와 __missing__ 메서드를 정의하면 된다.

### 1. 디폴트 값을 만드는 계산 비용이 높거나 만드는 과정에서 예외가 발생할 수 있는 상황에서는 dict의 setdefault 메서드를 사용하지 말라

→ 디폴트 값이란 딕셔너리에 찾는 키가 없을 때, 대신 넣어 주기로 약속한 기본값

- `setdefault`의 문제점: 답이 있어도 일단 계산

```python
import time

def 아주_오래_걸리는_계산():
    print("...10초 동안 계산 중...")
    time.sleep(10) # 10초 대기
    return "계산 결과"

data = {'test': "이미 있는 결과"}

# 'test'라는 키가 이미 있는데도, 
# setdefault는 '아주_오래_걸리는_계산()'을 무조건 먼저 실행
result = data.setdefault('test', 아주_오래_걸리는_계산())

print(result)
```

### 2. defaultdict에 전달되는 함수는 인자를 받지 않는다. 따라서 접근에 사용한 키 값에 맞는 디폴트 값을 생성하는 것은 불가능하다.

- defaultdict 의 open_file 이 키값을 받지 못한다.

```python
# 파일 경로(path)를 주면 파일을 열어주는 함수
def open_file(path): 
    return open(path, 'a+b')

pictures = defaultdict(open_file) 

# 여기서 문제 발생
handle = pictures['sensor_A.txt']
```

### 3. 디폴트 키를 만들 때 어떤 키를 사용했는지 반드시 알아야 하는 상황이라면 직접 dict의 하위 클래스와 __missing__ 메서드를 정의하면 된다.

- pictures 객체의 `key`: `'sensor_A.txt'` 에 `value : open_file` 한 것을 저장

```python
class Pictures(dict):
    def __missing__(self, key):
        value = open_file(key)
        self[key] = value
        return value

# 사용 예시
pictures = Pictures()
# 'sensor_A.txt'라는 키가 없으므로 __missing__이 호출
handle = pictures['sensor_A.txt']
```