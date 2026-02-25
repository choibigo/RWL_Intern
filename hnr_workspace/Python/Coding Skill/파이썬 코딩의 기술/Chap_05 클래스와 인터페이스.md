# Chap_05 클래스와 인터페이스

## **37. 내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성하라**

### 기억해야 할 내용

- 딕셔너리, 긴 튜플, 다른 내장 타입이 복잡하게 내포된 데이터를 값으로 사용하는 딕셔너리를 만들지 말라.
- 완전한 클래스가 제공하는 유연성이 필요하지 않고 가벼운 불변 데이터 컨테이너가 필요하다면 `namedtuple`을 사용한다.
- 내부 상태를 표현하는 딕셔너리가 복잡해지면 여러 클래스를 나눠서 작성한다.

```python
class SimpleGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('아이작 뉴턴')
book.report_grade('아이작 뉴턴', 90)
book.report_grade('아이작 뉴턴', 95)
book.report_grade('아이작 뉴턴', 85)

print(book.average_grade('아이작 뉴턴'))
```

`book = SimpleGradebook()`: 빈 장부 생성. `_grades = {}`

`book.add_student('아이작 뉴턴')`: 뉴턴 등록. `_grades = {'아이작 뉴턴': []}`

`book.report_grade('아이작 뉴턴', 90)`: 첫 점수. `_grades = {'아이작 뉴턴': [90]}`

`book.report_grade(..., 95)`, `(..., 85)`: 점수 누적. `_grades = {'아이작 뉴턴': [90, 95, 85]}`

`print(book.average_grade('아이작 뉴턴'))`: 270 / 3을 계산하여 `90.0` 출력.

```python
from collections import defaultdict

class BySubjectGradebook:
    def __init__(self):
        self._grades = {}  # 외부 dict

    def add_student(self, name):
        self._grades[name] = defaultdict(list)  # 내부 dict

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75)
book.report_grade('알버트 아인슈타인', '수학', 65)
book.report_grade('알버트 아인슈타인', '체육', 90)
book.report_grade('알버트 아인슈타인', '체육', 95)
print(book.average_grade('알버트 아인슈타인'))
```

```python
class WeightedGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0

        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count

book = WeightedGradebook()
book.add_student('알버트 아인슈타인')
book.report_grade('알버트 아인슈타인', '수학', 75, 0.05)
book.report_grade('알버트 아인슈타인', '수학', 65, 0.15)
book.report_grade('알버트 아인슈타인', '수학', 70, 0.80)
book.report_grade('알버트 아인슈타인', '체육', 100, 0.40)
book.report_grade('알버트 아인슈타인', '체육', 85, 0.60)
print(book.average_grade('알버트 아인슈타인'))

#
grades = []
grades.append((95, 0.45))
grades.append((85, 0.55))
total = sum(score * weight for score, weight in grades)
total_weight = sum(weight for _, weight in grades)
average_grade = total / total_weight

#
grades = []
grades.append((95, 0.45, '참 잘했어요'))
grades.append((85, 0.55, '조금 만 더 열심히'))
total = sum(score * weight for score, weight, _ in grades)
total_weight = sum(weight for _, weight, _ in grades)
average_grade = total / total_weight
```

- `average_grade` 메서드만 봐도 코드가 너무 깊숙이 파고 들어가 있어서 한눈에 보기 힘들다.
- 데이터 구조(튜플 구성 등)를 살짝만 바꿔도 프로그램 전체가 에러가 난다
- `WeightedGradebook`이라는 클래스 하나가 '학생 관리', '과목 관리', '가중치 계산'이라는 너무 많은 일을 혼자 다 하고 있다.

```python
from collections import namedtuple
Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]

book = Gradebook()
albert = book.get_student('알버트 아인슈타인')
math = albert.get_subject('수학')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)
gym = albert.get_subject('체육')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)
print(albert.average_grade())
```

## **38. 간단한 인터페이스의 경우 클래스 대신 함수를 받아라**

### 기억해야 할 내용

- 파이썬의 여러 컴포넌트 사이에 간단한 인터페이스가 필요할 때는 클래스를 정의하고 인스턴스화하는 대신 간단히 함수를 사용할 수 있다.
    - 클래스를 정의하는 방식 → 복잡함
        - 문자열 길이로 정렬하고 싶다 → 단순히 이 목적을 위해 클래스를 만드는 것은 과함
    
    ```python
    class LengthSorter:
        def sort_key(self, x):
            return len(x)
    
    names = ['소크라테스', '플라톤', '아리스토텔레스']
    sorter = LengthSorter()
    # 클래스를 만들고, 인스턴스화(sorter)하고, 그 안의 메서드를 넘겨줘야 함
    names.sort(key=sorter.sort_key)
    ```
    
    - 함수를 사용하는 방식 → 파이썬의 sort 는 함수를 인자로 받을 수 있기 때문에 간단
    
    ```python
    names = ['소크라테스', '플라톤', '아리스토텔레스']
    
    # 별도의 클래스 없이 len이라는 내장 함수를 바로 인터페이스로 사용
    names.sort(key=len)
    ```
    
    - 딕셔너리에 없는 키를 찾을 때마다 "키가 새로 추가되었습니다"라는 메시지를 찍고, 기본값으로 `0`을 넣는 상황
        - 파이썬 함수는 일급 시민이므로, 변수처럼 여기저기 보낼 수 있어 컴포넌트 간의 결합이 매끄럽다.
    
    ```python
    from collections import defaultdict
    
    # 1. 간단한 함수 정의
    def log_missing():
        print('키 추가됨')
        return 0
    
    current = {'초록': 12, '파랑': 3}
    
    # 2. 클래스를 만들 필요 없이 log_missing 함수 자체를 인터페이스로 넘김
    # defaultdict는 "키가 없을 때 실행할 함수"를 인자로 받도록 설계되어 있음
    result = defaultdict(log_missing, current)
    
    # 실행
    result['빨강'] += 5  # '빨강'이 없으므로 log_missing()이 호출됨
    ```
    
- 파이썬 함수나 메서드는 일급 시민이다. 따라서(다른 타입의 값과 마찬가지로) 함수나 함수 참조를 식에 사용할 수 있다.
    - 일급 시민의 3가지 조건
        1. 변수에 담을 수 있다.
        2. 인자로 넘길 수 있다.
        3. 반환값으로 쓸 수 있다.
    - 함수 참조를 식에 하용할 수 있다는 의미
        - 함수의 이름만 알고 있으면, 그 이름을 어디에든 적어서 마치 데이터처럼 활용할 수 있다
            - 리스트에 담기: `functions = [len, str, int]` 처럼 함수들을 리스트 안에 담을 수 있다.
            - 딕셔너리에 담기 :`actions = {'print': print, 'log': log_missing}` 처럼 키값으로 함수를 매핑할 수 있다.
    
    ```python
    from collections import defaultdict
    
    # 1. 함수를 정의
    def log_missing():
        print('키가 없어서 기본값 0을 반환합니다.')
        return 0
    
    # 2. 함수(log_missing)를 변수처럼 defaultdict라는 클래스에 인자로 전달.
    # 여기서 'log_missing' 뒤에 괄호()를 붙이지 않았음
    # 괄호를 붙이면 함수를 '실행'하는 것이고, 붙이지 않으면 함수 '자체'를 보내는 것.
    result = defaultdict(log_missing) 
    
    # 3. 함수가 변수에 저장될 수 있음
    my_func = log_missing
    print(my_func())  # 변수에 담긴 함수를 실행할 수 있음
    ```
    

- `__call __`특별 메서드를 사용하면 클래스의 인스턴스인 객체를 일반 파이썬 함수처럼 호출할 수 있다.
    - 파이썬에서 `__call__`은 클래스의 객체(인스턴스)에게 함수처럼 행동할 수 있는 능력을 부여
    - 보통 클래스로 만든 객체는 `객체.메서드()` 형태로 일을 시키지만, `__call__`이 정의된 객체는 함수처럼 `객체()`라고만 써도 바로 실행이 가능하다
    - 왜 `__call__`을 사용하나
        - 단순한 함수는 실행이 끝나면 내부의 데이터를 잊어버린다. 하지만 클래스로 만든 객체는 정보를 계속 보관할 수 있다. `__call__`을 사용하면 정보를 기억하는 능력(클래스)과 간편하게 호출하는 방식(함수)의 장점을 모두 가질 수 있다.

```python
class BetterCountMissing:
    def __init__(self):
        self.added = 0  # 몇 번 추가됐는지 기억할 '상태'

    def __call__(self):  # 객체를 함수처럼 호출할 때 실행되는 부분
        self.added += 1  # 상태를 업데이트함
        return 0         # 기본값 반환

# 1. 객체를 생성
counter = BetterCountMissing()

# 2. 객체를 함수처럼 호출 (counter.something()이 아님)
print(counter())  # 결과: 0 (함수처럼 작동)
print(f"추가된 횟수: {counter.added}")  # 결과: 1 (상태가 저장됨)

# 3. 이제 이 객체를 defaultdict에 '함수' 대신 넣어준다.
from collections import defaultdict
current = {'초록': 12, '파랑': 3}
result = defaultdict(counter, current)  # counter는 객체지만 함수처럼 취급됨

# 없는 키를 조회하면 counter()가 자동으로 호출된다.
result['빨강'] += 5
result['주황'] += 9

print(f"최종 추가 횟수: {counter.added}")  # 결과: 2
```

- 상태를 유지하기 위한 함수가 필요한 경우에는 상태가 있는 클로저를 정의하는 대신 `__call__` 메서드가 있는 클래스를 정의할지 고려한다.
    - 방법 A : 상태가 있는 클로저
        - 클로저란 함수 안에 함수를 또 정의해서 바깥쪽 함수의 변수를 기억하는 기술이다. 파이썬에서는 이때 `nonlocal` 이라는 키워드를 써야한다.
    
    ```python
    def make_counter():
        count = 0  # 이 상태를 기억하고 싶음
        
        def counter():
            nonlocal count  # 바깥에 있는 count를 수정하겠다고 선언
            count += 1
            return count
        
        return counter
    
    my_counter = make_counter()
    print(my_counter()) # 1
    print(my_counter()) # 2
    ```
    
    - 방법 B : `__call__` 메서드가 있는 클래스
    
    ```python
    class BetterCounter:
        def __init__(self):
            self.count = 0  # 상태 저장 주머니
    
        def __call__(self):
            self.count += 1  # 상태 업데이트
            return self.count
    
    my_better_counter = BetterCounter()
    print(my_better_counter()) # 1
    print(my_better_counter()) # 2
    ```
    

## **39. 객체를 제내릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라**

### 기억해야 할 내용

- 파이썬 클래스에는 생성자가 `__init__`메서드 뿐이다.
- `@classmethod`를 사용하면 클래스에 다른 생성자를 정의할 수 있다.
- 클래스 메서드 다형성을 활용하면 여러 구체적인 하위 클래스의 객체를 만들고 연결하는 제네릭한 방법을 제공한다.

### 파이썬 클래스에는 생성자가 `__init__`메서드 뿐이다.

```python
class User:
    def __init__(self, name, age): # 직접 입력용
        self.name = name
        self.age = age

    # 파이썬은 메서드 이름이 같으면 마지막 것만 기억한다.
    # 즉, 위의 __init__은 사라지고 아래 것만 남게 된다.
    def __init__(self, json_data): # JSON 입력용
        self.name = json_data['name']
        self.age = json_data['age']
```

### `@classmethod`를 사용하면 클래스에 다른 생성자를 정의할 수 있다.

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_json(cls, data):
        # cls는 User 클래스 자신을 의미한다.
        # 여기서 cls(name, age)를 호출하는 것은 User(name, age)를 하는 것과 같다.
        return cls(data['name'], data['age'])

    @classmethod
    def from_string(cls, user_str):
        # "홍길동,30" 같은 문자열을 받아서 객체 생성
        name, age = user_str.split(',')
        return cls(name, int(age))

# 사용 예시
user1 = User("Hannuri", 25) # 기본 생성자 사용
user2 = User.from_json({'name': '알버트', 'age': 30}) # 보조 생성자 사용
user3 = User.from_string("뉴턴,40") # 또 다른 보조 생성자 사용
```

1. `User.from_json` 입장: 일단 클래스 메서드 안으로 들어간다.
2. 데이터 가공: 메서드 내부에서 `data['name']`과 `data['age']`를 꺼낸다.
3. `cls(...)` 실행: `return cls(name, age)`를 하는 순간, 파이썬은 `User` 클래스의 `__init__`을 호출
4. `__init__` 완료: `self.name`과 `self.age`가 설정
5. 완성된 객체가 `from_json`을 거쳐 반환
- 이름이 있는 생성자
    - `__init__`은 이름이 고정되어 있개 때문에 무엇을 위해 객체를 만드는지 설명하기 어렵다. 하지만 `@classmethod`를 쓰면 이름을 마음대로 지을 수 있다.
- 복잡한 전처리 로직의 분리
    - `__init__`은 단순히 받은 재료를 조립하는 데 집중해야 한다. 만약 재료를 자르고(split), 형식을 바꾸고(int), 검증하는 복잡한 과정이 필요하다면 그 일을 `@classmethod`가 대신해준다.

## **40. super로 부모 클래스를 초기화하라**

### 기억해야 할 내용

- 파이썬은 표준 메서드 결정 순서를 활용해 상위 클래스 초기화 순서와 다이아몬드 상속 문제를 해결한다.
- 부모 클래스를 초기화할 때는 super 내장 함수를 아무 인자 없이 호출하라. super을 아무 인자 없이 호출하면 파이썬 컴파일러가 자동으로 올바른 파라미터를 넣어준다.

### 파이썬은 표준 메서드 결정 순서를 활용해 상위 클래스 초기화 순서와 다이아몬드 상속 문제를 해결한다.

- 부모를 직접 부를 때 생기는 문제
    - 부모 클래스의 이름을 직접 불러서 초기화(`MyBaseClass.__init__`)하면, 공통 부모가 두 번 실행되는 문제가 생긴다.

```python
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class TimesSeven(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value) # 부모 호출 1
        self.value *= 7

class PlusNine(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value) # 부모 호출 2
        self.value += 9

class ThisWay(TimesSeven, PlusNine):
    def __init__(self, value):
        TimesSeven.__init__(self, value)
        PlusNine.__init__(self, value)

foo = ThisWay(5)
print(foo.value) # 결과: 14 (???)
```

**왜 14가 나오나?**

1. `TimesSeven`이 실행되어 `value`가 35가 됨
2. 그런데 바로 다음에 `PlusNine`이 실행되면서 `MyBaseClass.__init__` 을 다시 호출 
3. 이 때문에 고생해서 계산한 35가 사라지고 다시 기본값 5로 초기화
4. 결국 `5 + 9`만 계산되어 `14`라는 결과가 나옴

- `super()`를 사용한 올바른 방식

```python
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class TimesSevenCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value) # "다음 순서"를 호출
        self.value *= 7

class PlusNineCorrect(MyBaseClass):
    def __init__(self, value):
        super().__init__(value) # "다음 순서"를 호출
        self.value += 9

class GoodWay(TimesSevenCorrect, PlusNineCorrect):
    def __init__(self, value):
        super().__init__(value)

foo = GoodWay(5)
print(foo.value) # 결과: 98
```

- **중복 방지**: 부모 이름을 직접 부르면 공통 부모가 두 번, 세 번 초기화되면서 데이터가 엉망이 될 수 있지만, `super()`는 딱 한 번만 방문하도록 보장해 준다.
- **순서 보장**: 우리가 괄호 안에 적어준 순서(MRO)를 파이썬이 분석해서, 논리적으로 가장 완벽한 계산 순서를 알아서 짜준다.
- **유지보수**: 나중에 상속 관계를 살짝 바꾸더라도, `super()`를 써두면 내부 코드를 일일이 수정할 필요 없이 파이썬이 바뀐 순서대로 길을 다시 찾아준다.

### 부모 클래스를 초기화할 때는 super 내장 함수를 아무 인자 없이 호출하라. super을 아무 인자 없이 호출하면 파이썬 컴파일러가 자동으로 올바른 파라미터를 넣어준다.

- 예전에는 super 을 쓸 때 두가지 정보를 꼭 넣어줘야 했다
    - 지금 내 클래스의 이름/ 현재 내 객체(self)
    - 이렇게 되면 클래스 이름을 중간에 바꾸면, super 안에 있는 이름도 다 고쳐야한다.

```python
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class ExplicitChild(MyBaseClass):
    def __init__(self, value):
        # 괄호 안에 (자기이름, self)를 다 써줘야 했다.
        super(ExplicitChild, self).__init__(value)
        self.value *= 2
```

- 권장하는 방식

```python
class ImplicitChild(MyBaseClass):
    def __init__(self, value):
        # 파이썬이 알아서 super(ImplicitChild, self)로 해석
        super().__init__(value) 
        self.value *= 2
```

## **41. 기능을 합성할 때는 믹스인 클래스를 사용하라.**

### 기억해야 할 내용

- 믹스인을 사용해 구현할 수 있는 기능을 인스턴스 애트리뷰트와 `__init__`을 사용하는 다중 상속을 통해 구현하지 않는다.
- 믹스인 클래스가 클래스별로 특화된 기능을 필요로 한다면 인스턴스 수준에서 끼워 넣을 수 있는 기능(정해진 메서드를 통해 해당 기능을 인스턴스가 제공하게 만듦)을 활용한다.
- 믹스인에는 필요에 따라 인스턴스 메서드는 물론 클래스 메서드도 포함될 수 있다.
- 믹스인을 합성하면 단순한 동작으로부터 더 복잡한 기능을 만들 수 있다.

### 믹스인을 사용해 구현할 수 있는 기능을 인스턴스 애트리뷰트와 `__init__`을 사용하는 다중 상속을 통해 구현하지 말라

- 하지 말아야하는 방식 : 상태를 가진 다중 상속

```python
class NameMixin:
    def __init__(self, name):
        self.name = name

class AgeMixin:
    def __init__(self, age):
        self.age = age

# 믹스인인데 __init__이 있으면 상속받을 때마다 상황이 어려워짐
class Person(NameMixin, AgeMixin):
    def __init__(self, name, age):
        # 부모들의 __init__ 인자가 제각각이라 호출하기가 매우 까다롭다.
        NameMixin.__init__(self, name)
        AgeMixin.__init__(self, age)
```

- 권장하는 방식 : 데이터는 자식에게, 믹스인은 기능만!

```python
class DisplayMixin:
    """이 믹스인은 __init__이 없으며, 오직 출력 기능만 제공한다."""
    def display(self):
        # 데이터(name, age)는 나를 상속받은 자식 객체가 가지고 있을 거라고 믿고 사용한다.
        print(f"이름: {self.name}, 나이: {self.age}")

class Person(DisplayMixin):
    def __init__(self, name, age):
        # 데이터는 오직 진짜 클래스인 Person에서만 관리한다.
        self.name = name
        self.age = age

p = Person("Hannuri", 25)
p.display() # 믹스인의 기능을 가져다 쓴다.
```

### 믹스인 클래스가 클래스별로 특화된 기능을 필요로 한다면 인스턴스 수준에서 끼워 넣을 수 있는 기능(정해진 메서드를 통해 해당 기능을 인스턴스가 제공하게 만듦)을 활용한다.

- 정해진 이름의 메서드를 자식이 구현하게 함으로써, 믹스인이 자식의 특화된 기능을 가져다 쓰는 구조를 만든다.
- 예시 코드
    - 메시지를 출력하는 믹스인을 만드는데, 어떤 클래스는 `[INFO]`라고 붙이고 싶고, 어떤 클래스는 `[ERROR]`라고 붙이고 싶어 하는 상황을 가정해 보자
    

```python
# 1. 믹스인 정의
class LoggerMixin:
    def log(self, message):
        # 믹스인은 get_prefix가 어떻게 생겼는지 모르지만,
        # 자식이 제공해줄 것이라고 믿고 호출한다.
        prefix = self.get_prefix() 
        print(f"{prefix} {message}")

# 2. 첫 번째 자식 클래스 (정보용)
class InfoService(LoggerMixin):
    # 믹스인이 요구하는 '정해진 메서드'를 구현한다.
    def get_prefix(self):
        return "[INFO]"

# 3. 두 번째 자식 클래스 (오류용)
class ErrorService(LoggerMixin):
    # 같은 메서드 이름이지만 내용을 다르게 끼워 넣는다.
    def get_prefix(self):
        return "[ERROR]"

# 사용해보기
info = InfoService()
info.log("서버가 시작.") # 출력: [INFO] 서버가 시작

err = ErrorService()
err.log("연결에 실패.")    # 출력: [ERROR] 연결에 실패
```

- 코드 설명
    - `LoggerMixin`: `log`라는 공통 기능을 제공한다. 그런데 출력을 예쁘게 하기 위해 `self.get_prefix()`를 호출. 정작 믹스인 본인에게는 이 함수가 없다. (이게 바로 ‘인스턴스가 제공하게 만든다’ 라는 의미이다.)
    - `get_prefix` 메서드: 믹스인과 자식 클래스 사이의 약속(Interface). 부모를 상속받으려면 최소한 이 이름의 함수는 네가 만들어야 한다는 의미.
    - 특화된 기능: `InfoService`와 `ErrorService`는 각각 자신만의 `get_prefix`를 구현. 믹스인은 똑같지만, 끼워 넣은(구현한) 메서드 덕분에 결과물이 달라진다.

### 믹스인에는 필요에 따라 인스턴스 메서드는 물론 클래스 메서드도 포함될 수 있다.

- 예시 코드 : JSON 마법사 믹스인
    - 딕셔너리 데이터를 받아서 객체를 만들고(`클래스 메서드`), 객체를 다시 JSON으로 바꾸는(`인스턴스 메서드`) 기능을 가진 믹스인을 만들어 보자.
    
    ```python
    import json
    
    class JsonMagicMixin:
        # 1. 클래스 메서드 (클래스 전체의 공통 매뉴얼)
        @classmethod
        def from_json(cls, json_data):
            # json 데이터를 읽어서 해당 클래스(cls)의 객체로 만들어준다. 
            kwargs = json.loads(json_data)
            return cls(**kwargs) # cls는 나중에 이 믹스인을 쓸 클래스가 된다.
    
        # 2. 인스턴스 메서드
        def to_json(self):
            # self에 있는 데이터를 JSON 문자열로 바꾼다.
            return json.dumps(self.__dict__)
    
    # 사용해보기
    class User(JsonMagicMixin):
        def __init__(self, name, age):
            self.name = name
            self.age = age
    
    # [클래스 메서드 사용] 문자열을 넣었더니 User 객체가 튀어 나온다.
    json_str = '{"name": "Hannuri", "age": 25}'
    new_user = User.from_json(json_str)
    print(f"생성된 유저: {new_user.name}")
    
    # [인스턴스 메서드 사용] 객체를 다시 문자열로 바꾼다.
    print(f"다시 JSON으로: {new_user.to_json()}")
    ```
    

### 믹스인을 합성하면 단순한 동작으로부터 더 복잡한 기능을 만들 수 있다.

```python
# 1. 대문자로 변환
class UpperCaseMixin:
    def process_text(self, text):
        # 부모나 다른 믹스인에 process_text가 있다면 그 결과를 먼저 받고, 
        # 없으면 받은 그대로를 대문자로 바꾼다.
        data = super().process_text(text) if hasattr(super(), 'process_text') else text
        return data.upper()

# 2. 느낌표 추가
class ExclamationMixin:
    def process_text(self, text):
        data = super().process_text(text) if hasattr(super(), 'process_text') else text
        return data + "!!!"

# 3. 기본 텍스트 반환
class BasicText:
    def process_text(self, text):
        return text

# 4. 합성
class ShoutMessage(UpperCaseMixin, ExclamationMixin, BasicText):
    pass

# 실행 결과
shouter = ShoutMessage()
print(shouter.process_text("hello world")) 
# 출력: HELLO WORLD!!!
```

## **42. 비공개 애트리뷰트보다는 공개 애트리뷰트를 사용하라**

### 기억해야 할 내용

- 파이썬 컴파일러는 비공개 애트리뷰트를 자식 클래스나 클래스 외부에서 사용하지 못하도록 엄격히 금지하지 않는다.
- 내부 API에 있는 클래스의 하위 클래스를 정의하는 사람들이 부모 클래스의 애트리뷰트를 사용하지 못하도록 막기보다는 애트리뷰트를 사용해 더 많은 일을 할 수 있게 허용하는 것이 좋다.
- 비공개 애트리뷰트로 (외부나 하위 클래스의) 접근을 막으려고 시도하기보다는 보호된 필드를 사용하면서 문서에 적절한 가이드를 넣는다.
- 코드 작성을 제어할 수 없는 하위 클래스에서 이름 충돌이 일어나는 경우를 막고 싶을 때만 비공개 애트리뷰트를 사용하는 것이 좋다.

## 43. **커스텀 컨테이너 타입은 `collections.abc`를 상속하라**

### 기억해야 할 내용

- 간편하게 사용할 경우에는 파이썬 컨테이너 타입(리스트나 딕셔너리 등)을 직접 상속하라.
- 커스텀 컨테이너를 제대로 구현하려면 수많은 메서드를 구현해야 한다.
- 커스텀 컨테이너 타입이 `collections.abc`에 정의된 인터페이스를 상속하면 커스텀 컨테이너 타입이 정상적으로 작동하기 위해 필요한 인터페이스와 기능을 제대로 구현하도록 보장할 수 있다.

### 간편하게 사용할 경우에는 파이썬 컨테이너 타입(리스트나 딕셔너리 등)을 직접 상속하라.

- 컨테이너란 무엇인가?
    - 리스트(`list`): `[1, 2, 3]` 처럼 데이터를 순서대로 담는 그릇
    - 딕셔너리(`dict`): `{'이름': 'Hannuri'}` 처럼 키와 값을 짝지어 담는 그릇
    - 세트(`set`): 중복을 허용하지 않고 담는 그릇
    - 튜플(`tuple`): 한 번 담으면 바꿀 수 없는 그릇
- 커스텀 컨테이너 타입이란?
    - `class MyList(list):` 라고 정의하면, `MyList`는 이제 파이썬의 기본 `list` 타입이 아니라, 내가 설계한 새로운 컨테이너 종류(타입)가 된다.

```python
# 1. 파이썬의 기본 list를 직접 상속
class FrequencyList(list):
    def __init__(self, members):
        super().__init__(members)

    # 2. "빈도수 계산" 기능 추가
    def frequency(self):
        counts = {}
        for item in self:  # self 자체가 리스트이므로 바로 루프를 돌 수 있다.
            counts[item] = counts.get(item, 0) + 1
        return counts

# 사용해보기
foo = FrequencyList(['사과', '바나나', '사과', '포도', '바나나', '사과'])

# list의 기본 기능인 len()과 pop()을 그대로 쓸 수 있다.
print(f"전체 개수: {len(foo)}") 

foo.pop() # 마지막 '사과' 하나 제거
print(f"남은 과일: {foo}")

print(f"과일별 빈도: {foo.frequency()}")
```

### 커스텀 컨테이너 타입이 `collections.abc`에 정의된 인터페이스를 상속하면 커스텀 컨테이너 타입이 정상적으로 작동하기 위해 필요한 인터페이스와 기능을 제대로 구현하도록 보장할 수 있다.
