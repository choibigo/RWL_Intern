# Weakly Supervised 3D Object Detection from Lidar Point Cloud

[www.ecva.net](https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123580511.pdf)

## Abstract

**문제**

- 고품질 3D 객체 탐지기(object detector)를 훈련시키기 위해서는 포인트 클라우드 데이터에 수동으로 라벨을 붙여야 함 → laborious 한 작업이다.

**제안하는 해결책 (WS3D):**

- weakly supervised 방식을 제안.
- 이 방식은 두 가지 종류의 최소한의 데이터만을 필요로 한다.
    1. weakly annotated scenes의 작은 집합: 전체 scene에 대한 일부 정보만 있음
    2. 정확하게 라벨이 붙은 객체 instances 몇 개: 소수의 객체에 대한 정밀한 3D 박스 정보가 있다.

**구체적인 방법 (2단계 아키텍처):**

- Stage-1 : weak supervision 하에 원통형(cylindrical) 객체 제안(proposal)을 생성하도록 학습한다.
    - 여기서 '약한 지도'란, 씬을 위에서 내려다보는 BEV 상에서 객체의 수평 중심(horizontal centers)만을 클릭하여 어노테이션(주석)한 것을 의미한다. 높이나 크기 정보는 없음
- Stage-2 : 1단계에서 생성된 원통형 proposal 받아, a few well-labeled instances 를 사용하여 이를 정제(refine)한다.
    - 이 단계에서 원통형 제안을 실제 3D 큐브(cuboid) 모양으로 만들고, 이것이 실제 객체일 확률(confidence scores)을 학습한다.

**주요 성과 및 결과:**

- 적은 데이터로 높은 성능 달성: 단 500개의 '약하게 어노테이션된 씬'과 534개의 '정확하게 라벨링된 차량 인스턴스'만을 사용
- 이는 기존의 최고 성능을 내는 fully supervised 모델들이 요구하는 데이터(3,712개 씬, 15,654개 인스턴스)보다 훨씬 적은 양.
- 이렇게 적은 데이터로도, 기존 최고 성능 모델들의 85% ~ 95%에 달하는 성능을 냈음

추가적인 이점 (어노테이션 도구):

- 훈련된 모델은 3D 객체 어노테이터(주석 도구)로도 활용될 수 있다.
- 두 가지 모드 지원
    1. 자동(Automatic) 모드: 모델이 스스로 라벨을 생성.
    2. 능동(Active, human-in-the-loop) 모드: 사람이 중간에 개입하여(예: 중심점 클릭) 모델을 돕는다.
- 이 모델이 생성한 라벨을 가지고 다른 3D 객체 탐지기를 훈련시켰을 때, (사람이 수동으로 라벨링한 데이터로 훈련했을 때의) 원래 성능의 94% 이상을 달성

결론:

- 이 연구의 접근 방식은 highly practical 하며, 훨씬 적은 어노테이션 비용으로 3D 객체 탐지 학습의 새로운 가능성을 열었다.

## Introduction

![image.png](image.png)

‘어노테이션 비용이 너무 비싸다’는 문제를 이 논문(WS3D)이 어떻게 해결할 것인가

여기서 저자들은 두 가지의 '완전하지 않은' 데이터를 사용하는 2단계(two-stage) 아키텍처를 제안

**문제 해결의 필요성**

- 3D 객체 탐지 시스템을 널리 보급(deployment)하려면, 이 무거운 어노테이션 부담을 줄이는 것이 필수적 → 하지만 이 방식은 주목을 받지 못하였음

**WS3D의 2단계(Two-Stage) 해결책**

약한 지도 학습(weakly supervised) 방식을 제안

이 모델은 두 개의 주요 단계로 구성된다.

1. Stage-1 : '약하지만(Weak)' '부정확한(Inexact)' 주석으로 원통형 제안 생성
    - 1단계 모델은 (x, z) 평면상의 객체 중심을 예측하고, 객체에 속하는 포인트(foreground points)를 식별하도록 학습
    - 이 단계의 훈련에는 ‘weakly annotated' BEV 맵의 작은 집합 (즉 500개의 scene)만 필요
    - (Fig. 1(b)) 에서 보듯이, 이 '약한 주석'이란 BEV 맵 상에 객체의 수평 중심(horizontal center)을 클릭(녹색 x 표시) 한 것을 의미한다
    - 이 주석은 부정확하고(inaccurate) 정밀하지 않지만(inexact), 어노테이션에 드는 노력을 줄여준다.
    - 결과: BEV 클릭에는 높이(y축) 정보가 없기 때문에, 1단계는 높이(y-axis)가 무제한인 원통형(cylindrical) proposal 을 생성한다.
2. Stage-2 : '몇 개의(Few)' '불완전한(Incomplete)' 주석으로 3D 박스 정제
    - 2단계 모델은 1단계에서 받은 원통형 제안을 가지고, 실제 3D 파라미터(크기, 방향 등)를 추정하고 신뢰도 점수(confidence)를 예측하도록 학습한다.
    - 이 단계는 '몇 개의 정밀하게 주석이 달린 객체 인스턴스(a few, precisely-annotated object instances)' (논문에서는 534개)를 incomplete supervision 으로 사용하여 학습한다.
    - (Fig. 1(c)) 에서 보듯이, '불완전한(incomplete)'의 의미는 씬(scene)에 있는 모든 객체에 라벨이 달린 것이 아니라, 단지 몇 개의 객체에만 정밀한 3D 박스 라벨이 있다는 뜻이다.
    

**기존 방식(Prior Arts)과의 비교**

- 이 방식은 기존의 연구들(예: PIXOR [5], VeloFCN [11])과 완전히 대조된다.
- 기존 연구들은 (Fig. 1(a)) 처럼, 방대하고(massive), 빠짐없이(exhaustively) 모든 객체에 정밀한 3D 박스가 라벨링된 씬(scene) 전체(3,712개 씬, 15,654개 인스턴스 )를 훈련 데이터로 사용하였다.

**첫 번째 특징: 매우 적은 양의 저렴한 데이터로 학습 가능**

- 이 모델은 (1) '약하게 라벨링된 BEV 데이터'의 작은 집합과 (2) '정밀하게 라벨링된 객체 인스턴스' 몇 개, 이 두 가지를 조합하여 학습을 진행한다.
- (1) 약한 라벨 (BEV 클릭)의 이점:
    - BEV 맵(버드아이 뷰)에서 객체의 수평 중심을 '클릭'하는 방식
    - 이는 3D 포인트 클라우드에서 정교한 3D 상자(cuboid)를 일일이 그리는 '강한 지도(strong supervision)' 방식보다 약 40~50배 더 빠르다.
- (2) 정밀한 라벨 (소수의 3D 박스)의 효율성:
    - '정밀한 라벨'이 필요하긴 하지만, 아주 조금만 필요하다.
    - 이 논문은 500개의 '약한' 씬(scene) 내에 있는 객체들 중 단 25%의 객체(총 534개)에 대해서만 정밀한 라벨을 사용
    - 이 수치(534개)는, 기존의 최고 성능 모델들이 사용하는 정밀 라벨(15,654개)의 단 3%에 불과한 양

→ 이 방식은 3D 탐지 분야의 가장 큰 문제인 '강한 지도(정밀한 라벨)'의 필요성을 획기적으로 줄여주며, 이는 즉각적인 상업적 이점(비용 절감)으로 이어진다.

**두 번째 특징: 훈련된 모델을 '어노테이션 도구'로 활용 가능**

- 이 모델은 한번 훈련되고 나면, 노동력이 많이 드는 '라벨링 과정'을 돕는 어노테이션 도구(annotation tool)로 거꾸로 사용될 수 있다.
- (기존의 다른 모델들은 데이터를 소모하기만 할 뿐, 데이터 생성을 돕는 데는 관심이 없었다.
- 이 모델(WS3D)은 두 가지 작동 모드를 지원한다.
    1. 자동 모드 (Automatic Mode)
    - 작동 방식: 사람이 전혀 개입하지 X(no annotator in the loop).
    - 훈련된 WS3D 모델을 사용하여 전체 KITTI 데이터셋을 자동으로 라벨링(re-annotate)한다.
    - 성능 검증: 이 '자동 생성된 라벨'을 가지고 다른 최신 모델(예: PointPillars [7], PointRCNN [13])을 훈련시켰다.
    - 결과: 이 모델들은 (사람이 만든 완벽한 라벨로 훈련했을 때의) 원래 성능의 94% 이상을 달성했다.
    
    1. 능동 모드 (Active Mode / Human-in-the-loop)
    - 작동 방식: 사람이 쉬운 일(중심 클릭)만 도와준다.
    - (1) 사람이 BEV 맵에서 객체 중심을 클릭한다.
    - (2) 모델(WS3D)은 이 클릭 정보를 특권 정보(privileged information)로 받아서, Stage-2(정제 단계)를 바로 실행하여 최종 3D 박스를 예측한다.
    - 성능 검증: 이 '사람이 클릭하고 기계가 완성한' 라벨을 가지고 PointPillars [7]와 PointRCNN [13]을 다시 훈련시켰다.
    - 결과: 이 모델들은 원래 성능의 96% 이상을 달성했다. (자동 모드보다 더 good)

## Data Annotation Strategy for Our Weak Supervision

![image.png](image%201.png)

### Traditional Precies But Laborious Labeling Strategy

전통적인 precise 한 3D 라벨링은 2D 라벨링보다 훨씬 복잡하며 , 높은 품질의 라벨을 얻기 위해 여러 단계를 거쳐야 하므로 매우 힘들고 비싸다.

이 단락에서 설명하는 정밀한 라벨링의 구체적인 단계는 다음과 같다.

1단계: 2D 뷰에서 객체 찾기

- 어노테이터(작업자)는 먼저 3D 씬(scene)을 탐색하면서, 카메라 이미지(Fig. 3(a))의 도움을 받으며 객체(자동차)를 찾는다.

2단계: 3D 뷰에서 대략적인 박스 그리기

- 그다음, 3D 포인트 클라우드 뷰로 전환하여, 대략적인(rough) 3D 상자(cuboid)와 방향을 나타내는 화살표를 배치한다. (Fig. 3(b))

3단계: 여러 뷰를 오가며 정밀하게 수정

- 마지막으로, 최적의(optimal) 라벨(Fig. 3(c)) 을 만든다.
- 이 작업은 3D 상자를 위에서 본 뷰(Top), 앞에서 본 뷰(Front), 옆에서 본 뷰(Side) 같은 직교 뷰(orthographic views) (Fig. 3(b)의 작은 상자들)에 투영된 2D 박스들을 점진적으로 수정해가며 완성한다.

결론:

- 이 라벨링 과정은 (1)여러 개의 하위 작업(subtasks)을 포함하고, (2)지속적인 수정(gradual corrections)이 필요하며, (3)2D 뷰와 3D 뷰를 계속 전환해야 한다.
- 따라서 이 방식은 품질은 높을지 몰라도 매우 힘들고 비쌀 수밖에 없다.

### Our Weak But Fast Annotation Scheme

이 단락에서 설명하는 "약한 어노테이션" 작업의 구체적인 단계는 다음과 같다. (Fig. 3 (d-f))

1단계: 카메라 뷰에서 대략적인 클릭

- 어노테이터(작업자)는 3D 뷰를 전혀 보지 X
- 대신, 카메라 정면 이미지(Fig. 3 (d))를 보고 "저기쯤 차가 있네"라고 생각되는 부분을 *대충 클릭(roughly click)한다.

2단계: BEV 맵에서 정확한 클릭

- (1단계)에서 클릭한 위치를 기준으로, 시스템이 자동으로 BEV 맵을 zoom in 해서 Fig. 3 (e)처럼 보여준다.
- 어노테이터는 이제 이 확대된 2D BEV 맵을 보고, 객체의 수평 중심(horizontal center)을 조금 더 정확하게(accurate) 다시 클릭

이 방식의 장점 (매우 빠름)

- 이 어노테이션 과정은 (앞선 '정밀한' 방식과 달리) 어떤 3D 뷰도 참조하지 X
- 오직 2D 이미지(카메라 뷰, BEV 맵)만 사용
- 대부분의 객체 라벨링이 two clicks 으로 끝난다.

이 방식의 단점 (그래서 "Weak"임)

- 하지만 이렇게 수집된 지도(supervision)는 weak 히
- 왜냐하면 이 '두 번의 클릭'은 오직 수평(x, z) 중심 위치 정보만 제공하기 때문
- 객체의 높이(y-axis) 정보가 완전히 빠져있고,객체의 크기(size)나 방향(orientation) 정보도 전혀 없음

## Proposed Algorithm

![image.png](image%202.png)

Stage-1 : 원통형 3D 제안 생성 (Cylindrical 3D Proposal Generation)

- 역할: proposal
- 학습 데이터: 이 단계는 'click supervision' 만을 사용하여 학습. (즉, 500개 씬의 '약한' BEV 중심점 클릭 데이터)
- 결과물: `Fig. 5 (a)`와 `Fig. 5 (b)` 에서 보듯이, 높이(y) 정보가 없는 weakly click 으로 학습했기 때문에, 높이가 무제한인 원통형(cylindrical) 모양의 proposal 을 생성
- `Fig. 5` 캡션의 추가 설명: `Fig. 5(b)`에서 노란색일수록 모델이 객체(foreground)일 확률이 높다.

Stage-2 : 제안 기반 3D 객체 위치 특정 (Proposal-based 3D Object Localization)

- 역할: 1단계에서 생성한 원통형 제안(`Fig. 5(b)`)을 입력으로 받아서, 정확한 3D 상자(`Fig. 5(c),(d)`)로 정제(refine)하고 위치를 특정하는 단계
- 학습 데이터: 이 단계는 '몇 개의 잘 어노테이션된 객체 인스턴스(a few, well-annotated object instances)' 를 사용하여 학습한다. (534개의 정밀한 3D 상자 라벨 데이터)
- 결과물: `Fig. 5 (e)` 방향과 크기가 정밀하게 조정된 최종 3D 박스(cuboid)

## 4.1 Learn to Generate Cylindrical Proposals from Click Annotations

**Stage-1의 두 가지 목표**

이 단계는 click annotations 라는 약한 단서만으로 두 가지 임무를 수행해야 한다.

1. **전경 포인트 분할 (Foreground Point Segmentation):** 씬(scene)의 수만 개 포인트 중에서 어떤 것이 자동차(전경)이고 어떤 것이 바닥(배경)인지 구분해내는 것.

2. **원통형 제안 생성 (Cylindrical Proposals):** 전경 포인트를 바탕으로 원통형 영역을 제안하는 것. (클릭에 높이 정보가 없으니 원통으로 제안한다)

**Pseudo Groundtruth Generation**

모델을 학습시킬 '정답(라벨)'이 없으니, '약한' BEV 클릭 정보를 '강한' 가짜 정답 정보로 바꾸는 작업이 필요하다.

**Step 1: '클릭'에 가상의 3D 좌표 부여하기**

- 어노테이터가 BEV 맵에 클릭한 수평 위치 $(x_o, z_o)$를 가져온다.
- 문제는 높이($y_o$)이다. 어노테이터는 높이를 클릭한 적이 없다.
- 여기서 저자들은 독특한 가정을 한다. 클릭의 높이($y_o$)를 '0'으로 설정한다. 이 '0'은 바닥이 아니라 LiDAR 센서 자체의 높이(자율주행차 지붕 높이)를 의미한다.
- 이제 모든 클릭마다 가상의 3D 중심점 $o = (x_o, 0, z_o)$를 갖게 되었다.

**Step 2: 모든 포인트에 '가상 전경 점수' 매기기**

- 이제 scene에 있는 모든 개별 포인트 $p$ 에 대해 이 포인트 $p$가 자동차(전경)일 확률을 계산한다. 이 가상의 점수가 바로 $f^p$이다.
- 이 점수 $f^p$는 다음과 같은 규칙(수식 $\iota(p, o)$)을 따른다.

![image.png](image%203.png)

- 수식 $\iota(p, o)$의 의미
    
    포인트 $p$와 가상 중심점 $o$ 사이의 '특수 거리' $d(p, o)$를 계산했을 때
    
    1. 만약 그 거리가 0.7m 이내로 매우 가깝다면: 이 포인트 $p$는 100% 자동차의 일부다. → 점수 $f^p = 1$.
    2. 만약 그 거리가 0.7m보다 멀다면: "자동차의 일부일 수도 있지만... 거리가 멀어질수록 확신이 줄어든다." → 가우시안 분포(종 모양 곡선 $\mathcal{N}$)를 따라 점수를 깎는다. (예: 0.9점, 0.7점, 0.3점...)

**Step 3: '특수 거리'** $d(p, o)$

- 이 '특수 거리' $d(p, o)$는 일반적인 3D 거리가 아니다. 수식은 다음과 같다.

$d(p, o) = \sqrt{(x_p - x_o)^2 + \mathbf{\frac{1}{2}}(y_p - y_o)^2 + (z_p - z_o)^2}$

- 가장 중요한 것은 높이(y축) 차이에 붙은 $\frac{1}{2}$ 계수이다.
- 이유: $y_o=0$이라는 값은 '임의로 정한' 가짜 높이이다. 즉, y축은 불확실성이 매우 큽다. 따라서 $y$축 방향의 거리 차이는 $x, z$축보다 절반만 반영하여(패널티를 줄여), 높이가 다른 포인트들도 "가깝다"고 판단할 수 있게 해준다.

**왜 가상 중심 높이 $y_o$를 '0'(센서 높이)로 설정했는가?**

- LiDAR 센서는 차 지붕에 달려있다. (높이 $y=0$)
- 탐지하려는 자동차의 대부분의 포인트(보닛, 트렁크, 바퀴 등)는 센서보다 아래에 있다. (예: $y = -1.0m$, $y = -1.5m$)
- 만약 가상 중심 $o$를 바닥에($y=-1.7m$ 정도) 뒀다면, 자동차 지붕 포인트는 가깝지만 바퀴는 멀어지는 등의 혼란이 생길 수 있다.
- 하지만 가상 중심 $o$를 센서 높이($y_o=0$)에 두면, 자동차를 구성하는 대부분의 포인트들이 이 가상 중심점보다 아래쪽에 일관되게 분포하게 된다.
- 바로 앞 단락에서 설명한 '특수 거리 공식' $d(p,o)$는, 포인트들이 이렇게 ($x_o, z_o$) 주변, 그리고 $y_o$보다 '아래쪽'에 모여 있을 때 '가깝다'고 판단(즉, '가상 전경 점수 $f^p$를 높게 주도록) 설계되었다.
- 센서와 높이가 같은( $y \approx 0$) 나뭇가지 같은 배경 포인트들은 어떻게 처리? → 그러한 포인트는 드물고(sparse), 어차피 $(x, z)$ 평면상에서 멀리 떨어져 있기 때문에 낮은 점수를 받아 무시된다

### Point Cloud Representations

- **Backbone Network**
    - 이 모델은 LiDAR가 수집한 원본(raw) 포인트 클라우드 (수만 개의 x, y, z 좌표)를 3D 격자(voxel)로 바꾸지 않고, 직접(directly) 입력으로 받는다.
    - 이 원본 포인트를 처리하기 위한 backbone 네트워크로, Set-Abstraction(SA) 레이어와 Multi-Scale Grouping(MSG)이라는 기술을 사용
    - Backbone → PointNet++
    - PointNet++를 통과시키면, 원본의 '위치' 정보만 있던 각 포인트가, 주변의 context을 이해하는 포인트별 특징(point-wise features)을 갖게 된다.
- **Two Branches**
    - Backbone 네트워크가 모든 포인트의 point-wise features 을 계산 → 이 특징들을 두 개의 서로 다른 '가지(branch)'로 동시에 보낸다.
    - 이 '두 개의 가지'는 1단계(Stage-1)의 두 가지 목표를 수행
        - branch 1: foreground Point Segmentation Branch
            
            이 가지는 point-wise features를 받아서, 모든 포인트에 대해 "이 포인트가 전경(자동차)일 확률은 몇 %인가?"를 예측한다.
            
            → $f^p$ 를 맞추도록 학습하는 부분
            
        - branch 2: (x, z) 중심 예측 (Vehicle (x, z)-center Prediction Branch):
            
            포인트를 종합하여 scene에 있는 객체(자동차)의 수평(x, z) 중심은 어디인지를 예측한다.
            
            → 어노테이터가 클릭한 'BEV 중심 클릭($x_o, z_o$) 을 맞추도록 학습하는 부분
            

### Foreground Point Segmentation

핵심은 모델의 예측($\tilde{f}^p$)과 가상 점수 ($f^p$)을 비교하기 위한 loss function

**1. 학습에 필요한 두 가지 재료**

이 foreground point segmentation branch를 학습시키기 위해 포인트 p마다 두 가지 값을 가지고 있음

1. Pseudo GT ($f^p$):
    - `Eq. 1` 에서 (클릭을 기준으로) 생성한 pseudo GT
    - 이 값은 0(배경) 또는 1(전경)이 아니라, [0, 1] 사이의 확률 값
2. 모델의 예측 값 ($\tilde{f}^p$):
    - Backbone 네트워크가 추출한 point wise feature을 foreground point segmentation branch에 넣었을 때 , 모델이 스스로 예측한 '전경일 확률'이다.
    

**2. 손실 함수 (Loss Function):** $\mathcal{L}_{seg}$

pseudo GT ($f^p$)과 모델 예측($\tilde{f}^p$)을 비교해서, 모델이 얼마나 틀렸는지(Loss) 계산해야 한다. 

→ Focal Loss 를 변형해서 사용

A.  $f^p$의 의미

- 단순히 $f^p - \tilde{f}^p$ (0.8 - 0.9)로 계산하지 않고, $\hat{f}^p$라는 중간 값을 만든다.
- $\hat{f}^p = \tilde{f}^p \cdot f^p + (1 - \tilde{f}^p) \cdot (1 - f^p)$
- 의미: 이 수식은 모델의 예측과 pseudo GT가 서로 일치할 확률을 계산하는 soft한  방식
    - $\tilde{f}^p \cdot f^p$ : 모델이 '전경'이라고 예측할 확률 $\tilde{f}^p$ 곱하기 정답이 '전경'일 확률 $f^p$ → 즉 둘다 전경이라고 동의할 확률
    - $(1 - \tilde{f}^p) \cdot (1 - f^p)$: 둘 다 배경(Background)이라고 동의할 확률
    - 결과적으로 $\hat{f}^p$는 모델의 예측과 정답 라벨이 일치할 총 확률을 나타내는 score 로 볼 수 있다.

B. $\mathcal{L}_{seg}$의 의미

- Focal Loss (원본 수식 ): $\mathcal{L}_{seg} = \alpha(1 - \hat{f}^p)^\gamma \log(\hat{f}^p)$
- Focal Loss [39]를 쓰는 이유: 3D 포인트 클라우드 씬에는 클래스 불균형 문제가 심각하기 때문
    - scene의 포인트 중 99%는 '맞추기 쉬운' 배경(예: 바닥)이고, 1%만 '맞추기 어려운' 전경(예: 자동차)이다.
    - 일반적인 손실 함수를 쓰면, 모델은 '바닥'만 99% 맞추고도 잘 학습했다고 착각하게 된다.
- 작동 방식: 논문에서는 γ=2, α= 0.25로 설정
    - '맞추기 쉬운' 포인트 ( $f^p$가 1에 가까움, 예: 0.9) → Loss 값이 많이 줄어든다.
    - '맞추기 어려운' 포인트 ( $f^p$가 0에 가까움, 예: 0.1) → Loss 값이 거의 줄어들지 않는다 → 계속 학습 진행

### Object $(x, z)$ Center Prediction

scene 에 있는 객체의 수평 중심 ($x, z$)이 어디인가? 를 맞춰야함
이 학습은 pseudo GT를 사용했던 '전경 분할' 과 달리, 어노테이터가 클릭한 '진짜 정답'(BEV 클릭 $o$) 을 사용한다.

하지만 좌표 $(x_o, z_o)$를 직접 예측(regression)하는 것은 매우 어렵고 불안정한 문제이다.

→ 저자들은 참고 문헌 [13] (PointRCNN) 에서 사용한 Bin-based 방식을 채택한다.

이 전략은 어려운 회귀(regression) 문제를 두 개의 쉬운 단계(분류 + 회귀)로 나누어 푼다.

1. 누가 학습하는가? : Support Points
- 모델은 정답 중심 ($o$) 4m 반경 안에 있으면서, 전경 확률이 0.1 이상인 '쓸모있는' 포인트들($p$)을 '서포트 포인트'로 지정한다.
- 이제 이 서포트 포인트 $p$가 정답 중심 ($o$)의 위치를 맞추도록 학습
1. 어떻게 맞추는가?: Bin-based 2단계 전략

Step 1: Coarse Classification 

- 목표: '서포트 포인트 $p$를 기준으로, '정답 중심 $o$'가 어느 바구니(bin)에 속하는지 먼저 맞춘다.
- 방법:
    - '서포트 포인트 $p$' 주변에 $L \times L$ (8m x 8m) 크기의 searching space 설정.
    - 이 공간을 $\delta$ (0.8m) 크기의 '바구니(bin)' 10개로 나눈다.
- 수식 (3): 정답 바구니
    - $b_x = \lfloor \frac{x_p - x_o + L}{\delta} \rfloor$, $b_z = \lfloor \frac{z_p - z_o + L}{\delta} \rfloor$
    - 이 수식은 '정답 중심 $o$'가 '서포트 포인트 $p$' 기준으로 몇 번째 '바구니' $b_x$에 속하는지 계산 (모델은 이 $b_x$ 값을 맞추도록 학습한다.)

Step 2: Fine-tuning Regression

- 목표: 바구니 안에서 정확히 어디인지를 맞춘다.
- 방법:
    - ex) 모델은 ‘7번 바구니의 정중앙에서, x축으로 +0.1m, z축으로 -0.05m 더 가야 함’ 이라는 residual 을 회귀(Regression) 문제로 푼다.
- 수식 (4): "정답 잔여값"
    - $r_{u \in \{x,z\}} = \frac{u}{\epsilon} (u_p - u_o + L - (b_u \cdot \delta + \frac{\delta}{2}))$,
    - 이 수식은 정답 $u_o$가 "모델이 예측한 바구니($b_u$)의 중심"에서 얼마나 떨어져 있는지 계산하는 '정답 잔여값' $r_u$ 이다. (모델은 이 $r_u$ 값을 맞추도록 학습한다.)
        - $(b_u \cdot \delta + \frac{\delta}{2})$ → 바구니의 정중앙
            - $b_u$ : 정답 바구니의 번호(index)
            - $\delta$: 바구니 하나의 크기 (0.8m) .
            - $b_u \cdot \delta$: 7번 바구니의 시작 위치 (7 * 0.8m = 5.6m).
            - $\frac{\delta}{2}$ : 바구니 크기의 *절반* (0.4m)
        - ($u_p - u_o + L$) → 정답의 상대적 위치
            - $(u_p - u_o + L)$ 부분 → 수식 (3)
        
1. 최종 손실 함수 (Loss Function)
    - 수식 (5): $\mathcal{L}_{bin} = \sum_{u \in \{x,z\}} (\mathcal{L}_{cls}(\tilde{b}_u, b_u) + \mathcal{L}_{reg}(\tilde{r}_u, r_u))$
    - 의미: 이 가지의 총 손실(Loss)은,
        
        [Step 1]의 loss: '바구니'에 대한 분류 손실($\mathcal{L}_{cls}$)
        
        [Step 2]의 loss: '잔여값'을 잘못 예측한 것에 대한 회귀 손실($\mathcal{L}_{reg}$)
        

### Cylindrical 3D Proposal Generation

1단계 모델이 후보 객체 Proposal 를 생성하는 단계

[Step 1: 불필요한 포인트 제거]

- (학습이 끝난) 전경 segmentation branch 를 실행시켜, scene의 모든 포인트에 대해 전경(자동차)일 확률($\tilde{f}^p$)을 예측한다.
- 이 확률(foreground score)이 0.1보다 낮은 포인트(즉, 바닥이나 벽일 확률이 90% 이상인)는 모두 버린다. → 이로써 '서포트 포인트' 후보군만 남게된다

[Step 2: 원통형 proposal]

- (학습이 끝난) center prediction branch 를 실행시켜, Step 1에서 살아남은 '서포트 포인트'들로부터 수많은 (x, z) 중심점들을 예측한다.
- (x, z) 수평 중심만 예측했을 뿐, 높이(y)나 크기는 모른다. → 따라서 3D 상자(cuboid)를 바로 만들 수 없다.
- 대신, 예측된 각 (x, z) 중심마다 cylindrical proposal 을 생성한다.
- 이 원통은 (x, z) 평면상으로는 반지름 4m를 갖고, y축(높이)으로는 범위가 unlimited

### Center-Aware Non-Maximum Suppression.

중복된 후보군의 제거

- Step 2를 거치면, 자동차 1대를 놓고도 수십 개의 '서포트 포인트'가 각자 중심을 예측하기 때문에 redundant 한 cylindrical proposal 들이 겹쳐있게 된다.
- 이 중복을 제거하기 위해, 저자들은 CA-NMS라는 새로운 전략을 제안한다.
    - (NMS: 겹친 것 중 최고점수 1개만 남기고 지우는 기술)
- CA-NMS의 아이디어
    - 가설 1: 중심에 가까운(center-close) '서포트 포인트'일수록 예측을 더 정확하게 할 것이다.
    - 가설 2: 1단계 foreground seg 학습시킬 때, 중심에 가까운 포인트에게 높은 GT ($f^p$) 를 주도록 설계하였다.
    - 따라서, 어떤 포인트의 전경 확률($\tilde{f}^p$)(from 분할 가지)이 높다는 것은, 그 포인트가 '진짜 중심'에 가깝다는 뜻이며, 그 포인트가 예측한 '중심점' 역시 신뢰할 수 있다
- CA-NMS의 작동 방식:
    1. 신뢰도 점수 부여: 각 원통형 proposal (중심점)의 confidence score 로, (중심점 예측에 사용된 '서포트 포인트' $p$의) '전경 확률($\tilde{f}^p$)' 값을 그대로 사용한다. (이것이 Center-Aware의 의미이다.)
    2. 순위 매기기: 모든 '원통형 제안'을 이 신뢰도 점수(전경 확률) 순서대로 내림차순 정렬한다.
    3. 중복 제거 (NMS): 1등부터 차례대로 확인한다.
        1. (x, z) 평면상에서, 이미 선택된(pre-selected) 제안들의 중심과 4m 이내에 겹치면, 이 제안은 중복이므로 제거한다.
        2. 겹치지 않으면(4m보다 멀면), 이 제안을 최종 후보로 보존한다.

## 4.2 Learn to Refine Proposals from A Few Well-Labeled Instances

![image.png](image%204.png)

1. **2단계(Stage-2)의 목표와 학습 데이터**
- 2단계의 임무 (두 가지):
    1. "Estimate Cuboids" (큐브 추정): 1단계가 넘겨준, 높이가 무제한인 '원통형 후보' 를 입력으로 받아, 정밀한 3D 박스(cuboid)로 변환한다.
    2. "Recognize False Estimates" (잘못된 예측 식별): 1단계가 실수로 '나무'나 '바닥'을 '원통형 후보'로 제안했을 수도 있다. 2단계는 이것이 "자동차가 아님"을 인식하고 낮은 신뢰도(confidence) 점수를 부여하는 필터 역할도 한다.
- 2단계의 학습 데이터:
    - 1단계와 달리, 2단계는 소수의, 정밀하게 라벨링된 객체 인스턴스 (a few well-annotated instances) 를 사용하여 학습한다. (논문 초록에 따르면 534개의 정밀 라벨 ).
1. **왜 이 방식을 사용하는가?** 
    1. 2단계의 임무는 proposal을 instance 단위로 정제하는 것이다. 따라서 학습 데이터도 '인스턴스' 단위의 정밀한 라벨(instance-wise annotations)을 사용하는 것이 타당할 것이다.
    2. 데이터 효율성
        - 1단계가 만든 '원통형 후보' 는 비록 rough 하지만, 그 안에는 이미 rich useful information이 있다. (예: 객체의 대략적인 (x, z) 위치, 객체에 속하는 포인트들).
        - 2단계는 맨땅(from scratch)에서 시작하는 것이 아니라, 이 '유용한 정보'가 담긴 '원통'을 입력으로 받는다.
        
        → 훈련 데이터가 매우 적어도(limited) 3D 박스를 예측하는 방법을 빠르게 배울 수 있다.
        
2. **2단계(Stage-2)의 상세 파이프라인 (2-Step Refinement)**

`Fig. 5 (b) -> (c) -> (d)` 의 흐름과 일치

- [Stage-2, Step 1] 초기 큐브 생성 (Initial Cuboid Generation)
    - 입력: 1단계가 만든 원통형 proposal (`Fig. 5 (b)`) .
    - 출력: 1차로 예측한 '초기 큐브' (`Fig. 5 (c)`) .
- [Stage-2, Step 2] 최종 큐브 정제 (Final Cuboid Refinement)
    - 입력: [Stage-2, Step 1]에서 만든 '초기 큐브' (`Fig. 5 (c)`) .
    - 출력: 최종적으로 정제된 '최종 큐브' (`Fig. 5 (d)`) 및 신뢰도 점수(confidence)

### Initial Cuboid Generation

Fig. 5 (b) $\rightarrow$ (c)

- 네트워크 아키텍처:
    - 입력으로 받은 원통형 후보 내부의 포인트들을 처리하기 위해, 1단계(Stage-1)에서처럼 PointNet++ [24] 아키텍처 사용
    - 단, 1단계와 달리 'Single-Scale Grouping'이라는 더 단순한 버전 사용
    - Backbone 네트워크를 통과시킨 후, MLP 가지를 붙여 3D 박스 파라미터 예측

- 학습 목표 (Loss Function):
    - 이 네트워크는 정답 3D 박스의 7가지 파라미터 `(x, y, z, h, w, l, θ)` 5를 모두 맞추도록 학습
    - 이 7개를 한 번에 맞추지 않고, 두 가지 다른 손실(Loss) 함수를 조합한다:
        - $\mathcal{L}_{ref} = \mathcal{L}_{bin}(\tilde{\theta}, \theta) + \sum_{u \in \{x,y,z,h,w,l\}} \mathcal{L}_{reg}(\tilde{u}, u)$ …….(6)
    
    1. 방향($\theta$) 예측 ( $\mathcal{L}_{bin}$ ):
    
    - 방향($\theta$)은 360도 회전 값이라 예측하기 까다롭다.
    - 그래서 1단계(Stage-1)의 중심 예측에서 썼던 "Bin-based 방식을 또 사용(즉, 방향이 1번 바구니(0~30도)라고 classification 하고, 거기서 +5도 더 가야 함이라고 잔여값(residual)을 회귀한다.)
    
    2. 나머지 6개 예측 ( $\mathcal{L}_{reg}$ ):
    
    - 중심점$(x, y, z)$과 크기$(h, w, l)$는 Smooth $\ell_1$ Loss 라는 표준적인 Regression 손실을 사용하여 직접 맞춘다.

### Final Cuboid Refinement

Fig. 5 (c) → (d). "더 정밀한 3D 박스 + 신뢰도 점수"

- 네트워크 아키텍처:
    - 첫 번째 세부 단계("Initial Cuboid Generation")와 거의 동일한 네트워크 구조

- 학습 목표 (Loss Functions):
    - 이 네트워크는 두개의 head 로 이루어진다.
    1. 박스 정제 ($\mathcal{L}_{ref}$, 수식 (6) 재사용):
        - 입력으로 받은 초기 큐브를 최종 큐브로 한 번 더 refine
        - 학습 방식은 Initial Cuboid Generation 과 동일한 손실 함수를 사용한다.
            
            $\mathcal{L}_{ref} = \mathcal{L}_{bin}(\tilde{\theta}, \theta) + \sum_{u \in \{x,y,z,h,w,l\}} \mathcal{L}_{reg}(\tilde{u}, u)$
            
    2. 신뢰도 예측 ($\mathcal{L}_{con}$ 수식 (7))
        - 이 '최종 큐브'가 얼마나 정답과 똑같은지 신뢰도 점수($\tilde{C}_{IoU}$)를 스스로 예측하는 Head 추가
        - 손실 함수: $\mathcal{L}_{con} = \mathcal{L}_{reg}(\tilde{C}_{IoU}, C_{IoU})$………(7)
            - 정답 신뢰도 점수($C_{IoU}$)는, 모델이 예측한 '최종 큐브'와 Groundtruth 박스' 사이의 실제 3D IoU 점수를 사용
            - 모델 → 예측한 박스가 정답과 90%(IoU 0.9) 겹치는 경우 → 0.9

### Training Data Selection

어떻게 소수의 정밀한 라벨(534개)을 이 두 네트워크의 학습에 사용하는가?

[Network 1 (Initial Cuboid Gen) 학습시키기]

1. '정밀한 정답(Groundtruth) 3D 박스' (534개 중 하나)를 가져온다.
2. 1단계(Stage-1)가 생성한 원통형 후보($C_{yl}$)들 중에서, 이 정답 박스의 중심과 (x, z 평면에서) 1.4m 이내에 있는 가까운 후보들을 모두 훈련 샘플로 선택
3. 네트워크 1은 이 가까운 원통($C_{yl}$)을 입력으로 받아, 정답 박스($Box_{GT}$)를 맞추도록 학습

[Network 2 (Final Cuboid Refine) 학습시키기]

1. 위에서 방금 학습시킨 Network 1에게 가까운 원통($C_{yl}$)을 입력으로 준다.
2. Network 1은 초기 큐브($Box_{Initial}$)를 예측한다.
3. 이 $Box_{Initial}$를 Network 2의 '훈련 샘플'로 사용한다.
4. Network 2는 이 $Box_{Initial}$를 입력으로 받아, 정답 박스($Box_{GT}$)를 맞추도록 (수식 (6) + 수식 (7)으로) 학습한다.