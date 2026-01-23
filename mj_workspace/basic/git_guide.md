# Git Guide
>커밋(commit): 작업 내용을 저장해 두는 기록(스냅샷)
>브랜치(branch): 커밋들이 쌓이는 작업 공간

## **1. 기본 (clone / add / commit / push / pull)**
### git clone
```bash
git clone ~/~/~.git
```
원격 저장소에 있는 프로젝트를 **내 컴퓨터로 clone**.

### git add
```bash
git add .                    # 전체 스테이징
git add <파일명>               # 스테이징
git restore --staged <파일명>   #스테이징 취소
```
변경된 파일을 커밋 대상(스테이징 영역)에 추가함.

### git commit
```bash
git commit -m "first commit"
```
변경 사항을 기록하여 저장.

### git push
```bash
git push origin main
```
로컬 저장소의 커밋을 **원격 저장소로 업로드**.

### git pull
```bash
git pull origin main
```
원격 저장소의 최신 변경 사항을 가져와 **로컬에 반영**.

<br>


## **2. 확인(status/ remote/ log/ diff)**

### git status
```bash
git status #현재 작업 상태(수정된 파일, 스테이징 여부)를 확인.
```

### remote
```bash
git remote -v   # 원격 저장소 연결 정보 확인.
```

### git log
```bash
git log              # 상세 로그 (전체 정보)
git log --oneline    # 요약 로그 (한 줄씩)
```
커밋 기록 확인.

### git log
```bash
git diff           #수정된 내용만 확인 (add 후 내용 X) [스테이징 전]
git diff --staged  #커밋 될 변경 내용 확인 (add 후 내용 O) [스테이징 후]
```
변경 내용 비교.

<br>

## **3. 브랜치 (branch / switch / merge)**

### git branch
```bash
git branch         # branch 목록 확인
git branch test1   # branch 목록 생성
```

### git switch
```bash
git switch test      # 특정 브랜치로 이동
git switch -c test   # 특정 브랜치를 생성 및 이동
```

### git merge
```bash
git merge test      # 브랜치 병합
```

### git stash
```bash
git stash        # 작업 내용 임시 저장
git stash pop    # 복원
```