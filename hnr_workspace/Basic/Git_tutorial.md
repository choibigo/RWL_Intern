# Git_tutorial

![image.png](image.png)

## Git

- 프로그램을 개발하다 보면 소스(코드, 문서, 설정 파일 등)가 지속적으로 업데이트 된다.
- Git 이랑 소스의 변화를 계속 감시하고 있음
    - 개발자의 코드 변경 사항 추적
    - 변경 사항 갱신
    - 관리
    - 일반적으로 코드의 버전을 관리한다고 표현함
- Git 이 관리하는 공간을 저장소(repository)라고 한다.
- 저장소는 내 컴퓨터 환경(Local)안에 존재한다.

→ Git 은 local 저장소의 코드 버전을 관리한다.

## Github

- Git이 관리하는 저장소를 온라인에서 사용할 수 있도록 지원해주는 플랫폼
- 코드 버전 관리를 온라인에서
- 다른 사람들과 코드를 공유, 협업 가능 → Github 만의 기능이 존재

## Repository(저장소)

- Git 과 Github 는 repo 단위로 코드를 관리한다.
- Repo : 내 코드를 담고 있는 저장소
    - local repo : 내 컴퓨터에서 저장된 프로젝트 & 코드
    - remote repo : Github 서버에 저장된 프로젝트 & 코드
- 작업은 로컬에서 → 원격에 업로드
- 필요시 원격에서 로컬로 다운로드

## Repository 만들기

![image.png](image%201.png)

![image.png](image%202.png)

![image.png](image%203.png)

```jsx
git init
```

- 해당 repo에서 git 을 쓰겠다고 선언해야함
- 정상적으로 진행된다면 local repo 내에 .git 폴더가 생성
- 해당 폴더 내에 소스 변화를 기록

![image.png](image%204.png)

![image.png](image%205.png)

## 작업 공간 config 설정

- Local repo 가 remote repo 와 연결되려면 local 환경에서 신원을 설정해야함
    - 로그인과 비슷한 개념이다.
- 신원 설정을 위한 config 를 세팅
    - 영향력의 범위
        - Global config : 컴퓨터의 모든 github repo에 영향(우선순위 낮음)
            - 주의해서 사용 필요
            - Github 계정이 2개 이상이거나, 서버에서는 사용 금지
        - Local config : 지금 있는 위치의 repo에서만 영향(우선순위 높음)
            - git init은 우선되어야 함

![image.png](image%206.png)

- 업로드용 테스트 파일 생성

![image.png](image%207.png)

```python
echo "# Hannuri_GithubBasic" >> README.md 
git init
git add README.md 
# 어떤 코드를 업로드 할 것 인가?
# add 뒤로는 내가 업로드할 파일이 들어간다.

git commit -m "first commit" 
# 그 코드는 무엇인가?
# -m : message 의 형태로 commit 을 달아주겠다.

git branch -M main
# 원격에 추가할 파일과 commit 설명들 main 이라고 하는 branch에 업로드가 될 것이다.

git remote add origin https://github.com/ResNet24/Hannuri_GithubBasic.git
# 로컬 저장소와 원격 저장소를 이어주는 기능을 한다.
# 로컬에게 origin 이라고 하는 것은 내가 만든 github 서버의 해당 페이지를 의미하게 된다.

git push -u origin main 
# 로컬 환경에서 원격 환경으로 코드를 동기화
```

![image.png](image%208.png)

- 로그인 필요

![image.png](image%209.png)

- 토큰 생성

![image.png](image%2010.png)

![image.png](image%2011.png)

![image.png](image%2012.png)

- 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

![image.png](image%2013.png)

- Repo 생성 완료

![image.png](image%2014.png)

## Git add, commit, push

![image.png](image%2015.png)

- 출처 : https://www.youtube.com/watch?v=HXsKNIz0VRk&t=26s

## Commit message

- 본인이 어떤 것을 변화 시켰는지를 파악하기 위해 알아보기 쉽게 적어야 함

## Git Pull

- 원격 repo 의 내용을 로컬 repo로 가지고 와서 덮어 씌우는 과정

## Github 용량 제한

- 50MB 이상을 Add 하고 Push 하면 경고
- 100MB 이상이면 에러
- 용량이 큰 파일(학습된 모델, 데이터, 중간 결과물(json,csv …)은 다른 경로(구글 드라이브 등)로 제공

## VSCode 와 Github

- VSCode 내에서 파일의 변화를 시각적으로 보여준다.
- M → Modified

![image.png](image%2016.png)

![image.png](image%2017.png)

- 내용을 수정하면 이를 시각적으로 볼 수 있고, 어떤 부분이 수정되었는지도 알 수 있다.

![image.png](image%2018.png)

- Untracked → 아직 원격에 올라가 있지 않은 파일 : 추적이 되고 있지 않음

![image.png](image%2019.png)

- VSCode 를 통해