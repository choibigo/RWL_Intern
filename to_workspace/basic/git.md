### 계획
- [x] git 이론 복습
- [x] PC 세팅 복습
- [x] 기본 명령어로 복습
- [ ] 추가로 유용한 명령어 익히기
- [ ] 브랜치 merge 문제 해결

---

# GIT 이론 복습

GIT은 분산 버전 관리 시스템(DVCS)으로, 파일을 변경 이력을 기록하고, 관리할 수 있도록 도와주는 개발자용 핵심 툴이다.

**기본 구조**
![alt text](images/git_arch.png)

위에 보이는 것을 제외하고, 작업 중 이동할때 임시 저장용으로 주로 사용하는 *stash*라는 상태도 존재한다.

## PC 세팅 복습

기존 키 삭제 후

`ssh-keygen -t ed25519 -C "tpingouin@gmail.com"`

`cat ~/.ssh/id_ed25519.pub`

`git clone git@github.com:choibigo/RWL_Intern.git`

`git remote -v`

![alt text](images/image.png)

## 기본 명령어 복습

`git status`

`git add .\to_workspace\basic\`

`git commit -m "First commit: Start from basic"`

`git push origin main`

# 유용한 명령어 익히기

`git show` = 마지막 커밋 정보 출력

![alt text](images/git_show.png)

`git show 커밋명` = 해당 커밋 정보 출력

`git log -p` = 커밋 로그 + 개별 변경점 전부 출력

`git diff` = add 전에 어떤 것들이 변경 됐는지 출력

`git commit --amend -m "새로운 메시지"` = 이전 커밋 메시지 수정 (*단, 이미 remote까지 푸쉬가 됐다면 --force으로 강제로 덮어씌워야함*)

## stash 실습

## 커밋 압축
커밋이 너무 많아질때 이를 유지보수하기 좋게 rebase를 이용하여 여러 커밋을 하나로 압축할 수 있다.

`git rebase -i`

이미 푸쉬를 했다면 --force 필요. 

개인 작업 브랜치에서 작업할 때 유지보수를 위해 rebase해도 상관없지만, 만약 공동 브랜치에서 rebase를 했다가 다른 사람과 커밋이 꼬이면 지옥의 merging 작업 펼쳐질 수 있기 때문에 각별한 주의가 필요하다. 그러니 공동 브랜치에서는 가급적으로 rebase을 사용하지 말아라.


## git reflog

## git worktree

## git bisect