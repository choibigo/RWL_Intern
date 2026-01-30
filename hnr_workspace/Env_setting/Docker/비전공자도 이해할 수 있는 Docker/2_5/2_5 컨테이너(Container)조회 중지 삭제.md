# 2.5 컨테이너(Container)조회/중지/삭제

- 중단된 컨테이너까지 모두 조회
    
    ![image.png](image.png)
    
    ![image.png](image%201.png)
    
- docker stop 과 docker kill
    - docker kill = 강제로 끄기
        - 중지되어 있는 것은 kill이 안된다.

![image.png](image%202.png)

- 실행 중인 컨테이너는 삭제할 수 없다. → 컨테이너를 중지해야함

![image.png](image%203.png)

![image.png](image%204.png)

- 중지되어 있는 모든 컨테이너 삭제

```python
docker rm $(docker ps -qa)
```

- 실행되고 있는 컨테이너를 삭제하는 방법

![image.png](image%205.png)