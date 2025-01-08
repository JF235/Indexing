FROM nvidia/cuda:12.6.3-base-ubuntu24.04

ENV TZ=America/Sao_Paulo \
    DEBIAN_FRONTEND=noninteractive

# Instala faiss via conda
ENV PATH="/root/miniconda/bin:${PATH}"
ARG PATH="/root/miniconda/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN MINICONDAURL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" && \
    wget $MINICONDAURL -O miniconda.sh && \
    mkdir -p /root/.conda && \
    bash miniconda.sh -b -p /root/miniconda && \
    rm -f miniconda.sh

RUN conda install -c pytorch -c nvidia faiss-gpu=1.9.0 && \
    conda install pytorch pytorch-cuda=12.4 -c pytorch -c nvidia && \
    conda install numpy