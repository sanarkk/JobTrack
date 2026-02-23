FROM python:3.11-slim-bullseye

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./backend/requirements.txt /usr/src/app/requirements.txt

COPY ./backend/main.py /usr/src/main.py

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

RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip
