# 추가환경 생성

>conda info --envs : 가상환경 목록 확인

>conda create --name newenv python : 가상환경 새로 생성. python version은 최신으로 함.<br>
(만약 특정 버전을 생성하고 싶다면: conda create --name myenv python=3.8)>

>conda activate newenv : 가상환경 활성화

>conda deactivate : 가상환경 비활성화

> conda env remove -n newenv : 가상환경 제거

# 설치 라이브러리 목록

* conda intall jupyter notebook<br>
* conda install numpy pandas matplotlib seaborn scikit-learn<br>
* conda install scipy<br>
* conda install tensorflow(안됨)<br>
* conda install keras<br>
* conda install pytorch(안됨)<br>
* conda install -c conda-forge xgboost<br>
