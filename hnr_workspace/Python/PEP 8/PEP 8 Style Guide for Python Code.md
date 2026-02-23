# PEP 8 Style Guide for Python Code

상태: 진행 중
담당자: 김한누리

# A Foolish Consistency is the Hobgoblin of Little Minds

### 1. Readability Counts

- 코드는 작성되는 것보다 읽히는 경우가 훨씬 더 많다
- 가독성을 높이고 일관성을 유지

### 2. The Hierarchy of Consistency

일관성은 중요하지만, 그 범위에 따라 우선순위가 다르다

1. 하나의 모듈이나 함수 내에서의 일관성
2. 해당 프로젝트 내에서의 일관성
- 이 스타일 가이드(PEP 8)를 따르는 것도 중요하지만, 위의 두 단계가 더 높은 우선순위를 가진다.

### 3. When to be Inconsistent

PEP 8은 기계적인 법전이 아님. 다음과 같은 상황에서는 스타일 가이드를 무시하는 것이 오히려 더 현명한 판단일 수 있다.

1. 가독성 저하: 가이드라인을 적용했을 때, PEP 8에 익숙한 사람이 봐도 코드가 더 읽기 어려워진다면 적용하지 말라
2. 주변 코드와의 조화
3. 오래된 코드: 가이드라인이 나오기 전부터 작성된 코드이고, 다른 이유 없이 스타일을 고치기 위해 코드를 수정할 필요가 없을 때
4. 하위 호환성 유지: 스타일 가이드가 권장하는 기능을 지원하지 않는 이전 버전의 파이썬과 호환성을 유지해야 하는 경우
5. 절대 금기: 오직 이 PEP를 준수하기 위해서 하위 호환성(Backwards compatibility)을 깨뜨리는 일은 절대 해서는 안 된다.

# Code Lay-out

## Indentation

- 코드가 너무 길어서 여러 줄로 나눌 때, 어떻게 들여쓰기를 해야 가독성이 좋아지는가
- 수직 정렬 or 내어쓰기
- 수직 정렬
    - 규칙 : 첫 번째 인자를 첫 줄(괄호 바로 옆)에 적었다면, 다음 줄의 인자들은 첫 줄의 시작 괄호 위치에 수직으로 맞춰야 한다.

```python
# Correct:

# 수직정렬
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
```

- 내어쓰기(Hanging Indent)
    - 괄호가 열린 줄에는 아무런 인자를 적지 않음.
    - 다음 줄부터 들여쓰기를 해서 인자를 적음
        - 규칙 A : 첫 번째 줄(괄호가 열리는 줄)에는 인자를 두지X
        - 규칙 B : 이어지는 줄임을 명확히 하기 위해 추가 들여쓰기를 사용
- 잘못된 경우
    - 첫 줄에 인자를 두고 내어쓰기를 한 경우
        
        ```python
        # 예: 수직 정렬을 할 게 아니라면 첫 줄에 인자를 두면 안 됨
        foo = long_function_name(var_one, var_two,
            var_three, var_four)
        ```
        
    - 함수 본문과 인자의 들여쓰기 수준이 같은 경우
        
        ```python
        # 어디까지가 인자고 어디서부터가 본문인지 한눈에 안 들어옴
        def long_function_name(
            var_one, var_two, var_three,
            var_four):
            print(var_one) # 위 인자들과 시작 위치가 같아서 혼란스러움
        ```
        
- 조건문의 연장선과 실제 실행 코드 블록을 어떻게 구분할 것인가?
    - 문제 상황 : 4칸의 우연
        - 파이썬에서 `if` 키워드(2글자) + 공백(1글자) + 여는 괄호(1글자)를 합치면 4칸이된다.
        
        ```python
        # 'if ('가 4칸을 차지함
        if (this_is_one_thing and
            that_is_another_thing): # 조건의 두 번째 줄이 4칸 들여쓰기 됨
            do_something()          # 실제 실행 코드도 4칸 들여쓰기 됨
        ```
        

→ 이렇게 되면 조건식의 끝과 코드의 시작이 시각적으로 구분이 안되어, 어디까지 조건이고 어디서부터가 본문인지 한눈에 파악하기 어렵다.

## Tabs or Spaces?

1. Spaces are the preferred indentation method (공백 사용 권장)
    - PEP 8은 들여쓰기를 할 때 ‘스페이스(공백) 4칸’ 을 사용하는 것을 권장한다.
    - 왜? : 가독성의 일관성
2. Tabs: 기존 코드와의 일관성 유지용
    - Tab 은 오직 이미 탭으로 작성된 기존 코드를 수정할 때만 사용한다.
3. Mixing tabs and spaces is disallowed
    - 파이썬 3부터는 한 파일 안에 탭과 스페이스를 섞어서 쓰는 것을 아예 금지
        
        → `IndentationError`
        

## Maximum Line Length

1. 79 자와 72자
    - PEP 8 은 코드의 가로 길이를 엄격하게 제한한다.
        - 일반코드 : 최대 79자
        - 주석 및 독스트링 : 최대 72자. 주석은 코드보다 폭을 더 좁게 가져가서 텍스트 블록으로서의 가독성을 높인다.
    - 왜 79자인가?
        - 에디터 창을 80칸으로 설정했을

## Should a Line Break Before or After a Binary Operator?

이진 연산자(Binary Operator) 주변에서 줄을 바꿀 때, 연산자 앞에서 줄을 바꾸는 것을 권장

1. 과거의 방식

```python
# Wrong:
# 연산자가 피연산자와 멀리 떨어져 있음
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)
```

1. 권장되는 방식(Knuth 스타일)
    - 수학자들과 그 편집자들은 정반대의 관습을 따른다
    - 도널드 커누스에 따르면, 수식을 나열할 때는 항상 이진 연산자 앞에서 줄을 바꾼다. 이 전통을 따르면 연산자와 피연산자를 매칭하기가 훨씬 쉬워져 가독성이 높아진다.

```python
# Correct:
# 연산자와 피연산자를 일치시키기 쉬움
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
```

## Blank Lines

- 2줄의 법칙 : 최상위 수준(Top-level)
    - 파일의 가장 바깥쪽에 정의하는 함수나 클래스 앞뒤에는 빈 줄을 2줄 넣는다.
    
    ```python
    class MyFirstClass:
        pass
    
    # 2줄
    def my_top_level_function():
        pass
    
    # 또 2줄
    class MySecondClass:
        pass
    ```
    
- 1줄의 법칙: 클래스 내부 (Methods)
    
    클래스 안에 들어있는 메서드(함수)들 사이에는 빈 줄을 1줄 넣는다.
    
    - 같은 클래스라는 울타리 안에 있으므로, 최상위 함수보다는 가깝지만 서로 구분은 필요하기 때문

```python
class MyClass:
    def method_one(self):
        pass

    # 1줄만 띄운다.
    def method_two(self):
        pass
```

## Source File Encoding

- 기본 인코딩: 파이썬 핵심 배포판의 코드는 항상 UTF-8을 사용해야 한다.
- 인코딩 선언: UTF-8이 기본이므로, 별도의 인코딩 선언(예: `# -*- coding: utf-8 -*-`)을 하지 않아야 한다.
- 표준 라이브러리 예외: 파이썬 표준 라이브러리에서 UTF-8이 아닌 인코딩은 오직 테스트 목적일 때만 허용된다.
- 비 ASCII 문자 사용: ASCII 이외의 문자(한글 등)는 사람의 이름이나 장소를 나타낼 때만 드물게 사용하는 것이 권장
- 식별자 규칙: 파이썬 표준 라이브러리의 모든 식별자(변수명, 함수명 등)는 반드시 ASCII 전용이어야 하며, 가능한 한 영단어를 사용해야 한다.
- 데이터로서의 유니코드: 만약 비 ASCII 문자를 데이터로 사용할 경우, 가독성을 해치는 복잡한 문자나 바이트 순서 표시(BOM)는 피해야 한다.

## Imports

### 1. 기본 원칙과 위치

- 줄 나누기: 각 모듈은 가급적 별도의 줄에 임포트
    - (권장) `import os`, `import sys`
    - (비권장) `import os, sys`
    - 단, 한 모듈에서 여러 항목을 가져올 때는 `from subprocess import Popen, PIPE`와 같이 한 줄에 쓰는 것이 허용
- 파일 내 위치: 임포트는 항상 파일의 가장 윗부분에 위치. 구체적으로는 모듈 설명(docstrings) 바로 뒤, 전역 변수(globals)나 상수(constants) 앞에 배치.

### 2. 권장되는 임포트 순서 (Grouping)

임포트는 다음 세 그룹으로 나누어 순서대로 배치하며, 각 그룹 사이에는 빈 줄을 하나 넣어야 한다.

1. 표준 라이브러리 임포트 (파이썬 내장 모듈)
2. 관련된 서드 파티(Third-party) 임포트 (외부 설치 라이브러리)
3. 로컬 애플리케이션/라이브러리 특정 임포트 (프로젝트 내 다른 파일)

### 3. 절대 임포트 vs 상대 임포트

- Absolute Imports : PEP 8에서 가장 권장하는 방식. 코드를 읽기 더 쉽고, 패키지 설정이 잘못되었을 때 더 명확한 오류 메시지를 제공하기 때문
- Explicit Relative Imports : 패키지 구조가 복잡하여 절대 경로가 너무 길어질 경우 수용 가능한 대안
- 표준 라이브러리 코드는 복잡한 패키지 레이아웃을 피하고 항상 절대 임포트를 사용해야 함

### 4. 주의사항: 와일드카드 임포트 (from <module> import *)

- 사용 지양: 와일드카드 임포트는 어떤 이름이 현재 네임스페이스에 포함되는지 불분명하게 만들기 때문에 피해야 한다. 이는 읽는 사람뿐만 아니라 자동 분석 도구도 혼란스럽게 만든다.
- 예외 상황: 내부 인터페이스를 공개 API로 다시 게시(republish)해야 하는 경우 등 아주 드문 상황에서만 정당화될 수 있다.

## Module Level Dunder Names

### 1. 배치의 순서 (Placement)

모듈의 최상단에서 아래의 순서를 엄격히 지켜야 한다.

1. 모듈 독스트링(Docstring): 모듈에 대한 설명.
2. `from __future__` 임포트: 파이썬의 하위 호환성을 위한 특수 임포트로, 독스트링 바로 뒤에 와야 한다.
3. 모듈 레벨 Dunder: `__all__`, `__version__` 등.
4. 일반 임포트 문: `import os` 등 일반적인 라이브러리 임포트.

주의: 일반적인 전역 변수는 임포트문 뒤에 위치하지만, Dunder 네임들은 임포트보다 앞에 위치한다는 점이 특징이다.

### 2. 코드 예시

PEP 8에서 권장하는 전형적인 모듈 구조는 다음과 같다.

```python
from __future__ import bar_feature  # 최우선 임포트

__all__ = ['LidarSensor', 'RadarSensor']
__version__ = '0.1'
__author__ = 'ResNet24'

import os
import sys

# 이후 일반적인 코드 작성...
```

### 3. 주요 Dunder 네임의 역할

- `__all__`: `from module import *`를 실행했을 때 외부로 노출될 심볼 목록을 정의
- `__version__`, `__author__`: 모듈의 메타데이터(버전, 제작자)를 명시하는 데 사용

# String Quotes

### 1. 선택은 당신의 몫 (Single vs Double)

파이썬에서는 작은따옴표(`'`)와 큰따옴표(`"`)가 완전히 동일하게 작동

- 규칙: PEP 8은 이 중 하나를 특별히 권장하지 않는다.
- 하나의 규칙을 정했다면, 프로젝트 내에서 일관성 있게 사용하는 것이 가장 중요하다.

### 2. 백슬래시(`\`) 피하기

문자열 안에 따옴표 자체가 포함되어야 할 때는 '반대되는' 따옴표를 사용해라

- 백슬래시를 써서 탈출(Escaping)시키는 것보다 코드가 훨씬 깔끔해지기 때문.
    
    
    | **상황** | **권장 방식 (Correct)** | **비권장 방식 (Avoid)** |
    | --- | --- | --- |
    | **작은따옴표 포함** | `"Python's great"`  | `'Python\'s great'`  |
    | **큰따옴표 포함** | `'He said "Hello"'`  | `"He said \"Hello\""`  |

### 3. 세 줄 따옴표 (Triple-quoted strings)

여러 줄에 걸친 문자열이나 독스트링(docstrings)을 작성할 때는 규칙이 엄격하다.

- 항상 큰따옴표 3개(`"""`)를 사용해야 한다.
- 이는 PEP 257(독스트링 규칙)과의 일관성을 유지하기 위함.

# Whitespace in Expressions and Statements

## Pet Peeves

- 괄호 바로 안쪽: 소괄호, 대괄호, 중괄호를 열자마자 혹은 닫기 직전에 공백을 두지 말아라
    - (Correct) `spam(ham[1], {eggs: 2})`
    - (Wrong) `spam( ham[ 1 ], { eggs: 2 } )`
- 쉼표, 세미콜론, 콜론 바로 앞:
    - (Correct) `if x == 4: print(x, y); x, y = y, x`
    - (Wrong) `if x == 4 : print(x , y) ; x , y = y , x`
- 함수 호출의 여는 괄호 앞: 함수 이름과 인자 리스트 사이에는 공백을 넣지 않는다.
    - (Correct) `spam(1)` / (Wrong) `spam (1)`
- 인덱스나 슬라이싱 여는 괄호 앞:
    - (Correct) `dct['key'] = lst[index]` / (Wrong) `dct ['key'] = lst [index]`
1. 슬라이싱에서의 공백
    - 슬라이싱에서 콜론(`:`)은 이항 연산자처럼 취급되어 양쪽에 동일한 양의 공백이 있어야 한다.
    - 확장된 슬라이스: `ham[1:9:3]` 처럼 콜론이 여러 개일 때도 모든 콜론 주위에 동일한 간격을 적용.
    - 생략된 매개변수: 만약 슬라이스 파라미터가 생략되면 공백도 생략.
        - (Correct) `ham[:9]`, `ham[1:9:]`, `ham[1::3]`
2. 연산자 주변의 공백
    - 항상 공백을 두는 경우: 할당(`=`), 증합 할당(`+=`), 비교(`==`, `<`, `!=`), 불리언(`and`, `or`, `not`) 연산자 양옆에는 항상 한 칸의 공백을 둔다.
    - 우선순위 고려: 우선순위가 다른 연산자들을 섞어 쓸 때는, 가장 우선순위가 낮은 연산자 주변에만 공백을 추가하는 것이 권장된다.
        - (Correct) `x = x*2 - 1`, `hypot2 = x*x + y*y`
    - 주의사항: 연산자 양옆에 한 칸 이상의 공백을 사용하지 말아라
3. 기타 권장 사항
- 줄 끝의 공백(Trailing Whitespace): 줄 마지막에 눈에 보이지 않는 공백을 남기지 말아라. 이는 특히 백슬래시(`\`) 뒤에 올 경우 줄 바꿈 인식을 방해하여 오류를 일으킬 수 있다.
- 복합 문장 지양: 한 줄에 여러 개의 문장을 쓰는 것(`if x == 1: print(x)`)은 일반적으로 권장되지 않는다.

# When to Use Trailing Commas

### 1. 필수적인 경우: 단일 원소 튜플 (Singleton Tuple)

요소가 하나만 들어있는 튜플을 만들 때는 후행 쉼표가 반드시(mandatory) 있어야 한다.

쉼표가 없으면 파이썬은 이를 튜플이 아닌 단순 괄호로 묶인 값으로 인식하기 때문.

- 권장 방식: 명확성을 위해 튜플을 소괄호로 감싸는 것이 좋다.
    - 예: `a = (1,)`

### 2. 권장되는 경우: 버전 관리와 확장성

리스트, 인자 목록, 혹은 임포트 항목이 시간이 지나면서 계속 늘어날 가능성이 있을 때 후행 쉼표가 유용하다.

- 작성 패턴: 각 값을 별도의 줄에 하나씩 적고, 마지막 값 뒤에도 항상 쉼표를 붙인 뒤, 닫는 괄호는 다음 줄에 작성
- 이점 (VCS 활용): 이렇게 작성하면 나중에 새로운 항목을 추가할 때, 기존 줄을 수정하지 않고 새 줄만 추가하면 된다.  이는 Git 같은 버전 관리 시스템에서 '어느 줄이 바뀌었는지'를 명확하게 보여주어 코드 리뷰를 편하게 만든다.

```python
# 처음 상태 (PEP 8 스타일)
python_libs = [
    'numpy',
    'pandas',  # 이미 쉼표가 있음
]
```

### 3. 피해야 할 경우

닫는 괄호와 같은 줄에 후행 쉼표를 두는 것은 권장되지 않는다.

# Comments

파이썬의 철학에서 주석은 코드만큼이나 중요하게 다뤄진다. PEP 8은 주석을 작성할 때 "코드와 모순되는 주석은 주석이 없는 것보다 못하다"는 원칙을 최우선으로 강조한다.

### 1. 일반적인 원칙

- 최신 상태 유지: 코드가 변경되면 주석도 반드시 업데이트.
- 완전한 문장: 주석은 되도록 완전한 문장으로 작성하며, 첫 글자는 대문자로 시작한다 (소문자로 시작하는 식별자 제외).
- 언어: 전 세계 개발자가 읽을 수 있도록 영어로 작성하는 것이 권장

## 2. Block Comments

코딩 로직의 앞부분에 위치하여 뒤따라오는 코드 전체 혹은 일부를 설명할 때 사용.

- 들여쓰기: 설명하려는 코드와 동일한 수준으로 들여쓰기 한다
- 형식: 각 줄은 `#`과 공백 한 칸으로 시작한다
- 문단 구분: 주석 내부에서 문단을 나눌 때는 `#`만 포함된 빈 줄을 사용

## 3. Inline Comments

코드와 같은 줄에 쓰는 주석으로, 꼭 필요한 경우에만 드물게 사용해야 한다.

- 간격: 코드 문장과 주석 사이에는 최소 두 칸 이상의 공백을 두어야 한다.
- 형식: `#`과 공백 한 칸으로 시작한다

## 4. DocStrings

모든 공개(Public) 모듈, 함수, 클래스, 메서드에 대해 작성해야 하는 주석.

- 형식: 큰따옴표 세 개(`"""`)를 사용하여 감싼다.
- 여러 줄 독스트링: 내용이 끝나고 마지막 닫는 `"""`는 반드시 별도의 줄에 배치
- 한 줄 독스트링: 닫는 `"""`를 같은 줄에 두어도 괜찮다.

# Naming Conventions

## Descriptive: Naming Styles

### 1. 일반적인 명명 스타일

| **스타일** | **예시** | **비고** |
| --- | --- | --- |
| **소문자 한 글자** | `b` |  |
| **대문자 한 글자** | `B` |  |
| **소문자** | `lowercase` |  |
| **밑줄을 포함한 소문자** | `lower_case_with_underscores` | **snake_case** |
| **대문자** | `UPPERCASE` |  |
| **밑줄을 포함한 대문자** | `UPPER_CASE_WITH_UNDERSCORES` | **SCREAMING_SNAKE_CASE** |
| **대문자로 시작하는 단어** | `CapitalizedWords` | **CapWords, CamelCase, StudlyCaps** |
| **혼합 케이스** | `mixedCase` | 첫 글자만 소문자인 방식 |
| **밑줄을 포함한 대문자 단어** | `Capitalized_Words_With_Underscores` | PEP 8은 이 스타일을 못생겼다(ugly!)고 표현 |

### 2. 스타일 적용 시 주의사항

- 약어 처리: `CapWords` 방식을 사용할 때 `HTTP` 같은 약어가 포함된다면, 약어의 모든 글자를 대문자로 써야 한다.
    - (좋음) `HTTPServerError`
    - (나쁨) `HttpServerError`
- 접두어(Prefix) 사용: 관련 있는 이름들을 묶기 위해 `st_mode`, `st_size`처럼 짧은 고유 접두어를 쓰는 방식이 있다. 이는 주로 POSIX 시스템 호출 구조와의 대응을 위해 사용되지만, 파이썬에서는 객체나 모듈 이름이 이미 접두어 역할을 하므로 일반적으로는 불필요하다고 본다.

### 3. 밑줄(`_`)이 붙은 특별한 형태

이름 앞뒤에 밑줄을 붙여 특별한 의미를 전달하기도 한다.

- `_single_leading_underscore`: "내부용"임을 나타내는 약한 지표. 예컨대 `from M import *`를 해도 이 이름은 가져오지 않는다.
- `single_trailing_underscore_`: `class`나 `list` 같은 파이썬 키워드와의 충돌을 피하기 위해 사용
- `__double_leading_underscore`: 클래스 속성에서 사용 시 네임 마글링(Name Mangling)을 일으켜 서브클래스의 속성과 이름이 겹치지 않게 한다.
- `__double_leading_and_trailing_underscore__`: `__init__`처럼 사용자가 제어하는 네임스페이스에 존재하는 매직 객체나 속성. 이런 형태의 이름을 직접 지어내지 말아라. 오직 문서화된 대로만 사용해야 한다.

## Prescriptive: Naming Conventions

### 1. Names to Avoid

단일 문자 변수명을 지을 때 다음 문자들은 절대 사용하지 X. 특정 글꼴에서 숫자 1이나 0과 구분이 안 되어 버그를 유발할 수 있다.

- 'l' (소문자 엘)
- 'O' (대문자 오)
- 'I' (대문자 아이)

만약 'l'을 쓰고 싶다면 대문자 'L'로 대체하는 것이 권장

### 2. ASCII Compatibility

- 파이썬 표준 라이브러리의 모든 식별자는 반드시 ASCII 전용이어야 한다.
- 가능한 한 영단어를 사용해야 하며, 약어나 전문 용어도 영어 기반이어야 한다.

### 3. Package and Module Names

- 모듈: 짧고 모두 소문자인 이름을 사용하며, 가독성을 위해 필요한 경우 밑줄(`_`)을 사용할 수 있다.
- 패키지: 짧고 모두 소문자인 이름을 사용하되, 밑줄 사용은 권장되지 않는다.
- C/C++로 작성된 확장 모듈이 파이썬 모듈과 함께 제공될 경우, 해당 C 모듈 이름 앞에 밑줄을 붙인다.(예: `_socket`).

### 4. Class Names

- 기본적으로 CapWords (첫 글자를 대문자로 하는 방식) 컨벤션을 사용
- 단, 함수처럼 호출되는 인터페이스로 문서화된 경우에는 함수 명명 규칙을 따를 수도 있다.
- 파이썬 내장(Built-in) 이름은 예외적으로 한 단어 혹은 두 단어를 붙여 쓰며, 예외 이름과 내장 상수에만 CapWords를 사용한다.

### 5. Type Variable Names

- `PEP 484`에서 도입된 타입 변수(T, AnyStr 등)는 보통 짧은 CapWords를 사용
- 공변(covariant)이나 반공변(contravariant) 동작을 나타낼 때는 접미사로 `_co` 또는 `_contra`를 붙이는 것이 권장

### 6. Exception Names

- 예외는 클래스이므로 클래스 명명 규칙을 따른다.
- 실제 에러를 나타내는 예외인 경우 이름 끝에 "Error"라는 접미사를 붙여야 한다. -

### 7. Global Variable Names

- 함수 명명 규칙과 거의 동일
- `from M import *`를 통해 내보내지 않으려는 전역 변수는 이름 앞에 밑줄을 붙이거나 `__all__` 메커니즘을 사용해 비공개임을 표시해야 한다.

### 8. Function and Variable Names

- 모두 소문자로 작성하며, 가독성을 위해 단어 사이에 밑줄을 넣는다 (snake_case).
- `mixedCase`는 오직 과거 버전과의 호환성을 유지해야 하는 경우에만 허용

### 9. Function and Method Arguments

- 인스턴스 메서드의 첫 번째 인자는 항상 `self` 사용
- 클래스 메서드의 첫 번째 인자는 항상 `cls`를 사용
- 인자 이름이 파이썬 예약어와 충돌할 경우, 약어를 쓰기보다는 이름 뒤에 밑줄을 하나 붙이는 것이 좋다.

### 10. Method Names and Instance Variables

- 함수 명명 규칙인 소문자와 밑줄 방식을 따른다.
- 공개가 아닌(non-public) 메서드나 변수에는 이름 앞에 밑줄 하나를 붙인다.
- 서브클래스와의 이름 충돌을 피해야 하는 경우 밑줄 두 개를 앞에 붙여 파이썬의 네임 마글링(name mangling) 규칙을 적용

### 11. Constants

- 보통 모듈 수준에서 정의되며, 모든 글자를 대문자로 쓰고 단어 사이를 밑줄로 구분 (예: `MAX_OVERFLOW`, `TOTAL`).

### 12. Designing for Inheritance

- 클래스의 속성(attribute)을 설계할 때는 항상 이것이 공개(public)인지 비공개(non-public)인지 결정해야 한다.
- 확신이 서지 않는다면 비공개로 설정하는 것이 좋다.
- 공개 속성: 이름 앞에 밑줄을 붙이지 않으며, 하위 호환성을 보장해야 한다.
- 단순 데이터 속성: 복잡한 getter/setter 메서드 대신 속성 이름만 노출하되, 나중에 기능 확장이 필요하면 `property`를 사용
- 서브클래스 충돌 방지: 서브클래스에서 사용하지 않길 원하는 속성은 밑줄 두 개(`__`)를 붙여 이름 충돌을 방지

## Programming Recommendation

- `None` 비교: `None`과 같은 싱글턴(Singleton) 객체를 비교할 때는 항상 `is`나 `is not`을 사용. `==`를 사용하면 안 된다.
- 부정 비교: `not x is None` 대신 `x is not None` 사용
- 람다 지양: `f = lambda x: x**2` 처럼 람다 식을 변수에 할당하기보다, `def f(x): return x**2`를 사용하여 명시적으로 함수를 정의. 이는 에러가 발생했을 때 Traceback 시 함수 이름이 명확히 나오게 해준다.
- Exceptions:
    - 모든 예외는 `Exception`이 아닌 `BaseException`에서 상속받지 않도록 주의
    - 비어있는 `except:` 문을 피해라. 어떤 에러가 났는지 알 수 없게 만든다. 반드시 명시적인 예외(`except ImportError:`)를 잡아야 한다.
    - `try` 절에는 에러가 발생할 수 있는 최소한의 코드만 넣어라
- 문자열 처리:
    - 문자열의 앞뒤를 확인할 때는 슬라이싱 대신 `.startswith()`와 `.endswith()`를 사용하라
    - 객체의 타입을 비교할 때는 `type(obj) is type(1)` 대신 `isinstance(obj, int)`를 사용하는 것이 상속 구조까지 고려하므로 더 안전
- 불리언(Boolean) 비교:
    - `if greeting == True:` 나 `if greeting:` 중 후자를 선택하라. 파이썬에서는 빈 시퀀스(리스트, 문자열 등)가 `False`로 취급되는 특성을 활용하는 것이 더 깔끔하다.

### 2. Function Annotations

파이썬 3에서 도입된 타입 힌트 기능에 대한 규칙

- 공백 규칙: 콜론(`:`) 뒤에는 공백을 한 칸 두고, 앞에는 두지 않는다. 화살표(`>`) 양옆에는 항상 공백을 한 칸씩 둔다.
    - (Correct) `def munge(input: AnyStr, sep: AnyStr = None) -> AnyStr:`
    - (Wrong) `def munge(input:AnyStr,sep:AnyStr=None)->AnyStr:`
- 기본값과 조합: 타입 힌트와 기본값(`=`)을 함께 쓸 때는 `=` 양옆에 공백을 넣어야 한다. (타입 힌트가 없을 때는 공백을 넣지 않는 것이 규칙이다.)

---

### 3. Variable Annotations

`PEP 526`에서 도입된 변수의 타입 힌트 작성법

- 형식: 함수 어노테이션과 마찬가지로 콜론 뒤에만 공백을 둔다.

```python
# 전역 변수나 클래스 변수 표기 시
code: int = 10
stats: list[int] = []
```