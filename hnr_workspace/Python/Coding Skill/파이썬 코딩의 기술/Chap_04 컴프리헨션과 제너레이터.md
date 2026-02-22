# Chap_04 컴프리헨션과 제너레이터

## **27. map과 filter 대신 컴프리헨션을 사용하라**

- 왜 컴프리헨션인가?
    - **수학적 의미:** 수학에서 집합을 정의할 때 `{ x² | x ∈ A }` (A에 속하는 x에 대하여 x의 제곱들의 집합)와 같이 정의하는 방식을 '포괄적 정의'라고 한다.
    - 'Comprehension'은 '이해'라는 뜻도 있지만, 어떤 것들을 '포괄'하거나 '포함'한다는 뜻이 있다.
    
    즉, "리스트가 담아야 할 내용(조건과 공식)을 한 구문 안에 모두 포괄하고 있다"는 뜻에서 컴프리헨션이라는 이름이 붙었다
    

```python
a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = []
for x in a:
    squares.append(x**2)

print(squares)
```

- 일반적인 `for` 루프의 방식
    - 작동방식 : 빈 리스트를 만들고, 원본 데이터를 하나씩 꺼내 계산한 뒤 `append` 로 집어 넣는다.
    - 시각적인 노이즈가 많다고 한다

```python
squares = [x**2 for x in a] # 리스트 컴프리핸션
print(squares)
```

- 리스트 컴프리헨션 기본 형
    - for 루프의 로직을 한줄로 압축
    - "a에 있는 x에 대해 x의 제곱을 수행한다"는 의도가 한눈에 보인다.
        - 파이썬 인터프리터 내부에서 `append` 를 반복 호출하는 것보다 리스트 컴프리헨션이 C 수준에서 더 빠르게 동작한다.

```python
alt = map(lambda x: x ** 2, a)
```

- `map` 함수 활용
    - `map(함수, 데이터)`
        - 첫 번째 인자 : 적용할 함수(`lambda x: x ** 2`)
        - 두 번째 인자 : 데이터를 꺼내올 반복 가능한 객체(리스트 `a` )

```python
even_squares = [x**2 for x in a if x % 2 == 0]
print(even_squares)
```

- 필터링이 추가된 컴프리헨션
    - `for x in a`: `a`에서 요소를 꺼낸다.
    - `if x % 2 == 0`: 짝수인지 확인한다 (필터).
    - `x**2`: 조건에 맞으면 제곱한다 (변환).
    - `[...]`: 결과들을 모아 새 리스트를 만든다.

```python
alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
assert even_squares == list(alt)
```

- `map` 과 `filter` 까지 중첩시킨 형태
    - `filter(lambda x: x % 2 == 0, a)`
        - filter 함수는 조건에 맞는 요소만 걸러낸다
            - 첫번째 인자 : 조건함수 `lambda x: x % 2 == 0` 에 대해 결과가 `True` 인것만 남긴다.
            - 두번째 인자 : 대상 데이터(`a`)
            - 결과 : 리스트 `a` 에서 짝수(2,4,6,8,10)만 통과시켜 다음 단계로 넘겨준다.
    - `map(lambda x: x**2, ...)`
        - filter 가 걸러낸 결과물을 map 이 받는다.
    - 여기서 문제
        - 안쪽(`filter`)에서 바깥쪽(`map`)으로 읽어야 한다.

```python
even_squares_dict = {x: x**2 for x in a if x % 2 == 0}
threes_cubed_set = {x**3 for x in a if x % 3 == 0}
print(even_squares_dict)
print(threes_cubed_set)
```

```python
{2: 4, 4: 16, 6: 36, 8: 64, 10: 100}
{216, 729, 27}
```

- 딕셔너리 컴프리헨션
    - 구조 : `{ 키 : 값 공식 for 항목 in 반복가능객체 if 조건 }`
- 집합 컴프리헨션
    - 구조: `{ 값 공식 for 항목 in 반복가능객체 if 조건 }`

```python
alt_dict = dict(map(lambda x: (x, x**2),
                filter(lambda x: x % 2 == 0, a)))
alt_set = set(map(lambda x: x**3,
              filter(lambda x: x % 3 == 0, a)))
```

### 기억해야 할 내용

- 리스트 컴프리헨션은 lambda 식을 사용하지 않기 때문에 같은 일을 하는 map 과 filter 내장 함수를 사용하는 것보다 더 명확하다.
    - [방법 A] map과 filter 사용 (복잡함)
    
    ```python
    numbers = [1, 2, 3, 4, 5, 6]
    
    # filter로 짝수를 거르고, map으로 제곱을 계산
    even_squares_map = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, numbers)))
    
    print(even_squares_map) # [4, 16, 36]
    ```
    
    - [방법 B] 리스트 컴프리헨션 사용 (명확함)
    
    ```python
    numbers = [1, 2, 3, 4, 5, 6]
    
    # 한 줄 안에서 필터링과 계산이 동시에 보임
    even_squares_comp = [x**2 for x in numbers if x % 2 == 0]
    
    print(even_squares_comp) # [4, 16, 36]
    ```
    

- 리스트 컴프리헨션을 사용하면 쉽게 입력 리스트의 원소를 건너뛸 수 있다. 하지만 map 을 사용하는 경우에는 filter 의 도움을 받아야한다.
    - lambda 의 특징
        - 이름이 없다: 메모리에 이름을 남기지 않고 한 번 쓰고 버려지는 경우가 많다.
        - 한 줄만 가능하다: 복잡한 로직이나 `if`, `for` 문을 여러 줄 작성할 수 없다. (오직 하나의 표현식만 허용)
        - 즉석 사용: 주로 `map()`, `filter()`, `sort()`와 같이 함수를 인자로 받는 다른 함수와 함께 쓰임
    - map 의 특징
        - 리스트와 같은 반복 가능한 객체의 모든 원소에 똑같은 기능을 일괄적으로 적용
        - map(함수, 반복_가능한_객체)
    - [방법 A] map + filter 조합
    
    ```python
    numbers = [1, 2, 3, 4, 5]
    
    # 1. filter로 짝수만 남김 (홀수를 건너뜀)
    # 2. 그 결과를 map으로 전달해 10을 곱함
    result_map = list(map(lambda x: x * 10, filter(lambda x: x % 2 == 0, numbers)))
    
    print(result_map)  # [20, 40]
    ```
    
    - [방법 B] 리스트 컴프리헨션
    
    ```python
    numbers = [1, 2, 3, 4, 5]
    
    # if 절 하나로 "건너뛰기"와 "계산"을 한 번에 끝냄
    result_comp = [x * 10 for x in numbers if x % 2 == 0]
    
    print(result_comp)  # [20, 40]
    ```
    
- 딕셔너리와 집합도 컴프리헨션으로 생성할 수 있다.
    - 딕셔너리 컴프리헨션
    
    ```python
    words = ['apple', 'banana', 'cherry']
    
    # 딕셔너리 컴프리헨션: {키: 값 for 변수 in 반복객체}
    word_lengths = {word: len(word) for word in words}
    
    print(word_lengths)
    # 출력: {'apple': 5, 'banana': 6, 'cherry': 6}
    ```
    
    - 집합 컴프리헨션
    
    ```python
    numbers = [1, 2, 2, 3, 4, 4, 5]
    
    # 집합 컴프리헨션: {식 for 변수 in 반복객체 if 조건}
    even_squares_set = {x**2 for x in numbers if x % 2 == 0}
    
    print(even_squares_set)
    # 출력: {16, 4} (중복되었던 2와 4가 하나씩만 계산되어 집합에 들어감)
    ```
    

## 28. 컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하지 말라

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [x for row in matrix for x in row]
print(flat)
```

```python
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- 컴프리헨션 안에 `for` 문이 여러 개 있을 때, 가장 중요한 규칙은 일반적인 `for` 루프를 쓸 때의 순서와 똑같이 적어야함.
- 위의 코드를 일반적인 for 루프로 풀어서 쓰면 아래와 같다.

```python
flat = []
for row in matrix:      # 1. 첫 번째 for 문
    for x in row:       # 2. 두 번째 for 문
        flat.append(x)  # 3. 결과값 (x)
```

```python
squared = [[x**2 for x in row] for row in matrix]
print(squared)
```

- 일반적인 코드로 풀면 다음과 같다

```python
squared = []
for row in matrix:
    new_row = []
    for x in row:
        new_row.append(x**2)
    squared.append(new_row)
```

```python
[[1, 4, 9], [16, 25, 36], [49, 64, 81]]
```

```python
my_lists = [
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [1, 2, 3]],
    [[4, 5, 6], [7, 8, 9]],
]
flat = [x for sublist1 in my_lists
        for sublist2 in sublist1
        for x in sublist2]
print(flat)
```

```python
[1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- `sublist1`: `my_lists`에서 큰 덩어리 하나를 가져온다. (예: `[[1, 2, 3], [4, 5, 6]]`)
- `sublist2`: 방금 가져온 덩어리 안에서 작은 리스트 하나를 가져온다 (예: `[1, 2, 3]`)
- `x`: 마지막으로 그 작은 리스트 안에서 실제 숫자 하나를 꺼낸다.(예: `1`, `2`, `3`)
- 이 과정을 끝까지 반복하면 모든 숫자가 한 줄로 늘어선 `[1, 2, 3, 4, 5, 6, 7, 8, 9, ...]` 리스트가 완성된다.

```python
flat = []
for sublist1 in my_lists:
    for sublist2 in sublist1:
        flat.extend(sublist2)
print(flat)
```

```python
[1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

- `for sublist1 in my_lists:`
    - 가장 바깥쪽 리스트에서 2차원 리스트 덩어리를 하나 꺼낸다.
    - 예: `[[1, 2, 3], [4, 5, 6]]`
- `for sublist2 in sublist1:`
    - 방금 꺼낸 덩어리 안에서 1차원 리스트를 하나 꺼낸다.
    - 예: `[1, 2, 3]`
- `flat.extend(sublist2)`
    - 여기서 `append`를 쓰지 않고 `extend`를 썼다.
    - `append`: 리스트 자체를 통째로 집어넣음 (결과가 `[[1, 2, 3]]`이 됨)
    - `extend`: 리스트 안의 내용물만 쏙 꺼내서 기존 리스트 뒤에 이어 붙임 (결과가 `[1, 2, 3]`이 됨)
    

```python
b = [x for x in a if x > 4 if x % 2 == 0]
```

- 컴프리헨션의 공식 : `b = [ (결과값) for (변수) in (대상) (조건문) ]`
- 작동 순서:
1. `x > 4`인가? (먼저 검사)
2. (위가 참이라면) `x % 2 == 0`인가? (그다음 검사)
- 일반 for 루프로 풀면 다음과 같다

```python
for x in a:
    if x > 4:
        if x % 2 == 0:
            b.append(x)
```

```python
c = [x for x in a if x > 4 and x % 2 == 0]
```

- 작동 순서: `x > 4`와 `x % 2 == 0` 두 조건이 모두 참인지 한꺼번에 검사
- 일반 for 루프로 풀면 다음과 같다

```python
for x in a:
    if x > 4 and x % 2 == 0:
        c.append(x)
```

---

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
filtered = [[x for x in row if x % 3 == 0]
            for row in matrix if sum(row) >= 10]
print(filtered)
```

### 기억해야할 내용

- 컴프리헨션은 여러 수준의 루프를 지원하며 각 수준마다 여러 조건을 지원한다.
    - 컴프리헨션 하나 안에서 `for` 문(루프)을 여러 번 쓸 수 있고, 각 `for` 문마다 `if`(조건)를 붙여서 아주 정교하게 데이터를 뽑아낼 수 있다.
- 제어 하위 식이 세 개 이상인 컴프리헨션은 이해하기 매우 어려우므로 가능하면 피해야한다.

## **29. 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하라**

```python
stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']

def get_batches(count, size):
    return count // size

result = {}
for name in order:
    count = stock.get(name, 0)
    batches = get_batches(count, 8)
    if batches:
        result[name] = batches

print(result)
```

```python
{'나사못': 4, '나비너트': 1}
```

```python
found = {name: get_batches(stock.get(name, 0), 8) # 결과값 
         for name in order # 반복문
         if get_batches(stock.get(name, 0), 8)} # 조건문
print(found)
```

```python
{'나사못': 4, '나비너트': 1}
```

- `for name in order`: 주문 목록에서 이름을 하나씩 꺼낸다.
- `if get_batches(stock.get(name, 0), 8)`: (조건문) 묶음 계산 결과가 0이 아닐 때만 통과시킨다.
- `name: get_batches(stock.get(name, 0), 8)`: (결과물) 이름을 키로, 묶음 계산 결과를 값으로 저장한다.
- 똑같은 함수를 두번이나 호출하여 낭비적으로 계산을 하게 됨

```python
has_bug = {name: get_batches(stock.get(name, 0), 4)
           for name in order
           if get_batches(stock.get(name, 0), 8)}

print('예상:', found)
print('실졔: ', has_bug)
```

```python
예상: {'나사못': 4, '나비너트': 1}
실졔:  {'나사못': 8, '나비너트': 2}
```

- 컴프리헨션 안에서 똑같은 로직을 두 번 쓰게 되면(하나는 필터링용, 하나는 저장용), 나중에 코드를 고칠 때 양쪽을 다 고쳐야하는 번거로움이 있다.

```python
found = {name: batches for name in order
         if (batches := get_batches(stock.get(name, 0), 8))}

# 오류가 나는 부분. 오류를 보고 싶으면 커멘트를 해제할것
#result = {name: (tenth := count // 10)
#          for name, count in stock.items() if tenth > 0}
print(found)
```

```python
{'나사못': 4, '나비너트': 1}
```

- 바다코끼리 연산자(Walrus Operator)
    - 일반 대입(`=`) vs 바다코끼리 대입(`:=`)
        - 일반 대입 : "상자에 값을 넣는 행위" 자체
        - 바다코끼리 대입 : “상자에 값을 넣는 행위” + 반환까지
        - 여기서 저장된 batches 는 name:batches 에서 그대로 사용한다

```python
result = {name: (tenth := count // 10)
          for name, count in stock.items() if tenth > 0}
```

- 파이썬 컴프리헨션이 실행될 때, 실제 실행 순서는 다음과 같다.
    1. 반복문(`for`) : 먼저 데이터를 하나 꺼낸다.
    2. 조건문(`if`) : 데이터를 결과에 넣을지 말지 검사한다
    3. 결과생성(`name: (tenth := ...)`)
- 지금 tenth 라는 변수가 태어나지도 않았는데 `if tenth > 0` 를 실행하려고 했기때문에 에러가 발생한다.

```python
# 일반적인 컴프리헨션 변수
half = [c // 2 for c in stock.values()]

print(c)

NameError: name 'd' is not defined
```

```python
#
half = [(last := count // 2) for count in stock.values()]
print(f'{half}의 마지막 원소는 {last}')
```

```python
[62, 17, 4, 12]의 마지막 원소는 12
```

- 변수 누출 (Variable Leakage)
    - 리스트 컴프리헨션 안에서 쓰는 변수는 밖으로 안 나오는 게 파이썬의 규칙이다. 그런데 바다코끼리 연산자는 이 규칙을 깨고 변수를 밖으로 유출시킬 수 있다.

```python
#
for count in stock.values(): # 루프 변수가 누출됨
    pass

print(f'{list(stock.values())}의 마지막 원소는 {count}')
```

```python
[125, 35, 8, 24]의 마지막 원소는 24
```

- **반복 시작:** `stock.values()`에서 숫자들을 하나씩 꺼내 `count`라는 이름표를 붙인다.
- **마지막 바퀴:** 가장 마지막 숫자인 **24**를 꺼내서 `count`에 담는다.
- **루프 종료:** 이제 더 꺼낼 숫자가 없어서 루프가 끝난다.
- 루프가 끝났음에도 불구하고, `count`라는 변수는 메모리에 그대로 남아 있고 가장 마지막에 담겼던 값(24)을 그대로 들고 있다.

```python
#
half = [count // 2 for count in stock.values()]
print(half)  # 작동함
print(count) # 루프 변수가 누출되지 않기 때문에 예외가 발생함
```

- 여기서 `count`는 리스트를 만들기 위해 임시로 사용하는 변수이다.
    - 리스트가 만들어지는 동안에는 `125`, `35`, `8`, `24`라는 값을 차례로 갖게 된다.
    - 결과물인 `half` 리스트는 `[62, 17, 4, 12]`가 되어 저장된다.
- 파이썬은 리스트 컴프리헨션 내부에서 선언된 반복 변수(`count`)를 그 계산이 끝나자마자 메모리에서 완전히 삭제한다.
- `[count // 2 for count in ...]` → `count`는 소멸함 (안전)
- `[(last := count // 2) for count in ...]` → `last` 는 생존 → 유출

```python
#
stock = {
    '못': 125,
    '나사못': 35,
    '나비너트': 8,
    '와셔': 24,
}

order = ['나사못', '나비너트', '클립']

found = ((name, batches) for name in order
         if (batches := get_batches(stock.get(name, 0), 8)))
print(found)
print(next(found))
print(next(found))
```

```python
<generator object <genexpr> at 0x00000219CCAC4E50>
('나사못', 4)
('나비너트', 1)
```

- 지연 계산(Lazy Evaluation): 리스트(`[]`)는 코드가 실행되는 즉시 모든 계산을 끝내고 메모리에 값을 다 올린다. 하지만 제너레이터(`()`)는 요청 받을 때만 계산을 수행한다.

### 기억해야 할 내용

- 대입식을 통해 컴프리헨션이나 제너레이터 식의 조건 부분에서 사용한 값을 같은 컴프리헨션이나 제너레이터의 다른 위치에서 재사용할 수 있다. 이를 가독성과 성능을 향상시킬 수 있다.
- 조건이 아닌 부분에도 대입식을 사용할 수 있지만, 그런 형태의 사용은 피해야 한다.

## 30. 리스트를 반환하기 보다는 제너레이터를 사용하라

### 기억해야 할 내용

- 제너레이터를 사용하면 결과를 리스트에 합쳐서 반환하는 것보다 더 깔끔하다.
- 제너레이터가 반환하는 이터레이터는 제너레이터 함수의 본문에서 yield 가 반환하는 값들로 이뤄진 집합을 만들어낸다.
- 제너레이터를 사용하면 작업 메모리에 모든 입력과 출력을 저장할 필요가 없으므로 입력이 아주 커도 출력 시퀀스를 만들 수 있다.

---

- 리스트 반환 방식(로직보다 관리 코드가 많음)
    - 리스트를 만들고, 담고, 반환한다 → 이 과정을 계속 따라가야 함

```python
def index_words(text):
    result = []
    if text:
        result.append(0)
    for index, letter in enumerate(text):
        if letter == ' ':
            result.append(index + 1)
    return result

#
address = '컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어:전산기)는 진공관'
result = index_words(address)
print(result[:10])
```

```python
[0, 8, 18, 23, 28, 38]
```

- 제너레이터 방식

```python
# 제너레이터 함수
def index_words_iter(text):
    if text:
        yield 0             # 찾았을 때 바로
    for index, letter in enumerate(text):
        if letter == ' ':
            yield index + 1 # 찾았을 때 바로
address = '컴퓨터(영어: Computer, 문화어: 콤퓨터, 순화어:전산기)는 진공관'
#
it = index_words_iter(address)
print(next(it))
print(next(it))

#
result = list(index_words_iter(address))
print(result[:10])
```

```python
0
8
18
23
28
38
[0, 8, 18, 23, 28, 38]
```

---

```python
def rainbow_factory():
    print("공장 가동 시작!")
    yield "빨강"
    yield "주황"
    yield "노랑"
    print("공장 가동 중지!")

# 1. 제너레이터 함수를 호출하여 '이터레이터'를 받음
factory_it = rainbow_factory()

# 2. 값들을 하나씩 꺼내기 (yield가 반환한 값들의 집합을 순회)
for color in factory_it:
    print(f"꺼낸 색깔: {color}")
```

- 시작: `factory_it` 기계한테 가서 값을 하나 받아와라
- 반복 (1회차): `next(factory_it)` 호출 → 기계가 "빨강"을 뱉고 멈춤 → `color` 변수에 빨강을 담음 → `print` 실행.
- 반복 (2회차): 다시 `next(factory_it)` 호출 → 기계가 아까 멈춘 곳부터 시작해서 "주황"을 뱉고 멈춤 → `color` 변수에 "주황"을 담음 → `print` 실행.
- 반복 (3회차): 다시 `next(factory_it)` 호출 → 기계가 "노랑"을 뱉고 멈춤 → `color` 변수에 "노랑"을 담음 → `print` 실행.
- 종료

## 31. 인자에 대해 이터레이션할 때는 방어적이 돼라

```python
def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result

#
visits = [15, 35, 80]
percentages = normalize(visits)
print(percentages)
assert sum(percentages) == 100.0
```

- 코드 로직 분석
    1. 합계 구하기 (`total = sum(numbers)`):
    입력받은 `numbers` 안의 모든 숫자를 꺼내서 다 더한다. 이 과정에서 `numbers`를 처음부터 끝까지 한 번 순회한다.
    2. 개별 비중 계산 (`for value in numbers:`):
    다시 `numbers`에서 숫자를 하나씩 꺼낸다. 즉, 두 번째 순회를 시작한다.
    `100 * 값 / 합계` 공식을 써서 전체에서 이 숫자가 차지하는 비율을 계산한다.
    3. 결과 반환:
    계산된 비율들을 `result` 리스트에 담아 반환
- `visits = [15, 35, 80]` 리스트를 넣었을 때
    
    예제 코드처럼 일반적인 리스트를 넣으면 아무 문제 없이 잘 작동
    
    - `sum(numbers)`: 리스트 `[15, 35, 80]`을 훑어서 `130`을 만든다.
    - `for value in numbers`: 리스트는 메모리에 값이 저장되어 있으므로, 다시 처음으로 돌아가서 `15`, `35`, `80`을 차례대로 꺼낼 수 있다.
    - 결과: `[11.53, 26.92, 61.53]` (합계 100.0)이 정상적으로 출력된다.
- 코드의 잠재적 위험
    
    눈여겨봐야 할 부분은 `numbers`라는 인자를 두 번 순회한다는 점
    
    - 한 번은 `sum()`에서.
    - 또 한 번은 `for` 루프에서.

```python
def read_visits(data_path):
    with open(data_path) as f:
        for line in f:
            yield int(line)

def normalize(numbers):
    total = sum(numbers)
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result
    
#
it = read_visits('my_numbers.txt')
percentages = normalize(it)
print(percentages)

#
it = read_visits('my_numbers.txt')
print(list(it)) # [15, 35, 80]
print(list(it)) # 이미 모든 원소를 다 소진했다
```

- 제너레이터(이터레이터)는 단 한 번만 읽을 수 있는 '소모성' 데이터다. 따라서 여러 번 순회해야 하는 함수에 넣으면 조용히 망가진다.

```python
def normalize_copy(numbers):
    numbers_copy = list(numbers) # 이터레이터 복사
    total = sum(numbers_copy)
    result = []
    for value in numbers_copy:
        percent = 100 * value / total
        result.append(percent)
    return result

#
it = read_visits('my_numbers.txt')
percentages = normalize_copy(it)
print(percentages)
assert sum(percentages) == 100.0
```

- 변수가 `numbers`가 아니라 `numbers_copy`로 바뀌어있다. `numbers_copy` 라는 리스트에 저장

```python
def normalize_func(get_iter):
    total = sum(get_iter())  # 새 이터레이터
    result = []
    for value in get_iter(): # 새 이터레이터
        percent = 100 * value / total
        result.append(percent)
    return result

#
path = 'my_numbers.txt'
percentages = normalize_func(lambda: read_visits(path))
print(percentages)
assert sum(percentages) == 100.0
```

- 대용량 데이터를 다룰 때, 메모리를 아끼기 위해 제너레이터를 쓰면서도 '데이터 소멸' 문제에 빠지지 않으려면, 이터레이터를 생성해주는 함수를 인자로 활용하라
- 함수를 호출할 때 매번 lambda라고 써야 해서 코드가 지저분

---

### 기억해야 할 내용

- 입력 인자를 여러 번 이터레이션하는 함수나 메서드를 조심하라. 입력받은 인자가 이터레이터면 함수가  이상하게 작동하거나 결과가 없을 수 있다.
    - **이터레이터는 '소모성'이다:** 이터레이터는 마치 한 번 읽으면 글자가 사라지는 종이와 같다. 한 번 끝까지 읽고 나면(Iteration), 다시 읽으려고 해도 이미 끝(StopIteration)에 도달했기 때문에 아무런 값도 나오지 않는다.
    - **여러 번 이터레이션:** 함수 안에서 `for` 문을 두 번 돌리거나, `sum()`을 한 뒤에 다시 평균을 구하려고 하면, 두 번째 시도부터는 데이터가 이미 다 소모되어 빈 리스트처럼 작동한다.
    
    ```python
    def normalize(numbers):
        # 1. 첫 번째 이터레이션: 합계 계산
        total = sum(numbers)
        
        # 2. 두 번째 이터레이션: 비율 계산 (여기서 문제 발생)
        result = []
        for value in numbers:
            percent = 100 * value / total
            result.append(percent)
        return result
    
    # 리스트가 아닌 '제너레이터(이터레이터)'를 입력으로 넣음
    data = [10, 20, 70]
    it = (x for x in data)  # 소괄호를 사용한 제너레이터 식
    
    print(f"결과: {normalize(it)}")
    ```
    
- 파이썬의 이터레이터 프로토콜은 컨테이너와 이터레이터가 `iter, next` 내장 함수나 for 루프 등의 관련 식과 상호작용하는 절차를 정의한다.
- `__iter__` 메서드를 제너레이터로 정의하면 쉽게 이터러블 컨테이너 타입을 정의할 수 있다.
- 어떤 값이 (컨테이너가 아닌) 이터레이터인지 감지하려면, 이 값을 `iter` 내장 함수에 넘겨서 반환되는 값이 원래 값과 같은지 확인하면 된다. 다른 방법으로 `collections.abc.Iterator` 클래스를 `isinstance`와 함께 사용할 수도 있다.

## **32. 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용하라**

### 기억해야 할 내용

- 입력이 크면 메모리를 너무 만이 사용하기 때문에 리스트 컴프리헨션은 문제를 일으킬 수 있다.
- 제너레이터 식은 이터레이터처럼 한 번에 원소 하나씩 출력하기 때문에 메모리 문제를 피할 수 있다
- 제너레이터 식이 반환된 이터레이터를 다른 제너레이터 식의 하위 식으로 사용함으로써 제너레이터 식을 서로 합성할 수 있다.
- 서로 연결된 제너레이터 식은 매우 빠르게 실행되며 메모리도 효율적으로 사용한다.

---

- 리스트 vs 제너레이터
    
    리스트 컴프리헨션 (뷔페): 음식을 미리 다 만들어서 테이블에 쫙 깔아두는 방식. 손님이 1만 명(입력이 큼)이면 테이블이 엄청나게 커야 하고, 공간(메모리)이 부족하면 식당이 터져버린다.
    
    제너레이터 식 (즉석 주문): 손님이 올 때마다 그 자리에서 하나씩 음식을 만들어 주는 방식. 접시(메모리) 하나만 있으면 아무리 많은 손님이 와도 순서대로 처리할 수 있다.
    
    제너레이터 합성: "고기를 굽는 사람" 뒤에 "쌈을 싸는 사람"을 연결하는 것과 같다. 고기가 구워지자마자 바로 쌈이 싸져서 손님에게 전달되므로, 중간에 고기를 쌓아둘 창고가 필요 없다.
    
- 코드 예시

```python
# 1. 입력 데이터 (아주 크다고 가정)
numbers = [1, 2, 3, 4, 5]

# 2. 첫 번째 제너레이터 식: 제곱 계산
# 대괄호 [] 대신 소괄호 ()를 쓰면 제너레이터가 된다.
squares = (x**2 for x in numbers)

# 3. 제너레이터 합성: 위에서 만든 squares를 재료로 사용
# 계산 결과가 메모리에 쌓이지 않는다.
final_results = (y + 10 for y in squares)

# 4. 실제로 값을 꺼낼 때만 계산이 일어남
for result in final_results:
    print(result)

# 출력: 11, 14, 19, 26, 35
```

- 왜 이 방식이 좋은가?
    - 메모리 효율: 입력 데이터가 1억 개라도, 파이썬은 한 번에 숫자 한두 개만 기억하면 된다.
    - 속도: 첫 번째 결과값이 나올 때까지 기다릴 필요가 없다. 계산이 준비되는 대로 즉시 출력이 시작. (리스트 컴프리헨션은 1억 개를 다 계산해서 리스트에 담을 때까지 기다려야 한다)

## 33. yield form 을 사용해 여러 제너레이터를 합성하라

### 기억해야 할 내용

- yield from 식을 사용하면 여러 내장 제너레이터를 모아서 제너레이터 하나로 합설할 수 있다.
- 직접 내포된 제너레이터를 이터레이션하면서 각 제너레이터의 출력을 내보내는 것보다 yield from 을 사용하는 것이 성능 면에서 더 좋다.

---

- `yield from`이란?
    - 비유 (대리 판매): 당신이 물건을 파는 점원이라고 해보자. 창고 A와 창고 B에 물건이 나뉘어 있다.
        - 직접 이터레이션 (`for` 루프): 창고 A에 가서 물건을 하나씩 꺼내 손님에게 주고, 다 비우면 창고 B에 가서 또 하나씩 꺼내 주는 방식. (일일이 옮기는 수고가 든다.)
        - `yield from`: 창고 A와 창고 B에게 "손님이 오면 너희가 직접 물건을 내줘"라고 권한을 넘기는 방식이다. 통로만 열어주는 셈이다.
    - 비유 (대리 판매): 당신이 물건을 파는 점원이라고 해보자. 창고 A와 창고 B에 물건이 나뉘어 있다.
        - 직접 이터레이션 (`for` 루프): 창고 A에 가서 물건을 하나씩 꺼내 손님에게 주고, 다 비우면 창고 B에 가서 또 하나씩 꺼내 주는 방식. (일일이 옮기는 수고가 든다.)
        - `yield from`: 창고 A와 창고 B에게 "손님이 오면 너희가 직접 물건을 내줘"라고 권한을 넘기는 방식이다. 통로만 열어주는 셈이다.
    - 왜 더 좋은가? (성능과 가독성): 파이썬 내부적으로 `yield from`은 단순한 루프보다 최적화되어 있어 속도가 더 빠르다. 또한 중첩된 `for` 루프를 쓰지 않아도 되므로 코드가 훨씬 간결해진다.
- 코드 예시 : 여러 제너레이터 합치기

[방법 A] `for` 루프를 직접 사용 

```python
def count_numbers(low, high):
    for i in range(low, high):
        yield i

def manual_combine(gen1, gen2):
    # 첫 번째 제너레이터에서 하나씩 꺼내서 내보냄
    for x in gen1:
        yield x
    # 두 번째 제너레이터에서 하나씩 꺼내서 내보냄
    for x in gen2:
        yield x

# 실행
it = manual_combine(count_numbers(1, 3), count_numbers(10, 12))
print(list(it))  # [1, 2, 10, 11]
```

[방법 B] `yield from` 사용 

```python
def count_numbers(low, high):
    for i in range(low, high):
        yield i

def yielding_from_combine(gen1, gen2):
    # "gen1의 모든 원소를 여기서 직접 내보내라"는 뜻
    yield from gen1
    yield from gen2

# 실행
it = yielding_from_combine(count_numbers(1, 3), count_numbers(10, 12))
print(list(it))  # [1, 2, 10, 11]
```

- `yield from gen1`: 이 문장은 "현재 제너레이터의 제어권을 잠시 `gen1`에게 넘겨줄 테니, `gen1`이 가진 모든 값을 다 내보낼 때까지 기다려라"라는 뜻
- 성능 차이: [방법 A]는 파이썬 인터프리터가 매번 값을 하나씩 꺼내서(`for x in gen1`) 다시 내보내는(`yield x`) 과정을 거쳐야 함. 반면 `yield from`은 파이썬 내부 엔진이 제너레이터들을 직접 연결해주기 때문에 오버헤드가 훨씬 적다.
- 가독성: [방법 B]가 훨씬 짧고 의도가 명확.

## 34. send로 제너레이터에 데이터를 주입하지 말라

### 기억해야 할 내용

- send 메서드를 사용해 데이터를 제너레이터에 주입할 수 있다. 제너레이터는 send 로 주입된 값을 yield 식이 반환하는 값을 통해 받으며, 이 값을 변수에 저장해 활용할 수 있다.
    - 예시코드
    
    ```python
    def adder_generator():
        total = 0
        while True:
            # 이 한 줄이 입구와 출구 역할을 동시에
            # 1. yield total: 현재 합계(total)를 밖으로 내보낸다.
            # 2. received = yield: 밖에서 send()로 보내준 값을 received에 저장.
            received = yield total
            
            if received is not None:
                total += received
                print(f"전달받은 값: {received}, 현재 합계: {total}")
    
    # 1. 제너레이터 객체 만들기
    gen = adder_generator()
    
    # 2. 첫 번째 yield까지 실행
    # 처음에 total인 0을 내보내고 멈춘다.
    print(f"처음 상태: {next(gen)}") 
    
    # 3. send()로 데이터 주입하기
    # 10을 주입하면, 멈춰있던 yield 자리로 10이 들어가서 total에 더해진다.
    print(f"결과 1: {gen.send(10)}")
    
    # 4. 한 번 더 주입하기
    print(f"결과 2: {gen.send(20)}")
    ```
    
    ```python
    --- 더하기 기계 가동 ---
    처음 상태: 0
    전달받은 값: 10, 현재 합계: 10
    결과 1: 10
    전달받은 값: 20, 현재 합계: 30
    결과 2: 30
    ```
    
- send 와 yield from 식을 함께 사용하면 제너레이터의 출력에 None 이 불쑥불쑥 나타나는 의외의 결과를 얻을 수도 있다.

```python
def child():
    # 밖에서 값을 주입받으려고 기다리는 입구
    received = yield
    print(f"  [자식] 주입받은 값: {received}")
    yield f"결과: {received}"

def parent():
    # 자식 두 개를 연결함
    yield from child() # 자식 1호기
    yield from child() # 자식 2호기

# 실행
it = parent()
next(it)  # 첫 번째 자식의 첫 yield까지 예열

print(f"출력 1: {it.send('데이터 A')}")
print("--- 다음 자식으로 넘어가는 지점 ---")
print(f"출력 2: {it.send('데이터 B')}")
```

```python
[자식] 주입받은 값: 데이터 A
출력 1: 결과: 데이터 A
--- 다음 자식으로 넘어가는 지점 ---
출력 2: None
```

## 35. 제너레이터 안에서 throw로 상태를 변화시키지 말라

### 기억해야 할 내용

- throw 메서드를 사용하면 제너레이터가 마지막으로 실행한 yield 식의 위치에서 예외를 다시 발생시킬 수 있다.
    - 제너레이터는 보통 `yield`를 만나면 그 자리에서 잠시 멈춘다. `it.throw(에러)`를 호출하면, 멈춰있던 바로 그 `yield` 줄에서 에러가 난다.
    - 제너레이터 내부에서는 이 에러를 `try/except` 문으로 감싸서 대응할 수 있다.
    
    ```python
    class MyError(Exception):
        pass
    
    def my_generator():
        yield 1
        try:
            yield 2  # 여기서 밖에서 throw(MyError)를 하면 아래 except로 감
        except MyError:
            print("내부에서 MyError 잡음")
            yield 3
        yield 4
    
    it = my_generator()
    print(next(it))  # 1 출력
    print(next(it))  # 2 출력 후 멈춤
    
    # 밖에서 에러를 던짐!
    print(it.throw(MyError)) # "내부에서 MyError 잡음" 출력 후, 다음 yield인 3을 받아옴
    ```
    
    - 문제점
        - 제너레이터가 '값 생성'이라는 본연의 임무보다 '에러 처리'에 더 많은 코드를 쓰게 된다.
        - 코드가 `try-except-yield` 식으로 겹겹이 쌓여 읽기 힘들다.
- throw 를 사용하면 가독성이 나빠진다. 예외를 다시 잡아내고 다시 발생시키는 데 준비 코드가 필요하며 내포 단계가 깊어지기 때문이다.
- 제너레이터에서 예외적인 동작을 제공하는 더 나은 방법은 __iter__ 메서드를 구현하는 클래스를 사용하면서 예외적인 경우에 상태를 전이시키는 것이다.
    - 에러를 밖에서 던져서 기계를 고장 내지 말고, 기계 안에 '모드 변경 버튼'을 만들라는 뜻
    - `throw` 방식은 멀쩡히 일하던 제너레이터에게 갑자기 폭탄을 던지는 격, 클래스 방식은 상태 변수(State Variable)를 바꿔서 스스로 비상 상황임을 판단하고 다른 일을 하도록 만드는 것
    - 상태를 전이시킨다
        - 상태(State): 기계의 현재 모드. (예: 정상 모드, 에러 모드, 점검 모드)
        - 전이(Transition): 상태를 바꾸는 것. (예: 정상 $\rightarrow$ 에러)
        - 클래스 사용: 제너레이터 함수는 자기 상태를 저장하기 어렵지만, 클래스는 `self.mode` 같은 변수에 상태를 저장해두고 언제든 꺼내 볼 수 있다.
    - 코드 예시
    
    ```python
    class SmartCounter:
        def __init__(self, limit):
            self.limit = limit
            self.current = 0
            self.error_happened = False  # 예외 상황을 기록하는 '상태 변수'
    
        def __iter__(self):
            while self.current < self.limit:
                # 상태를 확인해서 동작을 결정함 (상태 전이 로직)
                if self.error_happened:
                    yield "에러 발생 수리 모드로 전환."
                    self.current = 0     # 에러 시 처음부터 다시 시작하도록 상태 전이
                    self.error_happened = False # 수리 완료 후 상태 복구
                else:
                    self.current += 1
                    yield self.current
    
    # 1. 객체 생성
    counter = SmartCounter(limit=5)
    it = iter(counter)
    
    # 2. 정상 작동
    print(next(it))  # 1
    print(next(it))  # 2
    
    # 3. 예외 상황 (throw 대신 속성을 직접 변경)
    print("--- 외부에서 문제 감지 ---")
    counter.error_happened = True
    
    # 4. 다음 yield 시 기계가 알아서 상태를 보고 동작을 바꿈
    print(next(it))  # 에러 발생 수리 모드로 전환.
    print(next(it))  # 1 (상태 전이 결과로 다시 1부터 시작)
    ```
    
    - 즉
        - 클래스 변수(`self.error_happened`)는 밖에서도 안에서도 접근할 수 있는 공유 스위치이다.
        - 밖에서 이 스위치를 조절해서 제너레이터의 다음 행동을 결정
        - 이것을 '상태를 전이시킨다'라고 표현

## 36. 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라

### 기억해야 할 내용

- 이터레이터나 제너레이터를 다루는 itertools 함수는 세 가지 범주로 나눌 수 있다.
    - 여러 이터레이터를 연결함
    - 이터레이터의 원소를 걸러냄
    - 원소의 조합을 만들어냄
- 파이썬 인터프리터에서 help(itertools)를 입력한 후 표시되는 문서를 살펴보면 더 많은 고급 함수와 추가 파라미터를 알 수 있으며, 이를 사용하는 유용한 방법도 확인할 수 있다.

직접 `for` 루프나 `yield`를 써서 복잡하게 로직을 짤 필요 없이, 이미 잘 만들어진 고성능 함수들을 가져다 쓰기만 하면 되는 라이브러리

1. `itertools`

- 여러 이터레이터 연결하기 (Linking)
    - 흩어져 있는 여러 데이터 묶음을 마치 하나의 긴 줄처럼 이어 붙이기
    - `chain`, `zip_longest`
- 원소를 걸러내기 (Filtering)
    - 데이터 뭉치에서 내가 원하는 것만 뽑아내거나, 특정 조건까지만 가져오는 도구
    - `islice`, `takewhile`, `dropwhile`
- 원소의 조합 만들기 (Combinations)
    - '경우의 수'처럼 데이터를 섞어서 모든 가능성을 만들어내는 도구
    - `product`, `permutations`, `combinations`

```python
import itertools

# 1. 연결하기 (chain)
# 리스트 두 개를 복사하지 않고 하나처럼 순회
odds = [1, 3, 5]
evens = [2, 4, 6]
combined = itertools.chain(odds, evens)
print(f"연결하기: {list(combined)}") # [1, 3, 5, 2, 4, 6]

# 2. 걸러내기 (islice)
# 제너레이터를 원하는 인덱스만큼만 자른다
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 중 index 3부터 7전까지
digits = range(10)
filtered = itertools.islice(digits, 3, 7)
print(f"걸러내기(3~6): {list(filtered)}") # [3, 4, 5, 6]

# 3. 조합 만들기 (product)
# 두 리스트의 모든 가능한 쌍(데카르트 곱)을 만든다.
directions = ['앞', '뒤']
speeds = [10, 20]
combos = itertools.product(directions, speeds)
print(f"조합 만들기: {list(combos)}") 
# [('앞', 10), ('앞', 20), ('뒤', 10), ('뒤', 20)]
```