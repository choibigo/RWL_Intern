import os
import random
import numpy as np
import torch

# 딥러닝 실험의 랜덤성을 고정해서 결과를 재현 가능하게 만든다.
def set_seed(seed: int = 42): # 실험 결과를 항상 동일하게 만들기
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def calculate_accuracy(outputs, labels): # 모델 정확도 계산
    preds = outputs.argmax(dim=1) # 가장 큰 값의 index 찾기
    correct = (preds == labels).sum().item()
    total = labels.size(0)
    return correct / total


def save_model(model, path): # 학습된 모델 저장
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path) # state_dict 는 모델의 모든 weight 이다.