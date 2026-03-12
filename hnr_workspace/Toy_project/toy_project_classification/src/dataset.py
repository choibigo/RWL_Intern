import torch
from torch.utils.data import Dataset, DataLoader
# DataLoader
    # Dataset 이 데이터 하나를 꺼내는 규칙이라면,
    # DataLoader 는 그 데이터를
        # 여러개를 모아 batch 로 만들고
        # shuffle 하고
        # 병렬로 불러온다.
    # Dataset = 재료창고, DataLoader = 재료를 한 번에 담아오는 직원

from torchvision import datasets, transforms
# transforms : 이미지 전처리 도구

# 클래스에서 데이터 1개를 어떻게 꺼낼 것인가?
class CIFAR100CustomDataset(Dataset):
    # init 자세히 보기
        # 이 함수는 객체가 처음 만들어질 때 실행된다.
    def __init__(self, root, train=True, transform=None, download=True):
        self.dataset = datasets.CIFAR100(
            root=root, # 데이터 셋이 저장될 폴더 경로
            train=train, # 이 데이터셋이 학습용인가 검증 or test 용인가?
            transform=transform, # 전처리 : RandomCrop, ToTensor, Normalize
            download=download
        )

    def __len__(self):
        return len(self.dataset) # 총 데이터 개수 (Train: 50,000개, Valid: 10,000개)

    def __getitem__(self, idx):
        image, label = self.dataset[idx] # 인덱스(idx)에 해당하는 이미지 1장과 정답 1개 추출

        # torchvision dataset 은 (image, label) 로 만든다. 즉, 튜플의 형태이다.
        sample = {
            "image": image,
            "label": label,
            "index": idx
        }
        return sample

# 이미지 전처리와 데이터 증강
    # 학습용인지 검증용인지에 따라 다른 transform 을 반환하는 함수이다.
    # 학습 데이터를 augmentation 을 넣고, 검증 데이터는 augmentatioin 을 넣지 않기 때문이다.
def get_transforms(train=True):
    # transforms.Compose : 여러 transform 을 순서대로 연결한다.
        # 1. RandomCrop
        # 2. RandomHorizontalFlip
        # 3. ToTensor
        # 4. Normalize
    if train:
        return transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            # 이미지 주변에 padding 을 주고, 다시 32*32 로 랜덤하게 자른다.
            transforms.RandomHorizontalFlip(),
            # 좌우반전
            transforms.RandomRotation(15),
            transforms.ColorJitter(
                    brightness=0.2,
                    contrast=0.2,
                    saturation=0.2
                    ),
            transforms.ToTensor(),
            # [C,H,W] 형태로 변환한다.
            # 픽셀 값도 0~255 정수에서 0~1 실수 범위로 바꾼다.
            # transforms.RandomErasing(p=0.5),
            transforms.Normalize(
                mean=(0.5071, 0.4867, 0.4408),
                std=(0.2675, 0.2565, 0.2761)
            )
            # CIFAR-100 데이터셋 전체를 통계적으로 분석해서 계산된 평균(mean)과 표준편차(std)
            # 차례대로 R, G ,B Channel
        ])
    else:
        return transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                mean=(0.5071, 0.4867, 0.4408), 
                std=(0.2675, 0.2565, 0.2761)
            )
        ])

# Data Loader 만들기
    # train dataset, valid dataset을 만들고 각각에 대한 DataLoader 을 만들어 반환
def get_dataloader(root, batch_size, num_workers):
    train_dataset = CIFAR100CustomDataset(
        root=root,
        train=True,
        transform=get_transforms(train=True)
    )
    # CIFAR-100 학습 데이터 사용
    # 학습용 transform 적용
    # 필요하면 다운로드

    valid_dataset = CIFAR100CustomDataset(
        root=root,
        train=False,
        transform=get_transforms(train=False)
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers
    )

    valid_loader = DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers
    )

    return train_loader, valid_loader