FROM ubuntu:24.10

# Ajusta PATH para incluir o Miniconda
# Define ARG para PATH durante a build
ENV PATH="/root/miniconda/bin:${PATH}"
ARG PATH="/root/miniconda/bin:${PATH}"

# Atualiza repositórios, instala wget e limpa cache
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Baixa e instala o Miniconda, depois remove o instalador
RUN MINICONDAURL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh" && \
    wget $MINICONDAURL -O miniconda.sh && \
    mkdir -p /root/.conda && \
    bash miniconda.sh -b -p /root/miniconda && \
    rm -f miniconda.sh

# Verifica a versão instalada do conda
RUN conda --version

RUN conda install -c pytorch faiss-cpu=1.9.0 && \
    conda install pytorch torchvision torchaudio cpuonly -c pytorch; \
    conda install numpy matplotlib