# Git_basic
###### git은 컴퓨터 파일의 변경사항을 추적하고, 여러 명의 사용자들 간에 파일들의 작업을 조율 하기 위한 분산 버전 관리 시스템
-----

1. ``` bash
   git clone <URL>
   ```

- 원격 저장소의 전체 프로젝트를 내 컴퓨터(로컬)로 복사한다.

2. ``` bash
   git add [파일 경로]
   git commit -m "변경 내용 요약"
   ```
- git add를 통해 수정 사항을 local storaging으로 보내고
git commit -m ""을 통해 수정 내용들을 묶어서 local Repository로 보낸다.

3. ``` bash
   git push origin main
   ```
- git push를 통해 local Repository에 있던 commit들을 Github에 올린다.

4. ``` bash
   git pull origin main
   ```
- git pull을 통해 다른 사람들의 수정내용을 원격 저장소로부터 내 컴퓨터(로컬)로 받아올 수 있다.

