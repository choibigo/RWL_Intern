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


## Better way 8 여러 이터레이터에 대해 나란히 루프를 수행하려면 zip을 사용하라

## Better way 9 for나 while 루프 뒤에 else 블록을 사용하지 말라

## Better way 10 대입식을 사용해 반복을 피하라


# 2장 리스트와 딕셔너리

파이썬에서 정보 조직화의 가장 일반적인 방법은 리스트이다. 

여기서 리스트를 자연스럽게 보완해주는 존재가 딕셔너리이다.

이 장에서는 이들을 사용하는 것을 배운다.

## Better way 11 시퀀스를 슬라이싱하는 방법을 익혀라


## Better way 12 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라

## Better way 13 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라

## Better way 14 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라

## Better way 15 딕셔너리 삽입 순서에 의존할 때는 조심하라

## Better way 16 in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라

## Better way 17 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라

## Better way 18 __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라


# 3장 함수

파이썬 함수는 너가 원하는 일을 편하게 할 수 있도록 도와주는 장치가 생각보다 많다.

그 중에서 다른 언어에는 없는 것도 많다.

이 장에서는 함수를 사용해 의도를 명확히 밝히는 동시에, 재사용성 챙기고 버그를 줄이는 방법을 다룬다.

## Better way 19 함수가 여러 값을 반환하는 경우 절대로 네 값 이상을 언패킹하지 말라
## Better way 20 None을 반환하기보다는 예외를 발생시켜라
## Better way 21 변수 영역과 클로저의 상호작용 방식을 이해하라
## Better way 22 변수 위치 인자를 사용해 시각적인 잡음을 줄여라
## Better way 23 키워드 인자로 선택적인 기능을 제공하라
## Better way 24 None과 독스트링을 사용해 동적인 디폴트 인자를 지정하라
## Better way 25 위치로만 인자를 지정하게 하거나 키워드로만 인자를 지정하게 해서 함수 호출을 명확하게 만들라
## Better way 26 functools.wrap을 사용해 함수 데코레이터를 정의하라


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



