### 계획
- [ ] PEP 8 탐색 및 스터디 구상

# PEP 8

![alt text](images/p8_0_image.png)

https://peps.python.org/pep-0008/

PEP 8은 파이썬 코드 작성시 지켜야하는 공식 스타일 가이드. 코드는 작성하는 시간 보다 읽는 시간이 훨씬 길기에 가독성을 높이는 것이 목표.

들여쓰기, 이름 짓기, 코드 레이아웃 등, 다양한 규칙이 존재함.

해당 가이드라인은 어디까지는 기본적인 기준일 뿐이며, 만약 특정 프로젝트나 코드에서 다른 가이드라인을 이용하고 있다면 해당 환경에 맞추는 것이 맞다.

## Indentation

파이썬은 기본적으로 들여쓰기로 많은 것을 구분하기에 매우 중요하다.

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

```py

```