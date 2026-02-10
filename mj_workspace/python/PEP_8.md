# PEP 8 – Style Guide for Python Code
###### PEP 8 (https://peps.python.org/pep-0008/)

---
### 바로가기
[1. Code Lay-out](#1-code-lay-out) <br>
[2. String Quotes](#2-string-quotes) <br>
[3. Whitespace in Expressions and Statements](#3-whitespace-in-expressions-and-statements) <br>
[4. When to Use Trailing Commas](#4-when-to-use-trailing-commas) <br>
[5. Comments](#5-comments) <br>
[6. Naming Conventions](#6-naming-conventions) <br>
[7. Programming Recommendations](#7-programming-recommendations) <br>

---

## 1. Code Lay-out
- **들여쓰기 (Indentation)**
    * **Space 4칸** 사용
    * `tab`보다는 **space**를 사용하고 둘을 혼합 사용하지 말 것
- **줄 바꿈되어 이어지는 줄 (Continuation lines)**
    1. 괄호 `()`, 대괄호 `[]`, 중괄호 `{}` 내부에서 vertical alignment
    2. 내어쓰기 (hanging indent)
        1. 첫 줄에는 arguments 두지 않음
        2. continuation line은 명확하게 구분될 수 있도록 추가 indentation을 사용.

###### Correct:
```python
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```
###### Wrong:
```py
# Arguments on first line forbidden when not using **vertical alignment.**
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable. (한번 더 들여써야함)
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```
- **if-statement**
    - if 문에서 conditional part가 길어 여러줄로 나뉘는 경우, `if` + space + `(`가 자연스럽게 4-space indent를 형성하는데 **PEP 8에서는 명시적인 해법 제시 X (가독성 좋게 작성하기)**

- **Closing bracket alignment**
    - **마지막 줄의 첫번째나, 문자 아래에 정렬**
###### 예시:
```py
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```
- **Maximum Line Length**
    - 모든 line은 **최대 79 characters**로 제한
    - 구조적 제약이 적은 긴 텍스트 블록(예: docstrings("""로 감싼 블럭), comments(주석))의 경우, line length는 72 characters로 제한
    - **여러 파일을 side by side로 열기 위함**
    - 긴 줄은 괄호 `()`, 대괄호 `[]`, 중괄호 `{}`를 사용하여 줄바꿈 하는 것을 권장.(`\`사용하여 줄을 나누는 것 보다 우선적으로 권장)
        - python 3.10 이전에서는 예외
```py
# 소괄호()를 사용하여 여러 줄로 나눔
def function_with_long_logic():
    # 전체 식을 소괄호로 감싸면 줄 바꿈이 자유로움
    if (this_is_a_very_long_variable_name > 100 and
            another_long_variable_name < 50 and
            yet_another_condition == True):
        return "Success"
# 리스트나 딕셔너리에서도 동일하게 적용
my_list = [
    'first_element', 'second_element', 'third_element',
    'fourth_element', 'fifth_element'
]
# python 3.10이전 : 백슬래시(\)를 사용한 방식
if this_is_a_very_long_variable_name > 100 and \
   another_long_variable_name < 50 and \
   yet_another_condition == True:
    return "Not Recommended"
```
**Line Break (Binary operator)**
연산자 위치를 아래 예시와 같이 표기하는게 가독성에 좋음
```py
# Correct: easy to match operators with operands
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction)
```
**Blank Lines (빈 줄)**
    - **Top-level 함수 및 클래스**는 정의 앞뒤로 **두 줄의 빈줄**
    - **클래스 내부 Method** : 각 메서드 정의 사이는 **한 줄**의 빈줄
    - 함수 내부 : 논리적인 Section을 구분하고 싶을때만 한 줄의 빈줄 사용 가능
    - 서로 관련된 함수 그룹을 다른 그룹과 분리하고 싶을때 추가 빈줄 사용가능
    - one-liners(ex. dummy, pass) : 빈줄 생략 가능
`"즉, 큰 덩어리(클래스/함수) 사이는 2줄, 작은 덩어리(메서드) 사이는 1줄, 함수 내부는 꼭 필요할 때만 1줄 비운다."`
```py
import sys


# 1. 최상위 함수/클래스 사이는 '두 줄' 비움
class MyFirstClass:
    # 2. 클래스 내부 메서드 사이는 '한 줄' 비움
    def method_one(self):
        pass

    def method_two(self):
        pass


def top_level_function():
    # 3. 함수 내부 논리 구분을 위해 드물게 한 줄 비움
    step_one = 1 + 1
    
    step_two = step_one * 2
    return step_two


# 4. 관련 있는 한 줄짜리들은 붙여 써도 됨
def dummy1(): pass
def dummy2(): pass
```
**Source File Encoding**
    - 항상 `UTF-8` 사용하고, 인코딩 선언 포함하지 말 것
    - 모든 식별자는 ASCII 문자만 사용해야하며, 가능한 한 영어 단어를 사용할 것
**Wrong:** (인코딩 선언 표시하지말 것.)
```py
# -*- coding: utf-8 -*-
# 또는
# coding=utf-8

def hello():
    print("안녕하세요")
```

**Imports**
- 아래 예시와 같이 사용 (각 줄에 하나, From만 여러개 가능)
- 모듈 주석(comments) 또는 Docstring 과 전역변수 및 상수 사이에 위치해야함
- 절대 경로를 권장함 `from my_project.utils import my_func`
    - 패키지 구조가 너무 복잡해서 절대 경로가 지나치게 길어질 때만 .을 사용한 상대 경로를 사용 `(예: from . import sibling)`
- 순서 (각 그룹 사이는 한 줄의 빈줄로 시각적 구분할 것)
    a. Standard Library (os, sys, time,...) : 파이썬 기본 모듈
    b. Third party (numpy, pandas,..) : pip install로 설치된 외부 라이브러리
    c. Local Library : 직접 만든 모듈이나 패키지
- from 모듈 import 클래스 형식이 일반적이지만, 이름이 중복되어 충돌이 나면 import 모듈 후 모듈.클래스 형태로 사용
- 와일드카드(`*`) 금지: `from 모듈 import *`는 어떤 이름이 들어오는지 알 수 없어 혼란을 주므로 절대 피해야 합니다.
- `__`로 감쏴진 Dunder import 및 번수 선언은 독스트링과 standard library import 사이에 들어가야한다.
    - Dunder = Double Underscore의 약자이며, 파이썬이 특별한 기능을 위해 미리 찜해둔 '예약어'들이다. 매직 메서드(Magic Method)라고도 부름 (Ex. `__new__`, `__init__`)
    

```py
"""~~~~~~~~~ㅁㄴㅇㄹㅁㄴㅇㄹ~~~~~~~~~예시 독스트링입니다."""

from __future__ import annotations  # 0 순위 (특수 임포트)

__all__ = ['func_a']               # 0.5 순위 (던더 변수)
__version__ = '1.0'

# 1. 표준 라이브러리 그룹
import os
import sys

# 2. 외부 라이브러리(Third Party) 그룹
import numpy as np
import requests

# 3. 로컬 프로젝트 그룹
from my_workspace.utils import helper_function

# 전역 변수나 상수는 임포트 아래에 위치
VERSION = "1.0.0"
```
----
## 2. String Quotes
- Python에서 single-quoted(\`)와 double-quoted(\")는 동일.
- 하나의 규칙을 정하고 일관되게 사용할 것을 권유 (백슬래시 사용을 피해서 가독성 향상 권유)
- """ ~~~ """ : 항상 double quote (docstring)
```py
# 권장
text = 'He said "Hello"'
# 비권장 : 백슬래시 사용
text = "He said \"Hello\""
```
----
## 3. Whitespace in Expressions and Statements
**Pet Peeves (절대 피해야할 공백)**
```py
# ------괄호 바로 안쪽 공백------
# Correct
spam(ham[1], {eggs: 2})
# Wrong
spam( ham[ 1 ], { eggs: 2 } )

# ------쉼표 뒤 공백------
# Correct
foo = (0,)
# Wrong
bar = (0, )

# ------comma / semicolon / colon 앞 공백------
# Correct
if x == 4: print(x, y); x, y = y, x
# Wrong
if x == 4 : print(x , y) ; x , y = y , x
```

**Slice에서 공백 규칙 (중요)**
- Slice의 `:`는 Binary operator 취급 (양쪽 공백을 동일하게 맞출 것)
```py
# Correct
ham[1:9]
ham[:9:3]
ham[1::3]
ham[lower + offset : upper + offset]

# Wrong
ham[1: 9]
ham[lower + offset:upper + offset]
ham[lower : : step]
ham[ : upper]
```

**함수 호출/ 인덱싱 앞 공백**
```py
# Correct
spam(1)
dct['key'] = lst[index]
# Wrong
spam (1)
dct ['key'] = lst [index]
```

**정렬 목적 과도한 공백 금지**
```py
# Correct
x = 1
y = 2
long_variable = 3
# Wrong
x             = 1
y             = 2
long_variable = 3
```

**Other Recommendations**
- binary operator의 공백
    - 양쪽에 1칸씩
    - 우선순위 연산자 기준으로 가독성 확보
    - 공백 2칸이상 사용 금지
- Trailing whitespace 금지
    - 버그의 원인
    - `\` 뒤 공백은 line continuation 처리 X
- Function Annotations 공백
    - `->` 앞뒤 반드시 공백
- Keyword argument / default value 공백
    - `=` 주변 공백 금지
    - annotation + default value는 예외 (ex. `AnyStr = None`)
- Compound statements (한 줄에 여러 문장) 금지

```py
#____________binary operator의 공백 공백____________
# Correct
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)

# Wrong
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)

# ____________Function Annotations 공백____________
# Correct
def munge(input: AnyStr): ...
def munge() -> PosInt: ...

# Wrong
def munge(input:AnyStr): ...
def munge()->PosInt: ...

# ____________Keyword argument / default value 공백____________
# Correct
def complex(real, imag=0.0):
    return magic(r=real, i=imag)
# Annotation + default value
def munge(sep: AnyStr = None): ...

# Wrong
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
# Annotation + default value (Wrong)
def munge(input: AnyStr=None): ...

# ____________Compound statements (한 줄에 여러 문장) 금지____________
# Correct
if foo == 'blah':
    do_blah_thing()

do_one()
do_two()
do_three()

# Wrong
if foo == 'blah': do_blah_thing()
do_one(); do_two(); do_three()
```
----
## 4. When to Use Trailing Commas
- 단일 요소 Tuple (필수)
    - Trailing comma가 반드시 필요
    - 가독성을 위해 괄호로 감싸는 것을 권장
- 여러 줄 구조 (권장)
    - list / tuple / dict 등등
    - 각 항목을 한 줄에 하나씩 쓰고, 항상 trailing comma 추가
- 닫는 괄호와 같은 줄의 trailing comma는 금지
```py
# ____________단일 요소 Tuple____________
# Correct
FILES = ('setup.cfg',)

# Wrong
FILES = 'setup.cfg',

# ____________여러 줄 구조____________
# Correct
FILES = [
    'setup.cfg',
    'tox.ini',
]

initialize(
    FILES,
    error=True,
)

# ____________ 닫는 괄호와 같은 줄의 trailing comma는 금지____________
# Wrong
FILES = ['setup.cfg', 'tox.ini',]
initialize(FILES, error=True,)
```
----
## 5. Comments
- 주석의 첫 단어는 대문자로 시작해야 함.
    - 소문자로 시작하는 식별자인 경우에는 대소문자 변경 x
- 블록 주석은 하나 이상의 문단으로 구성되며, 각 문장은 마침표로 끝나는 문장이어야 함.
- 영어로 작성할 것.
- 코드 바로 뒤에 오는 Inline comments는 사용을 자제할 것
- 모든 Public 모듈, 함수,클래스, 메서드에는 반드시 docstring을 작성해야함.

----
## 6. Naming Conventions
- 단일 변수명으로 `1`, `O`, `I` 사용 금지 (숫자 `1`, `0`과 혼동됨)
- 패키지 / 모듈 이름은 모두 소문자
    - C/C++ 확장모듈의 low-level구현은 `_socket`처럼 언더스코어 접두어 사용
- 클래스 이름은 Capwords형식 따름 
    - CapWords는 단어의 첫 글자를 대문자로 쓰고, 단어 사이에 공백이나 언더스코어(_) 없이 붙여 쓰는 방식 (대문자가 중간중간에 있음)
    - 즉 Capwords로 이루어진 건 클래스, 소문자+언더스코어로 이루어진건 함수/변수
- Type variables(미리 type을 정의하지 않고 사용할떄 정의하는 변수)는 짧은 Capwords형식 따름
```py
from typing import TypeVar

T = TypeVar('T')  # T라는 타입 변수 생성

def get_first_item(items: list[T]) -> T:
    return items[0]
```
- Functions & Variables는 `lower_case_with_underscore`
- 인자(arguments) : 함수 호출시 함수 내부로 직접 전달하는 값
    - 인스턴스 메서드의 첫번째 인자는 항상 `self`
    - 클래서 메서드의 첫번째 인자는 항상 `cls`
```py
class Robot:
    brand = "Gemini-Factory"

    def __init__(self, name):
        self.name = name  # self를 통해 개별 로봇의 이름에 접근

    @classmethod
    def get_brand(cls):
        return cls.brand  # cls를 통해 클래스 공통 속성(brand)에 접근

# ______________________________self, cls 추가설명______________________________
# 1. 클래스(틀)에서 객체(붕어빵) 두 개를 찍어냅니다.
robot1 = Robot("로보")
robot2 = Robot("트론")

# [self의 경우] 
# robot1.name은 "로보"이고, robot2.name은 "트론"입니다.
# 각자 자기(self) 이름이 다르기 때문입니다.

# [cls의 경우]
# robot1.get_brand()를 호출하든, robot2.get_brand()를 호출하든,
# 심지어 Robot.get_brand() 클래스 자체로 호출하든 결과는 모두 "Gemini-Factory"입니다.
# 모두 같은 틀(cls)을 공유하기 때문입니다.
```
- 상수는 `UPPER_CASE_WITH_UNDERSCORES`
- INTERNAL Interfaces
    - 확실하지 않으면 비공개로 하기
    - `_`로 시작하여 `From module import *`시 제외되도록 함

| 대상       | 규칙                    | 예시                             |
| -------- | --------------------- | ------------------------------ |
| 패키지 / 모듈 | `lowercase`           | `requests`, `urllib`           |
| 클래스      | `CapWords`            | `UserProfile`, `HttpParser`    |
| 함수 / 변수  | `lower_case`          | `calculate_total()`, `user_id` |
| 상수       | `UPPER_CASE`          | `MAX_RETRIES`, `PI`            |
| 예외       | `CapWords + Error`    | `ConnectionError`              |
| 내부용      | `_leading_underscore` | `_internal_method()`           |
| 키워드 회피   | `trailing_underscore` | `type_`, `class_`              |
| 상속 충돌 방지 | `__double_leading`    | `__private_attr`               |
| 매직 메서드   | `__dunder__`          | `__init__`, `__call__`         |


----
## 7. Programming Recommendations
- 비교 및 논리연산
    - `None`과 비교할때는 `is` 또는 `is not` 사용 (`if x is not None:`)
    - 리스트, 문자열, 튜플이 비어있는지 확인할 때는 `len(seq)`말고 `if not seq:` / `if seq:` 과 같은 불리언값 활용
- Exception Handling
    - `except:`는 Control-C 까지 막을수 있으므로 잡을려는 예외를 확실히 명시 `except ImportError:`
        - 원하는 에러만 예외처리하고 나머지는 그대로 터지게 하기 위해
    - `Try` 블록 안에는 에러가 발생할 가능성이 있는 최소한의 코드만 넣기
        - 에러 발생 지점만 try, 이후는 else 블럭에서 수행 
- 로컬 리소스를 사용할 때는 항상 `with`문을 활용하여 자동으로 정리되도록함
    - with 문은 컨텍스트 매니저(context manager) 를 사용하여
        - 진입 시: 리소스 획득 (__enter__)
        - 종료 시: 무조건 정리 (__exit__)
```py
with open("file.txt") as f:
    data = f.read()
# 여기서 파일은 반드시 닫힘
```
- Type Annotations
    - 변수 annotation은 `:`앞에는 공백이 없고 뒤에는 하나 있어야함
        - `=` 양옆에는 공백 하나씩 있어야함
