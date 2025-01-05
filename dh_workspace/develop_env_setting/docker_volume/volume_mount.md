[volume종류설명](https://deveric.tistory.com/111)

[volume따라하기](https://www.daleseo.com/docker-volumes-bind-mounts/)

docker_experiment폴더에서 실행을 했다.

```docker
docker volume create my_vol
```
my_vol이라는 volume을 생성함.

```docker
docker volume ls
```
volume의 종류를 확인

```docker
docker volume inspect my_vol
```
my_vol을 자세히 보자.

```docker
docker run -v my_vol:/app --name testing -d -p 8080:80 cuda_exp
```
my_vol:/app은 my_vol을 mount하는데 컨테이너의 /app이라는 경로에 마운트 하는 것이다.

cd /를 한 후 dir을 하면 app이라는 경로가 있다는 것을 확인할 수 있다.

***

```ubuntu
apt install gedit -y
```
