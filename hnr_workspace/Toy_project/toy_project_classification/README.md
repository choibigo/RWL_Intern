### Conda (가상 환경): 
    파이썬 패키지(라이브러리)들의 충돌을 막기 위해 파이썬 버전을 포함한 패키지들을 독립적인 방(가상 환경)에 격리하는 도구이다. 
    "내 컴퓨터에서는 되는데 네 컴퓨터에서는 안 돼"라는 문제 중 '파이썬 패키지 버전' 문제를 해결해 준다.

### Docker (컨테이너): 
    파이썬뿐만 아니라 운영체제(OS) 환경 자체를 통째로 포장하는 도구이다. 우분투, CUDA(GPU 드라이버), 파이썬, 라이브러리를 모두 박스에 담아버리기 때문에, 윈도우든 맥이든 리눅스든 Docker만 깔려있으면 100% 똑같은 환경을 보장한다.


toy_project_classification/
├── configs/
│   └── config.py
├── data/
├── models/
│   └── resnet.py
├── outputs/
├── src/
│   ├── dataset.py
│   ├── engine.py
│   └── utils.py
└── train.py

### configs/: 
    하이퍼파라미터(Batch Size, Learning Rate 등)와 경로 설정 등 프로젝트 전체의 환경 변수를 모아두는 곳이다.

### data/: 
    CIFAR100과 같은 학습/평가 데이터셋이 다운로드되고 저장되는 공간

### models/: 
    ResNet, VGG 등 딥러닝 모델의 구조(Architecture) 코드를 정의하는 곳

### outputs/: 
    학습이 끝난 모델의 가중치(best_model.pth)나 텐서보드 로그 등 결과물이 저장되는 곳

### src/: 
    소스 코드의 핵심으로, 데이터 전처리(dataset.py), 학습/평가 루프(engine.py), 각종 편의 기능(utils.py)을 모아둔다.

### train.py: 
    이 모든 모듈을 조립하여 실제로 학습을 Run하는 메인 실행 파일

# Baseline Experiment
    - Model: ResNet18
    - Dataset: CIFAR-100
    - Epochs: 10
    - Batch size: 128
    - Optimizer: Adam
    - Learning rate: 1e-3
    - Train augmentation:
        - RandomCrop(32, padding=4)
        - RandomHorizontalFlip()
    - Best Valid Accuracy: 0.4635
