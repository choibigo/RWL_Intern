### 계획
- [x] PEP 8 탐색 및 스터디 구상
- [ ] 전문 읽기 및 필요 내용 작성

# PEP 8

![alt text](images/p8_0_image.png)

https://peps.python.org/pep-0008/

PEP 8은 파이썬 코드 작성시 지켜야하는 공식 스타일 가이드. 코드는 작성하는 시간 보다 읽는 시간이 훨씬 길기에 가독성을 높이는 것이 목표.

들여쓰기, 이름 짓기, 코드 레이아웃 등, 다양한 규칙이 존재함.

해당 가이드라인은 어디까지는 기본적인 기준일 뿐이며, 만약 특정 프로젝트나 코드에서 다른 가이드라인을 이용하고 있다면 해당 환경에 맞추는 것이 맞다.

## Code Lay-out

### Indentation

- 파이썬은 기본적으로 들여쓰기로 많은 것을 구분하기에 매우 중요하다.

들여쓰기는 스페이스 4칸이 기준.

```py
# Arguments는  () 기준으로 배치되는 것이 좋다.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

```py
# 함수 내부와 분리되는 것이 보여야한다.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

> 참고로 VScode 설정에서 Tab을 space 여러개로 바꿀 수 있다. ctrl+shit+p로 들어가서 설정을 space으로 바꿔주자. 그리고 size를 4로 할당하자.
![alt text](image.png)


### Maximum Line Length

- 모든 파이썬 줄은 최대 **79**자를 넘기면 안된다.

- 주석 텍스트의 경우 최대 **72**자.

```py
# 참고로 아래가 각각 총 72자다 (공백 포함)
# Tabs should be used solely to remain consistent with code that is alr
# 참고로 VScode 설정에서 Tab을 space 여러개로 바꿀 수 있다. ctrl+shit+p로 들어가서 설정을 space으로 
```

### 연산자 배치

- 여러 연산자를 배치할 때 연산자를 앞으로 배치하여 가독성을 높인다.

```py
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

### Blank Lines

- 함수 정의와 클래스 정의는 서로 두 줄 공백을 뛴다.

- 한 클래스 내부의 함수끼리는 한 줄만 뛴다.

**가급적 줄 공백 사용을 지양한다.**

### Imports

- Import는 항상 파일 맨 상단에 배치해야한다.

- Import 순서는:

    1. 파이썬 스탠다드 라이브러리
    1. 관련 서드파티 라이브러리
    1. 로커 어플리케이션, 또는 개별 특정 라이브러리.

- Import시 가급적 한 import에 호출하는 것이 하나여야한다.


```py
import os
import sys
```

- 다만 from import와 같이 특정 모듈을 여럿 가져올때는 한줄에 여러개를 사용한다.

```py
from subprocess import Popen, PIPE
```

- 가급적 모든 모듈을 가져오는 `*`는 사용하지 않는다.

### Whitespace in Expressions and Statements (띄어쓰기)

- **가급적 띄워쓰기를 지양해야한다.**

```py
# Wrong:
spam( ham[ 1 ], { eggs: 2 } )
bar = (0, )
if x == 4 : print(x , y) ; x , y = y , x
```

```py
# Correct:
spam(ham[1], {eggs: 2})
foo = (0,)
if x == 4: print(x, y); x, y = y, x
```

- 연산자 양쪽에는 띄어쓰기를 넣는다

```py
# Wrong:
i=i+1
i= i+ 1

# Correct:
i = i + 1
```

- 하지만 키워드 내부 `=` 등호에는 띄어쓰기를 추가하지 않는다.

```py
# Wrong:
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)

# Correct:
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
```


- 어노테이션에서 쓰는 화살표 양쪽도 띄워주기를 사용한다.

```py
def munge(input: str) -> int:
    return len(input)
# 참고로 어노테이션은 부가 정보 출력에 사용한다. 예를 들어 매개변수 정보 출력은 진행한다.
print(munge.__annotations__)
# 출력: {'input': <class 'str'>, 'return': <class 'int'>}
```

- 세미쿨룽 `;`을 사용하는게 가능하지만 가급적 사용하지 말아라.

- if/else/for/while 같은 것을 사용할 때 부피를 줄일 수 있는데, 딱히 그럴 필요 없으면 자리를 더 차지해도 그렇게 놔둬라. 짧아지면 그만큼 더 읽기가 어렵다.

```py
# Wrong:
if foo == 'blah': do_blah_thing()
for x in lst: total += x
while t < 10: t = delay()
if foo == 'blah': do_blah_thing()
else: do_non_blah_thing()
if foo == 'blah': one(); two(); three()
```

## When to Use Trailing Commas (쉼표는 언제 사용해야 할까)

- 문법적인 오류가 없더라고 쉼표는 가급적 어디 안에 넣어두는 것으로 해라.

```py
# Wrong:
FILES = 'setup.cfg',

# Correct:
FILES = ('setup.cfg',)
```

## Comments

- 주석 설명은 가급적 완전한 문장으로 마무리해라.

- 당연하지만 첫 글자는 대문자로 한다.
    - 하지만 첫 글자가 소문자로 시작하는 명칭이면 소문자로 시작해도 괜찮다.

- 주석은 언제나 영어로 작성해라.

### Documentation Strings (docstrings)

- 공개되는 코드에는 docstrings을 달아주는 것이 좋다.

- 각 코드 상단 및 함수 `def` 바로 아래에 설명을 기입하면 된다.

```py
"""Return a foobang

Optional plotz says to frobnicate the bizbaz first.
"""

"""Return an ex-parrot."""
```

## Naming Conventions (네이밍 규칙)

- 파이썬의 명명 규칙은 이미 혼돈이다. 하지만 그럼에도 일정하기 위해서 노력해야한다.

- 네이밍에는 다양하는 방법이 있다.
    - `b` (single lowercase letter)
    - `B` (single uppercase letter)
    - `lowercase`
    - `lower_case_with_underscores`
    - `UPPERCASE`
    - `UPPER_CASE_WITH_UNDERSCORES`
    - `CapitalizedWords` (or CapWords, or CamelCase – so named because of the bumpy look of its letters [4]). This is also sometimes known as StudlyCaps.
        - Note: When using acronyms in CapWords, capitalize all the letters of the acronym. Thus HTTPServerError is better than HttpServerError.
    - `mixedCase` (differs from CapitalizedWords by **initial lowercase** character!)

- `single_trailing_underscore_`: 중복 방지를 하려고할 때 위해 뒤에 `_`를 붙인다.

- `__double_leading_and_trailing_underscore_`: 양쪽 언더바 두개씩. 현 네임스페스에서 특별한 attributes이나 object에만 할당함. 새로 창조하지말것. (예:  `__init_`_, `__import__` or `__file__`)

### 피해야할 명칭

- 절대로 `l` (소문자 L), `O` (대문자 o), `I` (대분자 i)를 홀소 사용하지말아라. 어떤 폰트에서는 아예 구별이 안될 수도 있다. 

### Package와 Module

- 패키지와 모듈이름은 소문자를 사용해라. `_`는 사용가능하다.

### Class

- 클래스는 기본적으로 CapitalizedWords 체계를 사용한다.

### Function and Variable Names

- 변수와 함수는 기본적으로 소문자와 언더바를 사용한다. 

> 타입 변수의 경우 CapitalizedWords을 사용.

### Constants

- 상수는 대문자와 언더바를 사용한다.


## Programming Recommendations

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```

```py

```