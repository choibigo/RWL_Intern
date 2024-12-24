# docker의 구성
* image
* container

---

## image
* template이다.
* 불변
* 격리되지도 않고 실행되지도 않는다.
* 지속적
* 컨테이너는 이미지를 사용한다.
* 공통적
* 이미지 위에 컨테이너를 생성.

## container
* 독립적 실행환경
* 동적
* 다른 컨테이너와 격리됨(독립적)
* 실행 중에만 실시된다.
* 개별적
* application 실행



# docker 통신

도커 컨테이너는 기본적으로 독립적인 환경에서 실행되기 때문에 컨테이너 밖에서 접근될 수 없다.

컨테이너와 통신하기 위해서는 컨테이너를 가동시키면서 'p' 옵션을 사용하여 호스트(pc 또는 서버)의 포트와 컨테이너의 (컨테이너가 외부와 통신하기 위해 열리는)포트를 설정해야 함.

-p \${host_port}:${container_port}<br>
ex) 8080:80         (호스트가 8080, 컨테이너가 80)

이 설정을 사용하기 위해서는 host에서 사용 중인 포트와 번호가 겹치지 않는지 확인해야 한다.

예시)
>docker run --name test1 -d httpd<br>

>docker run --name test1 -d -p 8080:80 httpd

* --name1 > test1이라는 이름으로 컨테이너를 생성한다.
* -d > 백그라운드로 동작한다.
* -p 8080:80 > 호스트의 포트는 8080, 컨테이너의 포트는 80으로 세팅하여 네트워크를 설정한다.

<br>

### 상태 확인
>docker ps<br>
>docker ps -a
* docker ps : 현재 실행 중인 컨테이너만 나옵
* docker ps -a : 실행 중이든 종료되었든 모든 컨테이너를 나열

>docker container ls
* 실행중인 container만 보여준다.
>docker container ls -a
* 위의 docker ps -a와 같은 기능의 명령어이다. 근데 쓸 거면 얘를 써라.

>docker image ls
* 실행중인 이미지를 보여준다.

### 중지 및 삭제
container를 실습할 때 중지 및 삭제를 해주는 것이 좋다.

>docker stop test1
* test1 중지
>docker rm test1
* test1 삭제

또는 docker desktop에서 리스트를 보고 gui를 통해 삭제해도 괜찮다.


## 실습
>docker run --name test1 -d httpd<br>

를 하고 난 후<br>
>docker run --name test1 -d -p 8080:80 httpd

를 하면 에러가 남.<br>

왜 와이? 이미 test1이라는 container가 돌아가고 있는데 test1이라는 이름으로 또 run을 하면 충돌이 일어나기 때문.<br>
solution is ... 이름을 바꿔서 run을 하면 된다.<br>
>ex) docker run --name test2 -d -p httpd 8080:80

run 하다가 삭제할 거면 먼저 중지를 시킨다.
>docker stop test1

그러고 삭제
>docker rm test1