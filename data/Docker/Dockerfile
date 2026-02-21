FROM python:3.11-slim-bullseye

WORKDIR /usr/src

COPY ./data_requirements.txt /usr/src/data_requirements.txt

COPY ./data /usr/src/data

COPY ./ml /usr/src/ml

COPY ./parser /usr/src/parser

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    libpq-dev \
    cmake \
    ninja-build \
    git \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CMAKE_ARGS="-DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF"
ENV CMAKE_ARGS="${CMAKE_ARGS} -DCMAKE_EXE_LINKER_FLAGS=-pthread"
ENV CMAKE_ARGS="${CMAKE_ARGS} -DCMAKE_SHARED_LINKER_FLAGS=-pthread"

RUN pip install llama-cpp-python --prefer-binary

RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install -r /usr/src/data_requirements.txt \
    && rm -rf /root/.cache/pip
