[유튜브](https://www.youtube.com/watch?v=Rw1gRR7lZwQ&list=PLtUgHNmvcs6rS5aNCRIZtVcyk3gRX2iOd&index=4)

# 전체 흐름 느껴보기
```docker
docker pull nginx   #nginx의 이미지를 다운받는 명령어
```
```docker
docker image ls     # 다운받은 image 목록을 볼 수 있다.
```
```docker
docker run --name webserver -d -p 80:80 nginx #컨테이너 실행
```

chrome으로 가서
>localhost:80

을 입력하면 nginx가 설치되고 실행되었다는 것을 알 수 있다.

```docker
docker ps       #실행되고 있는 컨테이너의 목록을 나타낸다.
```
```docker 
docker stop webserver       #실행시킨 webserver 컨테이너를 정지시킨다.
```

chrome에서 localhost:80을 새로고침 하면 실행이 안된다.

---

# 이미지 다운로드

```docker
docker pull nginx   #nginx의 이미지를 다운받는 명령어
```

```docker
docker image ls     # 다운받은 image 목록을 볼 수 있다.
```

이미지를 어디서 다운 받았는가?
- dockerhub로부터 다운을 받음.
- dockerhub란?
    - 사람들이 올려놓은 이미지들이 저장되어 있고 그 이미지들을 pull을 통해 다운받아서 사용하도록 만든 저장소임.
- dockerhub에 올라온 이미지마다 버전이 있다. dockerhub에서 tags를 누르면 다양한 tag명이 나와있는데 이 tag명이 버전을 의미함. 특정 버전을 나타내는 이름을 tag명이라 하고 특정 tag명을 가진 image를 다운 받고 싶다면 https://hub.docker.com/_/nginx/tags 에서 원하는 tag를 찾은 후
```docker
docker pull nginx:stable-alpine3.19-perl # ":" 뒤에 tag명을 붙여서 쓰면 된다.
```

위에서 본
```docker
docker pull nginx  
```
의 경우 뒤에 :latest가 생략되어 있다.

---

# 이미지 조회
```docker
docker image ls     #다운받은 이미지 조회 가능. (ls는 list를 의미)
```

- tag는 각 이미지의 version을 뜻한다.
- image id는 각 이미지마다 고유의 id값이 있는데 그것을 의미함.
- created는 이미지가 생성된 날짜를 의미(이미지를 다운받은 날짜가 아니다!)

이미지를 삭제하려면
```docker
docker image rm [image id]
```
를 하면된다.

예시)
nginx:stable-alpine3.19-perl의 image id가 456c0c9bd0d4라면
```docker
docker image rm 456c0c9bd0d4
```
를 하면 됨.

하지만~~~ 그냥 아래와 같이 image id의 일부만 쳐도 가능하다.
```docker
docker image rm 456c
```

<br>
중단시키든, 사용되고 있든 존재하고 있는 컨테이너에서 이미지가 사용되고 있으면 이미지를 지우지 못한다. 즉 컨테이너에서 사용하고 있지 않은 이미지만 삭제가 가능하다.

만일 이미 중단된 컨테이너에 있는 이미지를 강제로 삭제하고 싶다면?

* -f를 이용해서 삭제.
```docker
docker rm -f 742e9       #42e9는 nginx의 image id이다.
```

* 그러고 docker image ls를 이용해서 확인을 하면 이미지가 잘 삭제된 것을 확인할 수 있다.