# Conda Setup

## 1. Miniconda 설치
| 구분 | Conda          | Miniconda         |
| -- | -------------- | ----------------- |
| 정체 | **패키지/환경 관리자** | **Conda의 최소 배포판** |
| 관계 | 도구 자체          | Conda를 담은 설치 패키지  |
| 기능 | 동일             | 동일                |

`Miniconda를 활용해 환경별로 패키지를 관리할 예정이므로 Miniconda 설치`
```code
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

## 2. Conda 명령어 정리
```sh
conda create -n env_1 python=3.10    # conda env 생성 (Python 3.10)
conda activate env_1                 # conda 환경 활성화
conda deactivate                    # conda 환경 비활성화
conda env list                       # 생성된 conda 환경 목록 확인
conda env remove -n env_1           # env_1이라는 환경 제거
```

#### env 내부
```sh
conda list               #현재 활성화된 conda 환경에 설치된 패키지 목록 출력
```

### conda 환경 생성 및 기본 설치 패키지 확인 실습
```sh
(base) minje@DESKTOP-3BL5NC1:~$ conda activate env_1
(env_1) minje@DESKTOP-3BL5NC1:~$ conda list
# packages in environment at /home/minje/miniconda3/envs/env_1:
#
# Name                     Version          Build            Channel
_libgcc_mutex              0.1              main
_openmp_mutex              5.1              1_gnu
bzip2                      1.0.8            h5eee18b_6
ca-certificates            2025.12.2        h06a4308_0
expat                      2.7.3            h7354ed3_4
ld_impl_linux-64           2.44             h153f514_2
libexpat                   2.7.3            h7354ed3_4
libffi                     3.4.4            h6a678d5_1
libgcc                     15.2.0           h69a1729_7
libgcc-ng                  15.2.0           h166f726_7
libgomp                    15.2.0           h4751f2c_7
libnsl                     2.0.0            h5eee18b_0
libstdcxx                  15.2.0           h39759b7_7
libstdcxx-ng               15.2.0           hc03a8fd_7
libuuid                    1.41.5           h5eee18b_0
libxcb                     1.17.0           h9b100fa_0
libzlib                    1.3.1            hb25bd0a_0
ncurses                    6.5              h7934f7d_0
openssl                    3.0.18           hd6dcaed_0
pip                        25.3             pyhc872135_0
pthread-stubs              0.3              h0ce48e5_1
python                     3.10.19          h6fa692b_0
readline                   8.3              hc2a1206_0
setuptools                 80.9.0           py310h06a4308_0
sqlite                     3.51.1           he0a8d7e_0
tk                         8.6.15           h54e0aa7_0
tzdata                     2025c            he532380_0
wheel                      0.45.1           py310h06a4308_0
xorg-libx11                1.8.12           h9b100fa_1
xorg-libxau                1.0.12           h9b100fa_0
xorg-libxdmcp              1.1.5            h9b100fa_0
xorg-xorgproto             2024.1           h5eee18b_1
xz                         5.6.4            h5eee18b_1
zlib                       1.3.1            hb25bd0a_0
```

**`필요한 패키지는 각 conda 환경 내에서 conda install ~~ 로 관리하여 환경 간 독립성을 유지 가능하다`**