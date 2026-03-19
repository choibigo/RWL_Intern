# models/transformer.py
import math
import torch
import torch.nn as nn

# PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
# PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        pe = torch.zeros(max_len, d_model)   # (max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()  # (max_len, 1)

        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)   # (1, max_len, d_model)
        self.register_buffer("pe", pe)

    def forward(self, x):
        # x: (B, L, D)
        x = x + self.pe[:, :x.size(1)]
        return self.dropout(x)

# Q, K, V 선형변환으로 만들기
# 여러 head 로 분할하기
# 각 head 에서 scaled dot-product attention 수행
# 다시 Concat 해서 최종 linear projection
class MultiHeadAttention(nn.Module):

    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()

        # d_model 을 n_heads 개로 균등하게 쪼개야한다.
        assert d_model % n_heads == 0

        # 기본 속성 저장
            # d_model = 512
            # n_heads = 8
            # head_dim = 64
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        # Q, K, V 용 선형 변환
            # Q = query × Wq
            # K = key   × Wk
            # V = value × Wv
        self.w_q = nn.Linear(d_model, d_model) # 512x512
        self.w_k = nn.Linear(d_model, d_model) # 512x512
        self.w_v = nn.Linear(d_model, d_model) # 512x512

        # 최종 출력 projection, 논문에서의 W^O
        self.fc_out = nn.Linear(d_model, d_model) # 512x512

        self.dropout = nn.Dropout(dropout)

        # Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V
        self.scale = math.sqrt(self.head_dim)

    # 1. query, key, value 를 받아서 Q, K, V 를 만든다.
    # 2. 8개 head 로 나눠 attention 수행한 뒤 합쳐서 다시 출력
    def forward(self, query, key, value, mask=None):
        # query는 3차원 형태의 텐서로 들어온다. (B, L, D)
            # B : Batch size = 32
            # L : Sequence Length = 4
            # D : 단어 하나의 feature vector = 512
        B = query.size(0)

        # Q, K, V 만들기
            # Q = query × Wq + bq
            # K = key   × Wk + bk
            # V = value × Wv + bv
        Q = self.w_q(query)  # (B, Lq, D) = (32, 10, 512) -> (32, 10, 512)
        K = self.w_k(key)    # (B, Lk, D) = (32, 12, 512) -> (32, 12, 512)
        V = self.w_v(value)  # (B, Lv, D) = (32, 12, 512) -> (32, 12, 512)

        # (B, L, D) -> (B, H, L, head_dim)
        # Q : (32, 10, 512) -> (32, 10, 8, 64) -> (32, 8, 10, 64)
        # K : (B, H, Lk, head_dim) = (32, 8, 12, 64)
        # V : (B, H, Lv, head_dim) = (32, 8, 12, 64)
        Q = Q.view(B, -1, self.n_heads, self.head_dim).transpose(1, 2)
        K = K.view(B, -1, self.n_heads, self.head_dim).transpose(1, 2)
        V = V.view(B, -1, self.n_heads, self.head_dim).transpose(1, 2)

        # energy: (B, H, Lq, Lk) 
        # K : (32, 8, 12, 64) -> K^T : (32, 8, 64, 12) = (B, H, head_dim, Lk)
        # Q : (32, 8, 10, 64)
        # Q @ K^T : (32, 8, 10, 64) @ (32, 8, 64, 12) = (32, 8, 10, 12) = (B, H, Lq, Lk)
        # 배치 B 에서 head H 가 query의 i 번째 위치가 key 의 j 번째 위치를 얼마나 참고할것인가?

        energy = torch.matmul(Q, K.transpose(-2, -1)) / self.scale

        # masked_fill(condition, value) : condition이 True인 위치를 value로 바꾼다
        # mask 는 왜 필요한가?
            # padding mask : <pad> 토큰은 진짜 단어가 아니니까 보면 안 된다.
            # causal mask : decoder self-attention 에서는 미래 단어를 보면 안된다.
        if mask is not None:
            energy = energy.masked_fill(mask == 0, float('-inf'))

        # score 을 attention weight 로 바꾸는 단계
        # 왜 dim = -1 인가?
            # (B, H, Lq, Lk) 에서 마지막 Lk 는 key 의 위치들이다.
            # 즉 query 하나가 key 전체를 보고 있을때 각 key를 얼마나 볼지 확률처럼 정규화해야함
            # 즉 query 한 위치는 key 전체에 대해 가중치 분포를 가진다.
        attention = torch.softmax(energy, dim=-1)

        # attention : (B, H, Lq, Lk)
        # query i → key j 로 가는 연결 weight 를 끊어버림
        attention = self.dropout(attention)

        # attention : (B, H, Lq, Lk) @ (B, H, Lv, head_dim)
        # Lk = Lv
        # x: (B, H, Lq, head_dim) = (32, 8, 10, 64)
        # 직관적으로 
            # attention = 비율표
            # V = 재료
            # x = 비율대로 섞은 최종 결과
        x = torch.matmul(attention, V)

        # Concat(head1, ..., headH)
        # x: (B, H, Lq, head_dim) = (32, 8, 10, 64)
        # transpose(1, 2) = (B, Lq, H, head_dim) = (32, 10, 8, 64)
        # (B, Lq, H, head_dim) -> (B, Lq, D) = (32, 10, 8, 64) -> (32, 10, 512)
        x = x.transpose(1, 2).contiguous().view(B, -1, self.d_model) 

        # 최종 projection W^O
            # fc_out = Linear(d_model, d_model)
            # (B, Lq, D) -> (B, Lq, D) = (32, 10, 512) → (32, 10, 512)
        x = self.fc_out(x)
        return x, attention

#1) Multi-Head Attention → 토큰 간 정보 섞기
#2) Feed Forward → 각 토큰을 개별적으로 가공
    # FFN(x) = max(0, xW1 + b1) W2 + b2
    # 입력 x : (B, L, d_model) -> (B, L, d_model)
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff), # (512, 2048) : (32, 10, 512) -> (32, 10, 2048)
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model) # (2048, 512) : (32, 10, 2048) -> (32, 10, 512)
        )

    def forward(self, x):
        return self.net(x)

# Self-Attention → Add & Norm → FFN → Add & Norm
class EncoderLayer(nn.Module):
    # 해당 layer 에 필요한 모듈들을 정의
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1): # d_ff = 2048
        super().__init__()

        self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)

        self.norm1 = nn.LayerNorm(d_model) # self-attention 뒤에
        self.norm2 = nn.LayerNorm(d_model) # FFN 뒤에

        self.dropout = nn.Dropout(dropout)

    def forward(self, src, src_mask):
        # src: (B, src_len, D) = (32, 20, 512)
            # B = 32: 문장 32개
            # src_len = 20: 각 문장의 길이 20
            # D = 512: 각 토큰 임베딩 차원
        
        # 첫 번째 sub-layer: Self-Attention
            # src = query, key, value -> encoder self-attention 에서는 Q, K, V 가 모두 같은 입력에서 부터 나온다.
            # Q=src*W_q / K=src*W_k / V =src*W_v​
            # _src.shape = (32, 20, 512)
        _src, _ = self.self_attn(src, src, src, src_mask)

        # LayerNorm(x+Sublayer(x))
        # output=LayerNorm(x+Dropout(SelfAttention(x)))
        src = self.norm1(src + self.dropout(_src))

        # 두 번째 sub-layer: Feed-Forward Network
            # FFN(x)= W_2​*(ReLU(x*W_1​+b_1​))+b_2​
            # 입력: 512
            # hidden: 2048
            # 출력: 512
            # 각 토큰 위치마다
            # 512차원 → 2048차원
            # ReLU
            # 2048차원 → 512차원
        _src = self.ffn(src)

        # output=LayerNorm(x+Dropout(FFN(x)))
        # shape 는 여전히 (32, 20, 512)
        src = self.norm2(src + self.dropout(_src))

        return src


# Masked self-attention → Add & Norm → encoder-decoder attention → Add & Norm → FFN → Add & Norm
class DecoderLayer(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()

        # decoder 내부 토큰들끼리 보는 self-attention
        self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)

        # decoder가 encoder output을 바라보는 encoder-decoder attention
        self.enc_dec_attn = MultiHeadAttention(d_model, n_heads, dropout)

        # FFN(x)=max(0,xW_1​+b_1​)W_2​+b_2​
            # 입력: d_model = 512
            # 내부 hidden: d_ff = 2048
            # 출력: 512
        self.ffn = PositionwiseFeedForward(d_model, d_ff, dropout)

        # LayerNorm 3개
        self.norm1 = nn.LayerNorm(d_model) # masked self-attention 뒤
        self.norm2 = nn.LayerNorm(d_model) # encoder-decoder attention 뒤
        self.norm3 = nn.LayerNorm(d_model) # FFN 뒤

        self.dropout = nn.Dropout(dropout)


        # layer 가 입력으로 받는 것
            # tgt: 현재 decoder 입력
            # enc_src: encoder의 최종 출력
            # tgt_mask: decoder self-attention용 mask
            # src_mask: encoder output에서 pad를 가리기 위한 mask
    def forward(self, tgt, enc_src, tgt_mask, src_mask):
        
        # 첫 번째 sub-layer: masked self-attention
            # tgt -> decoder 현재 입력
                # shape : (B,tgt_len,d_model) = (32, 15, 512)
                # 한 칸 오른쪽으로 shift된 decoder input
            # tgt_mask -> decoder self-attention 용 mask
                # <pad> 위치 가리기
                # 미래 토큰 가리기
                # -> look-ahead mask + padding mask
        _tgt, _ = self.self_attn(tgt, tgt, tgt, tgt_mask)
        tgt = self.norm1(tgt + self.dropout(_tgt))

        # 두 번째 sub-layer: encoder-decoder attention
            # enc_src -> encoder 최종 출력
                # shape : (B,src_len,d_model) = (32, 20, 512)
            # src_mask -> encoder-decoder attention에서 사용하는 mask
                # encoder 쪽 <pad> 위치를 가리기 위한 것
        _tgt, attention = self.enc_dec_attn(tgt, enc_src, enc_src, src_mask)
        tgt = self.norm2(tgt + self.dropout(_tgt))

        # 세 번째 sub-layer: FFN
            # FFN(x)=max(0,xW_1​+b_1​)W_2​+b_2​
        _tgt = self.ffn(tgt)
        tgt = self.norm3(tgt + self.dropout(_tgt))

        return tgt, attention


# Encoder layer 여러개를 쌓아서 Encoder stack 을 만드는 과정
class Encoder(nn.Module):
    def __init__(self, input_dim, d_model, n_layers, n_heads, d_ff, dropout, max_len):
        super().__init__()

        # 토큰 번호를 벡터로 바꾸는 임베딩 층
            # 예 
                # input_dim = 10000
                # d_model = 512
                # 10000개의 단어 각각에 대해 512 차원의 학습 가능한 벡터를 가진다.
        self.tok_embedding = nn.Embedding(input_dim, d_model)

        # PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
        # PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
        self.pos_embedding = PositionalEncoding(d_model, dropout, max_len)

        # n_layers = 6 
        # self.layers = [
        #    EncoderLayer1,
        #    EncoderLayer2,
        #    EncoderLayer3,
        #    EncoderLayer4,
        #    EncoderLayer5,
        #    EncoderLayer6
        #]   
        self.layers = nn.ModuleList([
            EncoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)
        ])
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(d_model)

    # src: source 문장 토큰 id
    # src_mask: source padding mask
    def forward(self, src, src_mask):
        # src: (B, src_len)
            # B = 32
            # src_len = 20 -> 길이가 20으로 padding 되어 있을 수 있음
            # 여기서 0 은 <pad>일 수 있다. -> 이때 src는 아직 벡터가 아니라 정수 인덱스이다.
            # src =
            # [
            #   [5, 19, 83, 2, 0, 0, 0],
            #   [7, 91, 14, 65, 3, 2, 0],
            #   ...
            # ]

        # 정수 토큰 id를 벡터로 바꾼다 : (32, 20) -> (32, 20, 512)
            # (B, src_len) -> (B, src_len, d_model)
            # 벡터로 바꾼 뒤에 각 값뒤에 sqrt{d_model}
        src = self.tok_embedding(src) * self.scale

        # positional encoding 추가
        src = self.pos_embedding(src)

        # Encoder layer 들을 차례대로 통과
            # src: (B, src_len, D) = (32, 20, 512) -> shape 은 계속 유지
            # src = EncoderLayer1(src, src_mask)
            # src = EncoderLayer2(src, src_mask)
            # src = EncoderLayer3(src, src_mask)
            # src = EncoderLayer4(src, src_mask)
            # src = EncoderLayer5(src, src_mask)
            # src = EncoderLayer6(src, src_mask)
        for layer in self.layers:
            src = layer(src, src_mask)

        return src


class Decoder(nn.Module):
    def __init__(self, output_dim, d_model, n_layers, n_heads, d_ff, dropout, max_len):
        super().__init__()

        # (B, tgt_len) -> (B, tgt_len, d_model)
        self.tok_embedding = nn.Embedding(output_dim, d_model)
        
        self.pos_embedding = PositionalEncoding(d_model, dropout, max_len)


        self.layers = nn.ModuleList([
            DecoderLayer(d_model, n_heads, d_ff, dropout) for _ in range(n_layers)
        ])

        # DecoderLayer 를 다 통과한 뒤 각 위체의 벡터 shape = (B, tgt_len, d_model)
        # 최종적으로 원하는 것 : 각 위치에서 target vocab의 모든 단어에 대한 점수
            # d_model = 512, output_dim = 8000 : 512차원 벡터 -> 8000차원 점수 벡터
        self.fc_out = nn.Linear(d_model, output_dim)

        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(d_model)

    def forward(self, tgt, enc_src, tgt_mask, src_mask):
        # tgt: (B, tgt_len) -> (B, tgt_len, d_model)
        tgt = self.tok_embedding(tgt) * self.scale
        # positional embedding
        tgt = self.pos_embedding(tgt)

        # tgt, attention = DecoderLayer1(tgt, enc_src, tgt_mask, src_mask)
        # tgt, attention = DecoderLayer2(tgt, enc_src, tgt_mask, src_mask)
        # tgt, attention = DecoderLayer3(tgt, enc_src, tgt_mask, src_mask)
        # tgt, attention = DecoderLayer4(tgt, enc_src, tgt_mask, src_mask)
        # tgt, attention = DecoderLayer5(tgt, enc_src, tgt_mask, src_mask)
        # tgt, attention = DecoderLayer6(tgt, enc_src, tgt_mask, src_mask)
        # 1) masked self-attention
            # 미래 토큰을 보면 안 됨
            # 그래서 tgt_mask 필요
        # 2) encoder-decoder attention
            # encoder 쪽 <pad>를 보면 안 됨
            # 그래서 src_mask 필요
        attention = None
        for layer in self.layers:
            tgt, attention = layer(tgt, enc_src, tgt_mask, src_mask)

        # (B, tgt_len, d_model) -> (B, tgt_len, output_dim)
        # (32, 15, 512) -> (32, 15, 8000) : 8000개 단어에 대한 점수(logits)
        output = self.fc_out(tgt)  # (B, tgt_len, vocab_size)
        return output, attention


class Transformer(nn.Module):
    def __init__(
        self,
        input_dim,
        output_dim,
        src_pad_idx,
        tgt_pad_idx,
        d_model=256,
        n_heads=4,
        num_encoder_layers=3,
        num_decoder_layers=3,
        d_ff=512,
        dropout=0.1,
        max_len=100
    ):
        super().__init__()

        self.encoder = Encoder(
            input_dim, d_model, num_encoder_layers, n_heads, d_ff, dropout, max_len
        )
        self.decoder = Decoder(
            output_dim, d_model, num_decoder_layers, n_heads, d_ff, dropout, max_len
        )

        self.src_pad_idx = src_pad_idx
        self.tgt_pad_idx = tgt_pad_idx
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def make_src_mask(self, src):
        # src: (B, src_len)
        # mask: (B, 1, 1, src_len)
        src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
        return src_mask

    def make_tgt_mask(self, tgt):
        # tgt: (B, tgt_len)
        B, tgt_len = tgt.shape

        tgt_pad_mask = (tgt != self.tgt_pad_idx).unsqueeze(1).unsqueeze(2)
        # (B,1,1,tgt_len)

        tgt_sub_mask = torch.tril(
            torch.ones((tgt_len, tgt_len), device=tgt.device)
        ).bool()
        # (tgt_len, tgt_len)

        tgt_mask = tgt_pad_mask & tgt_sub_mask.unsqueeze(0).unsqueeze(1)
        # (B,1,tgt_len,tgt_len)

        return tgt_mask

    def forward(self, src, tgt):
        src_mask = self.make_src_mask(src)
        tgt_mask = self.make_tgt_mask(tgt)

        enc_src = self.encoder(src, src_mask)
        output, attention = self.decoder(tgt, enc_src, tgt_mask, src_mask)

        return output, attention