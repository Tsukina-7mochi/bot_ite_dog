FROM python:3.8.16-bullseye AS dev
RUN apt -y update && \
    apt -y upgrade && \
    apt install -y mecab && \
    apt install -y libmecab-dev && \
    apt install -y mecab-ipadic-utf8 && \
    apt install -y git && \
    apt install -y make && \
    apt install -y curl && \
    apt install -y xz-utils && \
    apt install -y file && \
    apt install -y sudo
WORKDIR /
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y && \
    echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
    sudo cp /etc/mecabrc /usr/local/etc && \
    cd ..
COPY src/requirements.txt /src/requirements.txt
WORKDIR /src
RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir
