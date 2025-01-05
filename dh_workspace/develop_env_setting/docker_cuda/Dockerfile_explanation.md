Dockerfile이 존재하는 docker_experiment폴더에서

```docker
docker build -t cuda_exp .
```
을 하고 빌드가 된 후에

```docker
docker run --name testing -d -p 8080:80 cuda_exp
```
를 통해 컨테이너를 run한다.

```docker
docker exec -it testing /bin/bash
```
를 통해 exec하여 ubuntu에 들어간다.
(만약 ubuntu에서 나오고 싶다면 exit, 다시 들어가고 싶다면 docker start testing을 하면 된다.)

이후에 
```docker
docker run -it --gpus all cuda_exp:latest /bin/bash
```
---
**chatgpt 설명**

이 명령어는 Docker 컨테이너를 실행하는 명령입니다. 세부적으로 살펴보면:

* docker run: 새로운 Docker 컨테이너를 실행하는 명령어입니다.
* -it: -i는 인터랙티브 모드로 컨테이너를 실행하도록 하고, -t는 터미널을 할당하여, 터미널에서 직접 명령어를 입력할 수 있게 합니다.
* --gpus all: 이 옵션은 컨테이너가 모든 GPU에 접근할 수 있게 합니다. --gpus all은 Docker 컨테이너가 NVIDIA GPU를 사용할 수 있도록 하여, GPU 가속을 활용하는 작업을 가능하게 합니다.
* cuda_exp:latest: 실행하려는 Docker 이미지 이름입니다. 이 이미지는 cuda_exp라는 이름을 가진 이미지의 latest 태그 버전입니다. 이 이미지에는 GPU를 활용하는 CUDA 관련 프로그램이 포함되어 있을 수 있습니다.
* /bin/bash: Docker 컨테이너 내에서 실행할 명령어입니다. 이 경우, /bin/bash는 컨테이너 내에서 Bash 쉘을 실행하여 사용자가 명령어를 입력할 수 있게 합니다.

이 명령어의 목적은 CUDA 환경에서 GPU를 사용하는 Docker 컨테이너를 실행하는 것입니다. 즉, GPU를 활용하는 코드나 프로그램을 컨테이너 내에서 실행할 준비를 하는 것입니다.

---
```docker
nvidia-smi
```
---
**chatgpt 설명**
* nvidia-smi는 NVIDIA GPU 상태를 확인하는 명령어입니다. 이 명령어는 GPU의 상태, 드라이버 버전, 사용량, 온도, 메모리 사용량 등을 확인할 수 있게 해줍니다.

* nvidia-smi는 GPU 리소스의 상태를 모니터링하는 도구입니다.

이 명령어를 통해 현재 시스템에 설치된 GPU가 잘 작동하는지, GPU 메모리 사용량은 얼마인지, GPU 드라이버가 올바르게 설치되었는지 등을 확인할 수 있습니다.

---
**요약**

* docker run -it --gpus all cuda_exp:latest /bin/bash: Docker 컨테이너 내에서 GPU를 활용한 작업을 시작하려는 명령어.
* nvidia-smi: 시스템에서 GPU의 상태와 정보를 확인하는 명령어.
---

이 코드도 참고하자.
```
nvcc -V
```
-V의 의미는 volume의 V이다.
cuda이식은 여기까지...