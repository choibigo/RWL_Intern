from dataclasses import dataclass, field
from typing import List
import torch

@dataclass
class TransformerConfig:
    data_path: str = "/workspace/ToyProject-transformer/Multi30k/data/task1/raw" # 또는 /tok
    src_lang: str = "de" # 독일어 동화 같은 느낌임.
    tgt_lang: str = "en" # 영어
    
    # 특수 토큰 인덱스
    PAD_IDX: int = 0  # <pad> : 문장 길이 맞추기
    SOS_IDX: int = 1  # <SOS> : Start
    EOS_IDX: int = 2  # <EOS> : End
    UNK_IDX: int = 3  # <Unk> : Unknown : 빈도가 낮은 단어가 변환된다?
    # 위 4가지 특수 토큰의 문자열 리스트
    special_symbols: List[str] = field(default_factory=lambda: ["<pad>", "<sos>", "<eos>", "<unk>"])
    
    # 모델 하이퍼파라미터 (나중에 모델 정의 시 사용)
    batch_size: int = 128
    d_model: int = 512  # d_model
    n_head: int = 8     # multi-head attention을 수행하기위한 head 개수 (d_k = d_model/head -> 각 head의 차원)
    num_encoder_layers: int = 3 # N
    num_decoder_layers: int = 3 # N
    dim_feedforward: int = 512 # attention 뒤에 붙는 MLP (보통 d_model의 4배 정도)
    dropout: float = 0.1
    device: torch.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
