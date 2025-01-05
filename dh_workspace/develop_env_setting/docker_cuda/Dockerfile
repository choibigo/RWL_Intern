# CUDA 11.8.0 개발 이미지 사용
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# 시스템 업데이트 및 필수 패키지 설치
ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cuda-toolkit-11-8 \
    curl \
    bash \
    wget \
    software-properties-common \
    libpython3.8-dev \
    && apt-get clean

RUN apt-get install -y gcc
RUN apt-get install -y g++
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libglib2.0-0
RUN apt-get install -y tesseract-ocr tesseract-ocr-kor
RUN apt-get install -y x11-apps

# Anaconda 설치
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

# Conda 초기화
RUN conda init bash

# Conda 환경 활성화 및 PyTorch, torchvision, torchaudio 설치
RUN conda update conda -y && \
conda install pytorch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0  pytorch-cuda=11.8 -c pytorch -c nvidia

ENV DISPLAY=$DISPLAY:0

# 기본 셸 실행
CMD ["bash", "-c", "tail -f /dev/null"]

