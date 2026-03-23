### 계획

- [x] ViT 공부계획
- [ ] 영상 시청
- [ ] 논문보기

# ViT: Vision Transformer

AN IMAGE IS WORTH 16X16 WORDS: TRANSFORMERS FOR IMAGE RECOGNITION AT SCALE에서 제안됨.
https://arxiv.org/pdf/2010.11929

![](images/2026-03-23-18-54-54.png)


https://www.youtube.com/watch?v=vJF3TBI8esQ

- ViT는 그냥 인풋이 이미지인 Transformer임.

- 근데 이미지가 들어가니 이미지를 쪼개서 넣을 뿐.

![](images/2026-03-23-19-03-15.png)

이렇게 먼저 이미지를 여럿으로 쪼갠다. 각각의 조각들은 patches라고 부른다.

- 물론 RGB 이미지면 쪼갠 한 조각에 3개의 채널이 마찬가지로 있다.

![](images/2026-03-23-19-05-45.png)

- 0~255로 있던 값들은 전부 0~1로 정규화를 시키고.

- 이 조각을 (RGB 3개 채널 모두) 하나의 벡터로 평탄화 시킨다.

- 그리고 이를 모든 구역들의 조각에 똑같이한다.

![](images/2026-03-23-19-07-53.png)

즉, 지금은 나눠진 조각의 수 만큼 평탄화로 만들어진 벡터가 존재한다.

이 각 벡터들이 하나한의 토큰이다. (또는 토큰 임베딩)

