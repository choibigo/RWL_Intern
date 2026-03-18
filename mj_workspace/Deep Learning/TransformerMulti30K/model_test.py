import torch

from model import Transformer, Encoder, Decoder

# 1. 하이퍼파라미터 설정 (테스트용)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

INPUT_DIM = 7853  # 독어 사전 크기
OUTPUT_DIM = 5893 # 영어 사전 크기
D_MODEL = 512
N_LAYERS = 3      # 테스트니까 가볍게 3층만
N_HEADS = 8
D_FF = 2048
DROPOUT = 0.1
MAX_LEN = 100

# 패딩 인덱스 정의 (보통 1번이나 0번)
SRC_PAD_IDX = 1
TRG_PAD_IDX = 1

# 2. 모델 인스턴스 생성
enc = Encoder(INPUT_DIM, D_MODEL, N_LAYERS, N_HEADS, D_FF, DROPOUT, MAX_LEN)
dec = Decoder(OUTPUT_DIM, D_MODEL, N_LAYERS, N_HEADS, D_FF, DROPOUT, MAX_LEN)

model = Transformer(enc, dec, SRC_PAD_IDX, TRG_PAD_IDX, device).to(device)

# 3. 가짜 데이터 생성 (Batch_size=32, Seq_len=20)
# 각 숫자는 단어 번호를 의미함
src = torch.randint(0, INPUT_DIM, (20, 32)).to(device)
trg = torch.randint(0, OUTPUT_DIM, (15, 32)).to(device) # trg_input 역할

# 4. 모델 실행
output, attention = model(src, trg)

# 5. 결과 확인
print(f"입력 src 모양: {src.shape}")       # [20, 32]
print(f"입력 trg 모양: {trg.shape}")       # [15, 32]
print("-" * 30)
print(f"출력 output 모양: {output.shape}")  # [15, 32, 5893]
print(f"어텐션 맵 모양: {attention.shape}") # [32, 8, 15, 20]