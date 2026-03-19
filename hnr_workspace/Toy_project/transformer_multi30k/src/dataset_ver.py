import torch
from torch.nn.utils.rnn import pad_sequence
from torchtext.datasets import Multi30k
import torchtext.datasets.multi30k as multi30k
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

def _filter_fn(split, language_pair, i, x):
    return f"/{multi30k._PREFIX[split]}.{language_pair[i]}" in x[0]

multi30k._filter_fn = _filter_fn


SPECIALS = ['<unk>', '<pad>', '<bos>', '<eos>']
# <unk>: vocabulary에 없는 단어
# <pad>: 길이 맞추기용 빈 칸
# <bos>: beginning of sentence
# <eos>: end of sentence

# 데이터셋 전체에서 특정 언어 문장들을 하나씩 꺼내서 토큰 리스트를 생성하는 generator
def yield_tokens(data_iter, language, tokenizer):
    lang_idx = 0 if language == "de" else 1 
    for data_sample in data_iter:
        yield tokenizer(data_sample[lang_idx])

def build_tokenizers():
    src_tokenizer = get_tokenizer("basic_english") # source 용 tokenizer = 독일어
    tgt_tokenizer = get_tokenizer("basic_english") # target 용 tokenizer = 영어
    return src_tokenizer, tgt_tokenizer

# man -> 241 과 같은 정수 id 로 바꾸는 기준표가 필요하다. -> vocab

def build_vocabs(src_tokenizer, tgt_tokenizer, min_freq=2):
    # vocab 은 보통 train 데이터로만 만든다.
    train_iter = Multi30k(split='train', language_pair=('de', 'en'))

    src_vocab = build_vocab_from_iterator(
        yield_tokens(train_iter, "de", src_tokenizer), # 학습 데이터에서 독일어 문장만 뽑아서 토큰화한다.
        min_freq=min_freq, # 최소 2번 이상 나온 단어만 기록(기본값)
        specials=SPECIALS, # 특수 기호(<unk>, <pad>, <bos>, <eos>) 추가
        special_first=True # 특수 기호들에게 사전의 맨 앞 번호(0, 1, 2, 3)를 부여
    )
    src_vocab.set_default_index(src_vocab['<unk>']) 
    #vocab 에 없는 단어가 들어오면 에러 대신 <unk> index를 반환하라 

    train_iter = Multi30k(split='train', language_pair=('de', 'en'))
    tgt_vocab = build_vocab_from_iterator(
        yield_tokens(train_iter, "en", tgt_tokenizer),
        min_freq=min_freq,
        specials=SPECIALS,
        special_first=True
    )
    tgt_vocab.set_default_index(tgt_vocab['<unk>'])

    return src_vocab, tgt_vocab

# src_vocab 내부의 개념적인 모습
# {
#    '<unk>': 0,
#    '<pad>': 1,
#    '<bos>': 2,
#    '<eos>': 3,
#    'ein': 4,
#    'mann': 5,
#    'mit': 6,
#     ... (약 몇 천 개의 고유 단어들)
# }
# print(src_vocab['mann'])  # 출력: 5
# print(src_vocab['ein'])   # 출력: 4

def sequential_transforms(*transforms):

    # *transforms : 입력을 몇개 던지든 모아서 리스트로 만들겠다 
    # sequential_transforms(src_tokenizer, src_vocab, tensor_transform)
    # sequential_transforms(f1, f2, f3)
    # def new_func(x):
        # x = f1(x)
        # x = f2(x)
        # x = f3(x)
        # return x

    def func(txt_input):
        for transform in transforms:
            txt_input = transform(txt_input)
        return txt_input
    return func
    # 1바퀴 : txt_input = Tokenizer("Hello world") -> ['hello', 'world']
    # 2바퀴 : txt_input = Vocab(['hello', 'world']) -> [14, 25]
    # 3바퀴 : txt_input = tensor_transform([14, 25]) -> ([2, 14, 25, 3])


def tensor_transform(token_ids, bos_idx, eos_idx):
    # 입력값 3개
        # token_ids: 단어장을 거쳐 숫자로 바뀐 본문 단어들의 리스트 (예: [14, 25, 8])
        # bos_idx: <bos> 토큰의 고유 번호 (보통 2번)
        # eos_idx: <eos> 토큰의 고유 번호 (보통 3번)
    return torch.cat([
        torch.tensor([bos_idx]),
        torch.tensor(token_ids, dtype=torch.long),
        torch.tensor([eos_idx])
    ])


def get_text_transforms(src_vocab, tgt_vocab, src_tokenizer, tgt_tokenizer):
    bos_idx = src_vocab['<bos>'] # <bos> index 가져오기
    eos_idx = src_vocab['<eos>'] # <eos> index 가져오기

    # source 문장을 tensor 로 변환
    src_transform = sequential_transforms(
        src_tokenizer, # text -> token
        src_vocab, # token -> index mapping
        lambda x: tensor_transform(x, bos_idx, eos_idx)
    )

    # target 문장을 tensor 로 변환
    tgt_transform = sequential_transforms(
        tgt_tokenizer, # text -> token
        tgt_vocab, # token -> index mapping
        lambda x: tensor_transform(x, tgt_vocab['<bos>'], tgt_vocab['<eos>'])
    )
    return src_transform, tgt_transform

# 문장(batch) → tensor → padding → 모델 입력 형태(batch tensor)로 만드는 함수
def collate_fn(batch, src_transform, tgt_transform, pad_idx):
    src_batch = []
    tgt_batch = []

    for src_sample, tgt_sample in batch:
    # (List of (src_sentence, tgt_sentence))
        src_batch.append(src_transform(src_sample.rstrip("\n")))
        tgt_batch.append(tgt_transform(tgt_sample.rstrip("\n")))
    # 위의 과정이 종료되면 길이가 다른 tenspr 리스트가 담기게 된다.
    # ex)
    # src_batch = [
    # tensor([2, 57, 134, 982, 19, 3]),
    # tensor([2, 88, 45, 3]),
    # tensor([2, 12, 67, 90, 3])
    # ]

    src_batch = pad_sequence(src_batch, padding_value=pad_idx, batch_first=True)
    tgt_batch = pad_sequence(tgt_batch, padding_value=pad_idx, batch_first=True)
    # batch_first = True 인 경우 -> (batch_size, seq_len) = (3,6)

    return src_batch, tgt_batch

def get_dataloaders(batch_size=64, min_freq=2):
    # batch_size=64 → 한 번에 처리할 문장 개수
    # min_freq=2 → vocab에 포함할 최소 등장 횟수
    # (2번 이상 등장한 단어만 사용)

    from torch.utils.data import DataLoader

    # string -> 토큰 list
    src_tokenizer, tgt_tokenizer = build_tokenizers()
    
    # 토큰 -> 정수 index
    src_vocab, tgt_vocab = build_vocabs(src_tokenizer, tgt_tokenizer, min_freq=min_freq)
    
    # 문장
    # → tokenizer
    # → vocab
    # → bos/eos 추가
    # → tensor
    src_transform, tgt_transform = get_text_transforms(
        src_vocab, tgt_vocab, src_tokenizer, tgt_tokenizer
    )

    # padding
    pad_idx = src_vocab['<pad>']

    # dataset loading
    # Multi30k 구조
        # 각 element : ("독일어 문장", "영어 문장")
    # list 를 통해 memory 에 다 올려두기
    train_iter = list(Multi30k(split='train', language_pair=('de', 'en')))
    valid_iter = list(Multi30k(split='valid', language_pair=('de', 'en')))
    test_iter = list(Multi30k(split='test', language_pair=('de', 'en')))

    # Train_loader
        # DataLoader : dataset -> batch 단위로 꺼내주는 객체
    train_loader = DataLoader(
        train_iter,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda batch: collate_fn(batch, src_transform, tgt_transform, pad_idx)
    )

    valid_loader = DataLoader(
        valid_iter,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda batch: collate_fn(batch, src_transform, tgt_transform, pad_idx)
    )

    test_loader = DataLoader(
        test_iter,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda batch: collate_fn(batch, src_transform, tgt_transform, pad_idx)
    )

    return train_loader, valid_loader, test_loader, src_vocab, tgt_vocab