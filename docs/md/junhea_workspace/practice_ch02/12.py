a = b = [1, 2, 3]
a[1] = 4
print(b)
## 객체를 가리키는 이름만 다를 뿐 같은 객체를 지정하고 있기 때문에 결과가 a와 같다. 만약 이를 원하지 않는다면 copy() 모듈을 이용하자.