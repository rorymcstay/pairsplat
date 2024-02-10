FROM ubuntu

ENV TZ=Europe/London \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y  \
    && apt-get install -y  \
        vim \
        python3.8 \
        build-essential \
        python3-pip \
        python3.8-dev \
        python3.8-distutils \
        python3-psutil \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 100 \
    && update-alternatives  --config python3

WORKDIR /app/pysytemtrade/

RUN pip install virtualenv \
    && python3 -m virtualenv venv \
    && . venv/bin/activate \
    && pip install setuptools==68.2.2 \
        && pip install --upgrade pip \
    && pip install "https://github.com/robcarver17/pysystemtrade/zipball/master" --no-build-isolation \
    && pip install fx-pairs==0.0.6 \
                    pendulum \
                    arcticdb

ENTRYPOINT /app/pysytemtrade/venv/bin/python -m
