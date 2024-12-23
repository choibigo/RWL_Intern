# git

working directory: 사용자가 파일을 수정하는 곳.<br><br>
staging: coommit할 준비를 하는 곳. 이 영역에 있는 파일만 commit 한다.<br><br>
local repository: commit된 파일들이 저장되는 곳입니다.<br><br><br>

### git clone

git clone : 원격 저장소를 로컬 저장소로 복제.

>git clone https://github.com/choibigo/RWL_Intern.git

### git add

git add : Git에서 변경된 파일을 스테이징 영역에 추가하는 명령어
스

> git add . # 모든 파일을 추가
> git add README.md # README.md만 추가

### git commit

git commit : 로컬에서 변경 사항을 저장  (메시지 없이 commit이 안됨.)
>git commit -m "commit 할 때의 메시지"

### git push

git push : 로컬 변경 사항을 원격 저장소에 반영
> git push origin main      # main branch에 추가. origin 대신 링크를 넣어도 됨.

### git pull

git pull : 원격 저장소의 변경 사항을 로컬에 반영
> git pull origin main

### 다른 명령어들

git remote -v : 원격 저장소(Remote Repository)의 URL을 확인하는 명령어, 연결된 원격 저장소의 주소를 알 수 있다.
> git remote -v  

