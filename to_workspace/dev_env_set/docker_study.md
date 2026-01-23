### 계획
- [ ] 도커(Docker) 기초: 1~12강 시청
- [ ] [인프런] 비전공자도 이해할 수 있는 Docker 입문/실전: 1.1~2.8 시청.
- [ ] 도커 실습

# Docker study

![alt text](image.png)

[도커 기초 강의 1~12강](https://youtube.com/playlist?list=PLlTylS8uB2fDLJRJCXqUowsOViG-ZKnWy&si=r5twdtdIIQlsAnHI)

[비전공자도 이해할 수 있는 Docker 입문/실전 1.1~2.8강(총 12회)](https://youtube.com/playlist?list=PLtUgHNmvcs6rS5aNCRIZtVcyk3gRX2iOd&si=rcllx93oBu5SZAzI)

# 도커 기초 강의

## 1. [도커 기초강의 안내](https://youtu.be/p1-wm-ThnTI?si=5p0gFUGJ9eVFvugT)

도커란 **Container** 기반의 가상화 플랫폼.

어떤 프로그램이든 외부 환경과 격리된 채로 구동할 수 있게 만듬.

기본적으로 Linux 환경으로 설계됨.

![alt text](image-2.png)

- Infrastructure: PC의 하드웨어. (CPU, GPU, RAM)
- HOST Operating System: OS (Window, Linux)
- 그 위에 docker가 올라감. (정확히는 각 컨테이너를 돌릴 엔진 역할)
- 각각 하나의 App이 하나의 container인 것. (OS 위에 프로그램을 작동하는데 필요한 요소들만 모아 별도의 서버 처럼 작동.)


### 도커 생성과 배포는 윈도우, 리눅스 등을 따지지 않고 이루어질 수 있나?

양방향은 아니다. 리눅스 컨테이너는 윈도우, 맥, 리눅스 다른 버전 상관 없이 어디서든 실행가능하다. 기본적으로 리눅스 베이스로 설계 됐고. 윈도우와 맥 이용시 라이트한 리눅스 가상 머신을 띄워서 실행하기 때문이다.
> 참고로 그냥 리눅스에서 실행할때는 가상 머신을 만들지 않음.

하지만 윈도우 컨테이너는 오직 윈도우에서만 가능하다(윈도우에서 리눅스를 가상머신으로 띄워서 만든 컨테이너와 다른거다). 물론 이를 만들 일은 아마 없을 것이다.

### 도커 배포를 하드웨어 아키텍처를 고려하지 않고 할 수 있나?

배포는 가능하지만, 고려를 해야한다.

32비트와 64비트, 인텔/AMD CPU와 맥 CPU 등, 각각에서 돌아가고 만든 도커는 원래 다른 기기에서 작동하지 않는다.

그래서 도커에서 Multi-Arch Build이라는, 하나의 도커 이미지에 여러 아키텍처용 실행 파일을 담는 기능을 제공한다. 이를 통해 사용자는 본인 환경에 맞는 버전에 맞춰서 빌드를 할 수 있다.

물론 그러면 사용자 입장에서 할 일이 살짝 늘어나긴 한다.

근데 그 도커 속의 라이브러리들이 해당 아키텍처를 지원해야한다. 안하면 빌드가 안될 수도?

### 도커와 VM(Virtual Machine)의 차이는?

- VM: 완전히 독립된 완전한 OS. 모든 기능들을 다 갖추고 있음. But 넘 무겁고 느림. 사실상 집 안에다 집을 지은 느낌?
- Docker: OS 커널을 기존과 공유하면서도, 가상 환경의 최소 조건을 갖춤. 훨씬 가볍고 빠름. 집에 방을 월세 내서 다른 사람 입주 시킨 것과 같음.

물론 그대신에 Docker는 보안성이 약하다는 단점이 있음.

### 도커와 Conda/Venv의 차이는?

두쪽 모두 독립된 환경을 만드는 것은 같음. 하지만 어느 수준까지 독립시키느냐가 차이점이다.

- Venv/Conda: 패키지 및 시스템 라이브러리, Cuda 등을 분리.
- Docker: OS 전체를 분리. 파일, 시스템, 네트워크, 환경변수 등 다 분리됨. 심지어 NVIDA GPU 드라이버까지 분리됨 (물론 근데 이건 개인의 GPU마다 조금 다르니 마냥 배포를 따르게 할 수는 없음).


## 2. [컨테이너 구조 및 커맨드 사용법 -이론편-](https://youtu.be/M25Pl0tX8yw?si=vG3Za_augQ_MW-kW)

## 3. [도커 커맨드 사용법 -실습편-](https://youtu.be/prohMhNwZF0?si=4wZnvjEQ4tAUgwT6)

## 4. [도커 컨테이너 통신하기 -이론편-](https://youtu.be/jTOqXmRKGzA?si=5mae4-Qaf8IxxYuE)

## 5. [도커 컨테이너 통신하기 -실습편-](https://youtu.be/v6KJAovryCo?si=U-jwN2YAzKSKlsDt)

## 6. [도커파일(Dockerfile) 작성하기 -이론편-](https://youtu.be/8p9RvxVOQEY?si=WcrQxiOtltb42b_F)

## 7. [도커파일(Dockerfile) 작성하기 -실습편-](https://youtu.be/BCsiVlmEQCQ?si=USMi7pIvc-Z1iNMP)

## 8. [도커 컴포즈(docker-compose) 파일 작성하기 -이론편-](https://youtu.be/3FY-DzXYu7E?si=cmIGua6Z1AtuQ_fo)

## 9. [도커 컴포즈(docker-compose) 파일 작성하기 -실습편-](https://youtu.be/vwL0I5dhdyI?si=EGhaAOYFFRoBwOOp)

## 10. [도커 이미지 생성 및 저장하기 -이론편-](https://youtu.be/az46ttJ8JUQ?si=MBMz67SchFjzgyZt)

## 11. [도커 이미지 생성 및 저장하기 -실습편-](https://youtu.be/bK6sHpy9au0?si=YpPTirMAuV4pI3xX)

## 12. [스프링 부트 Dockerfile 만들기](https://youtu.be/MsMHStVibEk?si=NPNfP0_nUw5EGwfA)
