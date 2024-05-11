## Conda 명령어들
#### env (environment)
- 가상환경 리스트 확인 : conda env list
- 가상환경 삭제 : conda env remove -n (가상환경이름)
- env의 다른 명령어들 확인 : conda env --help

#### create
- 새로운 가상환경 생성 : conda create -n (가상환경이름) (라이브러리=버전)
- 가상환경 복제 : conda create --clone (복제할 가상환경) -n (새 가상환경)

#### 가상환경 활성화 비활성화
- 활성화 : conda activate (가상환경 이름)
- 비활성화 : conda deactivate

#### 더 많은 명령어들
- https://jwkim96.tistory.com/144


## json 에 관해서...
#### 읽기
- .json 은 거대한 dictionary 과 같다.
- .json 파일 읽어오기 예제 코드
===================================================================================================
import json
with open('파일주소/파일이름.json') as f:
    access_name = json.load(f)