
FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu18.04
LABEL maintainer "Jiwon Kim <jwkim@rcv.sejong.ac.kr>"

ENV LANG C.UTF-8

ARG PYTHON_VERSION=
ARG CONDA_ENV_NAME=

RUN apt-get update && apt-get install -y -qq --no-install-recommends \
    apt-utils \
    build-essential \
    sudo \
    cmake \
    git \
    curl \
    vim \
    ca-certificates \
    libglib2.0-0 \
    libjpeg-dev \
    libpng-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ssh \
    wget \
    unzip \
    tmux
RUN rm -rf /var/lib/apt/lists/*

RUN curl -o /tmp/miniconda.sh -sSL http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash /tmp/miniconda.sh -bfp /usr/local && \
    rm -rf /tmp/miniconda.sh

RUN conda update -y conda && \
    conda create -n $CONDA_ENV_NAME python=$PYTHON_VERSION

ENV PATH /usr/local/envs/$CONDA_ENV_NAME/bin:$PATH
RUN echo "source activate ${CONDA_ENV_NAME}" >> ~/.bashrc

SHELL ["/bin/bash", "-c"]

COPY requirements.txt /tmp/requirements.txt
RUN source activate ${CONDA_ENV_NAME} && pip install --no-cache-dir -r /tmp/requirements.txt

RUN source activate ${CONDA_ENV_NAME} && pip install torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117

RUN source activate ${CONDA_ENV_NAME} && \
    conda install -c conda-forge jupyterlab xeus-python nodejs && \
    jupyter serverextension enable --py jupyterlab --sys-prefix && \
    jupyter labextension install @jupyterlab/debugger
