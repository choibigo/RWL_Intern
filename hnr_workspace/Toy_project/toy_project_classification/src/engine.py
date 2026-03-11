# src/engine.py
# 학습/ 검증 1회 실행
from tqdm import tqdm
import torch
from src.utils import calculate_accuracy


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()

    total_loss = 0.0
    total_acc = 0.0

    pbar = tqdm(loader, desc="Train", leave=False)

    # batch의 대략적 구조
        # {"image": tensor[Batch, 3, 32, 32],
        #    "label": tensor[Bathch],
        #    "index": tensor[Batch]
        # }
    for batch in pbar:
        images = batch["image"].to(device) # batch["image"] = [Batch, 3, 32, 32]
        labels = batch["label"].to(device) # batch["label"] = [Batch]

        optimizer.zero_grad()
        # gradient 초기화

        outputs = model(images) # forward propagation, 출력 shape = [Batch,100] -> 100개 클래스에 대한 score
        loss = criterion(outputs, labels) # Batch 전체에 대한 평균 손실
        loss.backward()
        optimizer.step()

        acc = calculate_accuracy(outputs, labels)

        total_loss += loss.item()
        total_acc += acc

        pbar.set_postfix(loss=loss.item(), acc=acc)

    return total_loss / len(loader), total_acc / len(loader)
    # 전체 batch loss 합 / batch 수
    # 전체 batch acc 합 / batch 수


@torch.no_grad()
def valid_one_epoch(model, loader, criterion, device):
    model.eval()

    total_loss = 0.0
    total_acc = 0.0

    pbar = tqdm(loader, desc="Valid", leave=False)

    for batch in pbar:
        images = batch["image"].to(device)
        labels = batch["label"].to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)

        acc = calculate_accuracy(outputs, labels)

        total_loss += loss.item()
        total_acc += acc

        pbar.set_postfix(loss=loss.item(), acc=acc)

    return total_loss / len(loader), total_acc / len(loader)