### 계획
- [x] vscode 팁 서치
- [x] vscode 단축키 정리
- [x] merge 충돌 해결해보기

---
# VScode 팁

## 자동저장 꼭 사용하기
**매우 중요함**

![alt text](images/vs_image.png)

항상 체크해주자.

물론 자동저장으로 인해 피해볼 상황도 생길 수 있지만, 하지 않아서 피해본 경험이 더 많다.

## VScode를 깃 디폴트 편집기로 이용하기 (**중요**)

`git config --global core.editor "code --wait"` = Vim 대신에 vscode 사용해서 편집하기

## Merge 오류 해결

VScode에서 branch merge를 간편하게 해결할 수 있다.

- 먼저 merge를 받을 브랜치로 이동한 뒤

`git switch main`

- merge 수행

`git merge to_basic_git`

- 이때 git에서 vscode 편집을 디폴트로 세팅했다면 창에 바로 merge 편집 세팅이 뜬다.

- 그리고 충돌이 있다면 수동으로 merge를 진행하면 된다.

- 보통 다음 버튼 중에 누르면 된다.

    Accept Current Change: merge 받을 브랜치의(현 브랜치) 변경을 살리고, 들어오는 브랜치 변경은 버림.

    Accept Incoming Change: 들어오는 브랜치 코드를 살리고, merge 받을 브랜치 코드는 버림.

    Accept Both Changes: 둘 다 남김 (위아래로 붙여줌).

> 참고로 아래 처럼 둘다 비교하는 창으로도 들어올 수 있는데(compare 사용 시), 이때 수정은 안되고 보는 것만 된다. 확인한 뒤에 창 닫고 돌아가서 마저 수정하면 된다.
  <img src="images/vs_0_image.png" width="430">


- 모든 충돌을 해결했다면 변경사항을 스테이지에 올리고, 커밋을 하면 끝난다.

`git add . `

`git commit -m "Merge done"`

그러면 이런식으로 예쁘게 merging이 된다.

![alt text](images/vs_0_image-1.png)

### Project manager 익스텐션

그동안 여러 창을 켜둔 vscode 윈도우를 끄기 싫었지만 이제는 아니다.

![alt text](images/vs_0_image-5.png)

프로젝트 매니저를 사용해서 현재 창들을 다 세이브하고, 나중에 한꺼번에 다시 꺼내 사용할 수 있다.

1. ctrl + p

1. `>pmsp` 입력

1. save project

우측 창에 세이브 됐다!

![alt text](images/vs_0_image-6.png)

이제 vscode 윈도우를 끄고 새로 만들어도 해당 세이브를 가져오면 창들이 똑같이 열린다.

### GitLens
코드를 누가, 언제, 어떤 커밋에서 수정했는지 흐릿하게 볼 수 있음.

![alt text](images/gitlens.png)

## 단축키 모음

ctrl + p : 파일 찾기

ctrl + ` : 터미널 열기

> 참고로 `의 명칭은 백틱이다.

ctrl + k v : md 파일 시각화

ctrl + shift + f : 폴더 전체에서 찾기

ctrl + l : 현재 라인 전체 선택

ctrl + d : 똑같은 글 동시 수정

ctrl + k ctrl + t : 테마 변경

**ctrl + enter** : 다음 줄에 공백 줄을 추가함. 들여쓰는거랑 다름 (이전 줄 중간에 있을 때 들여쓰면 줄이 잘리고 들여써짐).

ctrl + shift + enter : 위에 공백줄 추가

**ctrl + space** : 자동완성 선택 재오픈

![alt text](images/vs_0_image-2.png)

ctrl + shift + space : 매개변수 정보 출력

**ctrl + shift + r** : 지정한 부분이 함수가 됨 or 변수로 담아쓰기 or 다른 파일로 옮기기.

alt + 위아래 방향키 : 선택한 것들 이동

alt + 여기저기 드래그 : 다중 선택

alt + 여기저기 클릭 : 여기저기 클릭한 곳들이 전부 커서가 됨.

**alt + z** : 우측 끝까지 넘어가게 설정 / 넘어가지 않게 설정

![alt text](images/vs_0_image-3.png)
![alt text](images/vs_0_image-4.png)


### VScode ctrl+enter 중복 문제
원래 ctrl + enter는 아래에 빈줄을 삽입하는 것이었다.

하지만 만약에 코파일럿을 동시에 사용중이면 코드를 생성하는 것으로 해당 단축키가 바뀌어있다.

ctrl + k ctrl + s로 단축키를 확인할 수 있다.

![alt text](images/vs_1_image.png)

충돌하는 기능은 Gemini Code Assist으로 해당 키를 변경해서 해결했다.

앞으로 Gemini Code Assist는 ctrl + alt + a로 바꾸기로 했다.

### VScode에서 분명히 있는데 특정 구문이나 단어가 잘 검색이 안된다면

아마 검색탭에서 보이는 `ab` 옵션이 활성화 돼서 그럴거다.

<img src="images/vs_search_image.png" width="400">

- 이 옵션이 켜져 있으면 전체 단어가 일치해야하만 검색이 된다.
  - 꺼두자.

> 참고로 그 옆에 있는 `Aa`는 대소문자 구분임.

> 그리고 `.*`은 정규표현식임 사용 옵션임. 예를 들어 `설.*요`를 검색하면 '설'로 시작하고 '요'로 끝나는 문장을 전부 찾음.


### Markdown Preview Enhanced 익스텐션

- 수식이라 그림이 실시간으로 렌더링됨. 변경점들도 거의 실시간으로 렌더링 됨.

- (중요) 현 md 파일과 시각화 페이지의 **스크롤 정렬** 알고리즘이 보다 정확해짐!

- 시각화 창을 따로 떼어냈을 때 원래 호환이 잘 안되고, 파일 바꾸면 반영안되고 그랬는데, 이제 안그럼.

- pdf나 html 출력 가능

### Image preview 익스텐션

- 이거는 별거 아니고 그냥 md 파일 좌측과 커서 올리면 이미지가 팝업되게 만든 만듬.
  - 생각보다 이미지가 안보일때 불편해서 추가함.

### (중요) Past Image 익스텐션

- 원래 md 파일로 노트 적을때 가장 불편한 것이 이미지 경로를 정리하는거였음.

- 이 익스텐션을 사용하면 이게 해결 됨.

- 우분투의 경우 일단 이거 설치 (익스텐션 사용에 필요):

```bash
sudo apt update
sudo apt install xclip
```

- 이 익스텐션을 사용하면 json 파일 설정에서 이미지들을 바로 어디로 보낼지, 내 마크다운에는 이게 어디로 표시될지 세팅할 수 있음.

- `>setting json`을 검색하면 여러 옵션이 나오는데

![](images/2026-03-18-21-25-33.png)

- 그 중에서 **Workspace**의 Json Setting을 고르면 된다.
  - 이 설정이 **현재 경로** 기준으로 `.vscode` 폴더와 `settings.json` 파일 만들어져, 이를 **지금 보고 있는** VScode창만의 설정이 되는 것.
  - 만약 Uset Settings를 고르면 VScode 프로그램에 **글로벌**에 통하는 설정임.

- 그러면 이제 Json 파일에서 이미지 저장 경로와 표시 경로를 지정해보자.

> 근데 이를 매번 편집하기 귀찮으니, 이번 노트를 끝으로 그냥 모든 이미지를 다 한 폴더에 넣어주자. 아 근데 생각해보니 md 파일에 표시되는 위치는 계속 바꿔야하나..? -> **아님!** **유동적**으로 바뀌게 할 수 있음!

아래 처럼 하면 된다.
```c++
{
    // 1. 실제 이미지가 저장될 경로 (예: 프로젝트 최상단 아래의 images 폴더)
    // "pasteImage.path": "${projectRoot}/images",
    "pasteImage.path": "${currentFileDir}/images", // 현재 파일 경로 기준, 나중에 images를 통합하면 지울 것.
    // 2. 마크다운에 찍힐 이미지 경로의 기준점
    // "pasteImage.basePath": "${projectRoot}/images",
    "pasteImage.basePath": "${currentFileDir}", // 현재 경로로, 나중에 주석처리할 것
    // 3. 윈도우 환경에서도 경로 슬래시(/)가 깨지지 않도록 강제 적용
    "pasteImage.forceUnixStyleSeparator": true,
    "cmake.sourceDirectory": "/home/theo_lab/RWL_Intern/to_workspace/dev_env_set/etc"
}
```

- 현재 위 세팅은 우리 폴더 구조인 현재 currentFileDir와 같은 선상에 있는 images 폴더에 집어넣게 만드는 것. 
  - 근데 사실 basePath의 경우 조금 이상하게 줘도 알아서 잘 찾아감. 지금도 알아서 images를 경로에 추가해서 인식함.
    - 그냥 단순 표기상의 깔끔함을 유지하기 위함임.

- 아 물론 일반 ctrl + v로 안됨.

`ctrl + alt + v` 로 이미지 복붙하는거임.