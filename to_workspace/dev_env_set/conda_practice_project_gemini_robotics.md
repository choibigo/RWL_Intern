### 계획
- [x] Conda 실습 프로젝트 구상
- [x] MuJoCo 코드 작성
    - [x] IK 문제 해결
- [x] Gemini VLM API 받오기
- [ ] Agentic system 구현

---

### Anaconda 실습 프로젝트

# Gemini Robot

### 가상 환경 생성

conda create -n gemini_robot python=3.10 

conda activate gemini_robot

mkdir ~/gemini_robot
cd ~/gemini_robot

### 패키지 설치

conda install -c conda-forge numpy opencv jupyter -y

pip install google-genai mujoco

... 아나콘다 공부할 때 가급적 pip을 이용한 설치를 지양하라고 했지만, 현실은 차갑다고한다.

요즘은 ai 분야 소프트웨어 업데이트가 워낙에 빨리 일어나서 conda 패키지들이 pip의 업데이트를 따라가지 못한다. 물론 뼈대 패키지들은 conda로 하는게 좋지만, 발 빠르게 업데이트가 필요한 패키지들은 pip를 정신건강에 좋다고한다.

### API 키 생성

구글ai스튜디오에서 API 키를 공수해온다.

![alt text](image.png)

예제를 보면 가장 최신 모델이 3 flash preview라고 한다.
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
)

print(response.text)
```

API 호출 테스트 중.

가끔 이렇게 503에러가 뜨는데, 이는 아마 서비스를 이용하는 이용자가 너무 많아서 그러는 듯?

```bash
503 UNAVAILABLE. {'error': {'code': 503, 'message': 'The model is overloaded. Please try again later.', 'status': 'UNAVAILABLE'}}
```

## 무조코에서 이미지 촬영 후 전송

인풋 쿼리:
```python
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=["이 화면에 무엇이 보이니? 로봇 공학 관점에서 설명해줘.", img]
)
```

![alt text](image-2.png)

Gemini에게 성공적으로 사진 전송 완료!

```bash
(gemini_robot) theo@theo-OMEN:~/gemini_robot$ python main_simulation.py 
🦾 시뮬레이션 시작... (Space: 캡처 및 Gemini 질문, ESC: 종료)

📸 [찰칵] 화면 캡처 중...
📤 Gemini에게 이미지 전송 중...
🧠 [Gemini 분석]:
로봇 공학(Robotics)의 관점에서 이 화면을 분석하면, 이는 로봇이 환경을 인식하고 상호작용하기 위한 **'가상 환경의 기초적인 객체 인식 및 조작 시나리오'**로 볼 수 있습니다. 구체적인 단계별 분석은 다음과 같습니다.

### 1. 컴퓨터 비전 및 인지 (Computer Vision & Perception)
*   **객체 탐지 (Object Detection):** 로봇의 카메라 센서(RGB)를 
```

conda install pink

설치는 잘 됐지만 계속 충돌이나서 일단 MuJoCo 내장 IK 함수 이용.

![alt text](image-1.png)


로봇 초기 위치가 위로 고정되있다.

![alt text](image-3.png)

아마 나중에 IK 푸는 과정에서 오류가날 수 있으니 잡기 포지션으로 먼저 수동으로 보내야할 것이다. 

잡기 포즈 키프레임은 일단 이거다:

```xml
<keyframe>
    <key name="home" qpos="0 0 0 -1.57079 0 1.57079 -0.7853 0.04 0.04" ctrl="0 0 0 -1.57079 0 1.57079 -0.7853 255"/>
</keyframe>
```

![alt text](image-4.png)

기억하고 있겠지만 자유 물체 배치시 키프레임에 파라미터들을 다 집어넣어야하니 가급적 쓰지말자.

몇번만 호출했는데 토큰이 다 떨어졌다고한다. 일단 유료버전으로 바꾸고, 무료 제공 크래딧을 사용해보자.

![alt text](image-5.png)

지금보니 로봇 IK 계산이 팔 끝단 기준으로 되고 있었음.

![alt text](image-6.png)

- 아이디어

제미니나이 아웃풋 출력을 하나의 좌표만 하는게 아님.

아래 처럼 이동 목표 좌표뿐만 아니라 해당 동작 설명을 추가.
그리고 이걸 몇개씩 출력.

```
{이동 좌표 or 그리퍼 닫기/열기, "이 행동을 하는 이유 설명"}
{좌표 or 그리퍼 닫기/열기, "이 행동을 하는 이유 설명"}
```

제미나이 인풋으로 이전 동자, 즉 지금 수행하고 있는 동작들을 다시 인풋으로 줌.

- 참고로 지금 방식의 API 호출은 이전 메모리가 없음. 채팅이 아니라 단발성 대화인 것.

채팅 방식을 사용하려면 아래 처럼 하면 됨.

```python
# 1. 채팅방 개설 (기억 시작)
chat = client.chats.create(model=MODEL_NAME)

# 2. 첫 번째 대화
response1 = chat.send_message(["이 화면 봐봐", image1])

# 3. 두 번째 대화 (Gemini가 image1을 기억함)
response2 = chat.send_message("아까 본 그 물체, 오른쪽으로 좀 더 갔어?")
```


- 옛날 강화학습하던 생각을 떠올려서 panda 그리퍼 끝단에 site를 추가하여 시각화하고

![alt text](image-8.png)

- 이를 기반으로 IK solve하게 만듬.

![alt text](image-7.png)

이런 표시가 Gemini한테도 도움이될듯?

- 근데 현재 방향을 고려하지 않고 있음. IK Solver에 회전 오차도 줄이게 만들 것.

![alt text](image-9.png)

정확도는 좋은 듯?

참고로 현재 방향 좌표계는 이거다:
```python
    target_rot = np.array([
            [1,  0,  0],
            [0, -1,  0],
            [0,  0, -1]
        ])

```

- 콘텍스트로 그리드의 사이즈도 주는게 좋을 듯, 뭔가 이정표가 될 것 같은데?

참고로 무조코 바닥 그리드 파란색 네모 하나가 각각 가로세로 20cm, 무조코 안에서 0.2이고, 흰색 그리드 네모는 하나가 각각 40cm, 0.4임.


- 참고로 잡기 포지션에서 회전이 된 키프레임은 다음과 같다.

```xml
  <keyframe>
    <key name="home" qpos="0 0 0 -1.57079 0 1.57079 0.732 0.04 0.04" ctrl="0 0 0 -1.57079 0 1.57079 0.732 255"/>
  </keyframe>
```

![alt text](image-10.png)

- API키 상위 폴더에서 가져오기.

- site를 구가 아니라 아예 기다랗고 얇은 초록색 원기둥으로 만들어 어딜가리키고 있는지 시각화해주는 것도 좋을 듯?

- 알게 된 것: 아직 가장 좋은 VLM도 이미지 속 공간을 잘 이해하지 못한다. 단순히 그리드 위에 도형이 어떻게 배치됐는지도 잘 모른다.

- 일단 로봇 base 정보를 주면 계속 헷갈려해서 base 정보를 빼고 이정표 박스를 여러개 심었다.

- 시점을 정면, 측면을 고정해서 진행했다.

API 요청 응답 시간은 약 24초 정도 소요된다.

- 드디어 잡는데 성공!!

main_agent_dual_cam.py

![alt text](image-11.png)

- 일단 한번 정리하고 넘어가주자.

