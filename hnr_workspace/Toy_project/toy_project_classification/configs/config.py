# 하이퍼파라미터
    #batch size
    # lr
    # epoch
    # num_workers
    # image size
    # num_classes

class CFG:
    SEED = 42

    BATCH_SIZE = 128
    NUM_WORKERS = 2 #CPU의 일꾼(프로세스) 수
    EPOCHS = 10
    LR = 1e-3

    NUM_CLASSES = 100
    IMAGE_SIZE = 32

    DEVICE = "cuda"
    DATA_ROOT = "./data"
    SAVE_DIR = "./outputs"