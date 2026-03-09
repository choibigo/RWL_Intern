import torch
from torch.optim.lr_scheduler import StepLR
import numpy as np # confusion matrix 사용시
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
from torch.utils.tensorboard import SummaryWriter

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# TensorBoard log directory 설정
log_dir = 'runs'
writer = SummaryWriter(log_dir)

def Train(model, train_DL, val_DL, criterion, optimizer, scheduler,
          EPOCH, BATCH_SIZE, save_model_path, save_history_path):
    
    loss_history = {"train": [], "val": []}
    acc_history = {"train": [], "val": []}
    best_loss = 9999
    for ep in range(EPOCH):
        epoch_start = time.time()
        current_lr = optimizer.param_groups[0]["lr"]
        print(f"Epoch: {ep+1}, current_LR = {current_lr}")
        
        model.train() # train mode로 전환
        train_loss, train_acc, _ = loss_epoch(model, train_DL, criterion, optimizer = optimizer)
        loss_history["train"] += [train_loss]
        acc_history["train"] += [train_acc]

        model.eval() # test mode로 전환
        with torch.no_grad():
            val_loss, val_acc, _ = loss_epoch(model, val_DL, criterion)
            loss_history["val"] += [val_loss]
            acc_history["val"] += [val_acc]
            if val_loss < best_loss:
                best_loss = val_loss
                # optimizer도 같이 save하면 이어서 학습 가능
                torch.save({"model": model,
                            "ep": ep+1,
                            "optimizer": optimizer,
                            "scheduler": scheduler}, save_model_path)
        
        if scheduler is not None:
            scheduler.step()

        # print loss
        print(f"train loss: {train_loss:.5f}, "
              f"val loss: {val_loss:.5f} \n"
              f"train acc: {train_acc:.1f} %, "
              f"val acc: {val_acc:.1f} %, time: {time.time()-epoch_start:.0f} s")
        print("-"*20)

        # train loss & acc 기록
        writer.add_scalar('Loss/train', train_loss, ep)
        writer.add_scalar('Accuracy/train', train_acc, ep)
        
        # val loss & acc 기록
        writer.add_scalar('Loss/val', val_loss, ep)
        writer.add_scalar('Accuracy/val', val_acc, ep)

    torch.save({"loss_history": loss_history,
                "acc_history": acc_history,
                "EPOCH": EPOCH,
                "BATCH_SIZE": BATCH_SIZE}, save_history_path)

    writer.close()

def Test(model,test_DL, criterion):
    model.eval() # test mode로 전환
    with torch.no_grad():
        test_loss, test_acc, rcorrect = loss_epoch(model, test_DL, criterion)
    print()
    print(f"Test loss: {test_loss:.3f}")
    print(f"Test accuracy: {rcorrect}/{len(test_DL.dataset)} ({test_acc:.1f} %)")
    return round(test_acc,1)
    
def loss_epoch(model, DL, criterion, optimizer = None):
    N = len(DL.dataset) # the number of data
    rloss = 0; rcorrect = 0
    for x_batch, y_batch in tqdm(DL, leave=False): #tqdm(DL, position=10, leave=False): # position은 줄바꿈 개수
        x_batch = x_batch.to(DEVICE)
        y_batch = y_batch.to(DEVICE)
        # inference
        y_hat = model(x_batch)
        # loss
        loss = criterion(y_hat, y_batch)
        # update
        if optimizer is not None:
            optimizer.zero_grad() # gradient 누적을 막기 위한 초기화
            loss.backward() # backpropagation
            optimizer.step() # weight update
        # loss accumulation
        loss_b = loss.item() * x_batch.shape[0] # batch loss # BATCH_SIZE 로 하면 마지막 18개도 32개로 계산해버림
        rloss += loss_b # running loss
        # corrects accumulation
        pred = y_hat.argmax(dim=1)
        corrects_b = torch.sum(pred == y_batch).item()
        rcorrect += corrects_b
    loss_e = rloss/N # epoch loss
    accuracy_e = rcorrect/N * 100

    return loss_e, accuracy_e, rcorrect

def Test_plot(model, test_DL):
    model.eval()
    with torch.no_grad():
        x_batch, y_batch = next(iter(test_DL))
        x_batch = x_batch.to(DEVICE)
        y_hat = model(x_batch)
        pred = y_hat.argmax(dim=1)

    x_batch = x_batch.to("cpu")

    plt.figure(figsize=(8,4))
    for idx in range(6):
        plt.subplot(2,3, idx+1, xticks=[], yticks=[])
        plt.imshow(x_batch[idx].permute(1,2,0), cmap="gray")
        pred_class = test_DL.dataset.classes[pred[idx]]
        true_class = test_DL.dataset.classes[y_batch[idx]]
        plt.title(f"{pred_class} ({true_class})", color = "g" if pred_class==true_class else "r") 

def count_params(model):
    num = sum([p.numel() for p in model.parameters() if p.requires_grad])
    return num

def get_conf(model, test_DL):
    N = len(test_DL.dataset.classes)
    model.eval()
    with torch.no_grad():
        confusion = torch.zeros(N,N)
        for x_batch, y_batch in test_DL:
            x_batch = x_batch.to(DEVICE)
            y_batch = y_batch.to(DEVICE)
            # inference
            y_hat = model(x_batch)
            # accuracy
            pred = y_hat.argmax(dim=1)
            
            confusion += torch.bincount(N * y_batch.cpu() + pred.cpu(), minlength=N**2).reshape(N, N)
        
    confusion = confusion.numpy()

    return confusion

def plot_confusion_matrix(confusion, classes=None):
    N = confusion.shape[0]
    accuracy=np.trace(confusion)/np.sum(confusion) * 100
    
    plt.figure(figsize=(10,7))
    plt.imshow(confusion, cmap="Blues")
    plt.title("confusion matrix")
    plt.colorbar()

    for i in range(N):
        for j in range(N):
            plt.text(j,i, round(confusion[i,j]), 
                     horizontalalignment="center", fontsize=10,
                     color="white" if confusion[i,j] > np.max(confusion) / 1.5 else "black")

    if classes is not None:
        plt.xticks(range(N), classes)
        plt.yticks(range(N), classes)
    else:
        plt.xticks(range(N))
        plt.yticks(range(N))

    plt.xlabel(f"Predicted label \n accuracy = {accuracy:.1f} %")
    plt.ylabel("True label")

def calculate_recall_precision_f1(confusion):
    # Calculate True Positives, False Positives, and False Negatives
    TP = np.diag(confusion)
    FP = np.sum(confusion, axis=0) - TP
    FN = np.sum(confusion, axis=1) - TP

    # Calculate recall, precision, and f1-score
    recall = TP / (TP + FN)
    precision = TP / (TP + FP)
    f1 = 2 * (recall * precision) / (recall + precision)

    return recall, precision, f1

















