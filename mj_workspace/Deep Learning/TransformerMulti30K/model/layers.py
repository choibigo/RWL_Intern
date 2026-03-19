import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        # 1. 위치 정보를 담을 행렬 초기화 (max_len, d_model)
        pe = torch.zeros(max_len, d_model)
        
        # 2. 위치 인덱스 생성 (0, 1, 2, ..., max_len-1)
        # shape: (max_len, 1)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # 3. 주기 함수에 들어갈 계수(div_term) 계산
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        # 4. 짝수 인덱스(2i)에는 sin, 홀수 인덱스(2i+1)에는 cos 적용
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # 5. 차원 맞추기: (max_len, 1, d_model) 
        pe = pe.unsqueeze(0).transpose(0, 1)
        
        # 6. 학습되지 않는 파라미터이므로 register_buffer로 등록
        self.register_buffer('pe', pe)

    def forward(self, x):

        # x의 길이만큼만 위치 정보를 가져와서 더해줌
        x = x + self.pe[:x.size(0), :]
        
        # 논문에서 언급된 대로 마지막에 Dropout 적용
        return self.dropout(x)

# Embedding + PE
class TransformerEmbedding(nn.Module):
    def __init__(self, vocab_size, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        # Embedding: 단어를 d_model 차원의 벡터로 변환
        self.token_emb = nn.Embedding(vocab_size, d_model)
        
        # Positional Encoding: 아까 정의했던 PositionalEncoding 클래스 사용
        self.pos_emb = PositionalEncoding(d_model, dropout, max_len)
        
        self.d_model = d_model

    def forward(self, x):
        # Embedding 후 sqrt(d_model)을 곱해줌으로써 scaling
        out = self.token_emb(x) * math.sqrt(self.d_model)
        # positional 정보 더하기
        out = self.pos_emb(out)
        
        return out # 최종 shape: (Seq_Len, Batch_Size, d_model)




class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, n_head, dropout=0.1):
        super().__init__()
        assert d_model % n_head == 0 # d_model이 head로 나눠지는지 확인
        
        self.d_model = d_model
        self.n_head = n_head
        self.d_k = d_model // n_head # 512 / 8 = 64 (head별 dimension)
        
        # 1. 가중치 행렬들 (W_q, W_k, W_v)
        # 512x512로 만들고 나중에 64x64로 쪼갬.
        self.w_q = nn.Linear(d_model, d_model)
        self.w_k = nn.Linear(d_model, d_model)
        self.w_v = nn.Linear(d_model, d_model)
        self.w_o = nn.Linear(d_model, d_model) # 최종 출력용 Wo
        
        self.dropout = nn.Dropout(dropout)
        # self.scale = torch.sqrt(torch.FloatTensor([self.d_k])) # 루트(d_k)
        self.register_buffer('scale', torch.sqrt(torch.tensor([self.d_k], dtype=torch.float)))

    def forward(self, q, k, v, mask=None):
        batch_size = q.shape[1] # (Seq, Batch, Dim) 기준이므로 index 1에서 가져옴.
        
        # Step 1: Linear 연산 수행
        Q = self.w_q(q)  # q(Lx512) @ W_q(512X512)
        K = self.w_k(k)
        V = self.w_v(v)
        
        # Step 2: 헤드 쪼개기
        # (Seq, Batch, 512) -> (Seq, Batch, 8, 64) -> (Batch, 8, Seq, 64)
        # transpose(0, 1) 등을 써서 Batch가 맨 앞으로 오게 정렬합니다 (연산 편의성)
        # 즉, Lx 512 -> Lx64 8channel
        Q = Q.view(-1, batch_size, self.n_head, self.d_k).permute(1, 2, 0, 3) 
        K = K.view(-1, batch_size, self.n_head, self.d_k).permute(1, 2, 0, 3)
        V = V.view(-1, batch_size, self.n_head, self.d_k).permute(1, 2, 0, 3)
        
        # Step 3: Scaled Dot-Product Attention 계산 (Q @ Kt -> LxL)
        # (Q @ Kt) / root d_k
        # Q,K,V = (Batch, Head, Seq_len_q, d_k) -> (B, 8, L_q, 64)
        # K.permute(0, 1, 3, 2) -> (B, 8, 64, L_k)
        # matmul은 앞의 (B, 8)은 건드리지 않고, 마지막 두 차원끼리만 행렬 곱을 수행 (L_q x 64 @ 64 x L_k -> L_q x L_k)
        energy = torch.matmul(Q, K.permute(0, 1, 3, 2)) / self.scale
        # energy = energy.masked_fill(mask == 0, float('-inf'))
        
        # Decoder의 Masked Multi-head attention
        if mask is not None:
            # mask가 0(False)인 부분을 아주 작은 값(-inf)으로 채워 softmax 결과가 0이 되게 함
            energy = energy.masked_fill(mask == 0, float('-inf'))
       
        # energy shape : [Batch_size, n_head, Seq_len_q(L_q), Seq_len_k(L_k)]    
        attention = self.dropout(torch.softmax(energy, dim=-1)) # softmax 통과 후 dropout
        
        # 결과물: (Batch, 8, Seq, 64)
        x = torch.matmul(attention, V) # attention과 V 행렬곱으로 최종 attention값 구함
        
        # Step 4: 다시 합치기 (Concat)
        # (Batch, 8, Seq, 64) -> (Seq, Batch, 512)
        # Lx 64 8 channel -> L x 512
        x = x.permute(2, 0, 1, 3).contiguous()
        x = x.view(-1, batch_size, self.d_model)
        
        return self.w_o(x), attention # 마지막 w_o 통과하여 return
    

class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.w_1 = nn.Linear(d_model, d_ff) # 512 -> 2048
        self.w_2 = nn.Linear(d_ff, d_model) # 2048 -> 512
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: (Seq_len, Batch, 512)
        x = self.dropout(torch.relu(self.w_1(x)))
        x = self.w_2(x)
        return x        # w_2(dropout(relu(w_1*x)))