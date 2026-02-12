### 계획
- [ ] 공부 계획

# 파이썬 코딩의 기술

![alt text](image.png)

~5장 까지

기본적으로 이 책은 하나의 커더란 강의라기 보다, 여러 조언들을 모은 느낌이다.

가볍게 읽고.

각 조언들의 결론 위주로 쭉 적으면 될 것 같다.

https://github.com/gilbutITbook/080235


# 1장 파이썬답게 생각하기

파이썬 커뮤니티에서 'Pythonic'이라는 형용사가 있다. 

파이썬 언어를 사용하고, 서로 협업하는 경험이 쌓여 시간이 지남에 따라 저절로 생긴 것이다.

이 장에서는 파이썬에서 가장 자주 하는 일을 수행하는 가장 좋은 방법을 알려준다.

## Better way 3 bytes와 str의 차이를 알아두라

파이썬에서 string을 표현하는데 str과 bytes가 있다.

- str: 유니코드 방식. 사람이 읽은 수 있는 글자 그 자체를 표현하는데 중점.

- bytes: 컴퓨터가 이해하는 0과 1의 8비트로 구성됨. 일명 `utf-8`.

별거 중요한건 서로 호환 안됨. 

예를 들어 서로 더하고 빼는게 직접적으로 안됨.

대부분의 경우 그냥 str을 쓰겠지만, 외부와 통신할 때 bytes를 많이 씀.


## Better way 4 C 스타일 형식 문자열을 str.format과 쓰기보다는 f-문자열을 통한 인터폴레이션을 사용하라

파이썬에서 문자열 안에 인수 집어넣고 출력하는데 여러 방식이 있음.

- C 스타일의 `%`를 사용하는 방식

- str.format 방식

- 인터폴레이션을 이용하는 f"" 방식

다 필요 없고 그냥 인터폴레이션, 즉 f""를 사용하면 됨.

## Better way 5 복잡한 식을 쓰는 대신 도우미 함수를 작성하라

파이썬으로 코드를 짧게 쓰는 것은 쉽다.

하지만 굳이 그러지말아라, 가독성과 유지보수성이 내려간다.

- 이렇게 쓰지말고

```py
from urllib.parse import parse_qs

my_values = parse_qs('빨강=5&파랑=0&초록=',
                     keep_blank_values=True)
print(repr(my_values))

# 질의 문자열이 `빨강=5&파랑=0&초록='인 경우
red = my_values.get('빨강', [''])[0] or 0
green = my_values.get('파랑', [''])[0] or 0
opacity = my_values.get('투명도', [''])[0] or 0
print(f'빨강: {red!r}')
print(f'초록: {green!r}')
print(f'투명도: {opacity!r}')
```

- 그냥 이렇게 써라

```
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        return int(found[0])
    return default

green = get_first_int(my_values, '초록')
```

- 함수를 하면 가독성을 더 높을뿐더러, 더 범용적으로 사용될 수도 있고, 무엇보다 반복을 줄일 수 있다.

- 짧게한줄에 쓰는 것보다 가독성을 잘 높이는 것이 훨씬 더 가치 있는 일이라는 것을 명심해라.


## Better way 6 인덱스를 사용하는 대신 대입을 사용해 데이터를 언패킹하라

- 튜플 안에 튜플을 넣을 수 있으니 딕셔너리를 이렇게 간단하게 튜플로 바꿀 수 있다.

```py
>>> snack_calories = {
...     '감자칩': 140,
...     '팝콘': 80,
...     '땅콩': 190,
... }
>>> items = tuple(snack_calories.items())
>>> print(items)
(('감자칩', 140), ('팝콘', 80), ('땅콩', 190))
```

### 다음 과정을 **언패킹**이라고 부른다.

```py
item = ('호박엿', '식혜')
first, second = item # 언패킹
print(first, '&', second)
```

이는 꼭 튜플에만 적요할 수 있는 것이 아니다.
- 이 언패킹을 이용해 서로 맞교환 같은 것이 가능하다.

이렇게 다음과 같이 중계 변수를 사용해서 쓰는 것을...

```py
temp = a[i]
a[i] = a[i-1]
a[i-1] = temp
```

아래와 같이 초간단하고, 직관성도 좋게 바꿀 수 있다!!!

```py
a[i-1], a[i] = a[i], a[i-1] # 맞바꾸기
```

- 물론 가장 쓸모 있을 때는 아마 무언가르 한번에 언패킹할 때일 것이다.

```py
snacks = [('베이컨', 350), ('도넛', 240), ('머핀', 190)]
```

위 같은 복잡한 리스트가 있을때, 그 속의 요소들을 그냥 빼면 아마 이린식이겠지만...

```py
for i in range(len(snacks)):
    item = snacks[i]
    name = item[0]
    calories = item[1]
    print(f'#{i+1}: {name} 은 {calories} 칼로리입니다.')
```

언패킹에 enumerate까지 사용하면 훨씬 깔끔해지고 가독성도 높아진다.

```py
for rank, (name, calories) in enumerate(snacks, 1):
    print(f'#{rank}: {name} 은 {calories} 칼로리입니다.')
```

## Better way 7 range보다는 enumerate를 사용하라 066

- for 문에서 range()와 len(리스트) 이런걸 많이 사용한다. (주로 리스트 + 번호가 필요할 때 이렇게 많이 씀)

```py
flavor_list = ['바닐라', '초콜릿', '피칸', '딸기']

for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print(f'{i + 1}: {flavor}')
```
```bash
1: 바닐라
2: 초콜릿
3: 피칸
4: 딸기
```
- 하지만 그런것보다 그냥 **enumerate**를 많이 사용해라. 그게 가독성이 훨씬 더 좋다.

```py
for i, flavor in enumerate(flavor_list):
    print(f'{i + 1}: {flavor}')
```

아니면 뒤에 번호 추가해서 시작 숫자를 정할 수도 있고.
```py
for i, flavor in enumerate(flavor_list, 1):
    print(f'{i}: {flavor}')
```

> 참고로 enumerate는 놀랍게도 제네레이터이다. 구체적으로 enumerate는 이터러블 루프를 감싸고 인덱스와 value를 쌍으로 넘겨주는 역학을 하는 제네레이터인 것이다.

그렇기에 이런식으로 우리가 흔히 보는 제네레이터 사용 방식 처럼 사용이 가능하다.

```py
it = enumerate(flavor_list)
print(next(it))
print(next(it))
```

## Better way 8 여러 이터레이터에 대해 나란히 루프를 수행하려면 zip을 사용하라

- 우리는 가끔씩 루프를 돌릴때 동시에 두개 이상의 이터러블을 사용한다.

예를 들어 한 리스트 속의 문자열 길이를 구하는 또다른 리스트가 있으면.

```py
names = ['Cecilia', '남궁민수', '毛泽东']
counts = [len(n) for n in names]
print(counts)
```

- 이 경우 zip을 쓰면 매우 편리하다.

(가장 긴 문자열 반환하기)

```py
for name, count in zip(names, counts):
    if count > max_count:
        longest_name = name
        max_count = count

print(longest_name)
```

- 심지어 **제네레이터는 한번에 하나씩만 불러오기에 메모리를 많이 아낄 수 있다**.

## Better way 9 for나 while 루프 뒤에 else 블록을 사용하지 말라

- 몰랐는데 for/while문 뒤에 무조건 실행되는 else 블록을 추가할 수 있음. 계속 모르고 있을 것.

## Better way 10 대입식을 사용해 반복을 피하라 (Walrus)

- 원래 아래 코드는 안된다.
```py
fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5,
}

if count = fresh_fruit.get('lemon', 0): # if문 입력 중에 바로 무언가를 넣을 수 없다.
    print(count)
```

원래는 위 count를 위에서 먼저 지정하고, if 문에 집어 넣는다.

- 하지만 **왈러스 연산자**라면?? (Walrus Operator)

쌉가능이다.

```py
if count := fresh_fruit.get('lemon', 0): # if문 입력 중에 바로 무언가를 넣을 수 없다.
    print(count)

print(count)
```

더 간단한 예시

```py
numbers = [1 , 2]

if count := numbers[1] : # if문 입력 중에 바로 무언가를 넣을 수 없다.
    print(count)
```

왈러스 연산자를 통해 더 가독성을 높일 수 있는 것이다.

- 물론 if문 말고 while이나 List Comprehension에도 적용 가능하다.

```py
# while에 왈러스 연산자
while (data := input("입력하세요 (종료: q): ")) != 'q':
    ...
# List comprehension에 왈러스 연산자
result = [res for x in numbers if (res := complex_calc(x)) > 13]
```

- 참고로 Walrus는 바다 코기리라는 뜻이다.

![alt text](image-1.png)

`:=`   <- 이거랑 닮아서 그렇게 만든 것이다.

# 2장 리스트와 딕셔너리

파이썬에서 정보 조직화의 가장 일반적인 방법은 리스트이다. 

여기서 리스트를 자연스럽게 보완해주는 존재가 딕셔너리이다.

이 장에서는 이들을 사용하는 것을 배운다.

- 딕셔너리. 키와 연관된 값을 주로 해시 테이블(hash table)에 저장하는 방식이다. 그리고 이는 특정 값을 찾을 때 시간 복잡도가 낮아 효율적이다.

- 파이썬은 이 리스트와 딕셔너리를 다룰 때 가독성을 좋게하고 기능을 확장해주는 특별한 구문과 모듈을 많이 제공한다.

## Better way 11 시퀀스를 슬라이싱하는 방법을 익혀라

유용한 슬라이싱 팁

- 슬라이싱을 조금 크게 해도 없는 값은 알아서 무시가 된다.

```py
a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

first_twenty_items = a[:20]
print(first_twenty_items)
```
`['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']`

근데 특정 지정은 안된다.
```py
a[20]
```

- 리스트 `a = b`와 `a = b[:]`는 다르다.

a = b는 a가 이제 b의 리스트 그 자체를 참조하는 것이다.
```py
a = [1, 2]
b = ['태','오']

a = b

b[:] = ['Theo'] # 만약 여기서 내용물은 바꾼다면? (참고로 그냥 `b =`는 아예 새로운 리스트를 만드는거라 `b[:]=`를 사용해야함. )

print(a)
```
놀랍게도 a도 같이 수정된다!
```
>>> print(a)
['Theo']
```

- 만약 리스트 참조가 아닌 복사를 원한다면 `a = b[:]`를 사용해야한다.

## Better way 12 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라

아래에서 앞에 2,6이 슬라이싱, 그리고 뒤에 -2가 스트라이딩이다 (그만큼 간격을 주고 계속 띄어서 입력하는 것.).

```py
x[2:6:2] 
```
- 위와 같은 방식으로 슬라이싱과 스트라이딩을 한번에 진행하는 경우가 많다.

- 하지만 그러지말아라. 줄을 늘리더라도 슬라이싱과 스트라이딩을 개별적으로 해라.

대충 아래 처럼.
```py
y = x[2:6]
z = y[::-2]
```

> 이유는 가독성이 떨어져서임. 뭔가 잘 적으면 한번 잘 굴러가게 만들 수 있겠지만, 이 코드를 보는 사람 입장에서 그 범위를 인지하기 쉽지 않음.

## Better way 13 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라 (`*`)

- 언패킹 과정에서 언패킹 하려는 인수보다 이터러블에 있는 value가 더 많으면 에러가난다.

```py
car_ages = [0, 9, 4, 8, 7, 20, 19, 1, 6, 15]
car_ages_descending = sorted(car_ages, reverse=True)

oldest, second_oldest = car_ages_descending # 오류 발생!!
```

원래라면 앞에 2개만 남기고 슬라싱을 한 뒤에 2개만 언패킹하는 과정을 지냈을 것이다.

- 하지만 그러면 가독성도 떨어지고, 무엇보다 더 편한 방법이 있다.
    - 바로 `*인수`로 나머지 모든 것을 **리스트**로 받아들리는 것이다.
```py
oldest, second_oldest, *others = car_ages_descending # *other이 모든 것을 받았으니 걱정말라구!
print(oldest, second_oldest, others)
```
`20 19 [15, 9, 8, 7, 6, 4, 1, 0]`

`*인수`로 받은 것은 위에 우측에 볼 수 있는 것 처럼 리스트로 반환된다.

- 하지만 그렇기에 메모리를 한번에 많이 잡아먹을 수 있고. 메모리가 이 리스트 전체를 다 핸들링 할 수 있을거라고 확신할때만 사용해라.


## Better way 14 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라

- 신기하게도 튜플 비교가 가능하다.

```py
saw = (5, '원형 톱') # 좌측이 무게, 우측이 공구를 표현
jackhammer = (40, '착암기')
assert not (jackhammer < saw) # 예상한 대로 결과가 나온다
```
위에 보면 알겠지만 가장 좌측을 우선해서 계산하고.

```py
drill = (4, '드릴')
sander = (4, '연마기')
assert drill < sander        # 그러므로 드릴이 더 먼저다
```

만약에 중복이다? 그러면 그때 뒤를 비교하는 것이다. (여기서는 문자열 비교)

## Better way 15 딕셔너리 삽입 순서에 의존할 때는 조심하라

- 파이썬 3.7 이후 딕셔너리의 순서에 의존하는 것이 가능해졌다.


```py
votes = {
    'otter': 1281,
    'polar bear': 587,
    'fox': 863,
}

def populate_ranks(votes, ranks_output):
    names = list(votes.keys())
    names.sort(key=votes.get, reverse=True)
    for i, name in enumerate(names, 1):
        ranks_output[name] = i

def get_winner(ranks):
    return next(iter(ranks))

ranks = {}
populate_ranks(votes, ranks)
print(ranks)
winner = get_winner(ranks)
print(winner)
```

> 참고로 이렇게 리스트를 넣고, 그 안에서 리스트를 수정했을 때, 원본도 그 수정사항이 반영된다.

- 대부분의 경우에서는 그렇게 해도 되지만. 딕셔너리의 형태의 클래스를 이용 중이면 키 순서가 보존된다고 가정할 수 없다.

## Better way 16 in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라

- 만약에 딕셔너리에 원하는 키가 없으면 어떻게 키를 추가하고 value를 집어넣는게 좋을까??

어떤 키에 대한 값을 1씩 추가하는 프로그램이 있다면

아마 아래 처럼 하는 것이 일반적일 것이다.

```py
counters = {
    '품퍼니켈': 2,
    '사워도우': 1,
}

key = '밀'

if key in counters: # 조회 1번
    count = counters[key] # 조회 2번
else:
    count = 0

counters[key] = count + 1 # 조회 3 번
```

만약 값이 있다면 위 기준으로 조회를 3번 한다.

위 방법 보다 조금 더 효율적인 방법이 있다.

- 바로 오류를 사용해서 넣는 것이다.

```py
try:
    count = counters[key] # 조회 1번
except KeyError:
    count = 0

counters[key] = count + 1 # 조회 2번
```

오오오, 신기하다.

- 하지만 이거말고 더 가독성 좋은 방식이 있다.

바로 딕셔너리 매서드 get을 사용하는 것이다!

**`딕셔너리.get(키,만약에없으면넣을값)`**

```py
count = counters.get(key, 0)
counters[key] = count + 1
```

그러면 깔끔하고, 빠르기까지 한다.

> 참고로 딕셔너리.get(키, 0)이 하는 일은 그 키의 value를 가져오고, 만약 그 키가 없으면 0을 반환하라는 것이다.

```py
key = '밀'

# 방법 A: 대괄호 사용
# count = counters['밀']  # <--- 여기서 KeyError 발생! (프로그램 종료)

# 방법 B: get 사용
count = counters.get('밀', 0) # <--- 없으면 0을 담고 다음 줄로 진행!
```

## Better way 17 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라

- 만약 리스트를 요소로 가지는 딕셔너리에서 키와 요소를 추가할 필요가 있을 때. setdefault 함수를 사용할 수 있다.
```py
visits = {
    '미국': {'뉴욕', '로스엔젤레스'},
    '일본': {'하코네'},
}

visits.setdefault('프랑스', set()).add('칸') # 짧다

print(visits)
```

- 이를 클래스로 작동시킬시 다음과 같이 할 수 있다.

```py
class Visits:
    def __init__(self):
        self.data = {}

    def add(self, country, city):
        city_set = self.data.setdefault(country, set())
        city_set.add(city)

visits = Visits()
visits.add('러시아', '예카테린부르크')
visits.add('탄자니아', '잔지바르')
print(visits.data)
```

- 하지만 이 보다 더 효율적인 **defauldict** 함수가 있다.

```py
class Visits:
    def __init__(self):
        self.data = defaultdict(set)

    def add(self, country, city):
        self.data[country].add(city)

visits = Visits()
visits.add('영국', '바스')
visits.add('영국', '런던')
print(visits.data)
```

위 방식으로 매번 디폴트로 쉽게 요소와 키를 추가할 수 있다. 

## Better way 18 __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라

- 경우에 따라 setdefault와 defaultdict 둘다 사용하기가 애매한 경우도 발생한다.

이 경우 `__missing__`인자를 클래스에 사용해서 키가 없을때를 핸들링 할 수 있다.

```py
class Pictures(dict):
    def __missing__(self, key):
        value = open_picture(key)
        self[key] = value
        return value

pictures = Pictures()
handle = pictures[path]
handle.seek(0)
image_data = handle.read()
```

# 3장 함수

파이썬 함수는 너가 원하는 일을 편하게 할 수 있도록 도와주는 장치가 생각보다 많다.

그 중에서 다른 언어에는 없는 것도 많다.

이 장에서는 함수를 사용해 의도를 명확히 밝히는 동시에, 재사용성 챙기고 버그를 줄이는 방법을 다룬다.

## Better way 19 함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹하지 말라

- 언패킹 4개 이상 부터는 가독성과 유지보수성이 떨어진다. 가급적 적게 유지해라.

아래를 보면 이게 왜 그런지 알 수 있다. 만약 순서가 꼬이면 바로 찾기 귀찮은 에러가 되는 것이다.

```py
minimum, maximum, average, median, count = get_stats(lengths)
```

많은 경우 작은 클래스 메서드로 세분화해라.

## Better way 20 None을 반환하기보다는 예외를 발생시켜라

- 함수 오류를 처리할 때 오류말고 None을 반환하는 경우가 있다.

```py
def careful_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

- 는 그러지말고 그냥 오류가 났을때는 확실히 오류가 났다고 해라. 

아니면 윗단에서 None을 굳이 처리해야 한다.

- 그냥 오류 raise를 하고, docstring으로 잘 정리하는 것이 더 좋다.

```py
def careful_divide(a: float, b: float) -> float:
    """a를 b로 나눈다.

    Raises:
        ValueError: b가 0이어서 나눗셈을 할 수 없을 때
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('잘못된 입력')
```

> **중요**: Docstring은 나중에 `help(함수)`으로 docstring을 외부에서 출력받을 수 있는 좋은 기능을 내포하고 있다!

## Better way 21 변수 영역과 클로저의 상호작용 방식을 이해하라

- **함수도 일급시민 객체**다. 그렇기에 변수에 대입되거나, 다른 함수에 인자로 전달될 수 있다.

- 그렇기에 함수를 클러저 형태로 사용할 수 있는 것이다.

클로저는 자신의 영역 밖에서 정의된 변수를 참조할 수 있는 상태나 현상을 말한다.

```py
def sort_priority(values, group):
    def helper(x): # 여기서 이 helper 함수를 클로저라고 부르기도한다.
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8, 3, 1, 2, 5, 4, 7, 6]
group = {2, 3, 5, 7}
sort_priority(numbers, group)
print(numbers)
```

- 하지만 주의할 것이 클로저가 일어나는 현상 내외부 함수 서로끼리 변수가 소통하지 않는다.

```py
def sort_priority2(numbers, group):
    found_ = False
    def helper(x):
        if x in group:
            found_ = True # 문제를 쉽게 해결할 수 있을 것 같다
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found_

found = sort_priority2(numbers, group)
print('발견:', found) # 하지만 결과는 False다, 외부 함수의 값만 나온 것이다.
print(numbers)
```

- 만약 내외부 변수끼리 소통하기 싶으면 nonlocal를 사용하면 된다.

```py
def sort_priority2(numbers, group):
    found = False
    def helper(x):
        nonlocal found       # 추가함
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found
```

하지만 그렇게 추천되는 방식은 아니다.

## Better way 22 변수 위치 인자를 사용해 시각적인 잡음을 줄여라

- 그동안 함수 가변 인수를 무조건 `*args`로 사용해야하는 줄 알았는데.. **알고보니 아니다**.

아무거나 앞에 `*`를 붙여도 되긴하다.
```py
def my_function(*a):
    for item in a:
        print(item)

my_function(1, 2, 3) # a는 (1, 2, 3)이라는 튜플이 됩니다.
```

물론 관례적으로 args라는 말을 많이 쓰는 것이니 지켜서 나쁠 것은 없다.

- 파이썬에서 `*`의 의미는 시퀀스의 요소들을 전부 넘긴다는 것이다.

그렇기에 만약 제네레이터 작동 앞에 붙이면 제네레이터는 끝까지 가동된다.

```py
def my_generator():
    for i in range(10):
        yield i

def my_func(*args):
    print(args)

it = my_generator()
my_func(*it)
```
`(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)`

한번에 이렇게 출력됨.

## Better way 23 키워드 인자로 선택적인 기능을 제공하라

- 위와 비슷하게 함수 인수로 `**인수`를 사용해라.

```py
def print_parameters(**kwargs):
    for key, value in kwargs.items():
        print(f'{key} = {value}')

print_parameters(alpha=1.5, beta=9, 감마=4)
```

- 또는 함수를 호출하는 단계에서 집어넣을 수 있다.

```py
def add(a,b):
    print(a + b)

numbers = {'a': 1, 'b': 2}
add(**numbers) # 딕셔너리의 value들을 한번에 집어넣기!
```

> 참고로 assert의 기능은 그 뒤 조건이 False일때 오류를 일으키기 위함이다.
```py
def remainder(number, divisor):
    return number % divisor
# 만약 누군가 실수를 해서 20 % 7의 결과가 6이 아니라고 생각한다면?
assert remainder(20, 7) == 6  # 20 % 7은 6이 맞으므로 아무 일 없음.
# 만약 아래처럼 잘못된 기대를 한다면?
assert remainder(20, 7) == 5  # 여기서 AssertionError 발생!
```

## Better way 24 None과 독스트링을 사용해 동적인 디폴트 인자를 지정하라

- 함수 디폴트를 절할때가 많다.

하지만 이런 디폴트 값들이 때때로 변해야할때가 있다.

```py
from time import sleep
from datetime import datetime

def log(message, when=datetime.now()):
    print(f'{when}: {message}')

log('안녕!')
sleep(0.3)
log('다시 안녕!')
```
위에 코드를 보면 0.3초의 timestep 차이가 있을거라고 생각하기 쉽다.

하지만 실제로 찍어보면 둘이 완전히 똑같다.

- 이유는 함수의 디폴트 값이 코드 실행 **처음 한번만 지정**되기 때문이다. **이를 동적으로 만들 수 없다**!

(더 가관인 것은 만약에 Mutable인 리스트를 디폴트로 지정했고, 한쪽에서 이를 수정했으면 다른쪽에서도 그 수정이 반영되는 진귀한 관경을 볼 수 있다. (같은 메모리를 쓰기 때문))

- 그냥 디폴트가 안들어오면 (None) 개별적으로 핸들링하는게 좋다.

물론 이를 위해 Docstring에 이 현상을 잘 설명해야할 것이다.

```py
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
sleep(0.3)
log('다시 안녕!')
```

이제야 타임스탭의 차이가 보인다.

## Better way 25 위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 해서 함수 호출을 명확하게 만들라

- 위치 인자: 
```py
def introduce(name, age):
    print(f"이름은 {name}이고, 나이는 {age}살입니다.") 

# 순서가 중요합니다!
introduce("태오", 25)
```

- 키워드 인자:
```py
# 순서 바꿔도 상관 ㄴㄴ
introduce(age=25, name="태오")
```

- 몇개 없으면 위치 인자로만 괜찮을 수도 있음.

- 하지만 많아지면 키워드 인자를 사용하는게 함수 사용자에게 좋다.

- 둘이 혼용할 경우 다음과 같이 구별해주는게 좋다.

```py
def safe_division_e(numerator, denominator, /,
                    ndigits=10, *,                 # 변경
                    ignore_overflow=False,
                    ignore_zero_division=False):
```
- `/` **앞**에 오는 매개변수들은 오직 위치 인자로만 지정 필요
- `*` **뒤**에 오는 매개변수들은 오직 키워드 인자로만 지정 필요

## Better way 26 functools.wrap을 사용해 함수 데코레이터를 정의하라

- @wrap이라는 외부 데코레이터를 사용해서 너가 만든 데코레이터를 데코레이트해라.

만약에 너가 함수를 만들고, 안에 docstring를 작성했다고 가정해보자.

- 하지만 만약에 그 함수에 데코레이터를 올려두면, help()같은 함수를 쓰면 붙인 데코레이터 설명이 나오면 나왔지 알고 싶은 함수가 나오지 않는다.


```py
def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}') # 게다가 현재 함수명인 `func.__name__`도 wrapper로 나오지 원래 이 함수의 의도인 데코레이트한 함수명이 나오지 않는다.
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return n 번째 피보나치 수"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

help(fibonacci) # wrapper로 나온다.
```

- 이 경우를 방지하기 위해 데코레이터 안의 wrapper 함수에 외부 모듈로 불러온 `@wrap`을 붙여라

```py
from functools import wraps

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__name__}({args!r}, {kwargs!r}) '
              f'-> {result!r}')
        return result
    return wrapper


@trace
def fibonacci(n):
    """Return n 번째 피보나치 수"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

help(fibonacci) # 피보나치 함수의 설명이 잘 나온다.
```

# 4장 컴프리헨션과 제너레이터

파이썬은 쉽게 이터레이션하면서, 다른 데이터 구조를 파생시킬 수 있는 특별한 문법을 제공한다.

파이썬은 함수가 한번씩 변환하는 이터레이션 가능한 값의 스트림을 만들 수 있게 허용한다.

이 장에서는 이런 기능을 사용해 성능을 높이고, 메모리 사용을 줄이며, 가독성을 향상시키는 방법을 설명한다.


## Better way 27 map과 filter 대신 컴프리헨션을 사용하라
## Better way 28 컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하지 말라
## Better way 29 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하라
## Better way 30 리스트를 반환하기보다는 제너레이터를 사용하라
## Better way 31 인자에 대해 이터레이션할 때는 방어적이 돼라
## Better way 32 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용하라
## Better way 33 yield from을 사용해 여러 제너레이터를 합성하라
## Better way 34 send로 제너레이터에 데이터를 주입하지 말라
## Better way 35 제너레이터 안에서 throw로 상태를 변화시키지 말라
## Better way 36 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라



# 5장 클래스와 인터페이스

파이썬은 객체 지향 언어이다. 모든게 객체다!

이 장에서는 클래스를 사용해 의도하고 있는 행동 방식을 어떻게 객체로 표현하는지를 보여준다.


## Better way 37 내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성하라
## Better way 38 간단한 인터페이스의 경우 클래스 대신 함수를 받아라
## Better way 39 객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라
## Better way 40 super로 부모 클래스를 초기화하라
## Better way 41 기능을 합성할 때는 믹스인 클래스를 사용하라
## Better way 42 비공개 애트리뷰트보다는 공개 애트리뷰트를 사용하라
## Better way 43 커스텀 컨테이너 타입은 collections.abc를 상속하라



