import os
import glob
import tarfile
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


def yield_tokens(data_iter, language, tokenizer):
    lang_idx = 0 if language == "de" else 1
    for data_sample in data_iter:
        yield tokenizer(data_sample[lang_idx])


def build_tokenizers():
    src_tokenizer = get_tokenizer("basic_english")
    tgt_tokenizer = get_tokenizer("basic_english")
    return src_tokenizer, tgt_tokenizer


def build_vocabs(src_tokenizer, tgt_tokenizer, min_freq=2):
    train_iter = Multi30k(split='train', language_pair=('de', 'en'))
    src_vocab = build_vocab_from_iterator(
        yield_tokens(train_iter, "de", src_tokenizer),
        min_freq=min_freq,
        specials=SPECIALS,
        special_first=True
    )
    src_vocab.set_default_index(src_vocab['<unk>'])

    train_iter = Multi30k(split='train', language_pair=('de', 'en'))
    tgt_vocab = build_vocab_from_iterator(
        yield_tokens(train_iter, "en", tgt_tokenizer),
        min_freq=min_freq,
        specials=SPECIALS,
        special_first=True
    )
    tgt_vocab.set_default_index(tgt_vocab['<unk>'])

    return src_vocab, tgt_vocab


def sequential_transforms(*transforms):
    def func(txt_input):
        for transform in transforms:
            txt_input = transform(txt_input)
        return txt_input
    return func


def tensor_transform(token_ids, bos_idx, eos_idx):
    return torch.cat([
        torch.tensor([bos_idx]),
        torch.tensor(token_ids, dtype=torch.long),
        torch.tensor([eos_idx])
    ])


def get_text_transforms(src_vocab, tgt_vocab, src_tokenizer, tgt_tokenizer):
    bos_idx = src_vocab['<bos>']
    eos_idx = src_vocab['<eos>']

    src_transform = sequential_transforms(
        src_tokenizer,
        src_vocab,
        lambda x: tensor_transform(x, bos_idx, eos_idx)
    )

    tgt_transform = sequential_transforms(
        tgt_tokenizer,
        tgt_vocab,
        lambda x: tensor_transform(x, tgt_vocab['<bos>'], tgt_vocab['<eos>'])
    )
    return src_transform, tgt_transform


def collate_fn(batch, src_transform, tgt_transform, pad_idx):
    src_batch = []
    tgt_batch = []

    for src_sample, tgt_sample in batch:
        src_batch.append(src_transform(src_sample.rstrip("\n")))
        tgt_batch.append(tgt_transform(tgt_sample.rstrip("\n")))

    src_batch = pad_sequence(src_batch, padding_value=pad_idx, batch_first=True)
    tgt_batch = pad_sequence(tgt_batch, padding_value=pad_idx, batch_first=True)

    return src_batch, tgt_batch


def _load_test_pairs_from_cache():
    import os
    import glob
    import tarfile

    tar_path = "/root/.cache/torch/text/datasets/Multi30k/mmt16_task1_test.tar.gz"

    if not os.path.exists(tar_path):
        raise FileNotFoundError(f"test tar 파일을 찾지 못했습니다: {tar_path}")

    extract_dir = "/workspace/multi30k_test_extract"
    os.makedirs(extract_dir, exist_ok=True)

    with tarfile.open(tar_path, "r:gz") as tar:
        members = [
            m for m in tar.getmembers()
            if os.path.basename(m.name) in ("test.de", "test.en")
        ]
        tar.extractall(path=extract_dir, members=members)

    de_files = glob.glob(os.path.join(extract_dir, "**", "test.de"), recursive=True)
    en_files = glob.glob(os.path.join(extract_dir, "**", "test.en"), recursive=True)

    if not de_files or not en_files:
        raise FileNotFoundError("추출 후 test.de 또는 test.en 파일을 찾지 못했습니다.")

    de_path = de_files[0]
    en_path = en_files[0]

    with open(de_path, "r", encoding="utf-8") as f:
        de_lines = [line.rstrip("\n") for line in f]

    with open(en_path, "r", encoding="utf-8") as f:
        en_lines = [line.rstrip("\n") for line in f]

    if len(de_lines) != len(en_lines):
        raise ValueError(f"test.de와 test.en 줄 수가 다릅니다: {len(de_lines)} vs {len(en_lines)}")

    return list(zip(de_lines, en_lines))


def get_dataloaders(batch_size=64, min_freq=2):
    from torch.utils.data import DataLoader

    src_tokenizer, tgt_tokenizer = build_tokenizers()
    src_vocab, tgt_vocab = build_vocabs(src_tokenizer, tgt_tokenizer, min_freq=min_freq)

    src_transform, tgt_transform = get_text_transforms(
        src_vocab, tgt_vocab, src_tokenizer, tgt_tokenizer
    )

    pad_idx = src_vocab['<pad>']

    train_iter = list(Multi30k(split='train', language_pair=('de', 'en')))
    valid_iter = list(Multi30k(split='valid', language_pair=('de', 'en')))
    test_iter = _load_test_pairs_from_cache()

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