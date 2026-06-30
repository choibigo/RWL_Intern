# Docker란?
###### 도커(Docker)는 컨테이너를 만들고 관리하는 프로그램이다.
###### container는 프로그램이 실행되는 독립적인 공간이다.

-----

### Docker를 사용하는 이유:

### **1. 동일한 환경을 어디서나 재현하기

### 2. 한 대의 컴퓨터에서 여러 환경을 사용하기




- image layer는 읽을 수만 있으며(수정 불가) container layer는 읽고 쓸 수가 있다. 아래 그림처럼 다른 container들이 하나의 image를 구성하는 image layer들을 공유한다.

![layer](../../images/layer.png)

---
# Docker command

#### docker command는 아래와 같은 규칙을 갖고 있다.

![command](../../images/docker_grammer_structure.png)

# command를 어떻게 사용할지 모르겠거나 어떤 옵션을 사용할 수 있을지 궁금하다면 맨 뒤에 --help를 붙히면 된다.





