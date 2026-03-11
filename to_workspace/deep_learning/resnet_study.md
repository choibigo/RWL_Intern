## 계획

- [ ] ResNet <- 이 사람들은 무엇을 해결하려고 했는가? gradient vanishing는 아님, degrading problem? (논문 참고할 것)
  - [x] 그리고 ResNet 논문 읽고 분석
  - [ ] 직접 구현할 것 (다 손으로 짜서)
  - [ ] 파이토치로 데이터로더, 즉 데이터셋을 직접 만들어봐야함.
    - [ ] init, get item, len을 사용할 것.


# ResNet

https://arxiv.org/pdf/1512.03385


![alt text](images/dl_resnet_image.png)

## 논문 분석

<details>

<summary>논문 자세히 보기</summary>

![alt text](images/dl_resnet_image-2.png)

![alt text](images/dl_resnet_image-3.png)

![alt text](images/dl_resnet_image-4.png)

![alt text](images/dl_resnet_image-5.png)

![alt text](images/dl_resnet_image-6.png)

![alt text](images/dl_resnet_image-7.png)

![alt text](images/dl_resnet_image-8.png)

![alt text](images/dl_resnet_image-9.png)

</details>

---

- 스킵연결에 대해서 배우면 Resnet를 만든 사람들이 그저 gradient vanishing 문제를 해결하려는 것으로 보일 수 있으나, **사실 아니다**.

- ResNet 논문을 읽으면 Vanishing 문제는 이미 초깃값 및 배치 정규화으로 어느 정도 해결 된것으로 보고 있으며.
    - 그들이 해결하려는 것은 모델이 깊어지고 커짐에 따라 오히려 성능이 이상하게 떨어지는 **degradation problem**을 해결하는 것이었다.

> Degradation 문제는 Bias Variance 문제와 **다르다**!! Bias Variance는 모델이 깊어짐에 따라 train에 대한 에러는 **내려**가지만, val에 대한 에러가 올라가는 문제고. **Degradation**은 모델이 깊어짐에 따라 train, val에 대한 **에러가 둘다 그냥 중가**하는거임!!

- 논리적으로 생각해보자, 어느 정도 성능이 나오는 얕은 모델에 레이어를 더 깊게 추가해본다. 이때, 더 추가된 레이어가 아무리 쓸모가 없어도, 그저 **항등 함수 역할**을 한다면, 아무리 못해도 얕은 모델 보다 깊은 모델이 **최소 같거나** 더 성능이 좋아야하지 않을까?
    - 하지만 실험적으로 봤을 때 그렇지 않았다.
    - 이 문제를 그들은 해결하려고 했다.
    - 바로 잔차 함수, **Residual Function**을 도입해서.

## Residual Function & Skip Connection

- 이론은 생각보다 매우 간단하다.

- 인풋이 x인 신경의 아웃풋을 H(x)라고 해보자. 신경망을 최대한 **함수 처럼 생각**하는 것이다.

- x가 들어갔다가, 변해서 H(x)가 돼서 나오는 것, 이는 당연하게 들린다.

- 하지만 더 쉽게 생각할 수 있다. 만약에, 이 함수가 x를 **단지 변동**하는 것이라고 생각할 때.. 그냥 단순히 x가 얼마나 변하고 이를 추가하는... 즉, **그 차이만 주는** 모델을 주면 어떨까?

- x -> H(x)가 아니라 x -> x + F(x) -> H(x)
    - 이 x에다가 그저 **F(x)**를 더하는 방식으로 x에 대한 변동을 주는 것이다!
    - 이 블록들이 **F(x)**를 학습하는 것이다!

![alt text](images/dl_resnet_image-1.png)

- 이론상으로 차이가 있다! 신경망 입장에서 **이 추측이 더 쉬운** 것이다!

    - 위에서 얕은 함수에 레이어를 추가했을 때 아무리 못해도 **항등함수**라도 되면 성능이 저하되지 않을텐데라는 말을 했다.
    - 하지만 한번 신경망에 들어가버리면 아웃풋이 어떻게 나올지 아무것도 모르는 모델 입장에서 그 **항등함수 조차 만들기 어렵다**.
    - 하지만 차이 F(x)라면? 극단적으로 생각했을 때 그냥 F(x)가 **0이 되버리면 그만**이다.
    - 그래고 최소 기준점이 있으니 모델이 학습하기가 더 쉬워지는 것!

- 이 F(x)를 **Residual Function**이라고 부르고.
    - 이 모델은 이를 적즉적으로 사용했기에 **Residual Network**, 즉 **ResNet**으로 불리는 것이다.

- 그리고 이 방법이 기존에 앞과 뒤를 연결하려고 했던 방법들 (맨앞과 뒤 Linear 모델들, gate을 지니고 앞과 뒤를 연결하는 highway network) 보다 가볍고, 학습하기 간편하다. 또한 기존 방법들은 100 레이어 이상에서 괜찮은 성적을 보여주지 못했다.

## ResNet 모델

- 아무튼 이 Residual Function을 적극적으로 사용한 이 모델을 탐구해보고 실습해보자.

- 일단 이 잔차 함수 적용을 위해 인풋과 아웃풋은 같아야한다.

- 기본적인 공식은 이렇게 생겼다:

$y = \mathcal{F}(x, \{W_i\}) + x$ 

- $x$: 블록의 첫 번째 입력값
- $W_i$: weight layer 행렬

- 근데 만약에 인풋과 아웃풋이 다르다? 그러면 인풋 x를 아웃풋에 맞춰 정사영 시켜야한다.

$y = \mathcal{F}(x, \{W_i\}) + W_sx$

- 이때 $W_s$ 는 정방행렬로, CNN 구조에서는 채널수를 맞춰주기 위해 1x1 합성곱 연산으로 구현된다.

> 참고로 잔차 함수에 포함되는 블록이 딱 하나면 사실 선형 레이어 형태가 되버려 거의 의미가 없고, 보통 2~3개 정도가 적당하다. 50층 이상의 깊은 모델은 연산의 효율을 위해서 3개로 묶어서 했다.

### CIFAR-10 적용

어떻게 학습했는지 파라미터까지 꽤 상세하게 논문에서 나타남.

- SGD
- weight decay 0.0001
- momentum 0.9
- 드롭아웃 미사용
- batch size 128 (GPU 2대 기준)
- lr 시작값 0.1
    - 32k와 48k 단계에서 각각 한번 1/10을 함.
- 45k/5k train/val
- 4픽셀 패딩
- 데이터 증강했음