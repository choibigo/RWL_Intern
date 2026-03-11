# 1. 베이스 이미지
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

# 2. 필수 시스템 패키지 설치
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    wget \
    git \
    bzip2 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Miniconda 설치 
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# 4. 환경 변수 등록
ENV PATH=/opt/conda/bin:$PATH

# 5. 작업 폴더 설정s
WORKDIR /workspace

# 6. 실행 명령
CMD ["/bin/bash"]