# Anaconda
###### Anaconda란 파이썬 인터프리터, 라이브러리, 패키지 관리자(conda) 등을 포함하는 Python 기반 개발자 도구입니다.
###### *conda는 프로젝트마다 독립적인 Python 환경을 만들고, 그 환경에 필요한 Python과 라이브러리를 설치,삭제,업데이트 해준다.
----


- 아나콘다를 쓰는 이유
    1. **환경 관리 용이: 서로 다른 프로젝트에서 다른 파이썬 버전, 라이브러리 버전을 사용할 수 있다.
    2. 데이터 과학에 최적화
    3. 간편한 설치와 유지보수


## Conda 명령어 모음집
    
1. conda 환경 관리


```bash
    conda create -n myenv #환경 생성
    conda create -n myenv python=3.10 #특정 파이썬 버전으로 생성
    conda env list #환경 목록 보기
    conda activate myenv #환경 활성화
    conda deactivate #환경 비활성화
    conda remove -n myenv --all #환경 삭제
    conda create --name myenv --clone oldenv #환경 복제
    conda list --export > requirements.txt #환경 내 패키지 목록 저장
    conda create --name myenv --file requirements.txt #환경 불러오기(복원)
```
    
2. 패키지 관리


```bash
    conda install numpy #패키지 설치
    conda install numpy=1.21 #특정 버전 설치
    conda install numpy pandas matplotlib #여러 패키지 설치
    conda remove numpy #패키지 제거
    conda update numpy #패키지 업데이트
    conda update conda #아나콘다 자체 업데이트
    conda list #설치된 패키지 목록 보기
```

3. 패키지 탐색

```bash
    conda search numpy #설치 가능한 버전 확인
```

4. 기타 유용한 명령어

```bash
    conda --version #conda 버전 확인
    conda env export > environment.yml #환경 정보를 YAML로 내보내기
    conda env create -f environment.yml #YAML로 환경 만들기
    conda env update -f environment.yml #환경 업데이트
```

![conda env list](images/conda_env_list.png)
- conda env list 확인
![conda install numpy](images/conda_install_numpy.png)
- conda conda install libarart 해보기

    